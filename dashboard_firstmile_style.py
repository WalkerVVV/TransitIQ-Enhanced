import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import io
import base64
import re
from datetime import datetime, timedelta
import numpy as np
import warnings
import json
import traceback
import sys

# Suppress the specific division warning
warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in scalar divide")

# FirstMile Brand Colors and Clean Modern CSS
st.markdown("""
<style>
    /* Import clean fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Remove default Streamlit padding */
    .main {
        padding: 0rem 1rem;
    }
    
    /* FirstMile Brand Colors */
    :root {
        --fm-green: #5CB85C;
        --fm-navy: #1E3A8A;
        --fm-light-gray: #F8F9FA;
        --fm-gray: #6C757D;
        --fm-dark: #212529;
    }
    
    /* Clean card design */
    .fm-card {
        background: white;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border: 1px solid rgba(0,0,0,0.06);
    }
    
    /* Section headers - clean and modern */
    .fm-section-header {
        background: white;
        padding: 16px 24px;
        border-radius: 8px;
        margin: 24px 0 16px 0;
        border-left: 4px solid var(--fm-green);
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    
    .fm-section-header h2 {
        color: var(--fm-navy);
        font-size: 2rem;  /* Increased from 1.5rem */
        font-weight: 700;
        margin: 0;
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid rgba(0,0,0,0.08);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        text-align: center;
    }
    
    [data-testid="metric-container"] > div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    [data-testid="metric-container"] label {
        color: var(--fm-gray);
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--fm-navy);
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Tables - clean and readable */
    .dataframe {
        font-size: 14px !important;
        border: none !important;
    }
    
    .dataframe thead tr th {
        background-color: var(--fm-light-gray) !important;
        color: var(--fm-navy) !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
        text-align: left !important;
        border-bottom: 2px solid var(--fm-green) !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #E5E7EB !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #F9FAFB !important;
    }
    
    .dataframe tbody tr td {
        padding: 12px 16px !important;
        color: var(--fm-dark) !important;
    }
    
    /* Buttons - FirstMile style */
    .stButton > button {
        background-color: var(--fm-green);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s;
        font-size: 14px;
    }
    
    .stButton > button:hover {
        background-color: #4CAF50;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Success/Info/Warning boxes */
    .stAlert {
        border-radius: 8px;
        border: none;
        padding: 16px;
    }
    
    div[data-baseweb="notification"] {
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--fm-light-gray);
        border-right: 1px solid rgba(0,0,0,0.08);
    }
    
    /* Headers and text - Bigger sizes */
    h1 {
        color: var(--fm-navy);
        font-weight: 700;
        font-size: 2.5rem !important;
    }
    
    h2 {
        color: var(--fm-navy);
        font-weight: 700;
        font-size: 2rem !important;
    }
    
    h3 {
        color: var(--fm-navy);
        font-weight: 600;
        font-size: 1.5rem !important;
    }
    
    /* Info boxes */
    .fm-info-box {
        background: #E7F3FF;
        border: 1px solid #3B82F6;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #1E3A8A;
    }
    
    /* Success boxes */
    .fm-success-box {
        background: #D4EDDA;
        border: 1px solid var(--fm-green);
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #155724;
    }
    
    /* Feature boxes */
    .fm-feature-box {
        background: var(--fm-light-gray);
        border: 1px solid var(--fm-green);
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
    
    .fm-feature-box h4 {
        color: var(--fm-navy);
        margin: 0 0 8px 0;
        font-size: 1.1rem;
    }
    
    /* Hide Streamlit branding but keep header for sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Keep header visible for sidebar toggle button */
    header[data-testid="stHeader"] {
        background-color: transparent;
        height: 3rem;
    }
    
    /* Plotly chart styling */
    .js-plotly-plot .plotly {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--fm-light-gray);
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background-color: var(--fm-navy);
    }
    
    .stDownloadButton > button:hover {
        background-color: #1a3270;
    }
    
    /* Column gaps */
    [data-testid="column"] {
        padding: 0 8px;
    }
    
    /* Make specific performance cells stand out */
    .performance-good {
        background-color: #D4EDDA !important;
        color: #155724 !important;
        font-weight: 600;
    }
    
    .performance-warning {
        background-color: #FFF3CD !important;
        color: #856404 !important;
        font-weight: 600;
    }
    
    .performance-bad {
        background-color: #F8D7DA !important;
        color: #721C24 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------
# Initialize Session State Early
# ----------------------
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

# ----------------------
# Sidebar with FirstMile styling
# ----------------------
with st.sidebar:
    # FirstMile Logo placeholder
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #5CB85C; margin: 0;">FirstMile</h2>
        <p style="color: #6C757D; margin: 5px 0; font-size: 14px;">Shipping Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    uploaded_file = st.file_uploader(
        "📁 Upload Tracking Report",
        type=["csv", "xlsx"],
        help="Upload your FirstMile export file (CSV or Excel format)"
    )
    
    st.divider()
    
    # Debug Mode Toggle
    st.session_state.debug_mode = st.checkbox(
        "🐛 Debug Mode", 
        value=st.session_state.debug_mode,
        help="Show detailed information about data processing"
    )
    
    # Data Generation Options
    st.markdown("### 🎲 Demo Options")
    
    demo_type = st.selectbox(
        "Demo Data Type",
        ["Complete Dataset", "Minimal Dataset", "No Dataset"],
        help="Generate demo data if no file is uploaded"
    )
    
    st.divider()
    
    # Toolkit Options with cleaner design
    st.markdown("### ⚙️ Analysis Tools")
    
    enable_national_select = st.checkbox("🚛 Carrier Optimization", value=True)
    enable_zone_toolkit = st.checkbox("🗺️ Zone Analysis", value=True)
    enable_xparcel_logic = st.checkbox("🎯 Smart Routing", value=True)
    enable_tet = st.checkbox("🚀 Express Lane", value=True)
    enable_cost_optimizer = st.checkbox("💰 Cost Analysis", value=True)
    enable_carrier_scoring = st.checkbox("📊 Performance Scoring", value=True)
    
    st.divider()
    
    # Show enabled features
    active_count = sum([enable_national_select, enable_zone_toolkit, enable_xparcel_logic, 
                       enable_tet, enable_cost_optimizer, enable_carrier_scoring])
    
    if active_count > 0:
        st.markdown(f"""
        <div class="fm-success-box" style="text-align: center;">
            <strong>{active_count} Tools Active</strong>
        </div>
        """, unsafe_allow_html=True)

# Copy all the helper functions from dashboard.py
def debug_log(message, level="INFO"):
    """Enhanced debug logging"""
    debug_enabled = False
    try:
        if 'debug_mode' in st.session_state:
            debug_enabled = st.session_state.debug_mode
    except:
        pass
    
    if debug_enabled:
        if level == "ERROR":
            st.error(f"🐛 DEBUG [{level}]: {message}")
        elif level == "WARNING":
            st.warning(f"🐛 DEBUG [{level}]: {message}")
        else:
            st.info(f"🐛 DEBUG [{level}]: {message}")

# Import enhanced column mapper
try:
    from firstmile_column_mapper import clean_and_rename_columns_enhanced
    use_enhanced_mapper = True
except ImportError:
    use_enhanced_mapper = False
    debug_log("Enhanced column mapper not available, using basic cleaning", "WARNING")

def clean_and_rename_columns(df):
    """Strip, normalize, and fix invisible chars with debug info"""
    if use_enhanced_mapper:
        try:
            debug_log(f"Using enhanced FirstMile column mapper on {len(df.columns)} columns")
            mapped_df = clean_and_rename_columns_enhanced(df)
            
            original_cols = set(df.columns)
            new_cols = set(mapped_df.columns)
            mapped_cols = new_cols - original_cols
            if mapped_cols:
                debug_log(f"Mapped columns: {list(mapped_cols)}")
            
            return mapped_df
        except Exception as e:
            debug_log(f"Error in enhanced mapping, falling back to basic: {e}", "ERROR")
    
    # Fallback to basic cleaning
    try:
        original_cols = df.columns.tolist()
        clean_cols = []
        for col in df.columns:
            cleaned = (
                str(col).replace('\xa0', ' ')
                       .replace('\u200b', '')
                       .replace('\ufeff', '')
                       .strip()
            )
            clean_cols.append(cleaned)
        df.columns = clean_cols
        
        debug_log(f"Basic cleaning: cleaned {len(original_cols)} columns")
        return df
    except Exception as e:
        debug_log(f"Error cleaning columns: {e}", "ERROR")
        return df

def safe_percentage(numerator, denominator, decimal_places=1):
    """Safely calculate percentage avoiding division by zero"""
    if denominator == 0 or pd.isna(denominator) or pd.isna(numerator):
        return 0.0
    try:
        result = 100 * numerator / denominator
        return round(result, decimal_places) if not pd.isna(result) else 0.0
    except:
        return 0.0

def safe_division(numerator, denominator, decimal_places=2):
    """Safely perform division avoiding division by zero"""
    if denominator == 0 or pd.isna(denominator) or pd.isna(numerator):
        return 0.0
    try:
        result = numerator / denominator
        return round(result, decimal_places) if not pd.isna(result) else 0.0
    except:
        return 0.0

def safe_aggregate_percentage(series, condition_value, decimal_places=1):
    """Safely calculate percentage for series aggregation"""
    if len(series) == 0:
        return 0.0
    try:
        valid_series = series.dropna()
        if len(valid_series) == 0:
            return 0.0
        matching_count = (valid_series == condition_value).sum()
        return safe_percentage(matching_count, len(valid_series), decimal_places)
    except:
        return 0.0

# Format dataframe with performance colors
def style_performance_dataframe(df, performance_column='On-Time %'):
    """Apply performance-based styling to dataframe"""
    def highlight_performance(val):
        try:
            # Remove % if present and convert to float
            if isinstance(val, str) and '%' in val:
                val = float(val.replace('%', ''))
            else:
                val = float(val)
            
            if val >= 95:
                return 'background-color: #D4EDDA; color: #155724; font-weight: 600;'
            elif val >= 90:
                return 'background-color: #FFF3CD; color: #856404; font-weight: 600;'
            else:
                return 'background-color: #F8D7DA; color: #721C24; font-weight: 600;'
        except:
            return ''
    
    # Apply styling only to performance columns
    if performance_column in df.columns:
        return df.style.applymap(highlight_performance, subset=[performance_column])
    return df

# Load all the other functions from dashboard_imports.py (avoids duplicate st.set_page_config)
try:
    # Import all analysis functions from our safe imports file
    from dashboard_imports import (
        analyze_comprehensive_performance_enhanced,
        analyze_tier_performance,
        analyze_service_mix,
        analyze_zone_distribution,
        analyze_zone_transit,
        analyze_exceptions,
        generate_exception_summary,
        analyze_regional_performance,
        analyze_day_of_week,
        analyze_weight_impact,
        analyze_carrier_performance,
        analyze_costs,
        generate_routing_recommendations,
        generate_demo_data,
        generate_empty_analysis_results,
        ensure_required_columns,
        analyze_carrier_options,
        calculate_zone_metrics,
        apply_xparcel_logic,
        NATIONAL_CARRIERS,
        SELECT_CARRIERS,
        ZONE_DEFINITIONS,
        XPARCEL_LOGIC
    )
    debug_log("Successfully imported all analysis functions", "INFO")
except ImportError as e:
    debug_log(f"Import error: {e}", "ERROR")
    # Define minimal versions if imports fail
    def generate_demo_data(demo_type):
        return None, {}
    
    def analyze_comprehensive_performance_enhanced(df):
        return generate_empty_analysis_results()
    
    def generate_empty_analysis_results():
        return {
            'tier_performance': pd.DataFrame(),
            'service_mix': pd.DataFrame(),
            'zone_distribution': pd.DataFrame(),
            'zone_transit': pd.DataFrame(),
            'exception_hotspots': pd.DataFrame(),
            'exception_summary': {},
            'regional_performance': pd.DataFrame(),
            'day_of_week': pd.DataFrame(),
            'weight_impact': pd.DataFrame(),
            'carrier_performance': pd.DataFrame(),
            'cost_analysis': {},
            'routing_optimization': {}
        }
    
    # Define minimal toolkit configurations if import fails
    NATIONAL_CARRIERS = {
        "UPS": {"zones": [1,2,3,4,5,6,7,8], "strength": "reliability", "avg_cost_multiplier": 1.2},
        "FedEx": {"zones": [1,2,3,4,5,6,7,8], "strength": "speed", "avg_cost_multiplier": 1.25},
        "USPS": {"zones": [1,2,3,4,5,6,7,8], "strength": "cost", "avg_cost_multiplier": 0.85}
    }
    
    SELECT_CARRIERS = {
        "OnTrac": {"zones": [1,2,3,4], "regions": ["CA", "NV", "AZ", "OR", "WA", "UT", "CO", "ID"], "strength": "regional speed"},
        "LaserShip": {"zones": [1,2,3,4], "regions": ["NY", "NJ", "PA", "MD", "VA", "DC", "DE", "CT", "MA", "RI"], "strength": "last-mile density"},
        "LSO": {"zones": [1,2,3,4,5], "regions": ["TX", "OK", "LA", "AR", "NM"], "strength": "Texas coverage"},
        "CDL": {"zones": [1,2,3], "regions": ["IL", "WI", "IN", "MI", "OH"], "strength": "midwest efficiency"}
    }
    
    ZONE_DEFINITIONS = {
        "1": {"miles": "0-50", "typical_transit": 1, "cost_index": 1.0},
        "2": {"miles": "51-150", "typical_transit": 2, "cost_index": 1.15},
        "3": {"miles": "151-300", "typical_transit": 2, "cost_index": 1.25},
        "4": {"miles": "301-600", "typical_transit": 3, "cost_index": 1.35},
        "5": {"miles": "601-1000", "typical_transit": 4, "cost_index": 1.5},
        "6": {"miles": "1001-1400", "typical_transit": 5, "cost_index": 1.65},
        "7": {"miles": "1401-1800", "typical_transit": 6, "cost_index": 1.8},
        "8": {"miles": "1801+", "typical_transit": 7, "cost_index": 2.0}
    }
    
    XPARCEL_LOGIC = {
        "Priority": {
            "sla_days": 3,
            "zone_limits": [1,2,3,4,5],
            "carrier_priority": ["FedEx", "UPS", "OnTrac", "LaserShip"],
            "cost_premium": 1.5,
            "features": ["Signature required", "Real-time tracking", "Money-back guarantee"]
        },
        "Expedited": {
            "sla_days": 5,
            "zone_limits": [1,2,3,4,5,6,7],
            "carrier_priority": ["UPS", "FedEx", "LSO", "CDL", "USPS"],
            "cost_premium": 1.2,
            "features": ["Standard tracking", "Residential delivery", "Insurance included"]
        },
        "Ground": {
            "sla_days": 8,
            "zone_limits": [1,2,3,4,5,6,7,8],
            "carrier_priority": ["USPS", "OnTrac", "LaserShip", "CDL", "LSO", "UPS"],
            "cost_premium": 1.0,
            "features": ["Economy service", "Basic tracking", "Best value"]
        }
    }