# dashboard_imports.py - Extract functions from dashboard.py without executing it
# This avoids the duplicate st.set_page_config() error

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

# Copy the essential constants and functions from dashboard.py

# Toolkit Configurations
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

def analyze_carrier_options(state, zone, service_type="Ground"):
    """Analyze best carrier options using National & Select toolkit"""
    carriers = []
    
    # Check national carriers
    for carrier, info in NATIONAL_CARRIERS.items():
        if int(zone) in info["zones"]:
            carriers.append({
                "carrier": carrier,
                "type": "National",
                "strength": info["strength"],
                "cost_index": info["avg_cost_multiplier"]
            })
    
    # Check select carriers
    for carrier, info in SELECT_CARRIERS.items():
        if state in info.get("regions", []) and int(zone) in info["zones"]:
            carriers.append({
                "carrier": carrier,
                "type": "Select",
                "strength": info["strength"],
                "cost_index": 0.9  # Select carriers typically 10% cheaper
            })
    
    # Sort by Xparcel logic priority
    if service_type in XPARCEL_LOGIC:
        priority_order = XPARCEL_LOGIC[service_type]["carrier_priority"]
        carriers.sort(key=lambda x: priority_order.index(x["carrier"]) if x["carrier"] in priority_order else 999)
    
    return carriers

def calculate_zone_metrics(df):
    """Enhanced zone analysis using Zone Toolkit"""
    if 'Calculated Zone' not in df.columns:
        return {}
    
    zone_metrics = {}
    for zone, info in ZONE_DEFINITIONS.items():
        zone_data = df[df['Calculated Zone'] == zone]
        if len(zone_data) > 0:
            zone_metrics[zone] = {
                "volume": len(zone_data),
                "avg_transit": zone_data['Days In Transit'].mean() if 'Days In Transit' in zone_data.columns else info["typical_transit"],
                "cost_index": info["cost_index"],
                "miles": info["miles"],
                "typical_transit": info["typical_transit"]
            }
    
    return zone_metrics

def apply_xparcel_logic(row):
    """Apply Xparcel routing logic - ONLY for demo data generation
    This should NOT override existing Xparcel Type values!"""
    
    # If Xparcel Type already exists and is not empty, DO NOT CHANGE IT
    if 'Xparcel Type' in row and pd.notna(row.get('Xparcel Type')) and row.get('Xparcel Type') != '':
        return row['Xparcel Type']
    
    # Only apply logic if there's no existing service type
    if pd.isna(row.get('Calculated Zone')):
        return "Ground"
    
    zone = int(row['Calculated Zone'])
    
    # Priority logic
    if zone <= 5 and row.get('Weight', 0) < 5:
        return "Priority"
    # Expedited logic
    elif zone <= 7 and row.get('Weight', 0) < 20:
        return "Expedited"
    # Ground logic
    else:
        return "Ground"

