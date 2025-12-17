@echo off
REM Windows build script for Space Shooter game
REM Run this on a Windows system with Python installed

echo ========================================
echo Space Shooter - Windows Build Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller
echo.

REM Clean previous builds
if exist "build" (
    echo Cleaning previous build artifacts...
    rmdir /s /q build
)
if exist "dist" (
    rmdir /s /q dist
)
if exist "*.spec" (
    del /q *.spec
)
echo.

REM Build the executable
echo Building executable...
echo This may take a few minutes...
pyinstaller --onefile --windowed --name "SpaceShooter" --add-data "sounds;sounds" src/main.py
echo.
echo NOTE: If you don't have a sounds folder, the build will succeed
echo       but the game will run without audio (which is fine!)
echo.

REM Check if build was successful
if exist "dist\SpaceShooter.exe" (
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Your executable is located at:
    echo   dist\SpaceShooter.exe
    echo.
    echo File size:
    dir dist\SpaceShooter.exe | find "SpaceShooter.exe"
    echo.
    echo You can now distribute this file to other Windows users.
    echo They do NOT need Python installed to run it.
    echo.
) else (
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo Check the output above for errors.
    echo.
)

pause
