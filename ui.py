"""
UI Components for Greene County Property Finder
Reusable Streamlit UI elements and styling
"""

import streamlit as st


def apply_custom_css():
    """Apply custom CSS styling to the app"""
    st.markdown("""
    <style>
        /* Main app background */
        .stApp {
            background-color: #1a1a2e;
        }
        
        /* Headers */
        h1, h2, h3, h4 {
            color: #e94560 !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #16213e;
        }
        
        /* Cards/Containers */
        .property-card {
            background: #16213e;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #0f3460;
        }
        
        /* Success boxes */
        .success-box {
            background: #1b4332;
            border: 1px solid #40916c;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        /* Info boxes */
        .info-box {
            background: #0f3460;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        /* Warning boxes */
        .warning-box {
            background: #5c4033;
            border: 1px solid #d4a373;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        /* Stat boxes */
        .stat-box {
            background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid #e94560;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #e94560;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #888;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #e94560;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #ff6b6b;
            transform: translateY(-2px);
        }
        
        /* Links */
        a {
            color: #e94560 !important;
        }
        
        /* Tables */
        .dataframe {
            background-color: #16213e !important;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            color: #e94560;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = None, icon: str = "🗺️"):
    """Render a styled page header"""
    st.markdown(f"# {icon} {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.markdown("---")


def render_stat_card(label: str, value: str, icon: str = "📊"):
    """Render a statistics card"""
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-value">{icon} {value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_property_card(parcel: dict):
    """Render a property information card"""
    st.markdown(f"""
    <div class="property-card">
        <h4>{parcel.get('owner', 'Unknown Owner')}</h4>
        <p><strong>Parcel ID:</strong> {parcel.get('parcel_id', 'N/A')}</p>
        <p><strong>Type:</strong> {parcel.get('property_class_desc', 'Unknown')}</p>
        <p><strong>Acreage:</strong> {parcel.get('acreage', 0):.2f} acres</p>
        <p><strong>Assessed Value:</strong> ${parcel.get('assessed_value', 0):,.0f}</p>
        <p><strong>Municipality:</strong> {parcel.get('municipality', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)


def render_info_box(content: str, box_type: str = "info"):
    """Render a styled info/warning/success box"""
    box_class = f"{box_type}-box"
    st.markdown(f"""
    <div class="{box_class}">
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_metrics_row(metrics: list):
    """
    Render a row of metrics
    
    Args:
        metrics: List of dicts with 'label', 'value', and optional 'delta'
    """
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            if 'delta' in metric:
                st.metric(
                    label=metric['label'],
                    value=metric['value'],
                    delta=metric['delta']
                )
            else:
                st.metric(
                    label=metric['label'],
                    value=metric['value']
                )


def render_sidebar_filters(df):
    """
    Render common sidebar filters
    
    Args:
        df: DataFrame with parcel data
        
    Returns:
        Dictionary of filter values
    """
    filters = {}
    
    with st.sidebar:
        st.markdown("### 🔍 Filters")
        
        # Search
        filters['search'] = st.text_input(
            "Search owner/parcel:",
            placeholder="Enter name or ID..."
        )
        
        # Property type
        if 'property_class_desc' in df.columns:
            prop_types = ['All'] + sorted(df['property_class_desc'].dropna().unique().tolist())
            filters['property_type'] = st.selectbox("Property Type:", prop_types)
        
        # Acreage range
        if 'acreage' in df.columns:
            max_acres = min(df['acreage'].max(), 500)
            filters['acreage_range'] = st.slider(
                "Acreage Range:",
                0.0,
                float(max_acres),
                (0.0, float(max_acres))
            )
        
        # Value range
        if 'assessed_value' in df.columns:
            max_value = min(df['assessed_value'].max(), 5000000)
            filters['value_range'] = st.slider(
                "Assessed Value:",
                0,
                int(max_value),
                (0, int(max_value)),
                step=10000,
                format="$%d"
            )
        
        # Municipality
        if 'municipality' in df.columns:
            munis = ['All'] + sorted(df['municipality'].dropna().unique().tolist())
            filters['municipality'] = st.selectbox("Municipality:", munis)
    
    return filters


def apply_filters(df, filters: dict):
    """
    Apply filters to DataFrame
    
    Args:
        df: DataFrame to filter
        filters: Dictionary of filter values from render_sidebar_filters
        
    Returns:
        Filtered DataFrame
    """
    filtered = df.copy()
    
    # Search filter
    if filters.get('search'):
        search = filters['search'].lower()
        mask = (
            filtered['owner'].str.lower().str.contains(search, na=False) |
            filtered['parcel_id'].str.lower().str.contains(search, na=False)
        )
        filtered = filtered[mask]
    
    # Property type filter
    if filters.get('property_type') and filters['property_type'] != 'All':
        filtered = filtered[filtered['property_class_desc'] == filters['property_type']]
    
    # Acreage filter
    if filters.get('acreage_range'):
        min_acres, max_acres = filters['acreage_range']
        filtered = filtered[
            (filtered['acreage'] >= min_acres) & 
            (filtered['acreage'] <= max_acres)
        ]
    
    # Value filter
    if filters.get('value_range'):
        min_val, max_val = filters['value_range']
        filtered = filtered[
            (filtered['assessed_value'] >= min_val) & 
            (filtered['assessed_value'] <= max_val)
        ]
    
    # Municipality filter
    if filters.get('municipality') and filters['municipality'] != 'All':
        filtered = filtered[filtered['municipality'] == filters['municipality']]
    
    return filtered


def get_property_color(property_class: str) -> str:
    """Get color for a property class"""
    property_class = str(property_class)
    
    if property_class.startswith('2'):
        return 'green'      # Residential
    elif property_class.startswith('3'):
        return 'yellow'     # Vacant
    elif property_class.startswith('9'):
        return 'blue'       # State/Forest
    elif property_class.startswith('1'):
        return 'lightgreen' # Agricultural
    elif property_class.startswith('4'):
        return 'orange'     # Commercial
    elif property_class.startswith('5'):
        return 'purple'     # Recreation
    elif property_class.startswith('6'):
        return 'gray'       # Community Service
    else:
        return 'gray'       # Other
