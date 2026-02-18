"""
Owner Lookup Page - Greene County Property Finder
"""
import streamlit as st
from data_loader import GreeneCountyParcelLoader

st.set_page_config(page_title="Owner Lookup", page_icon="👤")

st.title("👤 Owner Lookup")

st.error("⚠️ Greene County data not available. Select a different county.")

owner_name = st.text_input("Search by Owner Name")
county = st.selectbox("Select County", ['Albany', 'Suffolk', 'Ulster', 'Orange', 'Sullivan'])

if st.button("Search"):
    if county == 'Greene':
        st.error("Select a different county.")
    elif not owner_name:
        st.warning("Enter an owner name.")
    else:
        with st.spinner("Searching..."):
            try:
                df = GreeneCountyParcelLoader().fetch_parcels(county=county, limit=1000)
                results = df[df['owner'].str.contains(owner_name, case=False, na=False)]
                st.success(f"Found {len(results)} parcels")
                if len(results) > 0:
                    st.dataframe(results)
            except Exception as e:
                st.error(f"Error: {str(e)}")
