@echo off
cd /d "D:\Gold App"

echo ----------------------------------------
echo Checking for changes in Git repo...
echo ----------------------------------------

REM Refresh index
git update-index -q --refresh

REM Stage all files
git add .

REM Show files to be committed
echo Files staged for commit:
git status --short

REM ------------------------------
REM Generate safe date-time commit message
REM ------------------------------
for /f "tokens=1-3 delims=/- " %%a in ("%date%") do (
    set d=%%a
    set m=%%b
    set y=%%c
)
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set hh=%%a
    set mm=%%b
    set ss=%%c
)
set commitmsg=Update_%y%-%m%-%d%_%hh%-%mm%-%ss%
echo Commit message: %commitmsg%

REM ------------------------------
REM Commit all changes (force if nothing changed)
REM ------------------------------
git commit -m "%commitmsg%" --allow-empty

REM Push to GitHub
echo Pushing to GitHub...
git push origin main

echo ----------------------------------------
echo Done! Press any key to exit.
pause
