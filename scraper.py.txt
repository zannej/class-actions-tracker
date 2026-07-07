import os
import json
from datetime import datetime

print("Scraper started!")

SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU"  

try:
    import gspread
    from google.oauth2.service_account import Credentials
    
    print("Libraries imported successfully")
    
    # Get credentials
    creds_json = os.getenv('GOOGLE_CREDS')
    
    if creds_json:
        print("Using credentials from environment")
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
    else:
        print("Using local credentials.json")
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
    
    # Connect to sheet
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(SHEET_ID)
    print(f"Connected to sheet: {sheet.title}")
    
    # Add test data
    raw_scrapes = sheet.worksheet('Raw_Scrapes')
    timestamp = datetime.now().isoformat()
    raw_scrapes.append_row([timestamp, "Test entry", "Success"])
    
    print("Test entry added successfully!")
    print(f"Timestamp: {timestamp}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
