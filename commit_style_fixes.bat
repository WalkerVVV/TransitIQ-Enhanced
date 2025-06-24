@echo off
echo Committing style fixes to git...
cd /d C:\Users\BrettWalker\TransitIQ-Enhanced
git add -A
git commit -m "MAJOR FIX: Made table fonts HUGE (20px cells, 22px headers) and fixed alignment issues"
echo.
echo Style fixes committed!
pause
