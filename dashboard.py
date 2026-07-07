import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import json
import os

st.set_page_config(
    page_title="Class Actions Tracker",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== SETUP =====
SHEET_ID = "1t5JJwuzmmA3Ve6re946xVjXTHTEmz4uQqN1N8gHxhAU"  # Replace with your Google Sheet ID

@st.cache_resource
def get_sheet_connection():
    """Connect to Google Sheets"""
    try:
        # For local testing
        if os.path.exists('credentials.json'):
            creds = Credentials.from_service_account_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
        else:
            # For GitHub Actions / Streamlit Cloud
            creds_json = st.secrets.get("google_creds")
            if creds_json:
                creds_dict = json.loads(creds_json)
                creds = Credentials.from_service_account_info(
                    creds_dict,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
            else:
                st.error("Google credentials not found. Please configure secrets.")
                return None
        
        gc = gspread.authorize(creds)
        return gc.open_by_key(SHEET_ID)
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        return None

# ===== HEADER =====
st.title("🏛️ Automated Class Actions Tracker")
st.markdown("**Real-time tracking of class actions across Australian courts**")
st.markdown("---")

# Get sheet connection
sheet = get_sheet_connection()

if sheet is None:
    st.stop()

# ===== TABS =====
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Class Actions",
    "🔍 Investigations", 
    "🔔 Alerts & Updates",
    "📊 Statistics"
])

# ===== TAB 1: CLASS ACTIONS =====
with tab1:
    st.header("Class Actions")
    
    try:
        # Get data from Class_Actions sheet
        class_actions_data = sheet.worksheet('Class_Actions').get_all_records()
        
        if not class_actions_data:
            st.info("No class actions recorded yet.")
        else:
            df_class = pd.DataFrame(class_actions_data)
            
            # Convert to proper data types
            if 'Court filing date' in df_class.columns:
                df_class['Court filing date'] = pd.to_datetime(df_class['Court filing date'], errors='coerce')
            
            # ===== FILTERS =====
            st.subheader("Filters")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                status_options = ['All'] + sorted
