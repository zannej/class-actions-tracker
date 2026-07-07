import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime

print("=" * 60)
print("CLASS ACTIONS TRACKER SCRAPER")
print("=" * 60)

SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU" 

try:
    print("\n[1] Setting up credentials...")
    creds_json = os.getenv('GOOGLE_CREDS')
    
    if creds_json:
        print("    ✓ Using environment credentials")
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
    else:
        print("    ✓ Using local credentials.json")
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
    
    print("\n[2] Connecting to Google Sheet...")
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(SHEET_ID)
    print(f"    ✓ Connected to: {sheet.title}")
    
    print("\n[3] Accessing Raw_Scrapes tab...")
    raw_scrapes_tab = sheet.worksheet('Raw_Scrapes')
    print("    ✓ Raw_Scrapes tab found")
    
    print("\n[4] Adding scrape record...")
    timestamp = datetime.now().isoformat()
    raw_scrapes_tab.append_row([
        timestamp,
        "Automated scraper run - test entry",
        "1"
    ])
    print(f"    ✓ Record added at: {timestamp}")
    
    print("\n" + "=" * 60)
    print("✓✓✓ SCRAPER COMPLETED SUCCESSFULLY ✓✓✓")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Check your Google Sheet Raw_Scrapes tab")
    print("  2. You should see a new row with today's timestamp")
    print("  3. Scraper will run automatically every fortnight")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
