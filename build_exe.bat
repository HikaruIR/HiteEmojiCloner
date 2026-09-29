@echo off
setlocal
cd /d "%~dp0"
title Building HiteEmojiCloner EXE...

echo ==============================================
echo   Building HiteEmojiCloner Executable
echo ==============================================

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run run.bat first!
    pause
    exit /b 1
)

echo [*] Installing PyInstaller...
.venv\Scripts\python.exe -m pip install --upgrade pyinstaller requests rich >nul 2>&1

echo [*] Compiling standalone EXE with PyInstaller...
.venv\Scripts\pyinstaller.exe --onefile --clean --name "HiteEmojiCloner" --console main.py

if exist "dist\HiteEmojiCloner.exe" (
    echo.
    echo ==============================================
    echo [SUCCESS] Binary created: dist\HiteEmojiCloner.exe
    echo You can now upload this .exe to GitHub Releases!
    echo ==============================================
) else (
    echo.
    echo [ERROR] Build failed. Check terminal output above.
)

pause
