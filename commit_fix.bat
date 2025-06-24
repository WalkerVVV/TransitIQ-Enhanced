@echo off
echo Committing FirstMile Column Mapping Fix...

git add dashboard.py
git add dashboard_main.py  
git add firstmile_column_mapper.py
git add test_file_upload.py
git add test_mapper.py
git add FIRSTMILE_FIX_GUIDE.md

git commit -m "Fix: Enhanced column mapping for FirstMile data imports

- Created comprehensive column mapper supporting 50+ FirstMile variations
- Auto-calculates missing fields (Days In Transit, SLA Status)
- Integrated enhanced mapper into dashboard
- Added debug mode details for troubleshooting
- Created test utilities for column inspection
- No more falling back to demo mode!"

echo.
echo Done! Changes committed.
echo.
echo To test:
echo 1. Run: streamlit run app.py
echo 2. Enable Debug Mode in sidebar
echo 3. Upload your FirstMile file
echo.
pause
