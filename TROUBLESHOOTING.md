# Streamlit Cloud Deployment Troubleshooting

## 🚨 Common Errors and Solutions

### 1. ModuleNotFoundError: No module named 'distutils'
**Problem**: `distutils` was removed in Python 3.12+ but some packages still depend on it.

**Solutions**:
- Use `requirements_minimal.txt` (no version pins)
- Add `setuptools` to requirements.txt
- Use Python 3.11 or earlier if possible

### 2. FileNotFoundError: CSV files not found
**Problem**: CSV files are not in the repository or not accessible.

**Solutions**:
- Use `marketing_dashboard_final.py` (has built-in sample data)
- Upload CSV files to the same directory as the Python file
- The app will automatically generate sample data if files are missing

### 3. Installer returned a non-zero exit code
**Problem**: Dependency conflicts or incompatible package versions.

**Solutions**:
- Use minimal requirements without version pins
- Check Python version compatibility
- Use the simplified dashboard version

## 📁 Recommended File Structure

```
your-repo/
├── marketing_dashboard.py (renamed from marketing_dashboard_final.py)
├── requirements.txt (use requirements_minimal.txt)
├── Facebook.csv (optional)
├── Google.csv (optional)
├── TikTok.csv (optional)
└── Business.csv (optional)
```

## 🔧 Deployment Steps

### Option 1: Minimal Deployment (Recommended)
1. Rename `marketing_dashboard_final.py` to `marketing_dashboard.py`
2. Use `requirements_minimal.txt` as `requirements.txt`
3. Deploy to Streamlit Cloud
4. App will generate sample data automatically

### Option 2: With Your Data
1. Use `marketing_dashboard_final.py` as `marketing_dashboard.py`
2. Upload your CSV files to the repository
3. Use `requirements_minimal.txt` as `requirements.txt`
4. Deploy to Streamlit Cloud

## 🐍 Python Version Compatibility

- **Python 3.8-3.11**: Use `requirements.txt` with version pins
- **Python 3.12+**: Use `requirements_minimal.txt` without version pins
- **Streamlit Cloud**: Usually runs Python 3.11, but may use 3.12+

## 📊 Dashboard Features

The final dashboard includes:
- ✅ **Automatic Data Generation**: Works without CSV files
- ✅ **Error Handling**: Graceful handling of all errors
- ✅ **Interactive Filters**: Date range, platform, tactic selection
- ✅ **KPI Cards**: Marketing spend, revenue, ROAS, CTR
- ✅ **Platform Comparison**: Facebook, Google, TikTok performance
- ✅ **Tactic Analysis**: ROAS by marketing tactic
- ✅ **Automated Insights**: AI-generated recommendations
- ✅ **Responsive Design**: Works on all devices

## 🎯 Success Indicators

Your deployment is successful when:
- Dashboard loads without errors
- KPI cards display metrics
- Charts and visualizations work
- Filters respond correctly
- Insights are generated
- No error messages in logs

## 🆘 If Still Having Issues

1. **Check Streamlit Cloud logs** for specific error messages
2. **Try the minimal version** with no version pins
3. **Use Python 3.11** if possible
4. **Contact Streamlit support** for platform-specific issues

The dashboard is designed to work in all scenarios - with or without your data!