def generate_demo_data(data_type="Complete Dataset"):
    """Generate comprehensive demo data with all required fields"""
    if data_type == "No Dataset":
        return None, {}
    
    # Base parameters
    n_rows = 1000 if data_type == "Complete Dataset" else 100
    np.random.seed(42)  # For reproducibility
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, periods=n_rows)
    
    # State distribution for realistic data
    states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI',
              'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
    
    # Generate service types based on zone logic
    zones = np.random.choice(['1', '2', '3', '4', '5', '6', '7', '8'], 
                            n_rows, p=[0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05])
    weights = np.random.gamma(2, 2, n_rows)  # More realistic weight distribution
    
    # Generate demo raw data
    raw_df = pd.DataFrame({
        'Customer Name': 'Demo Customer',
        'Tracking Number': [f'FM{i:08d}' for i in range(n_rows)],
        'Request Date': dates,
        'Calculated Zone': zones,
        'Destination State': np.random.choice(states, n_rows),
        'Destination ZIP': [f'{np.random.randint(10000, 99999):05d}' for _ in range(n_rows)],
        'Destination City': np.random.choice(['Los Angeles', 'Houston', 'New York', 'Miami', 'Chicago', 
                                            'Philadelphia', 'Columbus', 'Atlanta', 'Charlotte', 'Detroit'], n_rows),
        'Weight': weights
    })
    
    # Apply Xparcel logic for service type ONLY if not already present
    if 'Xparcel Type' not in raw_df.columns or raw_df['Xparcel Type'].isna().all():
        raw_df['Xparcel Type'] = raw_df.apply(apply_xparcel_logic, axis=1)
    # Otherwise keep the existing Xparcel Type values
    
    # Calculate transit times based on service and zone
    def calc_transit(row):
        base_transit = ZONE_DEFINITIONS[row['Calculated Zone']]["typical_transit"]
        service_mult = {"Priority": 0.6, "Expedited": 0.8, "Ground": 1.0}[row['Xparcel Type']]
        variance = np.random.normal(0, 0.5)
        return max(1, int(base_transit * service_mult + variance))
    
    raw_df['Days In Transit'] = raw_df.apply(calc_transit, axis=1)
    raw_df['Delivery Date'] = raw_df['Request Date'] + pd.to_timedelta(raw_df['Days In Transit'], unit='D')
    
    # Add carrier information
    def assign_carrier(row):
        carriers = analyze_carrier_options(row['Destination State'], row['Calculated Zone'], row['Xparcel Type'])
        return carriers[0]['carrier'] if carriers else 'USPS'
    
    raw_df['Carrier'] = raw_df.apply(assign_carrier, axis=1)
    
    # Calculate costs
    def calc_cost(row):
        base_cost = 5 + (row['Weight'] * 0.5)
        zone_mult = ZONE_DEFINITIONS[row['Calculated Zone']]["cost_index"]
        service_mult = XPARCEL_LOGIC[row['Xparcel Type']]["cost_premium"]
        return round(base_cost * zone_mult * service_mult, 2)
    
    raw_df['Cost'] = raw_df.apply(calc_cost, axis=1)
    
    # Add SLA status with realistic performance
    # First, determine which shipments will miss SLA (about 8-10%)
    n_sla_misses = int(n_rows * 0.09)  # 9% SLA miss rate
    sla_miss_indices = np.random.choice(n_rows, n_sla_misses, replace=False)
    
    def get_sla_status(row):
        sla_days = XPARCEL_LOGIC[row['Xparcel Type']]["sla_days"]
        
        # Check if this row is designated as SLA miss
        if row.name in sla_miss_indices:
            return "SLA Miss"
        
        # Otherwise, determine if on-time or early
        if row['Days In Transit'] <= sla_days:
            return "On-Time" if row['Days In Transit'] >= sla_days - 1 else "Early"
        else:
            return "SLA Miss"
    
    raw_df['SLA Status'] = raw_df.apply(get_sla_status, axis=1)
    
    # Create comprehensive analysis results
    analysis_results = analyze_comprehensive_performance_enhanced(raw_df)
    
    return raw_df, analysis_results

def analyze_comprehensive_performance_enhanced(raw_df):
    """Enhanced performance analysis with guaranteed results for all 11 sections"""
    results = {}
    
    if raw_df is None or raw_df.empty:
        return generate_empty_analysis_results()
    
    try:
        df = raw_df.copy()
        
        # Ensure we have required columns
        ensure_required_columns(df)
        
        # 1. Performance by Xparcel Tier
        results['tier_performance'] = analyze_tier_performance(df)
        
        # 2. Service Mix
        results['service_mix'] = analyze_service_mix(df)
        
        # 3. Zone Distribution
        results['zone_distribution'] = analyze_zone_distribution(df)
        
        # 4. Transit Time by Zone
        results['zone_transit'] = analyze_zone_transit(df)
        
        # 5. Exception Analysis
        results['exception_hotspots'] = analyze_exceptions(df)
        results['exception_summary'] = generate_exception_summary(df)
        
        # 6. Regional Performance
        results['regional_performance'] = analyze_regional_performance(df)
        
        # 7. Day of Week Analysis
        results['day_of_week'] = analyze_day_of_week(df)
        
        # 8. Weight Impact Analysis
        results['weight_impact'] = analyze_weight_impact(df)
        
        # 9. Carrier Performance
        results['carrier_performance'] = analyze_carrier_performance(df)
        
        # 10. Cost Analysis
        results['cost_analysis'] = analyze_costs(df)
        
        # 11. Routing Optimization
        results['routing_optimization'] = generate_routing_recommendations(df)
        
    except Exception as e:
        return generate_empty_analysis_results()
    
    return results

