# enhanced_column_mapper.py - Better FirstMile column mapping
import pandas as pd
import re

def enhanced_clean_and_rename_columns(df):
    """Enhanced column cleaning and mapping specifically for FirstMile data"""
    
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # First, clean column names of special characters
    original_cols = df.columns.tolist()
    clean_cols = []
    for col in df.columns:
        cleaned = (
            str(col).replace('\xa0', ' ')  # Replace non-breaking space
                   .replace('\u200b', '')  # Remove zero-width space
                   .replace('\ufeff', '')  # Remove BOM
                   .replace('\t', ' ')     # Replace tabs with spaces
                   .strip()
        )
        # Remove multiple spaces
        cleaned = ' '.join(cleaned.split())
        clean_cols.append(cleaned)
    
    df.columns = clean_cols
    
    # Create lowercase version for mapping
    df_lower = df.copy()
    df_lower.columns = df_lower.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Comprehensive column mapping for FirstMile data
    column_mapping = {
        # Service Type columns
        'service': 'Xparcel Type',
        'service_type': 'Xparcel Type',
        'xparcel_type': 'Xparcel Type',
        'service_level': 'Xparcel Type',
        'shipment_service': 'Xparcel Type',
        'carrier_service': 'Xparcel Type',
        'shipping_service': 'Xparcel Type',
        
        # Weight columns (FirstMile might use various formats)
        'weight': 'Weight',
        'weight_oz': 'Weight',
        'weight_in_ounces': 'Weight',
        'weight_lbs': 'Weight',
        'package_weight': 'Weight',
        'shipment_weight': 'Weight',
        'actual_weight': 'Weight',
        
        # ZIP columns
        'dest_zip': 'Destination ZIP',
        'destination_zip': 'Destination ZIP',
        'to_zip': 'Destination ZIP',
        'ship_to_zip': 'Destination ZIP',
        'recipient_zip': 'Destination ZIP',
        'consignee_zip': 'Destination ZIP',
        'delivery_zip': 'Destination ZIP',
        
        # State columns
        'dest_state': 'Destination State',
        'destination_state': 'Destination State',
        'to_state': 'Destination State',
        'ship_to_state': 'Destination State',
        'recipient_state': 'Destination State',
        'consignee_state': 'Destination State',
        
        # City columns
        'dest_city': 'Destination City',
        'destination_city': 'Destination City',
        'to_city': 'Destination City',
        'ship_to_city': 'Destination City',
        'recipient_city': 'Destination City',
        
        # Zone columns
        'zone': 'Calculated Zone',
        'shipping_zone': 'Calculated Zone',
        'delivery_zone': 'Calculated Zone',
        'calculated_zone': 'Calculated Zone',
        
        # Transit time columns
        'transit_days': 'Days In Transit',
        'days_in_transit': 'Days In Transit',
        'delivery_days': 'Days In Transit',
        'actual_transit_days': 'Days In Transit',
        'business_days': 'Days In Transit',
        
        # Cost columns
        'cost': 'Cost',
        'shipping_cost': 'Cost',
        'total_cost': 'Cost',
        'price': 'Cost',
        'charge': 'Cost',
        'rate': 'Cost',
        'amount': 'Cost',
        
        # Date columns
        'ship_date': 'Request Date',
        'shipped_date': 'Request Date',
        'date_shipped': 'Request Date',
        'pickup_date': 'Request Date',
        'manifest_date': 'Request Date',
        'request_date': 'Request Date',
        
        'delivery_date': 'Delivery Date',
        'delivered_date': 'Delivery Date',
        'actual_delivery_date': 'Delivery Date',
        
        # Status columns
        'status': 'SLA Status',
        'delivery_status': 'SLA Status',
        'sla_status': 'SLA Status',
        'performance': 'SLA Status',
        
        # Customer columns
        'customer': 'Customer Name',
        'customer_name': 'Customer Name',
        'client': 'Customer Name',
        'client_name': 'Customer Name',
        'account': 'Customer Name',
        'account_name': 'Customer Name',
        
        # Tracking columns
        'tracking': 'Tracking Number',
        'tracking_number': 'Tracking Number',
        'tracking_id': 'Tracking Number',
        'package_id': 'Tracking Number',
        'barcode': 'Tracking Number',
        
        # Carrier columns
        'carrier': 'Carrier',
        'carrier_name': 'Carrier',
        'delivery_carrier': 'Carrier',
        'final_mile_carrier': 'Carrier'
    }
    
    # Apply the mapping to lowercase columns
    for old_col, new_col in column_mapping.items():
        # Check if the old column exists in lowercase version
        matching_cols = [col for col in df_lower.columns if old_col in col or col in old_col]
        if matching_cols and new_col not in df.columns:
            # Find the original column name (with proper case)
            idx = df_lower.columns.tolist().index(matching_cols[0])
            original_col = df.columns[idx]
            df.rename(columns={original_col: new_col}, inplace=True)
    
    # Convert weight to pounds if in ounces
    if 'Weight' in df.columns:
        # Check if weight seems to be in ounces (values > 16 likely)
        avg_weight = df['Weight'].mean()
        if pd.notna(avg_weight) and avg_weight > 16:
            df['Weight'] = df['Weight'] / 16
    
    # Ensure ZIP codes are properly formatted
    if 'Destination ZIP' in df.columns:
        df['Destination ZIP'] = df['Destination ZIP'].astype(str).str.strip()
        # Handle 5-digit and 9-digit ZIPs
        df['Destination ZIP'] = df['Destination ZIP'].apply(
            lambda x: x[:5] if len(x) >= 5 else x.zfill(5)
        )
    
    # Calculate Days in Transit if not present
    if 'Days In Transit' not in df.columns:
        if 'Request Date' in df.columns and 'Delivery Date' in df.columns:
            try:
                df['Request Date'] = pd.to_datetime(df['Request Date'], errors='coerce')
                df['Delivery Date'] = pd.to_datetime(df['Delivery Date'], errors='coerce')
                df['Days In Transit'] = (df['Delivery Date'] - df['Request Date']).dt.days
            except:
                pass
    
    # Add SLA Status if not present
    if 'SLA Status' not in df.columns and 'Days In Transit' in df.columns and 'Xparcel Type' in df.columns:
        def calculate_sla_status(row):
            if pd.isna(row['Days In Transit']) or pd.isna(row['Xparcel Type']):
                return 'Unknown'
            
            sla_days = {
                'Priority': 3,
                'Expedited': 5,
                'Ground': 8
            }
            
            service_type = str(row['Xparcel Type'])
            for service, sla in sla_days.items():
                if service.lower() in service_type.lower():
                    if row['Days In Transit'] <= sla:
                        return 'On-Time'
                    else:
                        return 'SLA Miss'
            
            return 'On-Time'  # Default
        
        df['SLA Status'] = df.apply(calculate_sla_status, axis=1)
    
    # Add any missing expected columns with reasonable defaults
    expected_columns = {
        'Weight': 1.0,
        'Destination ZIP': '00000',
        'Destination State': 'Unknown',
        'Destination City': 'Unknown',
        'Cost': 0.0,
        'Xparcel Type': 'Ground',
        'Days In Transit': 5,
        'Calculated Zone': '4',
        'SLA Status': 'On-Time',
        'Customer Name': 'Unknown Customer',
        'Tracking Number': 'N/A',
        'Carrier': 'Unknown',
        'Request Date': pd.Timestamp.now(),
        'Delivery Date': pd.Timestamp.now() + pd.Timedelta(days=5)
    }
    
    for col, default in expected_columns.items():
        if col not in df.columns:
            df[col] = default
    
    return df

# Add this function to dashboard.py to replace the existing clean_and_rename_columns
if __name__ == "__main__":
    print("Enhanced column mapper created successfully!")
    print("\nTo use this in your dashboard, replace the clean_and_rename_columns function in dashboard.py with:")
    print("from enhanced_column_mapper import enhanced_clean_and_rename_columns as clean_and_rename_columns")
