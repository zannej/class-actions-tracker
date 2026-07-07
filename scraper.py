import requests
from datetime import datetime
import os

AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

print("=" * 60)
print("CLASS ACTIONS TRACKER - AIRTABLE SCRAPER")
print("=" * 60)

def write_to_airtable(timestamp, description, count):
    """Write data to Airtable Raw_Scrapes table"""
    print(f"\n[WRITING] Adding entry to Airtable...")
    
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Raw_Scrapes"
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "records": [
            {
                "fields": {
                    "Timestamp": timestamp,
                    "Description": description,
                    "Count": count
                }
            }
        ]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print(f"  ✓ Success!")
            print(f"  Timestamp: {timestamp}")
            print(f"  Description: {description}")
            return True
        else:
            print(f"  ✗ Error: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

# Main
try:
    print("\n[CHECK] Verifying credentials...")
    
    if not AIRTABLE_TOKEN:
        print("  ✗ AIRTABLE_TOKEN not found!")
        exit(1)
    
    if not AIRTABLE_BASE_ID:
        print("  ✗ AIRTABLE_BASE_ID not found!")
        exit(1)
    
    print("  ✓ Credentials found")
    
    # Write test entry
    timestamp = datetime.now().isoformat()
    success = write_to_airtable(
        timestamp=timestamp,
        description="Scraper test run - Airtable working!",
        count=1
    )
    
    if success:
        print("\n" + "=" * 60)
        print("✓✓✓ SCRAPER COMPLETED SUCCESSFULLY ✓✓✓")
        print("=" * 60)
        print("\nCheck your Airtable Raw_Scrapes table!")
    else:
        print("\n" + "=" * 60)
        print("✗ SCRAPER FAILED")
        print("=" * 60)
        exit(1)

except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
