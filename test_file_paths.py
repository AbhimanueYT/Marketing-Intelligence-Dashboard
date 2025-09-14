import pandas as pd
import os

def test_csv_file_paths():
    """Test different file paths to find CSV files"""
    
    # List of possible file paths
    file_paths = [
        # Local development paths
        ('Facebook.csv', 'Google.csv', 'TikTok.csv', 'Business.csv'),
        # Cloud deployment paths (same directory)
        ('./Facebook.csv', './Google.csv', './TikTok.csv', './Business.csv'),
        # Alternative cloud paths
        ('/mount/src/marketing-intelligence-dashboard/Facebook.csv', 
         '/mount/src/marketing-intelligence-dashboard/Google.csv',
         '/mount/src/marketing-intelligence-dashboard/TikTok.csv',
         '/mount/src/marketing-intelligence-dashboard/Business.csv')
    ]
    
    print("🔍 Testing CSV file paths...")
    print("=" * 50)
    
    for i, (fb_path, go_path, tt_path, bus_path) in enumerate(file_paths):
        print(f"\n📍 Testing path set {i+1}:")
        print(f"  Facebook: {fb_path}")
        print(f"  Google: {go_path}")
        print(f"  TikTok: {tt_path}")
        print(f"  Business: {bus_path}")
        
        # Check if files exist
        files_exist = []
        for path in [fb_path, go_path, tt_path, bus_path]:
            if os.path.exists(path):
                files_exist.append(True)
                print(f"    ✅ {path} - EXISTS")
            else:
                files_exist.append(False)
                print(f"    ❌ {path} - NOT FOUND")
        
        # If all files exist, try to load them
        if all(files_exist):
            try:
                facebook_df = pd.read_csv(fb_path)
                google_df = pd.read_csv(go_path)
                tiktok_df = pd.read_csv(tt_path)
                business_df = pd.read_csv(bus_path)
                
                print(f"    🎉 SUCCESS! All files loaded successfully")
                print(f"    📊 Facebook records: {len(facebook_df)}")
                print(f"    📊 Google records: {len(google_df)}")
                print(f"    📊 TikTok records: {len(tiktok_df)}")
                print(f"    📊 Business records: {len(business_df)}")
                return True
            except Exception as e:
                print(f"    ⚠️ Error loading files: {str(e)}")
        else:
            print(f"    ❌ Some files missing in this path set")
    
    print(f"\n❌ No working file path found")
    print(f"💡 Make sure CSV files are in the same directory as the Python file")
    return False

if __name__ == "__main__":
    test_csv_file_paths()
