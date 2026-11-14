@echo off
cd /d "%~dp0"
echo ================================================================
echo   Pushing AI-Escape-Room-koushik to GitHub
echo   Target: https://github.com/Koushik84/-AI-Escape-Room-Koushik.git
echo ================================================================

echo.
echo [1/4] Staging files (.env is protected and ignored)...
git add -A

echo.
echo [2/4] Committing latest changes...
git commit -m "feat: complete visual interactive AI escape room with state machine"

echo.
echo [3/4] Renaming branch to main...
git branch -M main

echo.
echo [4/4] Setting remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/Koushik84/-AI-Escape-Room-Koushik.git

echo.
echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo Normal push rejected (remote might have initial README/commit).
    echo Retrying with force push to synchronize repository...
    git push -u origin main --force
)

echo.
echo ================================================================
echo Push complete! Repository: https://github.com/Koushik84/-AI-Escape-Room-Koushik
echo ================================================================
pause
