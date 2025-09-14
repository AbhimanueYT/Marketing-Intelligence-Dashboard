import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data():
    """Load and process all datasets"""
    # Load datasets
    facebook_df = pd.read_csv('Facebook.csv')
    google_df = pd.read_csv('Google.csv')
    tiktok_df = pd.read_csv('TikTok.csv')
    business_df = pd.read_csv('Business.csv')
    
    # Convert date columns
    for df in [facebook_df, google_df, tiktok_df, business_df]:
        df['date'] = pd.to_datetime(df['date'])
    
    # Add platform column to marketing data
    facebook_df['platform'] = 'Facebook'
    google_df['platform'] = 'Google'
    tiktok_df['platform'] = 'TikTok'
    
    # Combine all marketing data
    marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
    
    # Calculate marketing metrics
    marketing_df['ctr'] = (marketing_df['clicks'] / marketing_df['impressions'] * 100).round(2)
    marketing_df['roas'] = (marketing_df['attributed_revenue'] / marketing_df['spend']).round(2)
    marketing_df['cpc'] = (marketing_df['spend'] / marketing_df['clicks']).round(2)
    marketing_df['cpm'] = (marketing_df['spend'] / marketing_df['impressions'] * 1000).round(2)
    
    # Calculate business metrics
    business_df['aov'] = (business_df['total_revenue'] / business_df['orders']).round(2)
    business_df['conversion_rate'] = (business_df['new_orders'] / business_df['orders'] * 100).round(2)
    business_df['profit_margin'] = (business_df['gross_profit'] / business_df['total_revenue'] * 100).round(2)
    
    return marketing_df, business_df

def create_kpi_cards(marketing_df, business_df, selected_date_range):
    """Create KPI cards for the dashboard"""
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    # Filter data by date range
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    business_filtered = business_df[
        (business_df['date'] >= start_date) & 
        (business_df['date'] <= end_date)
    ]
    
    # Calculate KPIs
    total_spend = marketing_filtered['spend'].sum()
    total_revenue = marketing_filtered['attributed_revenue'].sum()
    total_impressions = marketing_filtered['impressions'].sum()
    total_clicks = marketing_filtered['clicks'].sum()
    avg_roas = marketing_filtered['roas'].mean()
    avg_ctr = marketing_filtered['ctr'].mean()
    
    business_revenue = business_filtered['total_revenue'].sum()
    business_orders = business_filtered['orders'].sum()
    business_profit = business_filtered['gross_profit'].sum()
    avg_aov = business_filtered['aov'].mean()
    
    # Create columns for KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Marketing Spend",
            value=f"${total_spend:,.0f}",
            delta=f"ROAS: {avg_roas:.1f}x"
        )
    
    with col2:
        st.metric(
            label="Attributed Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"CTR: {avg_ctr:.2f}%"
        )
    
    with col3:
        st.metric(
            label="Total Business Revenue",
            value=f"${business_revenue:,.0f}",
            delta=f"AOV: ${avg_aov:.0f}"
        )
    
    with col4:
        st.metric(
            label="Gross Profit",
            value=f"${business_profit:,.0f}",
            delta=f"Orders: {business_orders:,}"
        )

