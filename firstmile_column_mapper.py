# FirstMile Column Mapping Utility
# Maps various FirstMile export column names to dashboard expected names

FIRSTMILE_COLUMN_MAPPINGS = {
    # Days In Transit variations
    'days in transit': 'Days In Transit',
    'transit days': 'Days In Transit',
    'delivery days': 'Days In Transit',
    'actual transit days': 'Days In Transit',
    'transit time': 'Days In Transit',
    'days_in_transit': 'Days In Transit',
    'deliverydays': 'Days In Transit',
    
    # Service Type variations
    'xparcel type': 'Xparcel Type',
    'service type': 'Xparcel Type',
    'service level': 'Xparcel Type',
    'xparcel_type': 'Xparcel Type',
    'servicetype': 'Xparcel Type',
    'service': 'Xparcel Type',
    'method': 'Xparcel Type',
    'shipping method': 'Xparcel Type',
    
    # SLA Status variations
    'sla status': 'SLA Status',
    'delivery status': 'SLA Status',
    'on time status': 'SLA Status',
    'sla_status': 'SLA Status',
    'slastatus': 'SLA Status',
    'status': 'SLA Status',
    
    # Customer variations
    'customer name': 'Customer Name',
    'customer': 'Customer Name',
    'account name': 'Customer Name',
    'account': 'Customer Name',
    'customername': 'Customer Name',
    'customer_name': 'Customer Name',
    
    # Zone variations
    'calculated zone': 'Calculated Zone',
    'zone': 'Calculated Zone',
    'delivery zone': 'Calculated Zone',
    'shipping zone': 'Calculated Zone',
    'calculatedzone': 'Calculated Zone',
    'calculated_zone': 'Calculated Zone',
    
    # State variations
    'destination state': 'Destination State',
    'dest state': 'Destination State',
    'delivery state': 'Destination State',
    'state': 'Destination State',
    'destinationstate': 'Destination State',
    'destination_state': 'Destination State',
    'ship to state': 'Destination State',
    
    # ZIP variations
    'destination zip': 'Destination ZIP',
    'dest zip': 'Destination ZIP',
    'delivery zip': 'Destination ZIP',
    'zip': 'Destination ZIP',
    'postal code': 'Destination ZIP',
    'destinationzip': 'Destination ZIP',
    'destination_zip': 'Destination ZIP',
    'ship to zip': 'Destination ZIP',
    
    # Cost variations
    'cost': 'Cost',
    'shipping cost': 'Cost',
    'total cost': 'Cost',
    'charge': 'Cost',
    'shipping charge': 'Cost',
    'amount': 'Cost',
    'shippingcost': 'Cost',
    'shipping_cost': 'Cost',
    
    # Weight variations
    'weight': 'Weight',
    'package weight': 'Weight',
    'actual weight': 'Weight',
    'weight (oz)': 'Weight',
    'weight (lbs)': 'Weight',
    'packageweight': 'Weight',
    'package_weight': 'Weight',
    'weight_oz': 'Weight',
    
    # Date variations
    'request date': 'Request Date',
    'ship date': 'Request Date',
    'pickup date': 'Request Date',
    'manifest date': 'Request Date',
    'requestdate': 'Request Date',
    'request_date': 'Request Date',
    'date shipped': 'Request Date',
    
    'delivery date': 'Delivery Date',
    'delivered date': 'Delivery Date',
    'actual delivery date': 'Delivery Date',
    'deliverydate': 'Delivery Date',
    'delivery_date': 'Delivery Date',
    'date delivered': 'Delivery Date',
    
    # Tracking variations
    'tracking number': 'Tracking Number',
    'tracking': 'Tracking Number',
    'tracking #': 'Tracking Number',
    'trackingnumber': 'Tracking Number',
    'tracking_number': 'Tracking Number',
    'package id': 'Tracking Number',
    
    # Carrier variations
    'carrier': 'Carrier',
    'carrier name': 'Carrier',
    'shipping carrier': 'Carrier',
    'final carrier': 'Carrier',
    'delivery carrier': 'Carrier',
    'carriername': 'Carrier',
    'carrier_name': 'Carrier',
    
    # City variations
    'destination city': 'Destination City',
    'dest city': 'Destination City',
    'delivery city': 'Destination City',
    'city': 'Destination City',
    'destinationcity': 'Destination City',
    'destination_city': 'Destination City',
    'ship to city': 'Destination City',
}