def ensure_required_columns(df):
    """Ensure all required columns exist with reasonable defaults"""
    required_columns = {
        'Xparcel Type': 'Ground',
        'Days In Transit': 5,
        'Calculated Zone': '4',
        'Destination State': 'CA',
        'Destination ZIP': '90210',
        'Weight': 1.0,
        'Cost': 10.0,
        'SLA Status': 'On-Time',
        'Request Date': datetime.now(),
        'Delivery Date': datetime.now() + timedelta(days=5)
    }
    
    for col, default in required_columns.items():
        if col not in df.columns:
            df[col] = default

def generate_empty_analysis_results():
    """Generate empty but properly structured results for all sections"""
    return {
        'tier_performance': pd.DataFrame({
            'Xparcel Type': ['Ground', 'Expedited', 'Priority'],
            'Shipments': [0, 0, 0],
            'Avg Days': [0, 0, 0],
            'Median': [0, 0, 0],
            '95th Pctl': [0, 0, 0],
            'On-Time %': [0, 0, 0]
        }),
        'service_mix': pd.DataFrame({
            'Service': ['Ground', 'Expedited', 'Priority'],
            'Shipments': [0, 0, 0],
            'Percentage': [0, 0, 0]
        }),
        'zone_distribution': pd.DataFrame({
            'Zone': ['1', '2', '3', '4', '5', '6', '7', '8'],
            'Shipments': [0, 0, 0, 0, 0, 0, 0, 0],
            'Percentage': [0, 0, 0, 0, 0, 0, 0, 0]
        }),
        'zone_transit': pd.DataFrame({
            'Zone': ['1', '2', '3', '4', '5', '6', '7', '8'],
            'Avg Transit Days': [1, 2, 2, 3, 4, 5, 6, 7]
        }),
        'exception_hotspots': pd.DataFrame({
            'ZIP': ['No Data'],
            'SLA Misses': [0]
        }),
        'exception_summary': {
            'total_exceptions': 0,
            'exception_rate': 0,
            'avg_delay': 0
        },
        'regional_performance': pd.DataFrame({
            'State': ['No Data'],
            'Volume': [0],
            'Avg Transit': [0],
            'On-Time %': [0]
        }),
        'day_of_week': pd.DataFrame({
            'Day_of_Week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'Volume': [0, 0, 0, 0, 0, 0, 0],
            'Avg Transit': [0, 0, 0, 0, 0, 0, 0],
            'On-Time %': [0, 0, 0, 0, 0, 0, 0],
            'Volume %': [0, 0, 0, 0, 0, 0, 0]
        }),
        'weight_impact': pd.DataFrame({
            'Weight_Bucket': ['1-4 oz', '5-8 oz', '9-15 oz', '16-32 oz', '>32 oz'],
            'Volume': [0, 0, 0, 0, 0],
            'Avg Transit': [0, 0, 0, 0, 0],
            'On-Time %': [0, 0, 0, 0, 0]
        }),
        'carrier_performance': pd.DataFrame({
            'Carrier': ['No Data'],
            'Volume': [0],
            'On-Time %': [0],
            'Avg Cost': [0]
        }),
        'cost_analysis': {
            'avg_cost_by_service': {},
            'cost_per_zone': {},
            'potential_savings': 0
        },
        'routing_optimization': {
            'recommendations': [],
            'potential_improvement': 0
        }
    }

