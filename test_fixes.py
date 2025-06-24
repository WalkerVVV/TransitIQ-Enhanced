import subprocess
import sys

print("Testing TransitIQ Dashboard fixes...")
print("-" * 50)

# Test 1: Check if the app runs without errors
print("Test 1: Running dashboard...")
try:
    # Run streamlit in a subprocess for 5 seconds to check for startup errors
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for a bit to see if there are immediate errors
    import time
    time.sleep(5)
    
    # Check if process is still running
    if process.poll() is None:
        print("✓ Dashboard started successfully")
        process.terminate()
    else:
        print("✗ Dashboard crashed on startup")
        stdout, stderr = process.communicate()
        print("Error:", stderr)
        
except Exception as e:
    print(f"✗ Failed to run dashboard: {e}")

print("\nTest 2: Checking for deprecation warnings...")

# Test 2: Check the imports for warnings
try:
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        exec(open('dashboard_imports.py').read())
        
        if len(w) == 0:
            print("✓ No deprecation warnings found")
        else:
            print(f"✗ Found {len(w)} warnings:")
            for warning in w:
                print(f"  - {warning.category.__name__}: {warning.message}")
                
except Exception as e:
    print(f"✗ Failed to test imports: {e}")

print("\nTest 3: Testing demo data generation...")
try:
    from dashboard_imports import generate_demo_data
    df, results = generate_demo_data("Complete Dataset")
    
    # Check on-time percentage
    exception_rate = results['exception_summary']['exception_rate']
    on_time_pct = 100 - exception_rate
    
    print(f"✓ Demo data generated: {len(df)} records")
    print(f"  - Exception rate: {exception_rate:.1f}%")
    print(f"  - On-time rate: {on_time_pct:.1f}%")
    
    if on_time_pct == 100.0:
        print("  ⚠ Warning: 100% on-time rate is unrealistic")
    elif 85 <= on_time_pct <= 98:
        print("  ✓ On-time rate looks realistic")
    else:
        print(f"  ⚠ On-time rate {on_time_pct:.1f}% seems unusual")
        
except Exception as e:
    print(f"✗ Failed to test demo data: {e}")

print("\nAll tests completed!")
