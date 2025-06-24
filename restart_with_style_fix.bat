@echo off
echo.
echo ==============================================
echo    RESTARTING DASHBOARD WITH STYLE FIXES!    
echo ==============================================
echo.
echo Killing any existing Streamlit processes...
taskkill /F /IM streamlit.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting FirstMile Dashboard with BIG READABLE FONTS...
echo.
start cmd /k "cd /d %~dp0 && venv\Scripts\activate && streamlit run dashboard_main.py"

echo.
echo ============================================== 
echo    Dashboard starting in your browser...     
echo    Tables should now have HUGE fonts!        
echo    All text should be properly centered!     
echo ==============================================
echo.
echo Press any key to close this window...
pause >nul