# Individual analysis functions
def analyze_tier_performance(df):
    """Analyze performance by Xparcel tier - FIXED to show only actual services"""
    try:
        if 'Xparcel Type' not in df.columns or 'Days In Transit' not in df.columns:
            return generate_empty_analysis_results()['tier_performance']
        
        # Only analyze service types that actually exist in the data
        actual_services = df['Xparcel Type'].dropna().unique()
        
        # Filter dataframe to only include rows with valid service types
        valid_df = df[df['Xparcel Type'].isin(actual_services)]
        
        tier_analysis = valid_df.groupby('Xparcel Type', observed=True).agg({
            'Days In Transit': ['count', 'mean', 'median', 
                               lambda x: np.percentile(x.dropna(), 95) if len(x.dropna()) > 0 else 0]
        }).round(2)
        
        # Add SLA performance
        if 'SLA Status' in valid_df.columns:
            sla_perf = valid_df.groupby('Xparcel Type', observed=True)['SLA Status'].apply(
                lambda x: safe_aggregate_percentage(x, 'On-Time')
            )
            tier_analysis = pd.concat([tier_analysis, sla_perf.to_frame('On-Time %')], axis=1)
        else:
            tier_analysis['On-Time %'] = 95.0  # Default
        
        tier_analysis.columns = ['Shipments', 'Avg Days', 'Median', '95th Pctl', 'On-Time %']
        result = tier_analysis.reset_index()
        
        # Sort by a consistent order
        service_order = ['Priority', 'Expedited', 'Ground']
        result['sort_order'] = result['Xparcel Type'].apply(
            lambda x: service_order.index(x) if x in service_order else 999
        )
        result = result.sort_values('sort_order').drop('sort_order', axis=1)
        
        return result
    
    except Exception as e:
        return generate_empty_analysis_results()['tier_performance']

def analyze_service_mix(df):
    """Analyze service mix distribution - FIXED to respect actual data"""
    try:
        if 'Xparcel Type' not in df.columns:
            return generate_empty_analysis_results()['service_mix']
        
        # Get the actual service types in the data
        service_mix = df['Xparcel Type'].value_counts()
        
        # Only include services that actually exist in the data
        # Do NOT artificially add Ground if it doesn't exist
        total = service_mix.sum()
        service_mix_pct = service_mix.apply(lambda x: safe_percentage(x, total))
        
        result_df = pd.DataFrame({
            'Service': service_mix.index,
            'Shipments': service_mix.values,
            'Percentage': service_mix_pct.values
        })
        
        # Sort by a consistent order if needed
        service_order = ['Priority', 'Expedited', 'Ground']
        result_df['sort_order'] = result_df['Service'].apply(
            lambda x: service_order.index(x) if x in service_order else 999
        )
        result_df = result_df.sort_values('sort_order').drop('sort_order', axis=1)
        
        return result_df
    
    except Exception as e:
        return generate_empty_analysis_results()['service_mix']

def analyze_zone_distribution(df):
    """Analyze zone distribution"""
    try:
        zone_col = None
        for col in df.columns:
            if 'zone' in col.lower():
                zone_col = col
                break
        
        if not zone_col:
            return generate_empty_analysis_results()['zone_distribution']
        
        zone_dist = df[zone_col].value_counts().sort_index()
        total = zone_dist.sum()
        zone_pct = zone_dist.apply(lambda x: safe_percentage(x, total))
        
        return pd.DataFrame({
            'Zone': zone_dist.index,
            'Shipments': zone_dist.values,
            'Percentage': zone_pct.values
        })
    
    except Exception as e:
        return generate_empty_analysis_results()['zone_distribution']

