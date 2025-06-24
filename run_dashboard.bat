@echo off
echo Navigating to TransitIQ-Enhanced directory and running tests...
echo.

cd C:\Users\BrettWalker\TransitIQ-Enhanced

echo Current directory:
cd
echo.

echo Testing the column mapper...
python test_mapper.py
echo.
echo ========================================
echo.

echo Now let's run the dashboard...
echo.
streamlit run app.py

pause
