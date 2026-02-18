"""
Data Management Page - Greene County Property Finder
"""
import streamlit as st

st.set_page_config(page_title="Data Management", page_icon="🔧")

st.title("🔧 Data Management")

st.error("⚠️ Greene County parcel data is NOT available in the public NYS GIS API.")

st.info("""
**What this means:**
- Bulk data download for Greene County is not possible via the public API
- The county has not authorized NYS to share their data

**Your options:**
1. Contact Greene County Real Property Tax Services directly
2. Use the NYS Assessment Lookup tool (main app) for single properties
3. Try a different county

**To contact Greene County:**
- Phone: (518) 719-3530
- Website: greenegov.com
""")

st.subheader("API Status Check")
if st.button("Check API Status"):
    from data_loader import GreeneCountyParcelLoader
    loader = GreeneCountyParcelLoader()
    status = loader.check_data_availability()
    st.json(status)