def analyze_zone_transit(df):
    """Analyze transit time by zone"""
    try:
        zone_col = None
        for col in df.columns:
            if 'zone' in col.lower():
                zone_col = col
                break
        
        if not zone_col or 'Days In Transit' not in df.columns:
            return generate_empty_analysis_results()['zone_transit']
        
        zone_transit = df.groupby(zone_col, observed=False)['Days In Transit'].mean().round(2)
        
        return pd.DataFrame({
            'Zone': zone_transit.index,
            'Avg Transit Days': zone_transit.values
        })
    
    except Exception as e:
        return generate_empty_analysis_results()['zone_transit']

def analyze_exceptions(df):
    """Analyze exception hotspots"""
    try:
        if 'SLA Status' not in df.columns:
            return generate_empty_analysis_results()['exception_hotspots']
        
        exceptions = df[df['SLA Status'] == 'SLA Miss']
        
        if len(exceptions) == 0:
            return pd.DataFrame({'ZIP': ['No Exceptions'], 'SLA Misses': [0]})
        
        zip_col = None
        for col in df.columns:
            if 'zip' in col.lower() or 'postal' in col.lower():
                zip_col = col
                break
        
        if not zip_col:
            return generate_empty_analysis_results()['exception_hotspots']
        
        problem_zips = exceptions[zip_col].value_counts().head(10)
        
        return pd.DataFrame({
            'ZIP': problem_zips.index,
            'SLA Misses': problem_zips.values
        })
    
    except Exception as e:
        return generate_empty_analysis_results()['exception_hotspots']

def generate_exception_summary(df):
    """Generate exception summary statistics"""
    try:
        if 'SLA Status' not in df.columns:
            return generate_empty_analysis_results()['exception_summary']
        
        total_shipments = len(df)
        exceptions = df[df['SLA Status'] == 'SLA Miss']
        total_exceptions = len(exceptions)
        exception_rate = safe_percentage(total_exceptions, total_shipments)
        
        avg_delay = 0
        if 'Days In Transit' in exceptions.columns and 'Xparcel Type' in exceptions.columns:
            delays = []
            for _, row in exceptions.iterrows():
                sla = XPARCEL_LOGIC.get(row['Xparcel Type'], {}).get('sla_days', 8)
                delay = row['Days In Transit'] - sla
                if delay > 0:
                    delays.append(delay)
            avg_delay = np.mean(delays) if delays else 0
        
        return {
            'total_exceptions': total_exceptions,
            'exception_rate': exception_rate,
            'avg_delay': round(avg_delay, 1)
        }
    
    except Exception as e:
        return generate_empty_analysis_results()['exception_summary']

def analyze_regional_performance(df):
    """Analyze performance by region/state"""
    try:
        state_col = None
        for col in df.columns:
            if 'state' in col.lower():
                state_col = col
                break
        
        if not state_col:
            return generate_empty_analysis_results()['regional_performance']
        
        if 'Days In Transit' in df.columns:
            regional = df.groupby(state_col, observed=False).agg({
                'Days In Transit': ['count', 'mean']
            })
            regional.columns = ['Volume', 'Avg Transit']
            
            if 'SLA Status' in df.columns:
                sla_perf = df.groupby(state_col, observed=False)['SLA Status'].apply(
                    lambda x: safe_aggregate_percentage(x, 'On-Time')
                )
                regional['On-Time %'] = sla_perf
            else:
                regional['On-Time %'] = 95.0
            
            return regional.reset_index().rename(columns={state_col: 'State'}).head(10)
        else:
            return generate_empty_analysis_results()['regional_performance']
    
    except Exception as e:
        return generate_empty_analysis_results()['regional_performance']

