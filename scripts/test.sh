#!/usr/bin/env bash
# this_file: scripts/test.sh

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

echo -e "${BLUE}🧪 Testing vexy-mkdocs-strip-number-prefix${NC}"
echo "Project root: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo -e "${RED}❌ Not in a git repository${NC}"
    exit 1
fi

# Install test dependencies
echo -e "${BLUE}📦 Installing test dependencies...${NC}"
python -m pip install --upgrade pip
pip install -e .[dev]

# Run code quality checks
echo -e "${BLUE}🔍 Running code quality checks...${NC}"

# Run ruff
echo -e "${BLUE}  → Running ruff...${NC}"
ruff check --output-format=github .

# Run black
echo -e "${BLUE}  → Running black...${NC}"
black --check --diff .

# Run mypy
echo -e "${BLUE}  → Running mypy...${NC}"
mypy src

# Run tests with coverage
echo -e "${BLUE}🧪 Running tests with coverage...${NC}"
pytest -v --cov=mkdocs_strip_number_prefix --cov-report=term-missing --cov-report=html --cov-report=xml

# Check coverage threshold
echo -e "${BLUE}📊 Checking coverage threshold...${NC}"
coverage report --fail-under=90

# Run pre-commit hooks if available
if command -v pre-commit &>/dev/null && [[ -f .pre-commit-config.yaml ]]; then
    echo -e "${BLUE}🔒 Running pre-commit hooks...${NC}"
    pre-commit run --all-files
fi

# Show test results summary
echo -e "${GREEN}✅ All tests passed!${NC}"
echo "Coverage report generated in htmlcov/index.html"

# Show any warnings
if [[ -f .coverage ]]; then
    echo -e "${BLUE}📈 Coverage summary:${NC}"
    coverage report --skip-covered
fi

echo -e "${GREEN}🎉 Testing completed successfully!${NC}"