import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import sys

print("=" * 60)
print("SCRAPER DEBUG MODE")
print("=" * 60)

SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU"

try:
    print("\n[CHECK 1] Loading credentials.json file")
    try:
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        print(f"  ✓ Credentials loaded")
        print(f"  Client Email: {creds.service_account_email}")
    except Exception as e:
        print(f"  ✗ Failed to load credentials.json: {e}")
        sys.exit(1)
    
    print("\n[CHECK 2] Authorizing with Google Sheets")
    try:
        gc = gspread.authorize(creds)
        print("  ✓ Authorization successful")
    except Exception as e:
        print(f"  ✗ Authorization failed: {e}")
        sys.exit(1)
    
    print("\n[CHECK 3] Opening Sheet")
    print(f"  Sheet ID: {SHEET_ID}")
    try:
        sheet = gc.open_by_key(SHEET_ID)
        print(f"  ✓ Sheet opened: {sheet.title}")
    except Exception as e:
        print(f"  ✗ Failed to open sheet: {e}")
        print(f"  Make sure you shared the sheet with: {creds.service_account_email}")
        sys.exit(1)
    
    print("\n[CHECK 4] Finding Raw_Scrapes Worksheet")
    try:
        raw_scrapes_tab = sheet.worksheet('Raw_Scrapes')
        print("  ✓ Raw_Scrapes worksheet found")
    except Exception as e:
        print(f"  ✗ Raw_Scrapes worksheet not found: {e}")
        sys.exit(1)
    
    print("\n[CHECK 5] Writing Test Data")
    try:
        timestamp = datetime.now().isoformat()
        row_data = [timestamp, "Test from scraper", "1"]
        print(f"  Data to write: {row_data}")
        raw_scrapes_tab.append_row(row_data)
        print(f"  ✓ Data written successfully")
    except Exception as e:
        print(f"  ✗ Failed to write data: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓✓✓ ALL CHECKS PASSED ✓✓✓")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
