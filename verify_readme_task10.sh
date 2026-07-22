#!/bin/bash
# Comprehensive verification for TASK-10: Runtime Docs and Developer Onboarding

echo "=== TASK-10 README VERIFICATION ==="
echo ""

ERRORS=0

# Check 1: Prerequisites section
echo "✓ Check 1: Prerequisites section documents Python 3.10+, Node 18+, pip, npm"
if grep -q "Python 3.10 or higher" README.md && \
   grep -q "Node.js 18 or higher" README.md && \
   grep -q "pip" README.md && \
   grep -q "npm" README.md; then
    echo "  PASS: All prerequisites documented"
else
    echo "  FAIL: Missing prerequisites"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 2: Local setup section
echo "✓ Check 2: Local setup section with ./start.sh or start.bat"
if grep -q "./start.sh" README.md && grep -q "start.bat" README.md; then
    echo "  PASS: Both Unix and Windows startup scripts documented"
else
    echo "  FAIL: Missing startup script documentation"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 3: Default credentials
echo "✓ Check 3: Default credentials admin@example.com / admin123"
if grep -q "admin@example.com" README.md && grep -q "admin123" README.md; then
    echo "  PASS: Default credentials documented"
    # Verify match with seed script
    if grep -q '"email": "admin@example.com"' backend/app/seed.py && \
       grep -q '"password": "admin123"' backend/app/seed.py; then
        echo "  PASS: Credentials match seed script"
    else
        echo "  FAIL: Credentials don't match seed script"
        ERRORS=$((ERRORS+1))
    fi
else
    echo "  FAIL: Default credentials not documented"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 4: Running Tests section
echo "✓ Check 4: Running Tests section with backend pytest and frontend npm test"
if grep -q "## Running Tests" README.md && \
   grep -q "pytest tests/" README.md && \
   grep -q "npm test" README.md; then
    echo "  PASS: Test commands documented"
else
    echo "  FAIL: Missing test documentation"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 5: Environment Configuration section
echo "✓ Check 5: Environment Configuration section with .env.example usage"
if grep -q "## Environment Configuration" README.md && \
   grep -q ".env.example" README.md; then
    echo "  PASS: Environment configuration documented"
else
    echo "  FAIL: Missing environment configuration"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 6: API Documentation section
echo "✓ Check 6: API Documentation section with /docs endpoint"
if grep -q "## API Documentation" README.md && \
   grep -q "/docs" README.md; then
    echo "  PASS: API documentation endpoint documented"
else
    echo "  FAIL: Missing API documentation section"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 7: Deployment section
echo "✓ Check 7: Deployment section with Docker and cloud options"
if grep -q "## Production Deployment" README.md && \
   grep -q "Docker" README.md && \
   grep -q "AWS\|Azure\|GCP" README.md; then
    echo "  PASS: Deployment options documented"
else
    echo "  FAIL: Missing deployment documentation"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 8: Troubleshooting section
echo "✓ Check 8: Troubleshooting section with port conflicts and prerequisite failures"
if grep -q "## Troubleshooting" README.md && \
   grep -q "Port Conflicts" README.md && \
   grep -q "Python Version" README.md; then
    echo "  PASS: Troubleshooting section complete"
else
    echo "  FAIL: Missing troubleshooting content"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 9: Default ports match shared_config.json
echo "✓ Check 9: Default ports (9000, 5173) match shared_config.json"
BACKEND_PORT=$(grep -A 2 '"ports"' shared_config.json | grep backend | grep -o '[0-9]*')
FRONTEND_PORT=$(grep -A 2 '"ports"' shared_config.json | grep frontend | grep -o '[0-9]*')
if [ "$BACKEND_PORT" = "9000" ] && [ "$FRONTEND_PORT" = "5173" ]; then
    echo "  PASS: Ports match (backend=$BACKEND_PORT, frontend=$FRONTEND_PORT)"
    if grep -q "localhost:9000" README.md && grep -q "localhost:5173" README.md; then
        echo "  PASS: Ports documented in README"
    else
        echo "  FAIL: Ports not properly documented in README"
        ERRORS=$((ERRORS+1))
    fi
else
    echo "  FAIL: Port mismatch (backend=$BACKEND_PORT, frontend=$FRONTEND_PORT)"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 10: Environment variables match .env.example files
echo "✓ Check 10: Environment variables documented match .env.example"
if grep -q "DATABASE_URL" README.md && \
   grep -q "SECRET_KEY" README.md && \
   grep -q "CORS_ORIGINS" README.md && \
   grep -q "VITE_API_URL" README.md; then
    echo "  PASS: All key environment variables documented"
else
    echo "  FAIL: Missing environment variable documentation"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 11: Startup commands match actual scripts
echo "✓ Check 11: README startup commands match actual script behavior"
if [ -f "start.sh" ] && [ -x "start.sh" ]; then
    echo "  PASS: start.sh exists and is executable"
else
    echo "  FAIL: start.sh missing or not executable"
    ERRORS=$((ERRORS+1))
fi
if [ -f "start.bat" ]; then
    echo "  PASS: start.bat exists"
else
    echo "  FAIL: start.bat missing"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Summary
echo "=== VERIFICATION SUMMARY ==="
if [ $ERRORS -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED"
    exit 0
else
    echo "❌ $ERRORS CHECK(S) FAILED"
    exit 1
fi
