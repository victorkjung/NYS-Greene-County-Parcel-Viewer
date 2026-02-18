"""
Analytics Page - Greene County Property Finder
"""
import streamlit as st
import pandas as pd
from data_loader import GreeneCountyParcelLoader

st.set_page_config(page_title="Analytics", page_icon="📊")

st.title("📊 Analytics")

st.error("⚠️ Greene County data not available. Select a different county.")

county = st.selectbox("Select County", ['Albany', 'Suffolk', 'Ulster', 'Orange', 'Sullivan'])

if st.button("Load Analytics"):
    if county == 'Greene':
        st.error("Select a different county.")
    else:
        with st.spinner("Loading..."):
            try:
                df = GreeneCountyParcelLoader().fetch_parcels(county=county, limit=5000)
                st.success(f"Loaded {len(df)} parcels")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Parcels", len(df))
                col2.metric("Total Value", f"${df['assessed_value'].sum():,.0f}")
                col3.metric("Avg Value", f"${df['assessed_value'].mean():,.0f}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
