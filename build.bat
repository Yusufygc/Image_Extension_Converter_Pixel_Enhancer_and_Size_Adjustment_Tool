@echo off
echo ==========================================
echo Conventor Build Script (Nuitka)
echo ==========================================
echo.

REM Check if Nuitka is installed
python -c "import nuitka" 2>NUL
if %errorlevel% neq 0 (
    echo Nuitka is not installed. Installing...
    pip install nuitka zstandard
)

echo Cleaning previous builds...
rmdir /s /q build 2>NUL
rmdir /s /q dist 2>NUL
rmdir /s /q Conventor.dist 2>NUL
rmdir /s /q Conventor.build 2>NUL

echo.
echo Building executable...
echo This might take a few minutes...
echo.

REM --onefile: Creates a single executable file (slower startup, easier distribution)
python -m nuitka --onefile --enable-plugin=pyside6 --windows-console-mode=disable --windows-icon-from-ico=assets/icons/icon.ico --include-data-dir=assets=assets --include-module=PIL --include-module=core.converter --include-module=core.enhancer --include-module=core.resizer --output-dir=dist --main=main.py

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo Build SUCCESSFUL!
    echo Executable is located in: dist\main.exe
    echo You can move this file anywhere and run it.
    echo ==========================================
) else (
    echo.
    echo Build FAILED. Please check the errors above.
)
pause
