# Complete Streamlit Cloud Deployment Guide

## 🎯 Problem Solved: CSV Files Not Found on Streamlit Cloud

Your dashboard works locally but shows "CSV files not found" on Streamlit Cloud because the CSV files aren't uploaded to your GitHub repository.

## ✅ Solution: Upload CSV Files to GitHub

### Step 1: Prepare Your Files

Make sure you have these files ready:
- ✅ `marketing_dashboard.py` (updated with multiple file path support)
- ✅ `requirements.txt`
- ✅ `.streamlit/config.toml`
- ✅ `Facebook.csv`
- ✅ `Google.csv`
- ✅ `TikTok.csv`
- ✅ `Business.csv`

### Step 2: Upload to GitHub

#### Option A: Using GitHub Web Interface (Recommended)

1. **Go to your GitHub repository** in your web browser
2. **Click "Add file"** → "Upload files"
3. **Drag and drop** all CSV files:
   - `Facebook.csv`
   - `Google.csv`
   - `TikTok.csv`
   - `Business.csv`
4. **Add commit message**: "Add CSV data files for dashboard"
5. **Click "Commit changes"**

#### Option B: Using Git Commands

```bash
# Navigate to your project directory
cd C:\Users\abhim\OneDrive\Documents\Model\Lifesight

# Initialize git (if not already done)
git init
git remote add origin https://github.com/yourusername/your-repo-name.git

# Add all files
git add .
git commit -m "Add marketing dashboard with CSV data files"

# Push to GitHub
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Select your repository**
5. **Set main file path to**: `marketing_dashboard.py`
6. **Click "Deploy"**

## 🔧 Updated Dashboard Features

The updated dashboard now:
- ✅ **Tries multiple file paths** for local vs cloud deployment
- ✅ **Shows which path worked** when files are found
- ✅ **Falls back to sample data** if CSV files aren't found
- ✅ **Works both locally and on Streamlit Cloud**

### File Path Priority:
1. **Local paths**: `Facebook.csv`, `Google.csv`, etc.
2. **Cloud paths**: `./Facebook.csv`, `./Google.csv`, etc.
3. **Alternative cloud paths**: `/mount/src/marketing-intelligence-dashboard/...`

## 📁 Required Repository Structure

Your GitHub repository should look like this:
```
your-repo/
├── marketing_dashboard.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── Facebook.csv
├── Google.csv
├── TikTok.csv
├── Business.csv
├── upload_csv_to_github.md
├── DEPLOYMENT_COMPLETE_GUIDE.md
└── test_file_paths.py
```

## 🎯 Expected Results

### Before Uploading CSV Files:
- Dashboard shows: "⚠️ CSV files not found. Using sample data for demonstration."
- Uses generated sample data
- All features work but with fake data

### After Uploading CSV Files:
- Dashboard shows: "✅ Loaded data from CSV files at: Facebook.csv"
- Uses your actual marketing data
- Shows real campaign performance
- Generates insights based on your data

## 🚀 Testing Your Deployment

1. **Test locally first**:
   ```bash
   python -m streamlit run marketing_dashboard.py
   ```

2. **Verify CSV files are found**:
   ```bash
   python test_file_paths.py
   ```

3. **Deploy to Streamlit Cloud**
4. **Check the dashboard** - should show "✅ Loaded data from CSV files"

## 🆘 Troubleshooting

### If CSV files still not found on Streamlit Cloud:
1. **Check file names** - must be exactly `Facebook.csv`, `Google.csv`, etc.
2. **Check file location** - must be in the root directory of your repository
3. **Check file size** - ensure files uploaded completely
4. **Redeploy** - Streamlit Cloud should auto-update

### If dashboard shows sample data:
1. **Verify CSV files are in GitHub repository**
2. **Check file names match exactly**
3. **Wait a few minutes** for Streamlit Cloud to update
4. **Refresh the dashboard**

## 🎉 Success!

Once deployed correctly, your Marketing Intelligence Dashboard will:
- ✅ Load your actual marketing data
- ✅ Show real business metrics
- ✅ Display actual campaign performance
- ✅ Generate insights based on your data
- ✅ Work on both local and cloud environments

Your dashboard is now ready for production use!
