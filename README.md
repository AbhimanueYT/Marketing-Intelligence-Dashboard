# Marketing Intelligence Dashboard

A comprehensive BI dashboard for analyzing marketing performance and business outcomes across multiple channels.

## Features

### 📊 Key Performance Indicators
- Total marketing spend and attributed revenue
- Return on Ad Spend (ROAS) and Click-Through Rate (CTR)
- Business revenue, orders, and gross profit
- Average Order Value (AOV) and conversion rates

### 🔍 Platform Analysis
- Performance comparison across Facebook, Google, and TikTok
- Spend, revenue, ROAS, and CTR metrics by platform
- Interactive visualizations for easy comparison

### 🎯 Tactic Performance
- Analysis of different marketing tactics (Search, Display, Video, Shopping, Discovery, App Install)
- Efficiency scatter plots showing spend vs revenue
- ROAS and CTR analysis by tactic

### 📈 Trend Analysis
- Daily performance trends over time
- Marketing spend vs attributed revenue correlation
- Business revenue vs marketing revenue comparison
- ROAS trend analysis

### 🗺️ Geographic Analysis
- State-level performance breakdown
- Top performing states by spend and ROAS
- Geographic optimization opportunities

### 💡 Actionable Insights
- Automated insights generation
- Performance recommendations
- Underperforming platform identification
- Optimization opportunities

## Data Structure

The dashboard processes four main datasets:

### Marketing Data (Facebook.csv, Google.csv, TikTok.csv)
- **date**: Campaign date
- **tactic**: Marketing tactic type
- **state**: Geographic location
- **campaign**: Campaign identifier
- **impressions**: Ad impressions
- **clicks**: Ad clicks
- **spend**: Campaign spend
- **attributed_revenue**: Revenue attributed to campaigns

### Business Data (Business.csv)
- **date**: Business date
- **orders**: Total orders
- **new_orders**: New customer orders
- **new_customers**: New customer count
- **total_revenue**: Total business revenue
- **gross_profit**: Gross profit
- **cogs**: Cost of goods sold

## Calculated Metrics

- **ROAS**: Return on Ad Spend (attributed_revenue / spend)
- **CTR**: Click-Through Rate (clicks / impressions * 100)
- **CPC**: Cost Per Click (spend / clicks)
- **CPM**: Cost Per Mille (spend / impressions * 1000)
- **AOV**: Average Order Value (total_revenue / orders)
- **Conversion Rate**: New orders / total orders * 100
- **Profit Margin**: Gross profit / total revenue * 100

## Installation & Usage

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Ensure your data files are in the same directory:
   - Facebook.csv
   - Google.csv
   - TikTok.csv
   - Business.csv

3. Run the dashboard:
```bash
streamlit run marketing_dashboard.py
```

4. Open your browser to `http://localhost:8501`

## Dashboard Features

### Interactive Filters
- Date range selection
- Platform filtering (Facebook, Google, TikTok)
- Tactic filtering
- Real-time data updates

### Visualizations
- Bar charts for platform/tactic comparisons
- Scatter plots for efficiency analysis
- Line charts for trend analysis
- Heatmaps for geographic performance

### Export Capabilities
- Interactive tables with sortable columns
- Downloadable charts and data
- Real-time metric calculations

## Business Value

This dashboard helps marketing and business stakeholders:

1. **Optimize Budget Allocation**: Identify high-performing platforms and tactics
2. **Improve Campaign Efficiency**: Track ROAS and CTR trends
3. **Geographic Optimization**: Focus spend on high-performing states
4. **Performance Monitoring**: Track daily trends and anomalies
5. **Data-Driven Decisions**: Make informed choices based on comprehensive metrics

## Technical Architecture

- **Frontend**: Streamlit for interactive web interface
- **Visualization**: Plotly for interactive charts
- **Data Processing**: Pandas for data manipulation
- **Caching**: Streamlit caching for performance optimization
- **Responsive Design**: Mobile-friendly layout

## Future Enhancements

- Real-time data integration
- Advanced forecasting models
- Custom alert system
- Export to PDF/Excel
- User authentication
- Advanced segmentation analysis
