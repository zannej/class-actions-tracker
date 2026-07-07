import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import sys

print("=" * 60)
print("SCRAPER WITH ERROR DETAILS")
print("=" * 60)

try:
    print("\n[1] Loading credentials.json...")
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    print("    ✓ Success")
    
    print("\n[2] Authorizing with gspread...")
    gc = gspread.authorize(creds)
    print("    ✓ Success")
    
    print("\n[3] Opening Google Sheet...")
    sheet = gc.open_by_key("1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU")
    print(f"    ✓ Success - Sheet: {sheet.title}")
    
    print("\n[4] Getting worksheet list...")
    worksheets = sheet.worksheets()
    print(f"    Found {len(worksheets)} worksheets:")
    for ws in worksheets:
        print(f"      - {ws.title}")
    
    print("\n[5] Getting Raw_Scrapes worksheet...")
    raw_scrapes = sheet.worksheet('Raw_Scrapes')
    print(f"    ✓ Success - Title: {raw_scrapes.title}")
    
    print("\n[6] Preparing data...")
    timestamp = datetime.now().isoformat()
    row_data = [timestamp, "Test entry", "1"]
    print(f"    ✓ Data: {row_data}")
    
    print("\n[7] Appending row to worksheet...")
    result = raw_scrapes.append_row(row_data)
    print(f"    ✓ Success - Result: {result}")
    
    print("\n" + "=" * 60)
    print("✓✓✓ EVERYTHING WORKED ✓✓✓")
    print("=" * 60)
    print("\nIf you don't see data in your sheet, there may be a")
    print("permission or sharing issue. Check your Sheet sharing settings.")
    
except gspread.exceptions.APIError as e:
    print(f"\n✗ GSPREAD API ERROR: {e}")
    print(f"   Error code: {e.response.status_code}")
    print(f"   Error message: {e.response.text}")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
