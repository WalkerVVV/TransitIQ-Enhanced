@echo off
echo Installing matplotlib for dashboard styling...
echo.

pip install matplotlib

echo.
echo Installation complete! Now running the dashboard...
echo.

cd C:\Users\BrettWalker\TransitIQ-Enhanced
streamlit run app.py

pause
