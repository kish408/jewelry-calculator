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

    echo Committing changes...
    git commit -m "%commitmsg%"

    echo Pushing to GitHub...
    git push origin main
)

echo Done! Press any key to exit.
pause