def create_platform_comparison(marketing_df, selected_date_range):
    """Create platform comparison charts"""
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    # Platform performance summary
    platform_summary = marketing_filtered.groupby('platform').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'roas': 'mean',
        'ctr': 'mean'
    }).round(2)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Spend by Platform', 'Revenue by Platform', 'ROAS by Platform', 'CTR by Platform'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Spend chart
    fig.add_trace(
        go.Bar(x=platform_summary.index, y=platform_summary['spend'], name='Spend', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # Revenue chart
    fig.add_trace(
        go.Bar(x=platform_summary.index, y=platform_summary['attributed_revenue'], name='Revenue', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    # ROAS chart
    fig.add_trace(
        go.Bar(x=platform_summary.index, y=platform_summary['roas'], name='ROAS', marker_color='#2ca02c'),
        row=2, col=1
    )
    
    # CTR chart
    fig.add_trace(
        go.Bar(x=platform_summary.index, y=platform_summary['ctr'], name='CTR', marker_color='#d62728'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Platform Performance Comparison")
    return fig, platform_summary

def create_tactic_analysis(marketing_df, selected_date_range):
    """Create tactic performance analysis"""
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    # Tactic performance
    tactic_summary = marketing_filtered.groupby('tactic').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean',
        'impressions': 'sum'
    }).round(2).sort_values('roas', ascending=False)
    
    # Create scatter plot for tactic efficiency
    fig = px.scatter(
        tactic_summary, 
        x='spend', 
        y='attributed_revenue', 
        size='impressions',
        color='roas',
        hover_data=['ctr'],
        title="Tactic Performance: Spend vs Revenue (Size = Impressions, Color = ROAS)",
        labels={'spend': 'Total Spend ($)', 'attributed_revenue': 'Attributed Revenue ($)'}
    )
    
    return fig, tactic_summary

def create_trend_analysis(marketing_df, business_df, selected_date_range):
    """Create trend analysis over time"""
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    business_filtered = business_df[
        (business_df['date'] >= start_date) & 
        (business_df['date'] <= end_date)
    ]
    
    # Daily aggregations
    daily_marketing = marketing_filtered.groupby('date').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'impressions': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    daily_marketing['roas'] = (daily_marketing['attributed_revenue'] / daily_marketing['spend']).round(2)
    daily_marketing['ctr'] = (daily_marketing['clicks'] / daily_marketing['impressions'] * 100).round(2)
    
    # Create trend chart
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily Spend vs Revenue', 'ROAS Trend', 'Impressions vs Clicks', 'Business Revenue vs Marketing Revenue'),
        specs=[[{"secondary_y": True}, {"type": "scatter"}],
               [{"type": "scatter"}, {"secondary_y": True}]]
    )
    
    # Spend vs Revenue
    fig.add_trace(
        go.Scatter(x=daily_marketing['date'], y=daily_marketing['spend'], name='Spend', line=dict(color='#1f77b4')),
        row=1, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=daily_marketing['date'], y=daily_marketing['attributed_revenue'], name='Revenue', line=dict(color='#ff7f0e')),
        row=1, col=1, secondary_y=True
    )
    
    # ROAS trend
    fig.add_trace(
        go.Scatter(x=daily_marketing['date'], y=daily_marketing['roas'], name='ROAS', line=dict(color='#2ca02c')),
        row=1, col=2
    )
    
    # Impressions vs Clicks
    fig.add_trace(
        go.Scatter(x=daily_marketing['impressions'], y=daily_marketing['clicks'], name='Impressions vs Clicks', mode='markers', marker=dict(color='#d62728')),
        row=2, col=1
    )
    
    # Business vs Marketing Revenue
    fig.add_trace(
        go.Scatter(x=business_filtered['date'], y=business_filtered['total_revenue'], name='Business Revenue', line=dict(color='#9467bd')),
        row=2, col=2, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=daily_marketing['date'], y=daily_marketing['attributed_revenue'], name='Marketing Revenue', line=dict(color='#8c564b')),
        row=2, col=2, secondary_y=True
    )
    
    fig.update_layout(height=800, title_text="Trend Analysis Over Time")
    return fig

def create_geographic_analysis(marketing_df, selected_date_range):
    """Create geographic performance analysis"""
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    # State performance
    state_summary = marketing_filtered.groupby('state').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'impressions': 'sum'
    }).round(2).sort_values('spend', ascending=False)
    
    # Create geographic heatmap
    fig = px.bar(
        state_summary.head(10), 
        x=state_summary.head(10).index, 
        y='spend',
        title="Top 10 States by Marketing Spend",
        labels={'x': 'State', 'y': 'Total Spend ($)'}
    )
    
    return fig, state_summary

