import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import requests

SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def connect_sheet():
    """Connect to Google Sheet"""
    print("[STEP 1] Connecting to Google Sheets...")
    try:
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        print("  ✓ Credentials loaded")
        
        gc = gspread.authorize(creds)
        print("  ✓ Authorized")
        
        sheet = gc.open_by_key(SHEET_ID)
        print(f"  ✓ Sheet opened: {sheet.title}")
        
        return sheet
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_raw_scrapes_tab(sheet):
    """Get the Raw_Scrapes worksheet"""
    print("\n[STEP 2] Getting Raw_Scrapes worksheet...")
    try:
        raw_scrapes = sheet.worksheet('Raw_Scrapes')
        print("  ✓ Raw_Scrapes tab found")
        return raw_scrapes
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        print("  Available worksheets:")
        for ws in sheet.worksheets():
            print(f"    - {ws.title}")
        return None

def write_test_data(raw_scrapes):
    """Write test data to Raw_Scrapes"""
    print("\n[STEP 3] Writing test data...")
    try:
        timestamp = datetime.now().isoformat()
        row_data = [timestamp, "Test from full scraper", "1"]
        
        print(f"  Data to write: {row_data}")
        raw_scrapes.append_row(row_data)
        print("  ✓ Data written successfully!")
        return True
    except Exception as e:
        print(f"  ✗ ERROR writing data: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("SCRAPER DEBUG TEST")
    print("=" * 60)
    
    # Step 1: Connect to sheet
    sheet = connect_sheet()
    if sheet is None:
        print("\n✗ FAILED: Could not connect to sheet")
        return
    
    # Step 2: Get Raw_Scrapes tab
    raw_scrapes = get_raw_scrapes_tab(sheet)
    if raw_scrapes is None:
        print("\n✗ FAILED: Could not find Raw_Scrapes tab")
        return
    
    # Step 3: Write test data
    success = write_test_data(raw_scrapes)
    
    if success:
        print("\n" + "=" * 60)
        print("✓✓✓ SUCCESS! Check your Google Sheet ✓✓✓")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗✗✗ FAILED ✗✗✗")
        print("=" * 60)

if __name__ == "__main__":
    main()
