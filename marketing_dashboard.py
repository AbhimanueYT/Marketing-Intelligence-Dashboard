import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# Disable file watcher to avoid inotify issues on Streamlit Cloud
os.environ['STREAMLIT_SERVER_FILE_WATCHER_TYPE'] = 'none'

# Page configuration
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimalist CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #e1e8ed;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #f8f9fa;
        padding: 0.8rem;
        border-radius: 6px;
        border-left: 3px solid #6c757d;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #495057;
        margin: 1.5rem 0 1rem 0;
    }
    .stMetric > div {
        background-color: #ffffff;
        border: 1px solid #e1e8ed;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample data for demonstration"""
    np.random.seed(42)
    
    # Generate 120 days of data
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(120)]
    
    # Campaign tactics and states
    tactics = ['Search', 'Display', 'Video', 'Shopping', 'Discovery', 'App Install']
    states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
    platforms = ['Facebook', 'Google', 'TikTok']
    
    # Generate marketing data
    marketing_data = []
    for date in dates:
        for platform in platforms:
            for tactic in tactics:
                for state in states:
                    if np.random.random() < 0.3:  # 30% chance of having data
                        impressions = np.random.randint(1000, 50000)
                        clicks = np.random.randint(10, 500)
                        spend = np.random.uniform(50, 2000)
                        revenue = spend * np.random.uniform(2, 8)
                        
                        marketing_data.append({
                            'date': date,
                            'platform': platform,
                            'tactic': tactic,
                            'state': state,
                            'campaign': f'{platform}_{tactic}_{state}',
                            'impressions': impressions,
                            'clicks': clicks,
                            'spend': round(spend, 2),
                            'attributed_revenue': round(revenue, 2)
                        })
    
    # Generate business data
    business_data = []
    for date in dates:
        orders = np.random.randint(50, 200)
        new_orders = int(orders * np.random.uniform(0.6, 0.9))
        new_customers = int(new_orders * np.random.uniform(0.7, 0.95))
        total_revenue = np.random.uniform(10000, 50000)
        gross_profit = total_revenue * np.random.uniform(0.3, 0.5)
        cogs = total_revenue - gross_profit
        
        business_data.append({
            'date': date,
            'orders': int(orders),
            'new_orders': int(new_orders),
            'new_customers': int(new_customers),
            'total_revenue': round(total_revenue, 2),
            'gross_profit': round(gross_profit, 2),
            'cogs': round(cogs, 2)
        })
    
    return pd.DataFrame(marketing_data), pd.DataFrame(business_data)

