@echo off
REM Script to export netlist from eagle schematics

REM Define root directory
set "ROOT_DIR=RootCUBOs"

REM Define the output script file
set "SCRIPT_FILE=export_png.scr"

REM Define Eagle PATH
set "EAGLE_PATH=C:\EAGLE 9.6.2\eaglecon.exe"

REM Clear the output script file and add a header
echo # Auto-generated script to export PNGs > "%SCRIPT_FILE%"

REM Find all .sch files in subfolders and process them
for /r "%ROOT_DIR%" %%f in (*.sch) do (
    REM Replace backslashes with forward slashes and add single quotes
    set "FILE_PATH=%%f"
    setlocal enabledelayedexpansion
    set "FILE_PATH=!FILE_PATH:\=/!"
    REM Remove the "C:/EAGLE 9.6.2/" part from the path
    set "FILE_PATH=!FILE_PATH:C:/EAGLE 9.6.2/=!"
    echo EDIT '!FILE_PATH!' >> "%SCRIPT_FILE%"
    echo EXPORT IMAGE '!FILE_PATH:.sch=.png!' 600 >> "%SCRIPT_FILE%"
    REM echo QUIT >> "%SCRIPT_FILE%"
    endlocal
)

REM Run the script in Eagle
REM "%EAGLE_PATH%" -S "%SCRIPT_FILE%"