def analyze_day_of_week(df):
    """Analyze performance by day of week"""
    try:
        date_col = None
        for col in df.columns:
            if 'date' in col.lower() and 'request' in col.lower():
                date_col = col
                break
        
        if not date_col:
            return generate_empty_analysis_results()['day_of_week']
        
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['Day_of_Week'] = df[date_col].dt.day_name()
        
        if 'Days In Transit' in df.columns:
            dow_analysis = df.groupby('Day_of_Week', observed=False).agg({
                'Days In Transit': ['count', 'mean']
            })
            dow_analysis.columns = ['Volume', 'Avg Transit']
            
            if 'SLA Status' in df.columns:
                sla_perf = df.groupby('Day_of_Week', observed=False)['SLA Status'].apply(
                    lambda x: safe_aggregate_percentage(x, 'On-Time')
                )
                dow_analysis['On-Time %'] = sla_perf
            else:
                dow_analysis['On-Time %'] = 95.0
            
            total_volume = dow_analysis['Volume'].sum()
            dow_analysis['Volume %'] = dow_analysis['Volume'].apply(
                lambda x: safe_percentage(x, total_volume)
            )
            
            # Ensure proper day ordering
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_analysis = dow_analysis.reindex(day_order, fill_value=0)
            
            return dow_analysis.reset_index()
        else:
            return generate_empty_analysis_results()['day_of_week']
    
    except Exception as e:
        return generate_empty_analysis_results()['day_of_week']

def analyze_weight_impact(df):
    """Analyze performance by weight category"""
    try:
        weight_col = None
        for col in df.columns:
            if 'weight' in col.lower():
                weight_col = col
                break
        
        if not weight_col:
            return generate_empty_analysis_results()['weight_impact']
        
        df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')
        
        # Create weight buckets
        df['Weight_Bucket'] = pd.cut(
            df[weight_col], 
            bins=[0, 0.25, 0.5, 1, 2, float('inf')], 
            labels=['1-4 oz', '5-8 oz', '9-15 oz', '16-32 oz', '>32 oz']
        )
        
        if 'Days In Transit' in df.columns:
            weight_analysis = df.groupby('Weight_Bucket', observed=False).agg({
                'Days In Transit': ['count', 'mean']
            })
            weight_analysis.columns = ['Volume', 'Avg Transit']
            
            if 'SLA Status' in df.columns:
                sla_perf = df.groupby('Weight_Bucket', observed=False)['SLA Status'].apply(
                    lambda x: safe_aggregate_percentage(x, 'On-Time')
                )
                weight_analysis['On-Time %'] = sla_perf
            else:
                weight_analysis['On-Time %'] = 95.0
            
            return weight_analysis.reset_index()
        else:
            return generate_empty_analysis_results()['weight_impact']
    
    except Exception as e:
        return generate_empty_analysis_results()['weight_impact']

def analyze_carrier_performance(df):
    """Analyze performance by carrier using toolkit data"""
    try:
        if 'Carrier' not in df.columns:
            # If no carrier data, create sample
            return pd.DataFrame({
                'Carrier': list(NATIONAL_CARRIERS.keys()) + ['OnTrac', 'LaserShip'],
                'Volume': [100, 80, 120, 60, 40],
                'On-Time %': [96.5, 97.2, 94.8, 98.1, 97.5],
                'Avg Cost': [12.50, 13.25, 9.75, 8.90, 9.10]
            })
        
        carrier_perf = df.groupby('Carrier', observed=False).agg({
            'Days In Transit': 'count',
            'Cost': 'mean'
        })
        carrier_perf.columns = ['Volume', 'Avg Cost']
        
        if 'SLA Status' in df.columns:
            sla_perf = df.groupby('Carrier', observed=False)['SLA Status'].apply(
                lambda x: safe_aggregate_percentage(x, 'On-Time')
            )
            carrier_perf['On-Time %'] = sla_perf
        else:
            carrier_perf['On-Time %'] = 95.0
        
        return carrier_perf.reset_index()
    
    except Exception as e:
        return pd.DataFrame({
            'Carrier': ['No Data'],
            'Volume': [0],
            'On-Time %': [0],
            'Avg Cost': [0]
        })

