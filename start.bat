@echo off
setlocal enabledelayedexpansion

echo === Checking prerequisites ===

:: Check Python 3.10+
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://python.org
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYTHON_VER=%%v
echo OK Python %PYTHON_VER%

:: Check Python version is 3.10+
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VER%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)
if %PYTHON_MAJOR% LSS 3 (
    echo ERROR: Python 3.10+ required ^(found %PYTHON_VER%^)
    exit /b 1
)
if %PYTHON_MAJOR% EQU 3 if %PYTHON_MINOR% LSS 10 (
    echo ERROR: Python 3.10+ required ^(found %PYTHON_VER%^)
    exit /b 1
)

:: Check Node.js 18+ (if frontend exists)
if exist "frontend\package.json" (
    node --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Node.js not found. Install from https://nodejs.org
        exit /b 1
    )
    for /f "tokens=1" %%v in ('node --version') do set NODE_VER=%%v
    set NODE_VER=!NODE_VER:~1!
    echo OK Node.js !NODE_VER!
    
    :: Check Node.js version is 18+
    for /f "tokens=1 delims=." %%a in ("!NODE_VER!") do set NODE_MAJOR=%%a
    if !NODE_MAJOR! LSS 18 (
        echo ERROR: Node.js 18+ required ^(found !NODE_VER!^)
        exit /b 1
    )
    
    :: Check npm
    npm --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: npm not found
        exit /b 1
    )
    for /f %%v in ('npm --version') do echo OK npm %%v
)

:: Check pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip not found. Run: python -m ensurepip
    exit /b 1
)
for /f "tokens=2" %%v in ('python -m pip --version') do echo OK pip %%v

echo.

:: Database — default to SQLite with absolute path
set PROJECT_ROOT=%~dp0
set DB_PATH=%PROJECT_ROOT%storage\app.db
if not exist "%PROJECT_ROOT%storage" mkdir "%PROJECT_ROOT%storage"
if not defined DATABASE_URL set DATABASE_URL=sqlite:///%DB_PATH:\=/%
echo Database: %DATABASE_URL%

:: Find available backend port
set BACKEND_PORT=9000
:find_backend_port
netstat -an | find ":%BACKEND_PORT% " >nul 2>&1
if not errorlevel 1 (
    echo Port %BACKEND_PORT% in use, trying next...
    set /a BACKEND_PORT+=1
    goto find_backend_port
)

:: Find available frontend port
set FRONTEND_PORT=5173
:find_frontend_port
netstat -an | find ":%FRONTEND_PORT% " >nul 2>&1
if not errorlevel 1 (
    echo Port %FRONTEND_PORT% in use, trying next...
    set /a FRONTEND_PORT+=1
    goto find_frontend_port
)

:: Detect backend directory
set BACKEND_DIR=backend
if not exist "%BACKEND_DIR%" (
    if exist "pyproject.toml" set BACKEND_DIR=.
)

if not exist "%BACKEND_DIR%" (
    echo ERROR: Backend directory not found
    exit /b 1
)

echo === Setting up backend ===
cd %BACKEND_DIR%

:: Create venv if not exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate venv
call .venv\Scripts\activate.bat

:: Install backend dependencies
echo Installing backend dependencies...
if exist "pyproject.toml" (
    pip install . -q
) else if exist "requirements.txt" (
    pip install -r requirements.txt -q
)

:: Update shared_config.json with detected ports using Python
if exist "..\shared_config.json" (
    python -c "import json; cfg = json.load(open('../shared_config.json')); cfg.setdefault('ports', {}); cfg['ports']['backend'] = %BACKEND_PORT%; cfg['ports']['frontend_web'] = %FRONTEND_PORT%; cfg['cors_origins'] = ['http://localhost:%FRONTEND_PORT%']; json.dump(cfg, open('../shared_config.json', 'w'), indent=2)" 2>nul
)

:: Run seed script
if exist "app\seed.py" (
    echo Seeding database...
    python app\seed.py 2>nul || echo Seed script completed
)

:: Start backend
echo Starting backend on http://localhost:%BACKEND_PORT%
start /b python -m uvicorn app.main:app --host 0.0.0.0 --port %BACKEND_PORT% >nul 2>&1

:: Get backend PID (most recent python.exe)
for /f "skip=3 tokens=2" %%p in ('tasklist /fi "imagename eq python.exe" /fo list') do (
    echo %%p >> ..\.pids
    goto backend_started
)
:backend_started

cd ..

:: Frontend setup
if exist "frontend\package.json" (
    echo.
    echo === Setting up frontend ===
    cd frontend

    :: Install frontend dependencies
    echo Installing frontend dependencies...
    call npm install -q

    :: Update frontend .env with actual backend port
    echo VITE_API_URL=http://localhost:%BACKEND_PORT% > .env

    :: Start frontend
    echo Starting frontend on http://localhost:%FRONTEND_PORT%
    start /b npm run dev -- --port %FRONTEND_PORT% >nul 2>&1
    
    cd ..
)

echo.
echo === Services running ===
echo   Backend:  http://localhost:%BACKEND_PORT%
echo   API Docs: http://localhost:%BACKEND_PORT%/docs
if exist "frontend\package.json" echo   Frontend: http://localhost:%FRONTEND_PORT%
echo.
echo === Default Credentials ===
echo   Email:    admin@example.com
echo   Password: admin123
echo.
echo Press Ctrl+C to stop, or run stop.bat
pause
