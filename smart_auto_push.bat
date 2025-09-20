@echo off
cd /d "D:\Gold App"

echo Checking for changes...
REM Refresh index
git update-index -q --refresh

REM Check for unstaged changes
git diff --quiet --ignore-submodules HEAD
if %errorlevel%==0 (
    git diff --cached --quiet
)

if %errorlevel%==0 (
    echo No changes detected. Nothing to commit.
) else (
    echo Changes detected. Staging all files...
    git add .

    echo Files to be committed:
    git status --short

    echo Committing changes...
    for /f "tokens=1-5 delims=/:. " %%d in ("%date% %time%") do set commitmsg=Update_%%d-%%e-%%f_%%g-%%h-%%i
    git commit -m "%commitmsg%"

    echo Pushing to GitHub...
    git push origin main
)

echo Done! Press any key to exit.
pause
