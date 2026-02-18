"""
Download Data Page - Greene County Property Finder
"""
import streamlit as st
import pandas as pd
from data_loader import GreeneCountyParcelLoader

st.set_page_config(page_title="Download Data", page_icon="📥")

st.title("📥 Download Parcel Data")

loader = GreeneCountyParcelLoader()

st.error("⚠️ Greene County parcel data is NOT available in the public NYS GIS API.")
st.info("""
**Options:**
1. Contact Greene County Real Property directly
2. Use the Assessment Lookup in the main app
3. Try a different county (Albany, Suffolk, etc.)
""")

# Allow selecting different county
st.subheader("Try Another County")
col1, col2 = st.columns(2)
with col1:
    county = st.selectbox("Select County", ['Albany', 'Suffolk', 'Ulster', 'Orange', 'Sullivan', 'Greene'])
with col2:
    limit = st.number_input("Max Records", 100, 10000, 1000)

if st.button("Fetch Data"):
    if county == 'Greene':
        st.error("Greene County data is not available. Please select a different county.")
    else:
        with st.spinner(f"Fetching {county}..."):
            try:
                df = loader.fetch_parcels(county=county, limit=limit)
                st.success(f"Retrieved {len(df)} parcels!")
                if len(df) > 0:
                    st.dataframe(df)
                    
                    # Download buttons
                    csv = df.to_csv(index=False)
                    st.download_button("📄 Download CSV", csv, "parcels.csv", "text/csv")
                    st.download_button("📋 Download JSON", df.to_json(orient="records"), "parcels.json", "application/json")
            except Exception as e:
                st.error(f"Error: {str(e)}")
