#!/usr/bin/env bash
# this_file: scripts/release.sh

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
    echo "Usage: $0 [OPTIONS] <version>"
    echo ""
    echo "Create a new release with git tag-based versioning"
    echo ""
    echo "Arguments:"
    echo "  version     Version to release (e.g., 1.0.0, 1.0.1, 2.0.0)"
    echo ""
    echo "Options:"
    echo "  -h, --help  Show this help message"
    echo "  -d, --dry-run  Perform a dry run without making changes"
    echo "  -p, --publish  Publish to PyPI after creating release"
    echo ""
    echo "Examples:"
    echo "  $0 1.0.0                    # Create v1.0.0 release"
    echo "  $0 --dry-run 1.0.1         # Dry run for v1.0.1"
    echo "  $0 --publish 1.0.0         # Create and publish v1.0.0"
}

# Parse command line arguments
DRY_RUN=false
PUBLISH=false
VERSION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -p|--publish)
            PUBLISH=true
            shift
            ;;
        -*)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            usage
            exit 1
            ;;
        *)
            if [[ -z "$VERSION" ]]; then
                VERSION="$1"
            else
                echo -e "${RED}❌ Too many arguments${NC}"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate version argument
if [[ -z "$VERSION" ]]; then
    echo -e "${RED}❌ Version argument is required${NC}"
    usage
    exit 1
fi

# Validate version format (semantic versioning)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
    echo -e "${RED}❌ Invalid version format: $VERSION${NC}"
    echo "Version must follow semantic versioning (e.g., 1.0.0, 1.0.1-alpha)"
    exit 1
fi

echo -e "${BLUE}🚀 Creating release for vexy-mkdocs-strip-number-prefix${NC}"
echo "Version: $VERSION"
echo "Dry run: $DRY_RUN"
echo "Publish: $PUBLISH"
echo "Project root: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo -e "${RED}❌ Not in a git repository${NC}"
    exit 1
fi

# Check if we're on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo -e "${YELLOW}⚠️  Warning: Not on main branch (current: $CURRENT_BRANCH)${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if we have uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${RED}❌ You have uncommitted changes${NC}"
    git status --short
    exit 1
fi

# Check if tag already exists
TAG_NAME="v$VERSION"
if git tag -l | grep -q "^$TAG_NAME$"; then
    echo -e "${RED}❌ Tag $TAG_NAME already exists${NC}"
    exit 1
fi

# Pull latest changes
echo -e "${BLUE}📥 Pulling latest changes...${NC}"
if [[ "$DRY_RUN" == false ]]; then
    git pull origin "$CURRENT_BRANCH"
fi

# Run tests
echo -e "${BLUE}🧪 Running tests...${NC}"
if ! "$SCRIPT_DIR/test.sh"; then
    echo -e "${RED}❌ Tests failed${NC}"
    exit 1
fi

# Build package
echo -e "${BLUE}🔨 Building package...${NC}"
if ! "$SCRIPT_DIR/build.sh"; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

# Update CHANGELOG.md
echo -e "${BLUE}📝 Updating CHANGELOG.md...${NC}"
if [[ -f "CHANGELOG.md" ]]; then
    if [[ "$DRY_RUN" == false ]]; then
        # Move [Unreleased] section to new version
        sed -i "s/## \[Unreleased\]/## [$VERSION] - $(date +%Y-%m-%d)/" CHANGELOG.md
        # Add new [Unreleased] section
        sed -i "/## \[$VERSION\]/i\\## [Unreleased]\\n" CHANGELOG.md
        echo -e "${GREEN}✅ CHANGELOG.md updated${NC}"
    else
        echo -e "${YELLOW}🔍 Would update CHANGELOG.md${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  CHANGELOG.md not found${NC}"
fi

# Create git tag
echo -e "${BLUE}🏷️  Creating git tag...${NC}"
if [[ "$DRY_RUN" == false ]]; then
    git add .
    git commit -m "Release $VERSION

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    git tag -a "$TAG_NAME" -m "Release $VERSION"
    echo -e "${GREEN}✅ Created tag $TAG_NAME${NC}"
else
    echo -e "${YELLOW}🔍 Would create tag $TAG_NAME${NC}"
fi

# Push to remote
echo -e "${BLUE}📤 Pushing to remote...${NC}"
if [[ "$DRY_RUN" == false ]]; then
    git push origin "$CURRENT_BRANCH"
    git push origin "$TAG_NAME"
    echo -e "${GREEN}✅ Pushed to remote${NC}"
else
    echo -e "${YELLOW}🔍 Would push to remote${NC}"
fi

# Publish to PyPI if requested
if [[ "$PUBLISH" == true ]]; then
    echo -e "${BLUE}📦 Publishing to PyPI...${NC}"
    if [[ "$DRY_RUN" == false ]]; then
        python -m twine upload dist/*
        echo -e "${GREEN}✅ Published to PyPI${NC}"
    else
        echo -e "${YELLOW}🔍 Would publish to PyPI${NC}"
    fi
fi

echo -e "${GREEN}🎉 Release $VERSION completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "  1. Check GitHub Actions for automated release"
echo "  2. Verify package on PyPI: https://pypi.org/project/vexy-mkdocs-strip-number-prefix/"
echo "  3. Update documentation if needed"
echo "  4. Announce release to users"