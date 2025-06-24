# firstmile_column_mapper.py
# Enhanced column mapping for FirstMile tracking reports
# Handles special characters, encoding issues, and FirstMile-specific column names

def clean_and_rename_columns_enhanced(df):
    """
    Enhanced column cleaning and mapping for FirstMile files
    Handles invisible characters, special encodings, and FirstMile-specific formats
    """
    # First, clean all column names
    clean_cols = []
    for col in df.columns:
        # Remove all types of whitespace and invisible characters
        cleaned = (
            str(col)
            .replace('\xa0', ' ')      # Non-breaking space
            .replace('\u200b', '')     # Zero-width space
            .replace('\u200c', '')     # Zero-width non-joiner
            .replace('\u200d', '')     # Zero-width joiner
            .replace('\ufeff', '')     # BOM
            .replace('\u202f', ' ')    # Narrow no-break space
            .replace('\u00a0', ' ')    # Another non-breaking space
            .strip()                   # Remove leading/trailing spaces
        )
        clean_cols.append(cleaned)
    
    df.columns = clean_cols
    
    # FirstMile specific column mappings
    column_mappings = {
        # Request Date variations
        'Request\xa0Date': 'Request Date',
        'Request Date': 'Request Date',
        'Requested Date': 'Request Date',
        'Date Requested': 'Request Date',
        'Ship Date': 'Request Date',
        'Shipment Date': 'Request Date',
        
        # Delivery Date variations
        'Delivery\xa0Date': 'Delivery Date',
        'Delivery Date': 'Delivery Date',
        'Delivered Date': 'Delivery Date',
        'Date Delivered': 'Delivery Date',
        'Actual Delivery': 'Delivery Date',
        'Actual Delivery Date': 'Delivery Date',
        
        # Days In Transit variations
        'Days\xa0In\xa0Transit': 'Days In Transit',
        'Days In Transit': 'Days In Transit',
        'Transit Days': 'Days In Transit',
        'Days in Transit': 'Days In Transit',
        'Transit Time': 'Days In Transit',
        'Delivery Days': 'Days In Transit',
        
        # Zone variations
        'Calculated\xa0Zone': 'Calculated Zone',
        'Calculated Zone': 'Calculated Zone',
        'Zone': 'Calculated Zone',
        'Shipping Zone': 'Calculated Zone',
        'Delivery Zone': 'Calculated Zone',
        
        # Xparcel Type variations
        'Xparcel\xa0Type': 'Xparcel Type',
        'Xparcel Type': 'Xparcel Type',
        'Service Type': 'Xparcel Type',
        'Service Level': 'Xparcel Type',
        'Shipping Service': 'Xparcel Type',
        'Delivery Service': 'Xparcel Type',
        
        # SLA Status variations
        'SLA\xa0Status': 'SLA Status',
        'SLA Status': 'SLA Status',
        'Delivery Status': 'SLA Status',
        'Performance Status': 'SLA Status',
        'On Time Status': 'SLA Status',
        
        # Weight variations
        'Weight': 'Weight',
        'Package Weight': 'Weight',
        'Shipment Weight': 'Weight',
        'Weight (oz)': 'Weight',
        'Weight (lbs)': 'Weight',
        
        # Cost variations
        'Cost': 'Cost',
        'Shipping Cost': 'Cost',
        'Total Cost': 'Cost',
        'Shipment Cost': 'Cost',
        'Price': 'Cost',
        
        # State variations
        'Destination\xa0State': 'Destination State',
        'Destination State': 'Destination State',
        'Delivery State': 'Destination State',
        'Ship To State': 'Destination State',
        'State': 'Destination State',
        
        # ZIP variations
        'Destination\xa0ZIP': 'Destination ZIP',
        'Destination ZIP': 'Destination ZIP',
        'Delivery ZIP': 'Destination ZIP',
        'Ship To ZIP': 'Destination ZIP',
        'ZIP Code': 'Destination ZIP',
        'Postal Code': 'Destination ZIP',
        
        # Customer variations
        'Customer\xa0Name': 'Customer Name',
        'Customer Name': 'Customer Name',
        'Client Name': 'Customer Name',
        'Account Name': 'Customer Name',
        'Company Name': 'Customer Name',
        
        # Tracking Number variations
        'Tracking\xa0Number': 'Tracking Number',
        'Tracking Number': 'Tracking Number',
        'Tracking #': 'Tracking Number',
        'Tracking ID': 'Tracking Number',
        'Package ID': 'Tracking Number',
        
        # Carrier variations
        'Carrier': 'Carrier',
        'Shipping Carrier': 'Carrier',
        'Delivery Carrier': 'Carrier',
        'Service Provider': 'Carrier',
        
        # City variations
        'Destination\xa0City': 'Destination City',
        'Destination City': 'Destination City',
        'Delivery City': 'Destination City',
        'Ship To City': 'Destination City',
        'City': 'Destination City'
    }
    
    # Apply the mappings
    new_columns = []
    for col in df.columns:
        if col in column_mappings:
            new_columns.append(column_mappings[col])
        else:
            new_columns.append(col)
    
    df.columns = new_columns
    
    # Remove any completely empty columns
    df = df.dropna(axis=1, how='all')
    
    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    return df
