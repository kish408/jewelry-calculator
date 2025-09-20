@echo off
cd /d "D:\Gold App"

echo Checking for changes...
set changes=

REM Check if there are any uncommitted changes
for /f "delims=" %%i in ('git status --porcelain') do set changes=1

if "%changes%"=="" (
    echo No changes detected. Nothing to commit.
) else (
    echo Changes detected. Staging files...
    git add .

    echo Committing changes...
    for /f "tokens=1-5 delims=/:. " %%d in ("%date% %time%") do set commitmsg=Update_%%d-%%e-%%f_%%g-%%h-%%i
    git commit -m "%commitmsg%"

    echo Pushing to GitHub...
    git push origin main
)

echo Done! Press any key to exit.
pause