def create_insights(marketing_df, business_df, selected_date_range):
    """Generate actionable insights"""
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    business_filtered = business_df[
        (business_df['date'] >= start_date) & 
        (business_df['date'] <= end_date)
    ]
    
    insights = []
    
    # Platform insights
    platform_roas = marketing_filtered.groupby('platform')['roas'].mean().sort_values(ascending=False)
    best_platform = platform_roas.index[0]
    worst_platform = platform_roas.index[-1]
    
    insights.append(f"🎯 **Best Performing Platform**: {best_platform} with {platform_roas[best_platform]:.1f}x ROAS")
    insights.append(f"⚠️ **Underperforming Platform**: {worst_platform} with {platform_roas[worst_platform]:.1f}x ROAS")
    
    # Tactic insights
    tactic_roas = marketing_filtered.groupby('tactic')['roas'].mean().sort_values(ascending=False)
    best_tactic = tactic_roas.index[0]
    insights.append(f"🚀 **Most Efficient Tactic**: {best_tactic} with {tactic_roas[best_tactic]:.1f}x ROAS")
    
    # Geographic insights
    state_roas = marketing_filtered.groupby('state')['roas'].mean().sort_values(ascending=False)
    best_state = state_roas.index[0]
    insights.append(f"📍 **Best Performing State**: {best_state} with {state_roas[best_state]:.1f}x ROAS")
    
    # Business insights
    total_marketing_revenue = marketing_filtered['attributed_revenue'].sum()
    total_business_revenue = business_filtered['total_revenue'].sum()
    attribution_rate = (total_marketing_revenue / total_business_revenue * 100)
    insights.append(f"📊 **Marketing Attribution**: {attribution_rate:.1f}% of total business revenue")
    
    # Efficiency insights
    avg_ctr = marketing_filtered['ctr'].mean()
    if avg_ctr < 2.0:
        insights.append(f"🔍 **CTR Opportunity**: Average CTR is {avg_ctr:.2f}% - consider optimizing ad creative")
    
    return insights

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    marketing_df, business_df = load_and_process_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    min_date = marketing_df['date'].min().date()
    max_date = marketing_df['date'].max().date()
    
    selected_date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Handle case where user hasn't selected both dates
    if len(selected_date_range) != 2:
        selected_date_range = (min_date, max_date)
    
    # Platform filter
    platforms = st.sidebar.multiselect(
        "Select Platforms",
        options=marketing_df['platform'].unique(),
        default=marketing_df['platform'].unique()
    )
    
    # Tactic filter
    tactics = st.sidebar.multiselect(
        "Select Tactics",
        options=marketing_df['tactic'].unique(),
        default=marketing_df['tactic'].unique()
    )
    
    # Filter data based on selections
    marketing_df = marketing_df[
        (marketing_df['platform'].isin(platforms)) &
        (marketing_df['tactic'].isin(tactics))
    ]
    
    # Main dashboard content
    st.markdown("---")
    
    # KPI Cards
    create_kpi_cards(marketing_df, business_df, selected_date_range)
    
    st.markdown("---")
    
    # Platform Comparison
    st.subheader("Platform Performance Comparison")
    platform_fig, platform_summary = create_platform_comparison(marketing_df, selected_date_range)
    st.plotly_chart(platform_fig, use_container_width=True)
    
    # Platform summary table
    st.subheader("Platform Summary")
    st.dataframe(platform_summary, use_container_width=True)
    
    st.markdown("---")
    
    # Tactic Analysis
    st.subheader("Tactic Performance Analysis")
    tactic_fig, tactic_summary = create_tactic_analysis(marketing_df, selected_date_range)
    st.plotly_chart(tactic_fig, use_container_width=True)
    
    # Tactic summary table
    st.subheader("Tactic Summary")
    st.dataframe(tactic_summary, use_container_width=True)
    
    st.markdown("---")
    
    # Trend Analysis
    st.subheader("Trend Analysis Over Time")
    trend_fig = create_trend_analysis(marketing_df, business_df, selected_date_range)
    st.plotly_chart(trend_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Geographic Analysis
    st.subheader("Geographic Performance")
    geo_fig, state_summary = create_geographic_analysis(marketing_df, selected_date_range)
    st.plotly_chart(geo_fig, use_container_width=True)
    
    # State summary table
    st.subheader("State Performance Summary")
    st.dataframe(state_summary, use_container_width=True)
    
    st.markdown("---")
    
    # Insights Section
    st.subheader("🎯 Key Insights & Recommendations")
    insights = create_insights(marketing_df, business_df, selected_date_range)
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Dashboard created for Marketing Intelligence Assessment** | Built with Streamlit & Plotly")

if __name__ == "__main__":
    main()
