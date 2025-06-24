import pandas as pd
import sys

# Read the uploaded file
try:
    df = pd.read_excel("TransitIQ_Enhanced_Demo_Customer_20250620.xlsx")
    print("File loaded successfully!")
    print(f"\nShape: {df.shape}")
    print(f"\nColumns ({len(df.columns)}):")
    for col in df.columns:
        print(f"  - {col}")
    print(f"\nFirst few rows:")
    print(df.head())
except Exception as e:
    print(f"Error: {e}")
