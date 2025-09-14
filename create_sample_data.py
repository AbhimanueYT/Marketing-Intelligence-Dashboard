import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate 120 days of data
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(120)]

# Campaign tactics and states
tactics = ['Search', 'Display', 'Video', 'Shopping', 'Discovery', 'App Install']
states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']

# Generate Facebook data
facebook_data = []
for date in dates:
    for tactic in tactics:
        for state in states:
            if random.random() < 0.3:  # 30% chance of having data for this combination
                impressions = random.randint(1000, 50000)
                clicks = random.randint(10, 500)
                spend = random.uniform(50, 2000)
                revenue = spend * random.uniform(2, 8)  # ROAS between 2-8
                
                facebook_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'tactic': tactic,
                    'state': state,
                    'campaign': f'FB_{tactic}_{state}',
                    'impressions': impressions,
                    'clicks': clicks,
                    'spend': round(spend, 2),
                    'attributed_revenue': round(revenue, 2)
                })

# Generate Google data
google_data = []
for date in dates:
    for tactic in tactics:
        for state in states:
            if random.random() < 0.4:  # 40% chance
                impressions = random.randint(2000, 80000)
                clicks = random.randint(20, 800)
                spend = random.uniform(100, 3000)
                revenue = spend * random.uniform(1.5, 6)
                
                google_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'tactic': tactic,
                    'state': state,
                    'campaign': f'Google_{tactic}_{state}',
                    'impressions': impressions,
                    'clicks': clicks,
                    'spend': round(spend, 2),
                    'attributed_revenue': round(revenue, 2)
                })

# Generate TikTok data
tiktok_data = []
for date in dates:
    for tactic in tactics:
        for state in states:
            if random.random() < 0.25:  # 25% chance
                impressions = random.randint(500, 30000)
                clicks = random.randint(5, 300)
                spend = random.uniform(30, 1500)
                revenue = spend * random.uniform(1.8, 7)
                
                tiktok_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'tactic': tactic,
                    'state': state,
                    'campaign': f'TikTok_{tactic}_{state}',
                    'impressions': random.randint(500, 30000),
                    'clicks': clicks,
                    'spend': round(spend, 2),
                    'attributed_revenue': round(revenue, 2)
                })

# Generate Business data
business_data = []
for date in dates:
    # Base metrics with some seasonality
    day_of_week = date.weekday()
    weekend_multiplier = 1.2 if day_of_week >= 5 else 1.0
    
    orders = random.randint(50, 200) * weekend_multiplier
    new_orders = int(orders * random.uniform(0.6, 0.9))
    new_customers = int(new_orders * random.uniform(0.7, 0.95))
    total_revenue = random.uniform(10000, 50000) * weekend_multiplier
    gross_profit = total_revenue * random.uniform(0.3, 0.5)
    cogs = total_revenue - gross_profit
    
    business_data.append({
        'date': date.strftime('%Y-%m-%d'),
        'orders': int(orders),
        'new_orders': int(new_orders),
        'new_customers': int(new_customers),
        'total_revenue': round(total_revenue, 2),
        'gross_profit': round(gross_profit, 2),
        'cogs': round(cogs, 2)
    })

# Create DataFrames and save to CSV
df_facebook = pd.DataFrame(facebook_data)
df_google = pd.DataFrame(google_data)
df_tiktok = pd.DataFrame(tiktok_data)
df_business = pd.DataFrame(business_data)

# Save to CSV files
df_facebook.to_csv('Facebook.csv', index=False)
df_google.to_csv('Google.csv', index=False)
df_tiktok.to_csv('TikTok.csv', index=False)
df_business.to_csv('Business.csv', index=False)

print("Sample datasets created successfully!")
print(f"Facebook records: {len(df_facebook)}")
print(f"Google records: {len(df_google)}")
print(f"TikTok records: {len(df_tiktok)}")
print(f"Business records: {len(df_business)}")
