@echo off
echo ================================
echo To-Do List Application Builder
echo ================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)
echo ✅ Python found

echo.
echo [2/3] Installing required packages...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)
echo ✅ Requirements installed

echo.
echo [3/3] Building executable...
python build_exe.py
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 Build completed successfully!
echo 📁 Check the 'dist' folder for your executable
echo ========================================
pause
