import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU"

# Headers to avoid being blocked
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
    """Scrape Federal Court class actions"""
    print("\n[SCRAPING] Federal Court...")
    cases = []
    try:
        url = "https://www.fedcourt.gov.au/law-and-practice/class-actions/class-actions"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for class action links
        links = soup.find_all('a', href=True)
        for link in links[:10]:  # Get first 10
            text = link.get_text(strip=True)
            if 'class action' in text.lower() or len(text) > 20:
                cases.append({
                    'source': 'Federal Court',
                    'name': text[:100],
                    'url': link['href'],
                    'date_found': datetime.now().isoformat()
                })
        
        print(f"  ✓ Found {len(cases)} potential cases")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return cases

def scrape_nsw_supreme_court():
    """Scrape NSW Supreme Court class actions"""
    print("\n[SCRAPING] NSW Supreme Court...")
    cases = []
    try:
        url = "https://www.supremecourt.justice.nsw.gov.au/Pages/sco2_classactions/sco2_current_class_actions.aspx"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for case listings
        rows = soup.find_all('tr')
        for row in rows[:10]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                case_name = cols[0].get_text(strip=True)
                if case_name and len(case_name) > 5:
                    cases.append({
                        'source': 'NSW Supreme Court',
                        'name': case_name[:100],
                        'date_found': datetime.now().isoformat()
                    })
        
        print(f"  ✓ Found {len(cases)} cases")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return cases

def scrape_vic_supreme_court():
    """Scrape Victorian Supreme Court class actions"""
    print("\n[SCRAPING] Victorian Supreme Court...")
    cases = []
    try:
        url = "https://www.supremecourt.vic.gov.au/areas/group-proceedings"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for proceeding titles
        headings = soup.find_all(['h2', 'h3'])
        for heading in headings[:10]:
            text = heading.get_text(strip=True)
            if text and len(text) > 5:
                cases.append({
                    'source': 'VIC Supreme Court',
                    'name': text[:100],
                    'date_found': datetime.now().isoformat()
                })
        
        print(f"  ✓ Found {len(cases)} cases")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return cases

def scrape_lawyerly():
    """Scrape Lawyerly class actions news"""
    print("\n[SCRAPING] Lawyerly...")
    articles = []
    try:
        url = "https://www.lawyerly.com.au/category/practice-areas/class-actions/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for article headlines
        headlines = soup.find_all(['h2', 'h3', 'h1'])
        for headline in headlines[:10]:
            text = headline.get_text(strip=True)
            if text and len(text) > 10 and 'class' in text.lower():
                articles.append({
                    'source': 'Lawyerly',
                    'title': text[:100],
                    'date_found': datetime.now().isoformat()
                })
        
        print(f"  ✓ Found {len(articles)} articles")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return articles

def scrape_maurice_blackburn():
    """Scrape Maurice Blackburn class actions"""
    print("\n[SCRAPING] Maurice Blackburn...")
    cases = []
    try:
        url = "https://www.mauriceblackburn.com.au/class-actions/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for case links/titles
        links = soup.find_all('a', href=True)
        for link in links[:15]:
            text = link.get_text(strip=True)
            if text and len(text) > 5:
                cases.append({
                    'source': 'Maurice Blackburn',
                    'name': text[:100],
                    'url': link['href'] if link['href'].startswith('http') else 'mauriceblackburn.com.au',
                    'date_found': datetime.now().isoformat()
                })
        
        print(f"  ✓ Found {len(cases)} cases")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return cases

def scrape_shine_lawyers():
    """Scrape Shine Lawyers class actions"""
    print("\n[SCRAPING] Shine Lawyers...")
    cases = []
    try:
        url = "https://www.shine.com.au/service/class-actions"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for case headings
        headings = soup.find_all(['h2', 'h3'])
        for heading in headings[:10]:
            text = heading.get_text(strip=True)
            if text and len(text) > 5:
                cases.append({
                    'source': 'Shine Lawyers',
                    'name': text[:100],
                    'date_found': datetime.now().isoformat()
                })
        
        print(f"  ✓ Found {len(cases)} cases")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return cases

def scrape_slater_gordon():
    """Scrape Slater and Gordon class actions"""
    print("\n[SCRAPING] Slater and Gordon...")
    cases = []
    try:
        url = "https://www.slatergordon.com.au/class-actions/current-class-actions"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for case titles
        divs = soup.find_all('div', class_=['case', 'proceeding', 'item'])
        for div in divs[:10]:
            text = div.get_text(strip=True)
            if text and len(text) > 10:
                cases.append({
                    'source': 'Slater and Gordon',
                    'name': text[:100],
                    'date_found': datetime.now().isoformat()
                })
        
        print(f"  ✓ Found {len(cases)} cases")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return cases

def scrape_omni_bridgeway():
    """Scrape Omni Bridgeway funded cases"""
    print("\n[SCRAPING] Omni Bridgeway...")
    cases = []
    try:
        url = "https://omnibridgeway.com/insights/company-insights"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for case announcements
        articles = soup.find_all(['article', 'div'], class_=['post', 'case', 'item'])
        for article in articles[:10]:
            text = article.get_text(strip=True)
            if text and len(text) > 10:
                cases.append({
                    'source': 'Omni Bridgeway',
                    'name': text[:100],
                    'funder': 'Omni Bridgeway',
                    'date_found': datetime.now().isoformat()
                })
        
        print(f"  ✓ Found {len(cases)} cases")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return cases

def main():
    """Main scraper function"""
    print("=" * 60)
    print("CLASS ACTIONS TRACKER - FULL SCRAPER")
    print("=" * 60)
    
    start_time = datetime.now()
    all_cases = []
    
    # Run all scrapers
    all_cases.extend(scrape_federal_court())
    time.sleep(1)
    all_cases.extend(scrape_nsw_supreme_court())
    time.sleep(1)
    all_cases.extend(scrape_vic_supreme_court())
    time.sleep(1)
    all_cases.extend(scrape_lawyerly())
    time.sleep(1)
    all_cases.extend(scrape_maurice_blackburn())
    time.sleep(1)
    all_cases.extend(scrape_shine_lawyers())
    time.sleep(1)
    all_cases.extend(scrape_slater_gordon())
    time.sleep(1)
    all_cases.extend(scrape_omni_bridgeway())
    
    print(f"\n{'=' * 60}")
    print(f"Total items collected: {len(all_cases)}")
    print(f"Time taken: {(datetime.now() - start_time).seconds} seconds")
    print(f"{'=' * 60}")
    
    # Write to Raw_Scrapes tab
    try:
        sheet = connect_sheet()
        raw_scrapes = sheet.worksheet('Raw_Scrapes')
        
        timestamp = datetime.now().isoformat()
        raw_scrapes.append_row([
            timestamp,
            f"Scraped {len(all_cases)} items from 8 sources",
            len(all_cases)
        ])
        
        print(f"\n✓ Scrape record added to Raw_Scrapes")
        print(f"✓ SCRAPER COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"\n✗ Failed to write to sheet: {e}")

if __name__ == "__main__":
    main()
