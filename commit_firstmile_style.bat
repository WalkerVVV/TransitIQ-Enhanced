@echo off
echo Committing FirstMile Clean Design Updates...

git add dashboard_main.py
git add dashboard_firstmile_style.py
git add app.py
git add run_firstmile_dashboard.bat
git add FIRSTMILE_DESIGN_SUMMARY.md

git commit -m "Redesign: FirstMile clean modern styling without gradients

- Removed all matplotlib dependencies and gradient styling
- Implemented FirstMile brand colors (#5CB85C green, #1E3A8A navy)
- Clean card-based layout with proper spacing
- Readable tables with 14px font and 12px padding
- Performance indicators using solid colors (green/yellow/red)
- Professional business styling matching FirstMile website
- No additional dependencies needed - runs lean
- All 11 sections and 6 tools maintained"

echo.
echo Done! FirstMile styled dashboard committed.
echo.
echo To run: double-click run_firstmile_dashboard.bat
echo.
pause
