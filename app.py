"""
Greene County Property Finder - OnXHunt-style Property Owner Identification
A Streamlit application for exploring tax parcels in Greene County, NY

VERSION 3.0 - No Sample Data
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
from constants import DEFAULT_DATA_FILE
from data_loader import GreeneCountyParcelLoader

# Page configuration
st.set_page_config(
    page_title="Greene County Property Finder",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize loader
loader = GreeneCountyParcelLoader()

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; }
    [data-testid="stSidebar"] { background-color: #16213e; }
    h1, h2, h3 { color: #e94560 !important; }
    .stTextInput input { background-color: #16213e; color: #eaeaea; }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🗺️ Greene County Property Finder")
    
    # Sidebar - Data Source
    with st.sidebar:
        st.header("📡 Data Source")
        
        # Check availability
        with st.spinner("Checking API availability..."):
            status = loader.check_data_availability()
        
        if status['available']:
            st.success("✅ Greene County data available!")
        else:
            st.error("⚠️ Greene County data NOT available in public API")
            st.info("""
            **Options:**
            1. Greene County doesn't share parcel data publicly
            2. Contact Greene County Real Property directly
            3. Use a different county (Albany, Suffolk, etc.)
            4. Use Assessment Lookup (single parcel)
            """)
        
        # County selector
        available_counties = ['Greene', 'Albany', 'Suffolk', 'Ulster', 'Orange', 'Sullivan']
        selected_county = st.selectbox("Select County", available_counties)
        
        # Municipality
        municipality = st.text_input("Municipality (optional)", placeholder="e.g., Hunter, Catskill")
        
        # Limit
        limit = st.slider("Max parcels to fetch", 100, 5000, 1000)
        
        fetch_button = st.button("🔄 Fetch Data", type="primary")
    
    # Main content
    if fetch_button:
        if not status['available'] and selected_county == 'Greene':
            st.error("""
            ❌ ** Greene County parcel data is not available in the public NYS GIS API. **
            
            The county has not authorized NYS to share their parcel data publicly.
            
            **Alternatives:**
            - Contact Greene County Real Property Tax Services
            - Use the Assessment Lookup tool (sidebar)
            - Try a different county
            """)
        else:
            with st.spinner(f"Fetching {selected_county} parcels..."):
                try:
                    df = loader.fetch_parcels(county=selected_county, municipality=municipality, limit=limit)
                    
                    st.success(f"✅ Retrieved {len(df)} parcels")
                    
                    # Display data
                    if len(df) > 0:
                        st.dataframe(df, use_container_width=True)
                        
                        # Stats
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Parcels", len(df))
                        with col2:
                            st.metric("Total Value", f"${df['assessed_value'].sum():,.0f}")
                        with col3:
                            avg_value = df['assessed_value'].mean()
                            st.metric("Avg Value", f"${avg_value:,.0f}")
                    else:
                        st.warning("No parcels found with the selected criteria.")
                        
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")
    
    # Assessment Lookup section
    st.divider()
    st.subheader("🔍 NYS Assessment Lookup")
    st.info("Look up a specific property by coordinates (works for all of NY!)")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=42.25, format="%.6f")
    with col2:
        lon = st.number_input("Longitude", value=-74.25, format="%.6f")
    
    if st.button("Lookup"):
        with st.spinner("Looking up..."):
            result = loader.fetch_assessment_lookup(lon, lat)
            if result:
                st.json(result)
            else:
                st.warning("No property found at those coordinates")

if __name__ == "__main__":
    main()
