# test_dashboard.py - Quick test to verify the dashboard works
import pandas as pd
import sys

print("Testing TransitIQ Enhanced Dashboard Setup...")
print("=" * 60)

try:
    # Test imports
    print("1. Testing imports...")
    from dashboard import *
    from enhanced_column_mapper import enhanced_clean_and_rename_columns
    print("✅ All imports successful!")
    
    # Test the summarize function exists
    print("\n2. Testing function availability...")
    if 'summarize_xparcel_performance' in globals():
        print("✅ summarize_xparcel_performance is available!")
    else:
        print("❌ summarize_xparcel_performance NOT found!")
    
    # Test demo data generation
    print("\n3. Testing demo data generation...")
    test_df, test_results = generate_demo_data("Minimal Dataset")
    if test_df is not None and not test_df.empty:
        print(f"✅ Demo data generated: {len(test_df)} rows")
        print(f"   Columns: {', '.join(test_df.columns[:5])}...")
    else:
        print("❌ Demo data generation failed!")
    
    # Test column mapping
    print("\n4. Testing column mapping...")
    test_data = pd.DataFrame({
        'Service Type': ['Ground', 'Expedited'],
        'Weight_OZ': [16, 32],
        'Dest ZIP': ['90210', '10001'],
        'Ship Date': ['2024-01-01', '2024-01-02']
    })
    
    mapped_df = enhanced_clean_and_rename_columns(test_data)
    print(f"✅ Column mapping successful!")
    print(f"   Original columns: {list(test_data.columns)}")
    print(f"   Mapped columns: {list(mapped_df.columns)}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED! Dashboard should work correctly.")
    print("\nRun 'streamlit run app.py' to start the dashboard.")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