def clean_and_rename_columns_enhanced(df):
    """Enhanced column cleaning that maps FirstMile columns to dashboard expectations"""
    import pandas as pd
    
    # First, clean invisible characters
    clean_cols = []
    for col in df.columns:
        cleaned = (
            str(col).replace('\xa0', ' ')  # Replace non-breaking space
                   .replace('\u200b', '')   # Remove zero-width space
                   .replace('\ufeff', '')   # Remove BOM
                   .strip()
        )
        clean_cols.append(cleaned)
    df.columns = clean_cols
    
    # Create mapping for this specific dataframe
    column_mapping = {}
    
    for col in df.columns:
        col_lower = col.lower().strip()
        
        # Check direct mapping
        if col_lower in FIRSTMILE_COLUMN_MAPPINGS:
            column_mapping[col] = FIRSTMILE_COLUMN_MAPPINGS[col_lower]
        else:
            # Try partial matching for flexibility
            for pattern, target in FIRSTMILE_COLUMN_MAPPINGS.items():
                if pattern in col_lower or col_lower in pattern:
                    column_mapping[col] = target
                    break
    
    # Apply the mapping
    if column_mapping:
        df = df.rename(columns=column_mapping)
        print(f"Mapped {len(column_mapping)} columns:")
        for old, new in column_mapping.items():
            print(f"  '{old}' → '{new}'")
    
    # Calculate missing fields if we have the data
    
    # Calculate Days In Transit if not present but we have dates
    if 'Days In Transit' not in df.columns:
        if 'Request Date' in df.columns and 'Delivery Date' in df.columns:
            try:
                df['Request Date'] = pd.to_datetime(df['Request Date'], errors='coerce')
                df['Delivery Date'] = pd.to_datetime(df['Delivery Date'], errors='coerce')
                df['Days In Transit'] = (df['Delivery Date'] - df['Request Date']).dt.days
                print("Calculated 'Days In Transit' from date fields")
            except:
                pass
    
    # Infer Xparcel Type from other fields if missing
    if 'Xparcel Type' not in df.columns:
        # Check for service-related columns
        for col in df.columns:
            if 'service' in col.lower() or 'method' in col.lower():
                # Try to standardize values
                df['Xparcel Type'] = df[col].fillna('Ground')
                # Map common values
                type_mapping = {
                    'ground': 'Ground',
                    'standard': 'Ground',
                    'economy': 'Ground',
                    'expedited': 'Expedited',
                    'express': 'Expedited',
                    '2day': 'Expedited',
                    'priority': 'Priority',
                    'next day': 'Priority',
                    'overnight': 'Priority'
                }
                df['Xparcel Type'] = df['Xparcel Type'].str.lower().map(
                    lambda x: next((v for k, v in type_mapping.items() if k in str(x).lower()), 'Ground')
                )
                print(f"Created 'Xparcel Type' from '{col}'")
                break
    
    # Calculate SLA Status if we have the data
    if 'SLA Status' not in df.columns and 'Days In Transit' in df.columns and 'Xparcel Type' in df.columns:
        def calculate_sla_status(row):
            try:
                days = row['Days In Transit']
                service = row['Xparcel Type']
                
                sla_days = {
                    'Priority': 3,
                    'Expedited': 5,
                    'Ground': 8
                }.get(service, 8)
                
                if pd.isna(days):
                    return 'Unknown'
                elif days <= sla_days:
                    return 'On-Time'
                else:
                    return 'SLA Miss'
            except:
                return 'Unknown'
        
        df['SLA Status'] = df.apply(calculate_sla_status, axis=1)
        print("Calculated 'SLA Status' from transit times")
    
    # Ensure numeric columns are numeric
    numeric_columns = ['Days In Transit', 'Cost', 'Weight', 'Calculated Zone']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convert Weight to ounces if it appears to be in pounds
    if 'Weight' in df.columns:
        if df['Weight'].max() < 50:  # Likely in pounds
            df['Weight'] = df['Weight'] * 16  # Convert to ounces
            print("Converted Weight from pounds to ounces")
    
    return df


# Test function
def test_column_mapping():
    """Test the column mapping with sample data"""
    import pandas as pd
    
    # Create test dataframe with typical FirstMile columns
    test_df = pd.DataFrame({
        'Tracking #': ['FM12345', 'FM67890'],
        'Service Level': ['Ground', 'Expedited'],
        'Ship Date': ['2024-01-01', '2024-01-02'],
        'Delivered Date': ['2024-01-05', '2024-01-04'],
        'Dest State': ['CA', 'TX'],
        'Dest ZIP': ['90210', '75001'],
        'Shipping Cost': [10.50, 15.75],
        'Package Weight': [1.5, 2.3],  # in pounds
        'Zone': ['4', '3']
    })
    
    print("Original columns:")
    print(test_df.columns.tolist())
    print("\nSample data:")
    print(test_df)
    
    # Apply mapping
    mapped_df = clean_and_rename_columns_enhanced(test_df.copy())
    
    print("\n\nMapped columns:")
    print(mapped_df.columns.tolist())
    print("\nTransformed data:")
    print(mapped_df)
    
    return mapped_df


if __name__ == "__main__":
    test_column_mapping()
