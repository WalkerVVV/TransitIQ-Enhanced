import streamlit as st
import pandas as pd
import traceback

st.set_page_config(page_title="File Upload Tester", layout="wide")

st.title("FirstMile File Column Inspector")

uploaded_file = st.file_uploader(
    "Upload your FirstMile file to see its columns",
    type=["csv", "xlsx"]
)

if uploaded_file:
    try:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, nrows=5)
        else:
            df = pd.read_excel(uploaded_file, nrows=5)
        
        st.success(f"File loaded successfully! Shape: {df.shape}")
        
        # Show columns
        st.subheader("File Columns:")
        for i, col in enumerate(df.columns):
            st.write(f"{i+1}. **{col}** (type: {df[col].dtype})")
        
        # Show sample data
        st.subheader("Sample Data:")
        st.dataframe(df)
        
        # Show what the dashboard expects
        st.subheader("Dashboard Expected Columns:")
        expected = [
            'Days In Transit',
            'Xparcel Type', 
            'SLA Status',
            'Customer Name',
            'Calculated Zone',
            'Destination State',
            'Destination ZIP',
            'Cost',
            'Weight',
            'Request Date',
            'Delivery Date',
            'Tracking Number',
            'Carrier'
        ]
        
        st.write("The dashboard expects these columns:")
        for col in expected:
            found = any(col.lower() in fc.lower() for fc in df.columns)
            if found:
                st.write(f"✅ {col}")
            else:
                st.write(f"❌ {col}")
                
        # Suggest mappings
        st.subheader("Suggested Column Mappings:")
        st.write("Based on your file, here are suggested mappings:")
        
        mappings = {}
        for dash_col in expected:
            for file_col in df.columns:
                # Smart matching logic
                if dash_col.lower() in file_col.lower():
                    mappings[file_col] = dash_col
                    st.write(f"'{file_col}' → '{dash_col}'")
                elif 'zone' in dash_col.lower() and 'zone' in file_col.lower():
                    mappings[file_col] = dash_col
                    st.write(f"'{file_col}' → '{dash_col}'")
                elif 'state' in dash_col.lower() and 'state' in file_col.lower():
                    mappings[file_col] = dash_col
                    st.write(f"'{file_col}' → '{dash_col}'")
                    
    except Exception as e:
        st.error(f"Error: {e}")
        st.code(traceback.format_exc())

st.info("Run this with: streamlit run test_file_upload.py")
