import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_demo_insights():
    """Generate demo insights to showcase dashboard capabilities"""
    
    # Load and process data
    facebook_df = pd.read_csv('Facebook.csv')
    google_df = pd.read_csv('Google.csv')
    tiktok_df = pd.read_csv('TikTok.csv')
    business_df = pd.read_csv('Business.csv')
    
    # Convert date columns
    for df in [facebook_df, google_df, tiktok_df, business_df]:
        df['date'] = pd.to_datetime(df['date'])
    
    # Add platform column
    facebook_df['platform'] = 'Facebook'
    google_df['platform'] = 'Google'
    tiktok_df['platform'] = 'TikTok'
    
    # Combine marketing data
    marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
    
    # Calculate metrics
    marketing_df['roas'] = (marketing_df['attributed_revenue'] / marketing_df['spend']).round(2)
    marketing_df['ctr'] = (marketing_df['clicks'] / marketing_df['impressions'] * 100).round(2)
    
    business_df['aov'] = (business_df['total_revenue'] / business_df['orders']).round(2)
    
    print("🎯 MARKETING INTELLIGENCE DASHBOARD - DEMO INSIGHTS")
    print("=" * 60)
    
    # Overall Performance
    total_spend = marketing_df['spend'].sum()
    total_revenue = marketing_df['attributed_revenue'].sum()
    business_revenue = business_df['total_revenue'].sum()
    
    print(f"\n📊 OVERALL PERFORMANCE (120 days)")
    print(f"Total Marketing Spend: ${total_spend:,.0f}")
    print(f"Attributed Revenue: ${total_revenue:,.0f}")
    print(f"Business Revenue: ${business_revenue:,.0f}")
    print(f"Marketing Attribution Rate: {(total_revenue/business_revenue*100):.1f}%")
    
    # Platform Performance
    platform_summary = marketing_df.groupby('platform').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean',
        'impressions': 'sum'
    }).round(2).sort_values('roas', ascending=False)
    
    print(f"\n🏆 PLATFORM PERFORMANCE")
    print("-" * 40)
    for platform, row in platform_summary.iterrows():
        print(f"{platform:8} | ROAS: {row['roas']:4.1f}x | CTR: {row['ctr']:4.1f}% | Spend: ${row['spend']:8,.0f}")
    
    # Tactic Performance
    tactic_summary = marketing_df.groupby('tactic').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean'
    }).round(2).sort_values('roas', ascending=False)
    
    print(f"\n🎯 TOP PERFORMING TACTICS")
    print("-" * 40)
    for tactic, row in tactic_summary.head(5).iterrows():
        print(f"{tactic:12} | ROAS: {row['roas']:4.1f}x | CTR: {row['ctr']:4.1f}%")
    
    # Geographic Performance
    state_summary = marketing_df.groupby('state').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean'
    }).round(2).sort_values('spend', ascending=False)
    
    print(f"\n🗺️  TOP STATES BY SPEND")
    print("-" * 40)
    for state, row in state_summary.head(5).iterrows():
        print(f"{state:2} | Spend: ${row['spend']:8,.0f} | ROAS: {row['roas']:4.1f}x")
    
    # Business Metrics
    total_orders = business_df['orders'].sum()
    avg_aov = business_df['aov'].mean()
    total_profit = business_df['gross_profit'].sum()
    profit_margin = (total_profit / business_revenue * 100)
    
    print(f"\n💼 BUSINESS METRICS")
    print("-" * 40)
    print(f"Total Orders: {total_orders:,}")
    print(f"Average Order Value: ${avg_aov:.0f}")
    print(f"Gross Profit: ${total_profit:,.0f}")
    print(f"Profit Margin: {profit_margin:.1f}%")
    
    # Key Insights
    print(f"\n💡 KEY INSIGHTS & RECOMMENDATIONS")
    print("-" * 40)
    
    best_platform = platform_summary.index[0]
    best_platform_roas = platform_summary.loc[best_platform, 'roas']
    print(f"🎯 Best Platform: {best_platform} ({best_platform_roas:.1f}x ROAS)")
    
    worst_platform = platform_summary.index[-1]
    worst_platform_roas = platform_summary.loc[worst_platform, 'roas']
    print(f"⚠️  Underperforming Platform: {worst_platform} ({worst_platform_roas:.1f}x ROAS)")
    
    best_tactic = tactic_summary.index[0]
    best_tactic_roas = tactic_summary.loc[best_tactic, 'roas']
    print(f"🚀 Most Efficient Tactic: {best_tactic} ({best_tactic_roas:.1f}x ROAS)")
    
    best_state = state_summary.index[0]
    best_state_roas = state_summary.loc[best_state, 'roas']
    print(f"📍 Top State: {best_state} (${state_summary.loc[best_state, 'spend']:,.0f} spend, {best_state_roas:.1f}x ROAS)")
    
    avg_ctr = marketing_df['ctr'].mean()
    if avg_ctr < 2.0:
        print(f"🔍 CTR Opportunity: Average CTR is {avg_ctr:.2f}% - consider optimizing ad creative")
    else:
        print(f"✅ Good CTR Performance: Average CTR is {avg_ctr:.2f}%")
    
    print(f"\n🎉 Dashboard is ready! Run 'streamlit run marketing_dashboard.py' to view the interactive dashboard.")

if __name__ == "__main__":
    generate_demo_insights()
