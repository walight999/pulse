@echo off
REM ============================================================================
REM Build pulse Windows installer (.exe + .iss → setup.exe)
REM ============================================================================

setlocal

REM Step 1: build the .exe via PyInstaller
echo Building pulse.exe via PyInstaller...
pyinstaller --clean pulse.spec
if errorlevel 1 (
    echo PyInstaller build failed.
    exit /b 1
)

REM Step 2: compile installer via Inno Setup
REM   ISCC.exe is the Inno Setup compiler — install from https://jrsoftware.org/isinfo.php
echo Compiling Inno Setup installer...
set ISCC="%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
    echo Inno Setup not found at %ISCC%
    echo Install from https://jrsoftware.org/isinfo.php and try again.
    exit /b 1
)

%ISCC% scripts\installer.iss
if errorlevel 1 (
    echo Inno Setup compilation failed.
    exit /b 1
)

echo.
echo ============================================================================
echo Done. Installer is at: scripts\Output\pulse-setup-1.5.0.exe
echo ============================================================================
endlocal
