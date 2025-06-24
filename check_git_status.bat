@echo off
echo Checking Git Status...
echo.

cd C:\Users\BrettWalker\TransitIQ-Enhanced

echo Current branch:
git branch --show-current
echo.

echo Repository status:
git status
echo.

echo Recent commits:
git log --oneline -5
echo.

echo Remote repository:
git remote -v
echo.

pause
