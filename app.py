# FirstMile TransitIQ Dashboard - Clean Modern Design
# No matplotlib required - uses solid colors matching FirstMile brand

import streamlit as st

# Must be the FIRST Streamlit command
st.set_page_config(
    page_title="FirstMile TransitIQ | Shipping Analytics", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/WalkerVVV/TransitIQ-Enhanced',
        'Report a bug': "https://github.com/WalkerVVV/TransitIQ-Enhanced/issues",
        'About': "FirstMile TransitIQ - Professional Shipping Analytics"
    }
)

# Now we can safely import and execute
exec(open('dashboard_main.py', encoding='utf-8').read())
