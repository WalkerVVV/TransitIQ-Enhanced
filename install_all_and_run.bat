@echo off
echo ========================================
echo Installing ALL TransitIQ Dependencies
echo ========================================
echo.

echo Installing from requirements.txt...
pip install -r requirements.txt

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.

echo Starting TransitIQ Dashboard...
echo.
cd C:\Users\BrettWalker\TransitIQ-Enhanced
streamlit run app.py

pause
