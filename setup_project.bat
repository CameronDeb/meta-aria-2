@echo off
echo ========================================
echo Meta Aria 2 Surgical Training Analysis
echo Setup Script for Windows
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9-3.11 from python.org
    pause
    exit /b 1
)

echo Creating project directory structure...
cd /d C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2

:: Create directory structure
mkdir data 2>nul
mkdir data\recordings 2>nul
mkdir data\processed 2>nul
mkdir data\models 2>nul
mkdir src 2>nul
mkdir src\detection 2>nul
mkdir src\analysis 2>nul
mkdir src\visualization 2>nul
mkdir outputs 2>nul
mkdir outputs\reports 2>nul
mkdir outputs\videos 2>nul
mkdir configs 2>nul

echo.
echo Creating Python virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing required packages...
echo This may take several minutes...
python -m pip install --upgrade pip

:: Install core dependencies
pip install numpy>=1.24.0
pip install opencv-contrib-python>=4.8.0
pip install pillow>=10.0.0
pip install pandas>=2.0.0
pip install matplotlib>=3.7.0
pip install scikit-learn>=1.3.0

:: Install Project Aria Tools
echo.
echo Installing Project Aria Tools...
pip install projectaria-tools

:: Install visualization
pip install rerun-sdk

:: Install ML libraries (optional but recommended)
echo.
echo Installing optional ML libraries for custom detection...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install transformers>=4.30.0

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Place your Aria recordings (.vrs files) in: data\recordings\
echo 2. Run: python src\main.py
echo.
echo To activate the environment later, run:
echo   venv\Scripts\activate.bat
echo.
pause