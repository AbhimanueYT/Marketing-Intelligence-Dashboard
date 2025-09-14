import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Custom CSS
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
        # Try to load CSV files
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
        
        st.success("✅ Loaded data from CSV files")
        
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
        return None, pd.DataFrame()
    
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    if len(marketing_filtered) == 0:
        return None, pd.DataFrame()
    
    # Platform performance summary
    platform_summary = marketing_filtered.groupby('platform').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean'
    }).round(2)
    
    # Create simple bar chart
    fig = px.bar(
        platform_summary.reset_index(), 
        x='platform', 
        y='spend',
        title="Marketing Spend by Platform",
        labels={'platform': 'Platform', 'spend': 'Total Spend ($)'}
    )
    
    return fig, platform_summary

def create_tactic_analysis(marketing_df, selected_date_range):
    """Create tactic performance analysis"""
    if marketing_df.empty:
        return None, pd.DataFrame()
    
    # Convert date range to datetime for comparison
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    if len(marketing_filtered) == 0:
        return None, pd.DataFrame()
    
    # Tactic performance
    tactic_summary = marketing_filtered.groupby('tactic').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean'
    }).round(2).sort_values('roas', ascending=False)
    
    # Create simple bar chart
    fig = px.bar(
        tactic_summary.reset_index(), 
        x='tactic', 
        y='roas',
        title="ROAS by Tactic",
        labels={'tactic': 'Tactic', 'roas': 'ROAS'}
    )
    
    return fig, tactic_summary

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
    
    # Platform insights
    platform_roas = marketing_filtered.groupby('platform')['roas'].mean().sort_values(ascending=False)
    if len(platform_roas) > 0:
        best_platform = platform_roas.index[0]
        best_platform_roas = platform_roas.iloc[0]
        insights.append(f"🎯 **Best Performing Platform**: {best_platform} with {best_platform_roas:.1f}x ROAS")
    
    # Tactic insights
    tactic_roas = marketing_filtered.groupby('tactic')['roas'].mean().sort_values(ascending=False)
    if len(tactic_roas) > 0:
        best_tactic = tactic_roas.index[0]
        best_tactic_roas = tactic_roas.iloc[0]
        insights.append(f"🚀 **Most Efficient Tactic**: {best_tactic} with {best_tactic_roas:.1f}x ROAS")
    
    # Business insights
    total_marketing_revenue = marketing_filtered['attributed_revenue'].sum()
    total_business_revenue = business_filtered['total_revenue'].sum()
    if total_business_revenue > 0:
        attribution_rate = (total_marketing_revenue / total_business_revenue * 100)
        insights.append(f"📊 **Marketing Attribution**: {attribution_rate:.1f}% of total business revenue")
    
    return insights

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    marketing_df, business_df = load_and_process_data()
    
    if marketing_df.empty or business_df.empty:
        st.error("Failed to load data. Please check that all CSV files are present or the app will use sample data.")
        return
    
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
    if platform_fig:
        st.plotly_chart(platform_fig, width='stretch')
        st.dataframe(platform_summary, width='stretch')
    
    st.markdown("---")
    
    # Tactic Analysis
    st.subheader("Tactic Performance Analysis")
    tactic_fig, tactic_summary = create_tactic_analysis(marketing_df, selected_date_range)
    if tactic_fig:
        st.plotly_chart(tactic_fig, width='stretch')
        st.dataframe(tactic_summary, width='stretch')
    
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
