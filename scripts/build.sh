#!/usr/bin/env bash
# this_file: scripts/build.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BLUE}🔨 Building vexy-mkdocs-strip-number-prefix${NC}"
echo "Project root: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo -e "${RED}❌ Not in a git repository${NC}"
    exit 1
fi

# Check if we have uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
    git status --short
fi

# Clean previous builds
echo -e "${BLUE}🧹 Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo -e "${BLUE}📦 Installing build dependencies...${NC}"
python3 -m pip install build twine --break-system-packages

# Build the package
echo -e "${BLUE}🏗️  Building package...${NC}"
python3 -m build

# Check the built package
echo -e "${BLUE}🔍 Checking built package...${NC}"
python3 -m twine check dist/*

# Show build artifacts
echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo "Build artifacts:"
ls -la dist/

# Extract version from the built wheel
WHEEL_FILE=$(find dist -name "*.whl" | head -1)
if [[ -n "$WHEEL_FILE" ]]; then
    VERSION=$(python3 -c "import re; print(re.search(r'-([\d\.]+.*?)-', '$WHEEL_FILE').group(1))")
    echo -e "${GREEN}📦 Package version: $VERSION${NC}"
fi

echo -e "${GREEN}🎉 Build completed successfully!${NC}"