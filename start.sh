#!/bin/bash
# start.sh — Start the Tariff Resilience full-stack application
set -e
trap 'echo "Shutting down..."; [ -f .pids ] && while IFS= read -r pid; do kill "$pid" 2>/dev/null || true; done < .pids; rm -f .pids; exit 0' SIGINT SIGTERM

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
cd "$PROJECT_ROOT"

# Portable sed (macOS + Linux)
portable_sed() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# Port detection
find_available_port() {
    local port=$1
    if command -v lsof &>/dev/null; then
        while lsof -iTCP:$port -sTCP:LISTEN -t >/dev/null 2>&1; do
            echo "Port $port in use, trying $((port+1))..." >&2
            port=$((port+1))
        done
    fi
    echo $port
}

# === Prerequisite checks ===
check_prerequisites() {
    local errors=0
    echo "=== Checking prerequisites ==="

    # Python 3.10+
    if command -v python3 &>/dev/null; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
            echo "❌ Python 3.10+ required (found $PYTHON_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Python $PYTHON_VERSION"
        fi
    else
        echo "❌ Python 3 not found. Install from https://python.org"
        errors=$((errors+1))
    fi

    # Node.js 18+
    if [ -f "frontend/package.json" ]; then
        if command -v node &>/dev/null; then
            NODE_VERSION=$(node --version | sed 's/v//')
            NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
            if [ "$NODE_MAJOR" -lt 18 ]; then
                echo "❌ Node.js 18+ required (found $NODE_VERSION)"
                errors=$((errors+1))
            else
                echo "✓ Node.js $NODE_VERSION"
            fi
        else
            echo "❌ Node.js not found. Install from https://nodejs.org"
            errors=$((errors+1))
        fi

        # npm
        if ! command -v npm &>/dev/null; then
            echo "❌ npm not found"
            errors=$((errors+1))
        else
            echo "✓ npm $(npm --version)"
        fi
    fi

    # pip
    if command -v python3 &>/dev/null && ! python3 -m pip --version &>/dev/null; then
        echo "❌ pip not found. Run: python3 -m ensurepip"
        errors=$((errors+1))
    else
        echo "✓ pip $(python3 -m pip --version | cut -d' ' -f2)"
    fi

    # lsof (for port detection)
    if ! command -v lsof &>/dev/null; then
        echo "⚠ lsof not found — port detection may not work"
    fi

    if [ $errors -gt 0 ]; then
        echo ""
        echo "❌ $errors prerequisite(s) missing. Please install them and retry."
        exit 1
    fi
    echo ""
}

check_prerequisites

# Detect backend directory
BACKEND_DIR="$PROJECT_ROOT/backend"
[ ! -d "$BACKEND_DIR" ] && [ -f "$PROJECT_ROOT/pyproject.toml" ] && BACKEND_DIR="$PROJECT_ROOT"

if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found"
    exit 1
fi

echo "=== Setting up backend ==="
cd "$BACKEND_DIR"

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
if [ -f "pyproject.toml" ]; then
    pip install . -q
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
fi

# Database — default to SQLite with absolute path
DB_PATH="$PROJECT_ROOT/storage/app.db"
mkdir -p "$(dirname "$DB_PATH")"
export DATABASE_URL="${DATABASE_URL:-sqlite:///$DB_PATH}"
echo "  Database: $DATABASE_URL"

# Detect available ports
BACKEND_PORT=$(find_available_port 9000)
FRONTEND_PORT=$(find_available_port 5173)

# Update shared_config.json with detected ports using Python
if [ -f "$PROJECT_ROOT/shared_config.json" ]; then
    python3 -c "
import json, sys
with open('$PROJECT_ROOT/shared_config.json') as f: 
    cfg = json.load(f)
cfg.setdefault('ports', {})
cfg['ports']['backend'] = $BACKEND_PORT
cfg['ports']['frontend_web'] = $FRONTEND_PORT
cfg['cors_origins'] = ['http://localhost:$FRONTEND_PORT']
with open('$PROJECT_ROOT/shared_config.json', 'w') as f: 
    json.dump(cfg, f, indent=2)
" 2>/dev/null || echo "⚠ Could not update shared_config.json"
fi

# Update backend CORS
export CORS_ORIGINS="http://localhost:$FRONTEND_PORT"

# Run seed script
if [ -f "app/seed.py" ]; then
    echo "Seeding database..."
    python3 app/seed.py 2>/dev/null || echo "Seed script completed"
fi

# Start backend
echo "Starting backend on http://localhost:$BACKEND_PORT"
uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT >/dev/null 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$PROJECT_ROOT/.pids"

cd "$PROJECT_ROOT"

# Frontend setup
FRONTEND_DIR="$PROJECT_ROOT/frontend"
if [ -d "$FRONTEND_DIR" ] && [ -f "$FRONTEND_DIR/package.json" ]; then
    echo ""
    echo "=== Setting up frontend ==="
    cd "$FRONTEND_DIR"

    # Install frontend dependencies
    echo "Installing frontend dependencies..."
    npm install -q

    # Update frontend .env with actual backend port
    echo "VITE_API_URL=http://localhost:$BACKEND_PORT" > "$FRONTEND_DIR/.env"

    # Start frontend
    echo "Starting frontend on http://localhost:$FRONTEND_PORT"
    npm run dev -- --port $FRONTEND_PORT >/dev/null 2>&1 &
    FE_PID=$!
    echo "$FE_PID" >> "$PROJECT_ROOT/.pids"

    cd "$PROJECT_ROOT"
fi

echo ""
echo "=== Services running ==="
echo "  Backend:  http://localhost:$BACKEND_PORT"
echo "  API Docs: http://localhost:$BACKEND_PORT/docs"
[ -n "$FRONTEND_PORT" ] && echo "  Frontend: http://localhost:$FRONTEND_PORT"
echo ""
echo "=== Default Credentials ==="
echo "  Email:    admin@example.com"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C to stop all services"
wait
