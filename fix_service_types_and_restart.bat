@echo off
echo.
echo ==============================================
echo    COMMITTING SERVICE TYPE FIXES!            
echo ==============================================
echo.

cd /d C:\Users\BrettWalker\TransitIQ-Enhanced

echo Committing all service type fixes...
git add -A
git commit -m "CRITICAL FIX: Stop incorrectly splitting Expedited into Ground - respect actual service types in data"

echo.
echo ==============================================
echo    RESTARTING DASHBOARD WITH FIXES!         
echo ==============================================
echo.
echo Killing any existing Streamlit processes...
taskkill /F /IM streamlit.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting dashboard with corrected service logic...
start cmd /k "cd /d %~dp0 && venv\Scripts\activate && streamlit run dashboard_main.py"

echo.
echo ============================================== 
echo    FIXES APPLIED:                            
echo    - Service types now show ACTUAL data      
echo    - No more fake Ground shipments           
echo    - Priority and Expedited properly split   
echo ==============================================
echo.
timeout /t 5
