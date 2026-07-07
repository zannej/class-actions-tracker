import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

print("Starting test...")

try:
    print("\n1. Loading credentials...")
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    print("   ✓ Credentials loaded")
    
    print("\n2. Authorizing with Google...")
    gc = gspread.authorize(creds)
    print("   ✓ Authorized")
    
    print("\n3. Opening sheet...")
    sheet = gc.open_by_key("1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU")
    print(f"   ✓ Sheet opened: {sheet.title}")
    
    print("\n4. Getting Raw_Scrapes tab...")
    raw_scrapes = sheet.worksheet('Raw_Scrapes')
    print("   ✓ Tab found")
    
    print("\n5. Writing data...")
    timestamp = datetime.now().isoformat()
    raw_scrapes.append_row([timestamp, "SUCCESS - Data written!", "✓"])
    print("   ✓ Data written!")
    
    print("\n✓✓✓ TEST PASSED ✓✓✓")
    print("Check your Google Sheet now!")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
