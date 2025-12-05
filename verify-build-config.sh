#!/bin/bash

# Vercel Build Configuration Verification Script
# Run this before deploying to catch configuration issues early

echo "======================================================================"
echo "🔍 Vercel Build Configuration Verification"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Check 1: Repository structure
echo "📁 Checking repository structure..."
if [ -d "frontend" ]; then
    echo -e "${GREEN}✓${NC} frontend/ directory exists"
else
    echo -e "${RED}✗${NC} frontend/ directory NOT found"
    ERRORS=$((ERRORS + 1))
fi

if [ -d "api" ]; then
    echo -e "${GREEN}✓${NC} api/ directory exists"
else
    echo -e "${RED}✗${NC} api/ directory NOT found"
    ERRORS=$((ERRORS + 1))
fi

# Check 2: package.json files
echo ""
echo "📦 Checking package.json files..."
if [ -f "frontend/package.json" ]; then
    echo -e "${GREEN}✓${NC} frontend/package.json exists"
    
    # Check for vercel-build script
    if grep -q '"vercel-build"' frontend/package.json; then
        echo -e "${GREEN}✓${NC} frontend/package.json has vercel-build script"
    else
        echo -e "${YELLOW}⚠${NC} frontend/package.json missing vercel-build script (will use 'build')"
    fi
else
    echo -e "${RED}✗${NC} frontend/package.json NOT found"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "api/package.json" ]; then
    echo -e "${GREEN}✓${NC} api/package.json exists"
else
    echo -e "${RED}✗${NC} api/package.json NOT found"
    ERRORS=$((ERRORS + 1))
fi

# Check 3: vercel.json
echo ""
echo "⚙️  Checking vercel.json..."
if [ -f "vercel.json" ]; then
    echo -e "${GREEN}✓${NC} vercel.json exists"
    
    # Check if it contains correct paths or build commands
    if grep -q '"frontend/package.json"' vercel.json || grep -q '"frontend/build"' vercel.json || grep -q 'cd frontend' vercel.json; then
        echo -e "${GREEN}✓${NC} vercel.json has correct frontend configuration"
    else
        echo -e "${RED}✗${NC} vercel.json does not reference frontend correctly"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}✗${NC} vercel.json NOT found"
    ERRORS=$((ERRORS + 1))
fi

# Check 4: No /app/ paths
echo ""
echo "🚫 Checking for incorrect /app/ paths..."
if grep -r "cd app/" vercel.json 2>/dev/null; then
    echo -e "${RED}✗${NC} Found 'cd app/' in vercel.json - INCORRECT!"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} No 'cd app/' paths found"
fi

if grep -r "app/frontend" vercel.json 2>/dev/null; then
    echo -e "${RED}✗${NC} Found 'app/frontend' in vercel.json - INCORRECT!"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} No 'app/frontend' paths found"
fi

# Check 5: API function
echo ""
echo "🔌 Checking API function..."
if [ -f "api/appointment.js" ]; then
    echo -e "${GREEN}✓${NC} api/appointment.js exists"
else
    echo -e "${RED}✗${NC} api/appointment.js NOT found"
    ERRORS=$((ERRORS + 1))
fi

# Check 6: Required dependencies
echo ""
echo "📚 Checking dependencies..."
if [ -f "api/package.json" ]; then
    if grep -q "@supabase/supabase-js" api/package.json; then
        echo -e "${GREEN}✓${NC} Supabase dependency found"
    else
        echo -e "${RED}✗${NC} Supabase dependency NOT found in api/package.json"
        ERRORS=$((ERRORS + 1))
    fi
    
    if grep -q "resend" api/package.json; then
        echo -e "${GREEN}✓${NC} Resend dependency found"
    else
        echo -e "${RED}✗${NC} Resend dependency NOT found in api/package.json"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Check 7: .vercelignore
echo ""
echo "🚫 Checking .vercelignore..."
if [ -f ".vercelignore" ]; then
    echo -e "${GREEN}✓${NC} .vercelignore exists"
else
    echo -e "${YELLOW}⚠${NC} .vercelignore NOT found (optional but recommended)"
fi

# Check 8: Build can run
echo ""
echo "🔨 Testing if build can run..."
if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✓${NC} frontend/node_modules exists (dependencies installed)"
else
    echo -e "${YELLOW}⚠${NC} frontend/node_modules NOT found (run: cd frontend && yarn install)"
fi

# Summary
echo ""
echo "======================================================================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Configuration looks good.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Commit and push to GitHub"
    echo "  2. Connect repository to Vercel"
    echo "  3. Add environment variables in Vercel dashboard"
    echo "  4. Deploy!"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS error(s). Fix them before deploying.${NC}"
    echo ""
    echo "See VERCEL_BUILD_CONFIGURATION.md for detailed instructions."
    exit 1
fi
