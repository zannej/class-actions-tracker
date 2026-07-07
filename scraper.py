import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import requests
from bs4 import BeautifulSoup

SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def connect_sheet():
    """Connect to Google Sheet"""
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(SHEET_ID)

def scrape_federal_court():
    """Scrape Federal Court - simplified"""
    print("\n[1] Checking Federal Court...")
    try:
        url = "https://www.fedcourt.gov.au/law-and-practice/class-actions/class-actions"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print("    ✓ Federal Court website is accessible")
            return 1
        else:
            print(f"    ✗ Got status code {response.status_code}")
            return 0
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return 0

def scrape_nsw_supreme_court():
    """Scrape NSW Supreme Court - simplified"""
    print("\n[2] Checking NSW Supreme Court...")
    try:
        url = "https://www.supremecourt.justice.nsw.gov.au/Pages/sco2_classactions/sco2_current_class_actions.aspx"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print("    ✓ NSW Supreme Court website is accessible")
            return 1
        else:
            print(f"    ✗ Got status code {response.status_code}")
            return 0
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return 0

def scrape_vic_supreme_court():
    """Scrape VIC Supreme Court - simplified"""
    print("\n[3] Checking VIC Supreme Court...")
    try:
        url = "https://www.supremecourt.vic.gov.au/areas/group-proceedings"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print("    ✓ VIC Supreme Court website is accessible")
            return 1
        else:
            print(f"    ✗ Got status code {response.status_code}")
            return 0
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return 0

def scrape_lawyerly():
    """Scrape Lawyerly - simplified"""
    print("\n[4] Checking Lawyerly...")
    try:
        url = "https://www.lawyerly.com.au/category/practice-areas/class-actions/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print("    ✓ Lawyerly website is accessible")
            return 1
        else:
            print(f"    ✗ Got status code {response.status_code}")
            return 0
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return 0

def main():
    """Main scraper function"""
    print("=" * 60)
    print("CLASS ACTIONS TRACKER SCRAPER")
    print("=" * 60)
    
    # Test all sources
    fed_count = scrape_federal_court()
    nsw_count = scrape_nsw_supreme_court()
    vic_count = scrape_vic_supreme_court()
    lawyerly_count = scrape_lawyerly()
    
    total = fed_count + nsw_count + vic_count + lawyerly_count
    
    print(f"\n{'=' * 60}")
    print(f"Sources checked: {total}/4 accessible")
    print(f"{'=' * 60}")
    
    # Write to Raw_Scrapes tab
    try:
        print("\n[WRITING] Connecting to Google Sheet...")
        sheet = connect_sheet()
        raw_scrapes = sheet.worksheet('Raw_Scrapes')
        
        timestamp = datetime.now().isoformat()
        raw_scrapes.append_row([
            timestamp,
            f"Scraper check - {total}/4 sources accessible",
            total
        ])
        
        print("✓ Data written to Raw_Scrapes")
        print("✓ SCRAPER COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"✗ Failed to write to sheet: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
