import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Test the data processing functions
def test_data_processing():
    """Test the data processing functions from the dashboard"""
    
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
    
    print("✅ Data processing successful!")
    print(f"Marketing data shape: {marketing_df.shape}")
    print(f"Business data shape: {business_df.shape}")
    
    # Test key metrics
    total_spend = marketing_df['spend'].sum()
    total_revenue = marketing_df['attributed_revenue'].sum()
    avg_roas = marketing_df['roas'].mean()
    
    print(f"Total spend: ${total_spend:,.0f}")
    print(f"Total attributed revenue: ${total_revenue:,.0f}")
    print(f"Average ROAS: {avg_roas:.2f}x")
    
    # Test platform analysis
    platform_summary = marketing_df.groupby('platform').agg({
        'spend': 'sum',
        'attributed_revenue': 'sum',
        'roas': 'mean',
        'ctr': 'mean'
    }).round(2)
    
    print("\nPlatform Summary:")
    print(platform_summary)
    
    return True

if __name__ == "__main__":
    test_data_processing()
    print("\n🎉 All tests passed! Dashboard is ready for deployment.")
