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

# Enhanced Aesthetic CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main styling */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        border: none;
    }
    
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    
    .stMetric > div {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox > div > div {
        background-color: #ffffff;
        border-radius: 12px;
        border: 2px solid #e1e8ed;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .stDateInput > div > div {
        background-color: #ffffff;
        border-radius: 12px;
        border: 2px solid #e1e8ed;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .stMultiSelect > div > div {
        background-color: #ffffff;
        border-radius: 12px;
        border: 2px solid #e1e8ed;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Custom sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Chart containers */
    .plotly-graph-div {
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        background: white;
    }
    
    /* Data table styling */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* KPI styling */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Animation for loading */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
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
    
    # Calculate comprehensive KPIs
    total_spend = marketing_filtered['spend'].sum()
    total_revenue = marketing_filtered['attributed_revenue'].sum()
    total_impressions = marketing_filtered['impressions'].sum()
    total_clicks = marketing_filtered['clicks'].sum()
    avg_roas = marketing_filtered['roas'].mean() if len(marketing_filtered) > 0 else 0
    avg_ctr = marketing_filtered['ctr'].mean() if len(marketing_filtered) > 0 else 0
    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    avg_cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0
    
    business_revenue = business_filtered['total_revenue'].sum()
    business_orders = business_filtered['orders'].sum()
    business_profit = business_filtered['gross_profit'].sum()
    avg_aov = business_filtered['aov'].mean() if len(business_filtered) > 0 else 0
    profit_margin = (business_profit / business_revenue * 100) if business_revenue > 0 else 0
    attribution_rate = (total_revenue / business_revenue * 100) if business_revenue > 0 else 0
    
    # Create enhanced KPI cards
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Marketing Spend",
            value=f"${total_spend:,.0f}",
            delta=f"CPC: ${avg_cpc:.2f}"
        )
        st.metric(
            label="📊 Average ROAS",
            value=f"{avg_roas:.1f}x",
            delta=f"CPM: ${avg_cpm:.2f}"
        )
    
    with col2:
        st.metric(
            label="📈 Attributed Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"CTR: {avg_ctr:.2f}%"
        )
        st.metric(
            label="👆 Total Clicks",
            value=f"{total_clicks:,}",
            delta=f"Impressions: {total_impressions:,}"
        )
    
    with col3:
        st.metric(
            label="🛒 Total Orders",
            value=f"{business_orders:,}",
            delta=f"AOV: ${avg_aov:.0f}"
        )
        st.metric(
            label="💵 Business Revenue",
            value=f"${business_revenue:,.0f}",
            delta=f"Profit: ${business_profit:,.0f}"
        )
    
    with col4:
        st.metric(
            label="📊 Profit Margin",
            value=f"{profit_margin:.1f}%",
            delta=f"Attribution: {attribution_rate:.1f}%"
        )
        st.metric(
            label="🎯 Conversion Rate",
            value=f"{(total_clicks/total_impressions*100):.2f}%" if total_impressions > 0 else "0%",
            delta=f"Efficiency: {avg_roas*avg_ctr:.1f}"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

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
    
    # Create comprehensive platform comparison with subplots
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Spend by Platform', 'Revenue by Platform', 'ROAS by Platform', 'CTR by Platform'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Color palette
    colors = ['#667eea', '#764ba2', '#f093fb']
    
    # Spend chart
    fig.add_trace(
        go.Bar(
            x=platform_summary.index, 
            y=platform_summary['spend'], 
            name='Spend', 
            marker_color=colors[0],
            text=platform_summary['spend'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto'
        ),
        row=1, col=1
    )
    
    # Revenue chart
    fig.add_trace(
        go.Bar(
            x=platform_summary.index, 
            y=platform_summary['attributed_revenue'], 
            name='Revenue', 
            marker_color=colors[1],
            text=platform_summary['attributed_revenue'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto'
        ),
        row=1, col=2
    )
    
    # ROAS chart
    fig.add_trace(
        go.Bar(
            x=platform_summary.index, 
            y=platform_summary['roas'], 
            name='ROAS', 
            marker_color=colors[2],
            text=platform_summary['roas'].apply(lambda x: f'{x:.1f}x'),
            textposition='auto'
        ),
        row=2, col=1
    )
    
    # CTR chart
    fig.add_trace(
        go.Bar(
            x=platform_summary.index, 
            y=platform_summary['ctr'], 
            name='CTR', 
            marker_color='#ff6b6b',
            text=platform_summary['ctr'].apply(lambda x: f'{x:.2f}%'),
            textposition='auto'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600, 
        showlegend=False,
        title_text="",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12, family="Inter"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Update x-axis labels
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(tickangle=45, row=i, col=j)
    
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
        'impressions': 'sum',
        'clicks': 'sum'
    }).round(2).sort_values('roas', ascending=False)
    
    # Create comprehensive tactic analysis with scatter plot
    fig = px.scatter(
        tactic_summary.reset_index(), 
        x='spend', 
        y='attributed_revenue', 
        size='impressions',
        color='roas',
        hover_data=['ctr', 'clicks'],
        title="",
        labels={
            'spend': 'Total Spend ($)', 
            'attributed_revenue': 'Attributed Revenue ($)',
            'roas': 'ROAS',
            'impressions': 'Impressions',
            'ctr': 'CTR (%)',
            'clicks': 'Clicks'
        },
        color_continuous_scale='Viridis',
        size_max=50
    )
    
    # Add trend line
    fig.add_trace(
        go.Scatter(
            x=tactic_summary['spend'], 
            y=tactic_summary['attributed_revenue'],
            mode='lines+markers',
            name='Trend',
            line=dict(color='#ff6b6b', width=2, dash='dash'),
            marker=dict(size=8, color='#ff6b6b')
        )
    )
    
    # Add annotations for each tactic
    for i, row in tactic_summary.reset_index().iterrows():
        fig.add_annotation(
            x=row['spend'],
            y=row['attributed_revenue'],
            text=row['tactic'],
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='#667eea',
            ax=20,
            ay=-30,
            font=dict(size=10, color='#2c3e50')
        )
    
    fig.update_layout(
        height=500, 
        showlegend=True,
        title_text="",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(size=12, family="Inter"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
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
    
    # Create comprehensive trend analysis with multiple metrics
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily Spend vs Revenue', 'ROAS Trend', 'Impressions vs Clicks', 'Business vs Marketing Revenue'),
        specs=[[{"secondary_y": True}, {"type": "scatter"}],
               [{"type": "scatter"}, {"secondary_y": True}]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Daily Spend vs Revenue
    fig.add_trace(
        go.Scatter(
            x=daily_marketing['date'], 
            y=daily_marketing['spend'], 
            name='Spend', 
            line=dict(color='#667eea', width=3),
            mode='lines+markers'
        ),
        row=1, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=daily_marketing['date'], 
            y=daily_marketing['attributed_revenue'], 
            name='Revenue', 
            line=dict(color='#764ba2', width=3),
            mode='lines+markers'
        ),
        row=1, col=1, secondary_y=True
    )
    
    # ROAS trend
    fig.add_trace(
        go.Scatter(
            x=daily_marketing['date'], 
            y=daily_marketing['roas'], 
            name='ROAS', 
            line=dict(color='#f093fb', width=3),
            mode='lines+markers',
            fill='tonexty'
        ),
        row=1, col=2
    )
    
    # Impressions vs Clicks
    fig.add_trace(
        go.Scatter(
            x=daily_marketing['impressions'], 
            y=daily_marketing['clicks'], 
            name='Impressions vs Clicks', 
            mode='markers',
            marker=dict(
                color='#ff6b6b',
                size=8,
                opacity=0.7,
                line=dict(width=2, color='white')
            )
        ),
        row=2, col=1
    )
    
    # Business vs Marketing Revenue
    fig.add_trace(
        go.Scatter(
            x=business_filtered['date'], 
            y=business_filtered['total_revenue'], 
            name='Business Revenue', 
            line=dict(color='#4ecdc4', width=3),
            mode='lines+markers'
        ),
        row=2, col=2, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=daily_marketing['date'], 
            y=daily_marketing['attributed_revenue'], 
            name='Marketing Revenue', 
            line=dict(color='#45b7d1', width=3),
            mode='lines+markers'
        ),
        row=2, col=2, secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        height=700,
        title_text="",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12, family="Inter"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Spend ($)", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="ROAS", row=1, col=2)
    fig.update_yaxes(title_text="Clicks", row=2, col=1)
    fig.update_yaxes(title_text="Business Revenue ($)", row=2, col=2, secondary_y=False)
    fig.update_yaxes(title_text="Marketing Revenue ($)", row=2, col=2, secondary_y=True)
    
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
        'ctr': 'mean',
        'impressions': 'sum',
        'clicks': 'sum'
    }).round(2).sort_values('spend', ascending=False)
    
    # Create comprehensive geographic analysis
    fig = px.bar(
        state_summary.head(10).reset_index(), 
        x='spend', 
        y='state',
        orientation='h',
        title="",
        labels={'state': 'State', 'spend': 'Spend ($)'},
        color='roas',
        color_continuous_scale='Viridis',
        hover_data=['attributed_revenue', 'ctr', 'impressions']
    )
    
    # Add text annotations
    fig.update_traces(
        text=state_summary.head(10)['spend'].apply(lambda x: f'${x:,.0f}'),
        textposition='inside',
        textfont=dict(size=10, color='white')
    )
    
    # Add secondary metric as text
    for i, row in state_summary.head(10).reset_index().iterrows():
        fig.add_annotation(
            x=row['spend'] + max(state_summary['spend']) * 0.02,
            y=row['state'],
            text=f"ROAS: {row['roas']:.1f}x",
            showarrow=False,
            font=dict(size=9, color='#667eea'),
            xanchor='left'
        )
    
    fig.update_layout(
        height=500,
        title_text="",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(size=12, family="Inter"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Total Spend ($)",
        yaxis_title="State",
        coloraxis_colorbar=dict(
            title="ROAS",
            title_side="right"
        )
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
    avg_ctr = marketing_filtered['ctr'].mean()
    total_clicks = marketing_filtered['clicks'].sum()
    total_impressions = marketing_filtered['impressions'].sum()
    
    if total_spend > 0:
        insights.append(f"💰 Performance Summary: ${total_spend:,.0f} spend generated ${total_revenue:,.0f} revenue with {avg_roas:.1f}x ROAS")
    
    # Platform analysis
    platform_roas = marketing_filtered.groupby('platform')['roas'].mean().sort_values(ascending=False)
    platform_spend = marketing_filtered.groupby('platform')['spend'].sum().sort_values(ascending=False)
    
    if len(platform_roas) > 0:
        best_platform = platform_roas.index[0]
        best_platform_roas = platform_roas.iloc[0]
        worst_platform = platform_roas.index[-1]
        worst_platform_roas = platform_roas.iloc[-1]
        
        insights.append(f"🏆 Platform Performance: {best_platform} leads with {best_platform_roas:.1f}x ROAS, while {worst_platform} needs optimization at {worst_platform_roas:.1f}x")
    
    # Tactic analysis
    tactic_roas = marketing_filtered.groupby('tactic')['roas'].mean().sort_values(ascending=False)
    tactic_spend = marketing_filtered.groupby('tactic')['spend'].sum().sort_values(ascending=False)
    
    if len(tactic_roas) > 0:
        best_tactic = tactic_roas.index[0]
        best_tactic_roas = tactic_roas.iloc[0]
        insights.append(f"🚀 Best Performing Tactic: {best_tactic} delivers {best_tactic_roas:.1f}x ROAS - consider increasing budget allocation")
    
    # Geographic insights
    state_roas = marketing_filtered.groupby('state')['roas'].mean().sort_values(ascending=False)
    state_spend = marketing_filtered.groupby('state')['spend'].sum().sort_values(ascending=False)
    
    if len(state_roas) > 0:
        best_state = state_roas.index[0]
        best_state_roas = state_roas.iloc[0]
        insights.append(f"📍 Geographic Opportunity: {best_state} shows highest ROAS at {best_state_roas:.1f}x - consider expanding presence")
    
    # Business insights
    total_business_revenue = business_filtered['total_revenue'].sum()
    total_business_profit = business_filtered['gross_profit'].sum()
    
    if total_business_revenue > 0:
        attribution_rate = (total_revenue / total_business_revenue * 100)
        profit_margin = (total_business_profit / total_business_revenue * 100)
        insights.append(f"📊 Business Impact: Marketing drives {attribution_rate:.1f}% of total revenue with {profit_margin:.1f}% profit margin")
    
    # Efficiency insights
    if avg_ctr < 2.0:
        insights.append(f"🔍 Optimization Opportunity: CTR of {avg_ctr:.2f}% is below industry average - focus on ad creative and targeting")
    
    # Trend insights
    daily_roas = marketing_filtered.groupby('date')['roas'].mean()
    if len(daily_roas) > 7:
        recent_roas = daily_roas.tail(7).mean()
        previous_roas = daily_roas.head(7).mean()
        roas_trend = ((recent_roas - previous_roas) / previous_roas * 100) if previous_roas > 0 else 0
        
        if roas_trend > 5:
            insights.append(f"📈 Positive Trend: ROAS improved {roas_trend:.1f}% over the period - maintain current strategy")
        elif roas_trend < -5:
            insights.append(f"📉 Declining Performance: ROAS decreased {abs(roas_trend):.1f}% - review and optimize campaigns")
    
    # Budget allocation insights
    if len(platform_spend) > 1:
        top_platform_spend = platform_spend.iloc[0]
        total_platform_spend = platform_spend.sum()
        top_platform_share = (top_platform_spend / total_platform_spend * 100)
        
        if top_platform_share > 60:
            insights.append(f"⚖️ Budget Concentration: {platform_spend.index[0]} receives {top_platform_share:.1f}% of budget - consider diversifying for risk mitigation")
   
    return insights

def main():
    # Enhanced header with gradient
    st.markdown('<h1 class="main-header">Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Add description
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #6c757d; font-size: 1.1rem;">
        Comprehensive analytics for marketing performance and business impact
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    marketing_df, business_df = load_and_process_data()
    
    if marketing_df.empty or business_df.empty:
        st.error("Failed to load data. Please check that all CSV files are present or the app will use sample data.")
        return
    
    # Enhanced sidebar with more options
    with st.sidebar:
        st.markdown("### 🎛️ Dashboard Controls")
        
        # Date range filter
        min_date = marketing_df['date'].min().date()
        max_date = marketing_df['date'].max().date()
        
        selected_date_range = st.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Select the date range for analysis"
        )
        
        # Handle case where user hasn't selected both dates
        if len(selected_date_range) != 2:
            selected_date_range = (min_date, max_date)
        
        st.markdown("---")
        
        # Platform filter
        platforms = st.multiselect(
            "🌐 Platforms",
            options=marketing_df['platform'].unique(),
            default=marketing_df['platform'].unique(),
            help="Select marketing platforms to analyze"
        )
        
        # Tactic filter
        tactics = st.multiselect(
            "🎯 Tactics",
            options=marketing_df['tactic'].unique(),
            default=marketing_df['tactic'].unique(),
            help="Select marketing tactics to analyze"
        )
        
        st.markdown("---")
        
        # Additional filters
        st.markdown("#### 📊 View Options")
        
        show_data_tables = st.checkbox("📋 Show Data Tables", value=False, help="Display detailed data tables")
        show_insights = st.checkbox("💡 Show Insights", value=True, help="Display AI-generated insights")
        
        # Metric selection
        st.markdown("#### 📈 Key Metrics")
        selected_metrics = st.multiselect(
            "Choose metrics to highlight",
            options=['ROAS', 'CTR', 'CPC', 'CPM', 'Revenue', 'Spend'],
            default=['ROAS', 'CTR', 'Revenue']
        )
    
    # Filter data based on selections
    marketing_df = marketing_df[
        (marketing_df['platform'].isin(platforms)) &
        (marketing_df['tactic'].isin(tactics))
    ]
    
    # Add loading animation
    with st.spinner('🔄 Loading dashboard data...'):
        # KPI Cards
        create_kpi_cards(marketing_df, business_df, selected_date_range)
        
        # Create tabs for better organization
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Performance", "🎯 Tactics", "📈 Trends", "🗺️ Geography", "💡 Insights"])
        
        with tab1:
            st.markdown('<div class="section-header">Platform Performance Analysis</div>', unsafe_allow_html=True)
            platform_fig, platform_summary = create_platform_comparison(marketing_df, selected_date_range)
            if platform_fig:
                st.plotly_chart(platform_fig, width='stretch')
            
            if show_data_tables:
                st.markdown("#### 📋 Platform Summary Data")
                st.dataframe(platform_summary, width='stretch')
        
        with tab2:
            st.markdown('<div class="section-header">Tactic Performance Analysis</div>', unsafe_allow_html=True)
            tactic_fig, tactic_summary = create_tactic_analysis(marketing_df, selected_date_range)
            if tactic_fig:
                st.plotly_chart(tactic_fig, width='stretch')
            
            if show_data_tables:
                st.markdown("#### 📋 Tactic Summary Data")
                st.dataframe(tactic_summary, width='stretch')
        
        with tab3:
            st.markdown('<div class="section-header">Trend Analysis Over Time</div>', unsafe_allow_html=True)
            trend_fig = create_trend_analysis(marketing_df, business_df, selected_date_range)
            if trend_fig:
                st.plotly_chart(trend_fig, width='stretch')
        
        with tab4:
            st.markdown('<div class="section-header">Geographic Performance</div>', unsafe_allow_html=True)
            geo_fig, state_summary = create_geographic_analysis(marketing_df, selected_date_range)
            if geo_fig:
                st.plotly_chart(geo_fig, width='stretch')
            
            if show_data_tables:
                st.markdown("#### 📋 State Performance Data")
                st.dataframe(state_summary.head(10), width='stretch')
        
        with tab5:
            if show_insights:
                st.markdown('<div class="section-header">AI-Generated Insights & Recommendations</div>', unsafe_allow_html=True)
                insights = create_insights(marketing_df, business_df, selected_date_range)
                
                for i, insight in enumerate(insights, 1):
                    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
            else:
                st.info("💡 Enable 'Show Insights' in the sidebar to view AI-generated recommendations")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 2rem;">
        🚀 <strong>Marketing Intelligence Dashboard</strong> | Built with Streamlit & Plotly | 
        <em>Real-time analytics for data-driven marketing decisions</em>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
