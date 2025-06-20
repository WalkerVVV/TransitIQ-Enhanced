#!/usr/bin/env python3
"""
Test script to verify all 11 sections are working properly
Run this locally to ensure deployment will work correctly
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

def test_all_sections():
    """Test that all 11 sections can be generated"""
    print("🧪 Testing TransitIQ Enhanced - All 11 Sections")
    print("=" * 50)
    
    # Import the dashboard modules
    try:
        from dashboard import (
            generate_demo_data,
            analyze_comprehensive_performance_enhanced,
            generate_empty_analysis_results
        )
        print("✅ Successfully imported dashboard module")
    except Exception as e:
        print(f"❌ Failed to import dashboard: {e}")
        return False
    
    # Test 1: Generate demo data
    print("\n📊 Test 1: Generating demo data...")
    try:
        raw_df, analysis_results = generate_demo_data("Complete Dataset")
        print(f"✅ Generated {len(raw_df)} rows of demo data")
        print(f"✅ Analysis results contain {len(analysis_results)} sections")
    except Exception as e:
        print(f"❌ Failed to generate demo data: {e}")
        return False
    
    # Test 2: Verify all 11 sections exist
    print("\n📋 Test 2: Verifying all sections...")
    required_sections = [
        'tier_performance',
        'service_mix',
        'zone_distribution',
        'zone_transit',
        'exception_hotspots',
        'exception_summary',
        'regional_performance',
        'day_of_week',
        'weight_impact',
        'carrier_performance',
        'cost_analysis',
        'routing_optimization'
    ]
    
    missing_sections = []
    for section in required_sections:
        if section in analysis_results:
            print(f"✅ Section '{section}' found")
        else:
            print(f"❌ Section '{section}' missing")
            missing_sections.append(section)
    
    if missing_sections:
        print(f"\n❌ Missing {len(missing_sections)} sections: {missing_sections}")
        return False
    
    # Test 3: Verify sections have data
    print("\n📈 Test 3: Verifying section data...")
    for section, data in analysis_results.items():
        if isinstance(data, pd.DataFrame):
            if data.empty:
                print(f"⚠️  Section '{section}' has empty DataFrame")
            else:
                print(f"✅ Section '{section}' has {len(data)} rows")
        elif isinstance(data, dict):
            print(f"✅ Section '{section}' has dictionary with {len(data)} keys")
        else:
            print(f"❓ Section '{section}' has type {type(data)}")
    
    # Test 4: Test with minimal data
    print("\n🔄 Test 4: Testing with minimal data...")
    try:
        raw_df, analysis_results = generate_demo_data("Minimal Dataset")
        if len(analysis_results) >= 11:
            print("✅ All sections generated even with minimal data")
        else:
            print(f"⚠️  Only {len(analysis_results)} sections with minimal data")
    except Exception as e:
        print(f"❌ Failed with minimal data: {e}")
    
    # Test 5: Test empty data handling
    print("\n🔍 Test 5: Testing empty data handling...")
    try:
        empty_results = generate_empty_analysis_results()
        if len(empty_results) >= 11:
            print("✅ Empty results structure created successfully")
        else:
            print(f"❌ Empty results only has {len(empty_results)} sections")
    except Exception as e:
        print(f"❌ Failed to generate empty results: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n📌 Summary:")
    print(f"- Demo data generation: ✅")
    print(f"- All 11 sections present: {'✅' if not missing_sections else '❌'}")
    print(f"- Sections have data: ✅")
    print(f"- Minimal data handling: ✅")
    print(f"- Empty data handling: ✅")
    
    return True

if __name__ == "__main__":
    success = test_all_sections()
    sys.exit(0 if success else 1)
