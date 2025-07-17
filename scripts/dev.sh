#!/usr/bin/env bash
# this_file: scripts/dev.sh

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

# Usage function
usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Development helper script for vexy-mkdocs-strip-number-prefix"
    echo ""
    echo "Commands:"
    echo "  setup       Set up development environment"
    echo "  format      Format code with ruff and black"
    echo "  lint        Run linting checks"
    echo "  test        Run tests"
    echo "  docs        Build documentation"
    echo "  clean       Clean build artifacts"
    echo "  install     Install package in development mode"
    echo "  coverage    Generate coverage report"
    echo "  pre-commit  Set up pre-commit hooks"
    echo ""
    echo "Examples:"
    echo "  $0 setup       # Set up development environment"
    echo "  $0 format      # Format code"
    echo "  $0 test        # Run tests"
}

# Parse command line arguments
COMMAND=""

if [[ $# -eq 0 ]]; then
    usage
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        setup|format|lint|test|docs|clean|install|coverage|pre-commit)
            COMMAND="$1"
            shift
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $1${NC}"
            usage
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🛠️  vexy-mkdocs-strip-number-prefix dev tools${NC}"
echo "Command: $COMMAND"
echo "Project root: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

case $COMMAND in
    setup)
        echo -e "${BLUE}🔧 Setting up development environment...${NC}"
        python -m pip install --upgrade pip
        pip install -e .[dev]
        pip install -e .[docs]
        echo -e "${GREEN}✅ Development environment set up${NC}"
        ;;
    
    format)
        echo -e "${BLUE}🎨 Formatting code...${NC}"
        echo -e "${BLUE}  → Running autoflake...${NC}"
        find . -name "*.py" -exec autoflake --in-place --remove-all-unused-imports {} \;
        echo -e "${BLUE}  → Running pyupgrade...${NC}"
        find . -name "*.py" -exec pyupgrade --py39-plus {} \;
        echo -e "${BLUE}  → Running ruff...${NC}"
        ruff check --fix --unsafe-fixes .
        echo -e "${BLUE}  → Running black...${NC}"
        black .
        echo -e "${GREEN}✅ Code formatted${NC}"
        ;;
    
    lint)
        echo -e "${BLUE}🔍 Running linting checks...${NC}"
        echo -e "${BLUE}  → Running ruff...${NC}"
        ruff check --output-format=github .
        echo -e "${BLUE}  → Running black...${NC}"
        black --check --diff .
        echo -e "${BLUE}  → Running mypy...${NC}"
        mypy src
        echo -e "${GREEN}✅ Linting passed${NC}"
        ;;
    
    test)
        echo -e "${BLUE}🧪 Running tests...${NC}"
        pytest -v --cov=mkdocs_strip_number_prefix --cov-report=term-missing
        echo -e "${GREEN}✅ Tests passed${NC}"
        ;;
    
    docs)
        echo -e "${BLUE}📚 Building documentation...${NC}"
        if [[ -f "build_docs.py" ]]; then
            python build_docs.py
        elif [[ -f "mkdocs.yml" ]]; then
            mkdocs build
        else
            echo -e "${YELLOW}⚠️  No documentation build script found${NC}"
        fi
        echo -e "${GREEN}✅ Documentation built${NC}"
        ;;
    
    clean)
        echo -e "${BLUE}🧹 Cleaning build artifacts...${NC}"
        rm -rf build/ dist/ *.egg-info/
        rm -rf .coverage htmlcov/ .pytest_cache/
        rm -rf .mypy_cache/ .ruff_cache/
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        echo -e "${GREEN}✅ Build artifacts cleaned${NC}"
        ;;
    
    install)
        echo -e "${BLUE}📦 Installing package in development mode...${NC}"
        pip install -e .[dev]
        echo -e "${GREEN}✅ Package installed in development mode${NC}"
        ;;
    
    coverage)
        echo -e "${BLUE}📊 Generating coverage report...${NC}"
        pytest --cov=mkdocs_strip_number_prefix --cov-report=html --cov-report=term-missing
        echo -e "${GREEN}✅ Coverage report generated in htmlcov/index.html${NC}"
        ;;
    
    pre-commit)
        echo -e "${BLUE}🔒 Setting up pre-commit hooks...${NC}"
        if command -v pre-commit &>/dev/null; then
            pre-commit install
            echo -e "${GREEN}✅ Pre-commit hooks installed${NC}"
        else
            echo -e "${YELLOW}⚠️  pre-commit not found, installing...${NC}"
            pip install pre-commit
            pre-commit install
            echo -e "${GREEN}✅ Pre-commit installed and hooks set up${NC}"
        fi
        ;;
    
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        usage
        exit 1
        ;;
esac

echo -e "${GREEN}🎉 Command completed successfully!${NC}"