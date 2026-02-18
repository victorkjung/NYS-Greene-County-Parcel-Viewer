"""
Owner Lookup - OPTIMIZED VERSION
"""

import streamlit as st
import pandas as pd
import folium
import streamlit.components.v1 as components
from pathlib import Path
import json

st.set_page_config(
    page_title="Owner Lookup | Greene County Property Finder",
    page_icon="👤",
    layout="wide"
)

# Cache data in session state - load ONCE
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_all_data():
    """Load parcel data once and cache it"""
    data_path = Path(__file__).parent.parent / "data" / "zip_12450_parcels.json"
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Pre-compute owner stats - cached
@st.cache_data(ttl=3600)
def get_owner_stats(df):
    """Pre-compute owner statistics"""
    stats = df.groupby('owner').agg({
        'parcel_id': 'count',
        'acreage': 'sum',
        'assessed_value': 'sum',
        'annual_taxes': 'sum'
    }).reset_index()
    stats.columns = ['owner', 'parcel_count', 'total_acreage', 'total_value', 'total_taxes']
    return stats

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #1a1a2e; }
    h1, h2, h3 { color: #e94560 !important; }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("👤 Owner Lookup")
    st.markdown("*Search property portfolios by owner*")
    
    # Load data ONCE
    with st.spinner("Loading data..."):
        df = load_all_data()
        owner_stats = get_owner_stats(df)
    
    st.success(f"Loaded {len(df):,} parcels, {len(owner_stats):,} owners")
    
    # Search with instant filtering
    search_query = st.text_input("🔍 Search Owner Name:", placeholder="Type to search...")
    
    # Fast filtering using pre-computed stats
    if search_query:
        # Use vectorized string matching - much faster!
        mask = owner_stats['owner'].str.lower().str.contains(search_query.lower(), na=False)
        filtered_owners = owner_stats[mask]
    else:
        filtered_owners = owner_stats.head(100)  # Show top 100 by default
    
    st.markdown(f"**{len(filtered_owners):,} owners found**")
    
    if len(filtered_owners) > 0:
        # Owner selection dropdown
        owner_options = filtered_owners['owner'].tolist()
        selected_owner = st.selectbox("Select Owner:", owner_options)
        
        if selected_owner:
            owner_info = filtered_owners[filtered_owners['owner'] == selected_owner].iloc[0]
            owner_parcels = df[df['owner'] == selected_owner]
            
            # Quick stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Parcels", int(owner_info['parcel_count']))
            with col2:
                st.metric("Acres", f"{owner_info['total_acreage']:.1f}")
            with col3:
                st.metric("Value", f"${owner_info['total_value']:,.0f}")
            with col4:
                st.metric("Taxes", f"${owner_info['total_taxes']:,.0f}")
            
            # Address
            first = owner_parcels.iloc[0]
            st.write(f"📬 {first['mailing_address']}, {first['mailing_city']}, {first['mailing_state']} {first['mailing_zip']}")
            
            # Simple map
            if len(owner_parcels) > 0:
                center = [owner_parcels['latitude'].mean(), owner_parcels['longitude'].mean()]
                m = folium.Map(location=center, zoom_start=13)
                
                for _, row in owner_parcels.iterrows():
                    folium.Marker(
                        location=[row['latitude'], row['longitude']],
                        popup=f"{row['parcel_id']}: ${row['assessed_value']:,}"
                    ).add_to(m)
                
                components.html(m._repr_html_(), height=300)
            
            # Show parcels in expandable section
            with st.expander(f"View {len(owner_parcels)} Parcels"):
                st.dataframe(owner_parcels[['parcel_id', 'property_class_desc', 'acreage', 'assessed_value', 'municipality']])
                
                # Download
                csv = owner_parcels.to_csv(index=False)
                st.download_button("📥 Download CSV", csv, f"{selected_owner[:10]}_parcels.csv", "text/csv")
    
    # Sidebar stats
    with st.sidebar:
        st.markdown("### Top Landowners")
        top = owner_stats.nlargest(10, 'total_acreage')
        for _, o in top.iterrows():
            st.write(f"• {o['owner'][:25]} ({o['total_acreage']:.0f} ac)")

if __name__ == "__main__":
    main()
