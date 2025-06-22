@echo off
echo ====================================
echo Creating Release Package
echo ====================================
echo.

echo [1/3] Building executable...
if exist "setup_and_build.bat" (
    call setup_and_build.bat
) else (
    echo setup_and_build.bat not found, running build directly...
    python build_exe.py
)

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Build failed, cannot create release
    pause
    exit /b 1
)

echo.
echo [2/3] Creating release folders...
if not exist "release" mkdir release
if not exist "release\end-user" mkdir release\end-user
if not exist "release\developers" mkdir release\developers

echo.
echo [3/3] Copying files...

rem Copy executable for end users
if exist "dist\ToDo-List.exe" (
    copy "dist\ToDo-List.exe" "release\end-user\" >nul
    echo ✅ Copied executable to release\end-user\
) else (
    echo ❌ Executable not found in dist folder
    pause
    exit /b 1
)

rem Copy source files for developers
copy "main.py" "release\developers\" >nul 2>&1
copy "requirements.txt" "release\developers\" >nul 2>&1
copy "README.md" "release\developers\" >nul 2>&1
copy "LICENSE" "release\developers\" >nul 2>&1
if exist "setup_and_build.bat" copy "setup_and_build.bat" "release\developers\" >nul 2>&1
if exist "build_exe.py" copy "build_exe.py" "release\developers\" >nul 2>&1
if exist "ToDo-List.spec" copy "ToDo-List.spec" "release\developers\" >nul 2>&1
echo ✅ Copied source files to release\developers\

rem Create a simple instruction file for end users
echo This is your To-Do List application. > "release\end-user\README.txt"
echo. >> "release\end-user\README.txt"
echo Simply double-click ToDo-List.exe to run the application. >> "release\end-user\README.txt"
echo No installation required! >> "release\end-user\README.txt"
echo. >> "release\end-user\README.txt"
echo The app will create its own data files when you first use it. >> "release\end-user\README.txt"

echo.
echo 🎉 Release package created!
echo.
echo 📁 For END USERS: Share the 'release\end-user' folder
echo    - Contains: ToDo-List.exe + README.txt
echo.
echo 📁 For DEVELOPERS: Share the 'release\developers' folder  
echo    - Contains: Source code + build scripts + documentation
echo.
echo 💡 TIP: You can zip these folders for easy sharing
pause