def analyze_costs(df):
    """Analyze shipping costs using cost optimization toolkit"""
    try:
        cost_analysis = {}
        
        if 'Cost' in df.columns and 'Xparcel Type' in df.columns:
            cost_by_service = df.groupby('Xparcel Type', observed=False)['Cost'].mean().to_dict()
            cost_analysis['avg_cost_by_service'] = cost_by_service
        else:
            cost_analysis['avg_cost_by_service'] = {
                'Ground': 8.50,
                'Expedited': 12.75,
                'Priority': 18.25
            }
        
        if 'Cost' in df.columns and 'Calculated Zone' in df.columns:
            cost_by_zone = df.groupby('Calculated Zone', observed=False)['Cost'].mean().to_dict()
            cost_analysis['cost_per_zone'] = cost_by_zone
        else:
            cost_analysis['cost_per_zone'] = {
                str(i): 5 + (i * 2) for i in range(1, 9)
            }
        
        # Calculate potential savings
        if 'Cost' in df.columns:
            current_total = df['Cost'].sum()
            optimized_total = current_total * 0.85  # 15% savings potential
            cost_analysis['potential_savings'] = round(current_total - optimized_total, 2)
        else:
            cost_analysis['potential_savings'] = 1250.00
        
        return cost_analysis
    
    except Exception as e:
        return generate_empty_analysis_results()['cost_analysis']

def generate_routing_recommendations(df):
    """Generate routing optimization recommendations"""
    try:
        recommendations = []
        
        # Analyze current routing efficiency
        if 'Calculated Zone' in df.columns and 'Xparcel Type' in df.columns:
            # Check for over-servicing
            overservice = df[
                (df['Calculated Zone'].isin(['1', '2', '3'])) & 
                (df['Xparcel Type'].isin(['Expedited', 'Priority']))
            ]
            if len(overservice) > 0:
                pct = safe_percentage(len(overservice), len(df))
                recommendations.append({
                    'issue': 'Over-servicing detected',
                    'impact': f'{pct:.1f}% of short-zone shipments using premium service',
                    'recommendation': 'Downgrade zones 1-3 to Ground service where SLA permits',
                    'savings': f'${len(overservice) * 3.50:.2f}'
                })
        
        # Check for carrier optimization opportunities
        if 'Destination State' in df.columns:
            for state in ['CA', 'TX', 'NY', 'FL']:
                state_shipments = df[df['Destination State'] == state]
                if len(state_shipments) > 50:
                    recommendations.append({
                        'issue': f'High volume to {state}',
                        'impact': f'{len(state_shipments)} shipments',
                        'recommendation': f'Consider regional carrier for {state} deliveries',
                        'savings': f'${len(state_shipments) * 1.25:.2f}'
                    })
        
        # Friday cutoff recommendation
        if 'Request Date' in df.columns:
            df['Request Date'] = pd.to_datetime(df['Request Date'], errors='coerce')
            friday_shipments = df[df['Request Date'].dt.dayofweek == 4]
            if len(friday_shipments) > len(df) * 0.15:
                recommendations.append({
                    'issue': 'High Friday volume',
                    'impact': f'{len(friday_shipments)} Friday shipments',
                    'recommendation': 'Implement 2 PM Friday cutoff with auto-upgrade for zones 7-8',
                    'savings': 'Reduced SLA misses'
                })
        
        if not recommendations:
            recommendations.append({
                'issue': 'No major issues detected',
                'impact': 'System operating efficiently',
                'recommendation': 'Continue monitoring for optimization opportunities',
                'savings': 'N/A'
            })
        
        # Calculate total potential improvement
        total_savings = sum([
            float(r['savings'].replace('$', '').replace(',', '')) 
            for r in recommendations 
            if r['savings'] != 'N/A' and '$' in r['savings']
        ])
        
        return {
            'recommendations': recommendations,
            'potential_improvement': total_savings
        }
    
    except Exception as e:
        return generate_empty_analysis_results()['routing_optimization']
