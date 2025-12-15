@echo off
echo ========================================
echo Organizing MPS Data Structure
echo ========================================
echo.

cd C:\Users\camer\OneDrive\Documents\Projects\Meta-Aria-2

echo Creating MPS data folder structure...
mkdir data\mps_data 2>nul

echo.
echo Current recordings found:
dir /b data\recordings\*.vrs 2>nul

echo.
echo Creating MPS folders for each recording...

:: Create folder for Surgery_1 if it exists
if exist "data\recordings\Surgery_1.vrs" (
    mkdir "data\mps_data\Surgery_1" 2>nul
    echo   Created: data\mps_data\Surgery_1\
)

:: Create folder for Surgery_2 if it exists
if exist "data\recordings\Surgery_2.vrs" (
    mkdir "data\mps_data\Surgery_2" 2>nul
    echo   Created: data\mps_data\Surgery_2\
)

echo.
echo ========================================
echo Folder structure created!
echo ========================================
echo.
echo Next steps:
echo 1. Place MPS files for each recording in its folder:
echo    - hand_tracking_results.csv
echo    - general_eye_gaze.csv
echo    - summary.json
echo.
echo Example:
echo   data\mps_data\Surgery_2\hand_tracking_results.csv
echo   data\mps_data\Surgery_2\general_eye_gaze.csv
echo   data\mps_data\Surgery_2\summary.json
echo.
echo 2. Run the updated analysis:
echo    python src\main.py --recording data\recordings\Surgery_2.vrs
echo.
pause