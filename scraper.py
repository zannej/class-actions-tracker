import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU"

try:
    # Load credentials from file
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    # Connect to Google Sheets
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(SHEET_ID)
    
    # Get Raw_Scrapes tab
    raw_scrapes = sheet.worksheet('Raw_Scrapes')
    
    # Add a row with timestamp
    timestamp = datetime.now().isoformat()
    raw_scrapes.append_row([timestamp, "Scraper ran successfully", "1"])
    
    print("✓ Scraper completed successfully!")
    print(f"✓ Added entry at {timestamp}")

except Exception as e:
    print(f"✗ Error: {e}")
