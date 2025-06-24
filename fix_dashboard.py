# fix_dashboard.py - Comprehensive fix for FirstMile data processing
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def enhanced_clean_and_rename_columns(df):
    """Enhanced column cleaning and mapping for FirstMile data"""
    
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # First, clean column names
    original_cols = df.columns.tolist()
    clean_cols = []
    for col in df.columns:
        cleaned = (
            str(col).replace('\xa0', ' ')  # Replace non-breaking space
                   .replace('\u200b', '')  # Remove zero-width space
                   .replace('\ufeff', '')  # Remove BOM
                   .strip()
        )
        clean_cols.append(cleaned)
    df.columns = clean_cols
    
    # Standardize column names (lowercase, replace spaces with underscores for mapping)
    df_lower = df.copy()
    df_lower.columns = df_lower.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Comprehensive column mapping for FirstMile data
    column_mapping = {
        # Weight columns (FirstMile might use various formats)
        'weight': 'Weight',
        'weight_oz': 'Weight',
        'weight_in_ounces': 'Weight',
        'weight_lbs': 'Weight',
        'package