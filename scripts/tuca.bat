@echo off
setlocal EnableDelayedExpansion

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."

REM Change to root directory
cd /d "%ROOT_DIR%"

if "%1"=="" goto :usage
if "%1"=="--help" goto :usage

if "%1"=="emu" (
    if "%2"=="" goto :usage
    
    set "program_dir=%2"
    set "test_name=%3"
    set "verbose=false"
    
    REM Check for verbose flag
    if "%4"=="--verbose" set "verbose=true"
    if "%3"=="--verbose" set "verbose=true"
    
    REM Setup paths (using proper Windows path separators)
    set "prog_dir=%ROOT_DIR%\Programs\%program_dir%"
    set "prog_file=!prog_dir!\prog.txt"
    
    echo Debug: Checking directory !prog_dir!
    
    REM Check if program exists
    if not exist "!prog_dir!" (
        echo Error: Program Directory not found
        exit /b 1
    )
    
    REM Check if program file exists
    if not exist "!prog_file!" (
        echo Error: Program file not found
        exit /b 1
    )
    
    REM If no test specified, test is "all", or only --verbose flag, run all tests from config
    if "%test_name%"=="" (
        python "!ROOT_DIR!\Pipeline\Emulator\src\run.py" "!prog_file!" %4
        exit /b !ERRORLEVEL!
    ) else if "%test_name%"=="--verbose" (
        python "!ROOT_DIR!\Pipeline\Emulator\src\run.py" "!prog_file!" --verbose
        exit /b !ERRORLEVEL!
    ) else if "%test_name%"=="all" (
        python "!ROOT_DIR!\Pipeline\Emulator\src\run.py" "!prog_file!" %4
        exit /b !ERRORLEVEL!
    ) else (
        REM Run specific test
        set "mem_file=!prog_dir!\test_mems\%test_name%.txt"
        set "output_file=!prog_dir!\results\emulator\%test_name%.txt"
        
        echo Debug: Looking for test file !mem_file!
        
        if not exist "!mem_file!" (
            echo Error: Test file not found
            exit /b 1
        )
        
        REM Create results directory if it doesn't exist
        if not exist "!prog_dir!\results\emulator" mkdir "!prog_dir!\results\emulator"
        
        if "%verbose%"=="true" (
            python "!ROOT_DIR!\Pipeline\Emulator\src\run.py" "!prog_file!" "!mem_file!" "!output_file!" --verbose
        ) else (
            python "!ROOT_DIR!\Pipeline\Emulator\src\run.py" "!prog_file!" "!mem_file!" "!output_file!"
        )
        exit /b !ERRORLEVEL!
    )
)

if "%1"=="build" (
    if "%2"=="" goto :usage
    python "%SCRIPT_DIR%\build.py" build "%2"
    exit /b %ERRORLEVEL%
)

if "%1"=="verify" (
    if "%2"=="" goto :usage
    if "%3"=="" goto :usage
    python "%SCRIPT_DIR%\verify.py" "%2" "%3"
    exit /b %ERRORLEVEL%
)

if "%1"=="clean" (
    shift
    python "%SCRIPT_DIR%\build.py" clean %*
    exit /b %ERRORLEVEL%
)

:usage
echo TUCA Development Tools
echo.
echo Usage: tuca ^<command^> [args...]
echo.
echo Commands:
echo   emu ^<program^> ^<test^>  Run program through emulator
echo     ^<program^>: Program directory name
echo     ^<test^> can be either:
echo       - test name: Run specific test (e.g., mem1)
echo       - 'all': Run all tests in test_mems/
echo     Options:
echo       --verbose: Show detailed execution trace
echo     Results saved to results/emulator/^<test^>.txt
echo     Examples:
echo       tuca emu example1 mem1         # Run with minimal output
echo       tuca emu example1 mem1 --verbose  # Show execution trace
echo       tuca emu example1 all          # Run all tests
echo.
echo   build ^<program^>       Build a TUCA program
echo     Example: tuca build example1
echo.
echo   verify ^<program^> ^<test^>  Verify Verilog against emulator
echo     Compares:
echo       results/emulator/^<test^>.txt
echo       results/verilog/^<test^>.txt
echo     Example: tuca verify example1 mem1
echo.
echo   clean [program...]    Clean build artifacts
echo     Example: tuca clean              # Clean all
echo             tuca clean example1      # Clean specific program
echo             tuca clean p1 p2         # Clean multiple programs
exit /b 1 