@st.cache_data(ttl=3600)  # Cache for 1 hour to reduce file system access
def load_and_process_data():
    """Load and process all datasets"""
    try:
        # Try different file paths for local vs cloud deployment
        file_paths = [
            # Local development paths
            ('Facebook.csv', 'Google.csv', 'TikTok.csv', 'Business.csv'),
            # Cloud deployment paths (same directory)
            ('./Facebook.csv', './Google.csv', './TikTok.csv', './Business.csv'),
            # Streamlit Cloud specific paths
            ('/mount/src/marketing-intelligence-dashboard/Facebook.csv', 
             '/mount/src/marketing-intelligence-dashboard/Google.csv',
             '/mount/src/marketing-intelligence-dashboard/TikTok.csv',
             '/mount/src/marketing-intelligence-dashboard/business.csv'),
            # Alternative Streamlit Cloud paths
            ('/app/marketing-intelligence-dashboard/Facebook.csv',
             '/app/marketing-intelligence-dashboard/Google.csv',
             '/app/marketing-intelligence-dashboard/TikTok.csv',
             '/app/marketing-intelligence-dashboard/business.csv')
        ]
        
        facebook_df = None
        google_df = None
        tiktok_df = None
        business_df = None
        
        
        for i, (fb_path, go_path, tt_path, bus_path) in enumerate(file_paths):
            try:
                facebook_df = pd.read_csv(fb_path)
                google_df = pd.read_csv(go_path)
                tiktok_df = pd.read_csv(tt_path)
                business_df = pd.read_csv(bus_path)
                break
            except FileNotFoundError:
                continue
        
        if facebook_df is None:
            raise FileNotFoundError("Could not find CSV files in any expected location")
        
        # Convert date columns
        for df in [facebook_df, google_df, tiktok_df, business_df]:
            df['date'] = pd.to_datetime(df['date'])
        
        # Add platform column to marketing data
        facebook_df['platform'] = 'Facebook'
        google_df['platform'] = 'Google'
        tiktok_df['platform'] = 'TikTok'
        
        # Combine all marketing data
        marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
        
    except FileNotFoundError:
        st.warning("⚠️ CSV files not found. Using sample data for demonstration.")
        marketing_df, business_df = generate_sample_data()
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.warning("Using sample data for demonstration.")
        marketing_df, business_df = generate_sample_data()
    
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
    if marketing_df.empty or business_df.empty:
        st.error("No data available")
        return
    
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
    avg_roas = marketing_filtered['roas'].mean() if len(marketing_filtered) > 0 else 0
    avg_ctr = marketing_filtered['ctr'].mean() if len(marketing_filtered) > 0 else 0
    
    business_revenue = business_filtered['total_revenue'].sum()
    business_orders = business_filtered['orders'].sum()
    business_profit = business_filtered['gross_profit'].sum()
    avg_aov = business_filtered['aov'].mean() if len(business_filtered) > 0 else 0
    
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
    if marketing_df.empty:
        st.error("No marketing data available")
        return None, pd.DataFrame()
    
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    if len(marketing_filtered) == 0:
        st.warning("No data available for selected date range")
        return None, pd.DataFrame()
    
    # Platform performance summary
    platform_summary = marketing_filtered.groupby('platform').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'roas': 'mean',
        'ctr': 'mean'
    }).round(2)
    
    # Create simple bar chart
    fig = px.bar(
        platform_summary.reset_index(), 
        x='platform', 
        y='spend',
        title="",
        labels={'platform': 'Platform', 'spend': 'Spend ($)'},
        color='platform',
        color_discrete_sequence=['#3498db', '#e74c3c', '#2ecc71']
    )
    
    fig.update_layout(
        height=400, 
        showlegend=False,
        title_text="",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig, platform_summary

def create_tactic_analysis(marketing_df, selected_date_range):
    """Create tactic performance analysis"""
    if marketing_df.empty:
        st.error("No marketing data available")
        return None, pd.DataFrame()
    
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    if len(marketing_filtered) == 0:
        st.warning("No data available for selected date range")
        return None, pd.DataFrame()
    
    # Tactic performance
    tactic_summary = marketing_filtered.groupby('tactic').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean',
        'impressions': 'sum'
    }).round(2).sort_values('roas', ascending=False)
    
    # Create simple bar chart
    fig = px.bar(
        tactic_summary.reset_index(), 
        x='tactic', 
        y='roas',
        title="",
        labels={'tactic': 'Tactic', 'roas': 'ROAS'},
        color='roas',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=400, 
        showlegend=False,
        title_text="",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig, tactic_summary

def create_trend_analysis(marketing_df, business_df, selected_date_range):
    """Create trend analysis over time"""
    if marketing_df.empty or business_df.empty:
        st.error("No data available")
        return None
    
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
    
    # Create simple line chart
    fig = px.line(
        daily_marketing, 
        x='date', 
        y='spend',
        title="",
        labels={'date': 'Date', 'spend': 'Daily Spend ($)'}
    )
    
    fig.update_layout(
        height=400,
        title_text="",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_geographic_analysis(marketing_df, selected_date_range):
    """Create geographic performance analysis"""
    if marketing_df.empty:
        st.error("No marketing data available")
        return None, pd.DataFrame()
    
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    if len(marketing_filtered) == 0:
        st.warning("No data available for selected date range")
        return None, pd.DataFrame()
    
    # State performance
    state_summary = marketing_filtered.groupby('state').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'impressions': 'sum'
    }).round(2).sort_values('spend', ascending=False)
    
    # Create simple bar chart
    fig = px.bar(
        state_summary.head(10).reset_index(), 
        x='state', 
        y='spend',
        title="",
        labels={'state': 'State', 'spend': 'Spend ($)'},
        color='spend',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=400,
        title_text="",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig, state_summary


def create_insights(marketing_df, business_df, selected_date_range):
    """Generate actionable insights"""
    if marketing_df.empty or business_df.empty:
        return ["No data available for insights"]
    
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
    
    if len(marketing_filtered) == 0 or len(business_filtered) == 0:
        return ["No data available for selected date range"]
    
    insights = []
    
    # Key metrics
    total_spend = marketing_filtered['spend'].sum()
    total_revenue = marketing_filtered['attributed_revenue'].sum()
    avg_roas = marketing_filtered['roas'].mean()
    
    if total_spend > 0:
        insights.append(f"💰 Spend: ${total_spend:,.0f} | Revenue: ${total_revenue:,.0f} | ROAS: {avg_roas:.1f}x")
    
    # Best platform
    platform_roas = marketing_filtered.groupby('platform')['roas'].mean().sort_values(ascending=False)
    if len(platform_roas) > 0:
        best_platform = platform_roas.index[0]
        best_platform_roas = platform_roas.iloc[0]
        insights.append(f"🏆 Top Platform: {best_platform} ({best_platform_roas:.1f}x ROAS)")
    
    # Best tactic
    tactic_roas = marketing_filtered.groupby('tactic')['roas'].mean().sort_values(ascending=False)
    if len(tactic_roas) > 0:
        best_tactic = tactic_roas.index[0]
        best_tactic_roas = tactic_roas.iloc[0]
        insights.append(f"🚀 Top Tactic: {best_tactic} ({best_tactic_roas:.1f}x ROAS)")
    
    # Attribution
    total_business_revenue = business_filtered['total_revenue'].sum()
    if total_business_revenue > 0:
        attribution_rate = (total_revenue / total_business_revenue * 100)
        insights.append(f"📊 Attribution: {attribution_rate:.1f}% of business revenue")
   
    return insights

def main():
    # Minimalist header
    st.markdown('<h1 class="main-header">Marketing Intelligence</h1>', unsafe_allow_html=True)
    
    # Load data
    marketing_df, business_df = load_and_process_data()
    
    if marketing_df.empty or business_df.empty:
        st.error("Failed to load data. Please check that all CSV files are present or the app will use sample data.")
        return
    
    # Minimalist sidebar
    with st.sidebar:
        st.markdown("### Filters")
        
        # Date range filter
        min_date = marketing_df['date'].min().date()
        max_date = marketing_df['date'].max().date()
        
        selected_date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Handle case where user hasn't selected both dates
        if len(selected_date_range) != 2:
            selected_date_range = (min_date, max_date)
        
        # Platform filter
        platforms = st.multiselect(
            "Platforms",
            options=marketing_df['platform'].unique(),
            default=marketing_df['platform'].unique()
        )
        
        # Tactic filter
        tactics = st.multiselect(
            "Tactics",
            options=marketing_df['tactic'].unique(),
            default=marketing_df['tactic'].unique()
        )
    
    # Filter data based on selections
    marketing_df = marketing_df[
        (marketing_df['platform'].isin(platforms)) &
        (marketing_df['tactic'].isin(tactics))
    ]
    
    # KPI Cards
    create_kpi_cards(marketing_df, business_df, selected_date_range)
    
    # Platform Performance
    st.markdown('<div class="section-header">Platform Performance</div>', unsafe_allow_html=True)
    platform_fig, platform_summary = create_platform_comparison(marketing_df, selected_date_range)
    if platform_fig:
        st.plotly_chart(platform_fig, width='stretch')
    
    # Tactic Analysis
    st.markdown('<div class="section-header">Tactic Performance</div>', unsafe_allow_html=True)
    tactic_fig, tactic_summary = create_tactic_analysis(marketing_df, selected_date_range)
    if tactic_fig:
        st.plotly_chart(tactic_fig, width='stretch')
    
    # Trend Analysis
    st.markdown('<div class="section-header">Trends</div>', unsafe_allow_html=True)
    trend_fig = create_trend_analysis(marketing_df, business_df, selected_date_range)
    if trend_fig:
        st.plotly_chart(trend_fig, width='stretch')
    
    # Geographic Analysis
    st.markdown('<div class="section-header">Geographic Performance</div>', unsafe_allow_html=True)
    geo_fig, state_summary = create_geographic_analysis(marketing_df, selected_date_range)
    if geo_fig:
        st.plotly_chart(geo_fig, width='stretch')
    
    # Key Insights
    st.markdown('<div class="section-header">Key Insights</div>', unsafe_allow_html=True)
    insights = create_insights(marketing_df, business_df, selected_date_range)
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
