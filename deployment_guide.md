# Deployment Guide for Marketing Intelligence Dashboard

## Local Testing

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Locally**:
   ```bash
   streamlit run marketing_dashboard.py
   ```

3. **Access Dashboard**: Open `http://localhost:8501` in your browser

## Streamlit Cloud Deployment

### Option 1: Direct Upload to Streamlit Cloud

1. **Create GitHub Repository**:
   - Create a new repository on GitHub
   - Upload all files: `marketing_dashboard.py`, `requirements.txt`, and CSV files
   - Ensure the repository is public

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path to `marketing_dashboard.py`
   - Click "Deploy"

### Option 2: Manual Deployment

1. **Prepare Files**:
   - Ensure all required files are in the repository
   - Verify `requirements.txt` has all dependencies
   - Test locally before deployment

2. **Deploy**:
   - Follow Streamlit Cloud deployment process
   - Monitor deployment logs for any issues

## Files Required for Deployment

- `marketing_dashboard.py` - Main dashboard application
- `requirements.txt` - Python dependencies
- `Facebook.csv` - Facebook marketing data
- `Google.csv` - Google marketing data  
- `TikTok.csv` - TikTok marketing data
- `Business.csv` - Business performance data
- `README.md` - Documentation
- `.streamlit/config.toml` - Streamlit configuration (optional)

## Dashboard Features

### 📊 Key Performance Indicators
- Total marketing spend and attributed revenue
- Return on Ad Spend (ROAS) and Click-Through Rate (CTR)
- Business revenue, orders, and gross profit
- Average Order Value (AOV) and conversion rates

### 🔍 Interactive Analysis
- Platform performance comparison (Facebook, Google, TikTok)
- Tactic performance analysis
- Geographic performance breakdown
- Trend analysis over time
- Automated insights and recommendations

### 🎯 Business Value
- Optimize budget allocation across platforms
- Identify high-performing tactics and states
- Track marketing efficiency metrics
- Make data-driven marketing decisions

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure all dependencies are installed
   - Check Python version compatibility

2. **Data Loading Issues**:
   - Verify CSV files are in the correct directory
   - Check file permissions

3. **Performance Issues**:
   - Use data caching (already implemented)
   - Consider data aggregation for large datasets

### Support

For technical issues:
1. Check Streamlit Cloud deployment logs
2. Verify all dependencies are correctly specified
3. Test locally before deployment
4. Check data file formats and locations

## Dashboard URL

Once deployed, your dashboard will be available at:
`https://your-app-name.streamlit.app`

## Next Steps

1. **Customize Data**: Replace sample data with real marketing data
2. **Add Features**: Implement additional metrics or visualizations
3. **Schedule Updates**: Set up automated data refresh
4. **User Access**: Configure user authentication if needed
5. **Monitoring**: Set up performance monitoring and alerts
