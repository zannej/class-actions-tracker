import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime
import sys

print("=" * 60)
print("SCRAPER DEBUG MODE")
print("=" * 60)

SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU"  # Replace with your actual Sheet ID

try:
    print("\n[CHECK 1] Environment Variables")
    print(f"  GOOGLE_CREDS set: {bool(os.getenv('GOOGLE_CREDS'))}")
    creds_json = os.getenv('GOOGLE_CREDS')
    
    if not creds_json:
        print("  ✗ GOOGLE_CREDS not found!")
        sys.exit(1)
    
    print("\n[CHECK 2] Parsing Credentials JSON")
    try:
        creds_dict = json.loads(creds_json)
        print(f"  ✓ JSON parsed successfully")
        print(f"  Project ID: {creds_dict.get('project_id')}")
        print(f"  Client Email: {creds_dict.get('client_email')}")
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON parsing failed: {e}")
        sys.exit(1)
    
    print("\n[CHECK 3] Creating Credentials Object")
    try:
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        print("  ✓ Credentials object created")
    except Exception as e:
        print(f"  ✗ Failed to create credentials: {e}")
        sys.exit(1)
    
    print("\n[CHECK 4] Authorizing with Google Sheets")
    try:
        gc = gspread.authorize(creds)
        print("  ✓ Authorization successful")
    except Exception as e:
        print(f"  ✗ Authorization failed: {e}")
        sys.exit(1)
    
    print("\n[CHECK 5] Opening Sheet")
    print(f"  Sheet ID: {SHEET_ID}")
    try:
        sheet = gc.open_by_key(SHEET_ID)
        print(f"  ✓ Sheet opened: {sheet.title}")
    except Exception as e:
        print(f"  ✗ Failed to open sheet: {e}")
        print(f"  Make sure you shared the sheet with: {creds_dict.get('client_email')}")
        sys.exit(1)
    
    print("\n[CHECK 6] Finding Raw_Scrapes Worksheet")
    try:
        raw_scrapes_tab = sheet.worksheet('Raw_Scrapes')
        print("  ✓ Raw_Scrapes worksheet found")
    except Exception as e:
        print(f"  ✗ Raw_Scrapes worksheet not found: {e}")
        print("  Available worksheets:")
        for ws in sheet.worksheets():
            print(f"    - {ws.title}")
        sys.exit(1)
    
    print("\n[CHECK 7] Writing Test Data")
    try:
        timestamp = datetime.now().isoformat()
        row_data = [timestamp, "Test from scraper", "1"]
        print(f"  Data to write: {row_data}")
        raw_scrapes_tab.append_row(row_data)
        print(f"  ✓ Data written successfully")
    except Exception as e:
        print(f"  ✗ Failed to write data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓✓✓ ALL CHECKS PASSED ✓✓✓")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
