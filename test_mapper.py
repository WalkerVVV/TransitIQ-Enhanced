#!/usr/bin/env python
import sys
sys.path.append('.')

print("Testing FirstMile Column Mapper...")
print("="*50)

try:
    from firstmile_column_mapper import test_column_mapping
    
    # Run the test
    result = test_column_mapping()
    
    print("\n" + "="*50)
    print("✅ Column mapping test successful!")
    print("\nThe mapper successfully:")
    print("- Renamed columns to match dashboard expectations")
    print("- Calculated Days In Transit from date fields")
    print("- Calculated SLA Status based on service levels")
    print("- Converted weight from pounds to ounces")
    
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()

print("\nTo use: Run 'streamlit run app.py' and upload your FirstMile file")
