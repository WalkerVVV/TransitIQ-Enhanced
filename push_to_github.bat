@echo off
echo ========================================
echo Pushing FirstMile Dashboard to GitHub
echo ========================================
echo.

cd C:\Users\BrettWalker\TransitIQ-Enhanced

echo 1. Adding all changed files...
git add -A

echo.
echo 2. Committing with comprehensive message...
git commit -m "Major Update: FirstMile Clean Dashboard Design + Fix st.set_page_config error

DESIGN CHANGES:
- Implemented FirstMile brand colors (#5CB85C green, #1E3A8A navy)
- Removed all matplotlib dependencies and gradient styling
- Clean card-based layout with proper spacing
- Professional tables with 14px font and 12px padding
- Performance indicators: Green (95%+), Yellow (90-94%), Red (<90%)
- Matches FirstMile.com website aesthetic

TECHNICAL FIXES:
- Resolved duplicate st.set_page_config() error
- Created dashboard_imports.py to safely import functions
- Moved page config to app.py (called only once)
- Fixed circular import dependencies

FEATURES MAINTAINED:
- All 11 dashboard sections operational
- 6 integrated analysis tools (Carrier Optimization, Zone Analysis, etc.)
- FirstMile column mapping for tracking reports
- Export to Excel/CSV functionality
- Debug mode for troubleshooting

FILES CHANGED:
- app.py - Main entry point with page config
- dashboard_imports.py - Safe function imports
- dashboard_firstmile_style.py - FirstMile styling
- dashboard_main.py - Main dashboard logic
- firstmile_column_mapper.py - Column mapping
- FIRSTMILE_DESIGN_SUMMARY.md - Documentation"

echo.
echo 3. Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo ✅ Dashboard pushed to GitHub!
echo ========================================
echo.
echo Your repository is now updated with:
echo - FirstMile clean design (no gradients)
echo - Fixed configuration errors
echo - All features working properly
echo.
echo View on GitHub: https://github.com/YourUsername/TransitIQ-Enhanced
echo.
pause
