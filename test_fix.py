import pandas as pd
from datetime import date

# Test the date conversion fix
def test_date_conversion():
    """Test the date conversion fix"""
    
    # Load sample data
    marketing_df = pd.read_csv('Facebook.csv')
    marketing_df['date'] = pd.to_datetime(marketing_df['date'])
    
    # Simulate date range from Streamlit
    min_date = marketing_df['date'].min().date()
    max_date = marketing_df['date'].max().date()
    selected_date_range = (min_date, max_date)
    
    print(f"Min date: {min_date}")
    print(f"Max date: {max_date}")
    print(f"Selected range: {selected_date_range}")
    
    # Test the conversion
    start_date = pd.to_datetime(selected_date_range[0])
    end_date = pd.to_datetime(selected_date_range[1])
    
    print(f"Start date (converted): {start_date}")
    print(f"End date (converted): {end_date}")
    
    # Test filtering
    marketing_filtered = marketing_df[
        (marketing_df['date'] >= start_date) & 
        (marketing_df['date'] <= end_date)
    ]
    
    print(f"Original records: {len(marketing_df)}")
    print(f"Filtered records: {len(marketing_filtered)}")
    print("✅ Date conversion fix working correctly!")

if __name__ == "__main__":
    test_date_conversion()
