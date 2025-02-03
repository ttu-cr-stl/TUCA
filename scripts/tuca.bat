@echo off
setlocal

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%\.."

REM Change to root directory
cd /d "%ROOT_DIR%"

if "%1"=="" goto :usage
if "%1"=="--help" goto :usage

if "%1"=="emu" (
    if "%2"=="" goto :usage
    if "%3"=="" goto :usage
    
    set "program_dir=%2"
    set "test_name=%3"
    set "verbose=false"
    
    REM Check for verbose flag
    if "%4"=="--verbose" set "verbose=true"
    
    REM Setup paths
    set "prog_dir=Programs\%program_dir%"
    set "prog_file=%prog_dir%\prog.txt"
    set "test_mems_dir=%prog_dir%\test_mems"
    
    REM Check if program exists
    if not exist "%prog_dir%" (
        echo Error: Program directory %prog_dir% not found
        exit /b 1
    )
    
    REM Check if program file exists
    if not exist "%prog_file%" (
        echo Error: Program file %prog_file% not found
        exit /b 1
    )
    
    if "%test_name%"=="all" (
        REM Run all tests in test_mems directory
        if not exist "%test_mems_dir%" (
            echo Error: Test directory %test_mems_dir% not found
            exit /b 1
        )
        
        echo Running emulator on all tests in %test_mems_dir%
        set "success=true"
        set "found_files=false"
        
        for %%f in ("%test_mems_dir%\*.txt") do (
            set "found_files=true"
            call :run_emulator "%prog_file%" "%%f" "%verbose%" || set "success=false"
        )
        
        if "%found_files%"=="false" (
            echo Error: No .txt files found in %test_mems_dir%
            exit /b 1
        )
        
        if "%success%"=="false" exit /b 1
    ) else (
        REM Run specific test
        set "mem_file=%test_mems_dir%\%test_name%.txt"
        if not exist "%mem_file%" (
            echo Error: Test file %mem_file% not found
            exit /b 1
        )
        call :run_emulator "%prog_file%" "%mem_file%" "%verbose%" || exit /b 1
    )
    exit /b 0
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

:run_emulator
set "prog_file=%~1"
set "mem_file=%~2"
set "verbose=%~3"
for %%F in ("%mem_file%") do set "test_name=%%~nF"
set "prog_dir=%~dp1"
set "results_dir=%prog_dir%results"
set "output_file=%results_dir%\emulator\%test_name%.txt"

echo.
echo Running emulator with memory file: %mem_file%
echo Results will be saved to: %output_file%
echo ----------------------------------------

REM Create results directory
if not exist "%results_dir%\emulator" mkdir "%results_dir%\emulator"

REM Run emulator and save results
if "%verbose%"=="true" (
    python "%ROOT_DIR%\Pipeline\Emulator\src\run.py" "%prog_file%" "%mem_file%" "%output_file%" --verbose
) else (
    python "%ROOT_DIR%\Pipeline\Emulator\src\run.py" "%prog_file%" "%mem_file%" "%output_file%"
)
set "status=%ERRORLEVEL%"
echo ----------------------------------------
exit /b %status% 