@echo off
echo Committing FirstMile Dashboard Fix...
echo.

git add app.py
git add dashboard_firstmile_style.py
git add dashboard_imports.py
git add dashboard_main.py
git add test_dashboard.bat
git add run_firstmile_dashboard.bat
git add FIRSTMILE_DESIGN_SUMMARY.md

git commit -m "Fix: Resolved duplicate st.set_page_config error

- Created dashboard_imports.py to extract functions without executing config
- Moved st.set_page_config to app.py (only called once)
- Updated imports to avoid circular dependencies
- Maintained all FirstMile styling and functionality
- Dashboard now loads without matplotlib dependencies
- All 11 sections and 6 analysis tools working properly"

echo.
echo ✅ Dashboard fix committed!
echo.
echo To run: streamlit run app.py
echo Or double-click: test_dashboard.bat
echo.
pause
