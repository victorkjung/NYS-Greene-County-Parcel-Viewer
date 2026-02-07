"""
Constants for Greene County Property Finder
"""

# Greene County ArcGIS API
GREENE_COUNTY_API = "https://services6.arcgis.com/EbVsqZ18sv1kVJ3k/arcgis/rest/services/Greene_County_Tax_Parcels/FeatureServer/0"

# Default location (Lanesville, NY)
DEFAULT_LAT = 42.1856
DEFAULT_LON = -74.2848
DEFAULT_ZOOM = 14

# Default dataset file used by the app
DEFAULT_DATA_FILE = "data/zip_12450_parcels.json"

# Map settings
MAP_STYLES = {
    "satellite": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    "topo": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    "streets": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    "dark": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
}

# Property class colors
PROPERTY_COLORS = {
    "2": "#28a745",      # Green - Residential
    "3": "#ffc107",      # Yellow - Vacant
    "9": "#007bff",      # Blue - State/Forest
    "1": "#90EE90",      # Light Green - Agricultural
    "4": "#fd7e14",      # Orange - Commercial
    "5": "#6f42c1",      # Purple - Recreation
    "6": "#6c757d",      # Gray - Community Service
    "default": "#6c757d" # Gray - Other
}

# Property class descriptions
PROPERTY_CLASS_DESC = {
    "100": "Agricultural",
    "105": "Agricultural Vacant",
    "110": "Livestock",
    "112": "Dairy Farm",
    "113": "Cattle Farm",
    "117": "Horse Farm",
    "120": "Field Crops",
    "200": "Residential",
    "210": "One Family Residential",
    "220": "Two Family Residential",
    "230": "Three Family Residential",
    "240": "Rural Residence",
    "250": "Estate",
    "260": "Seasonal Residence",
    "270": "Mobile Home",
    "280": "Multiple Residences",
    "281": "Multiple Res - 2 to 3 Units",
    "283": "Multiple Res - 4 to 6 Units",
    "300": "Vacant Land",
    "311": "Vacant Land - Residential",
    "312": "Vacant Land - Under 10 Acres",
    "314": "Vacant Land - Rural",
    "322": "Vacant Land - Over 10 Acres",
    "323": "Vacant Land - Forest",
    "330": "Vacant Land - Commercial",
    "340": "Vacant Land - Industrial",
    "400": "Commercial",
    "411": "Apartments",
    "421": "Restaurant",
    "422": "Diner/Luncheonette",
    "425": "Bar",
    "430": "Motel",
    "432": "Hotel",
    "449": "Other Storage",
    "464": "Office Building",
    "480": "Multiple Use",
    "485": "One Story Small Structure",
    "500": "Recreation & Entertainment",
    "534": "Social Organization",
    "570": "Marina",
    "582": "Camping Facility",
    "590": "Park",
    "600": "Community Service",
    "612": "School",
    "620": "Religious",
    "632": "Health Facility",
    "651": "Highway Garage",
    "662": "Police/Fire Station",
    "700": "Industrial",
    "710": "Manufacturing",
    "800": "Public Service",
    "822": "Water Supply",
    "831": "Telephone",
    "900": "Wild/Forest/Conservation",
    "910": "Private Forest",
    "911": "Forest Land - Private",
    "920": "State Forest",
    "930": "State Owned - Other",
    "931": "State Owned - Forest",
    "940": "State Reforestation",
    "941": "State Land - Reforestation",
    "942": "State Land - Wilderness",
    "961": "State Owned - Other Agency",
    "962": "State Owned - DEC",
    "963": "State Park",
    "970": "Federal",
    "980": "County Land",
    "990": "Town Land",
}

# Supported zip codes
SUPPORTED_ZIP_CODES = {
    "12450": {"name": "Lanesville", "town": "Hunter", "county": "Greene"},
    "12442": {"name": "Hunter", "town": "Hunter", "county": "Greene"},
    "12485": {"name": "Tannersville", "town": "Hunter", "county": "Greene"},
    "12434": {"name": "Haines Falls", "town": "Hunter", "county": "Greene"},
    "12424": {"name": "Elka Park", "town": "Hunter", "county": "Greene"},
    "12439": {"name": "Jewett", "town": "Jewett", "county": "Greene"},
    "12436": {"name": "Hensonville", "town": "Windham", "county": "Greene"},
    "12496": {"name": "Windham", "town": "Windham", "county": "Greene"},
    "12468": {"name": "Prattsville", "town": "Prattsville", "county": "Greene"},
    "12452": {"name": "Lexington", "town": "Lexington", "county": "Greene"},
    "12492": {"name": "West Kill", "town": "Lexington", "county": "Greene"},
    "12414": {"name": "Catskill", "town": "Catskill", "county": "Greene"},
    "12451": {"name": "Leeds", "town": "Catskill", "county": "Greene"},
    "12463": {"name": "Palenville", "town": "Catskill", "county": "Greene"},
    "12464": {"name": "Phoenicia", "town": "Shandaken", "county": "Ulster"},
    "12480": {"name": "Shandaken", "town": "Shandaken", "county": "Ulster"},
    "12457": {"name": "Mt Tremper", "town": "Shandaken", "county": "Ulster"},
}

# Greene County municipalities
GREENE_MUNICIPALITIES = [
    "Ashland",
    "Athens",
    "Cairo",
    "Catskill",
    "Coxsackie",
    "Durham",
    "Greenville",
    "Halcott",
    "Hunter",
    "Jewett",
    "Lexington",
    "New Baltimore",
    "Prattsville",
    "Windham",
]
