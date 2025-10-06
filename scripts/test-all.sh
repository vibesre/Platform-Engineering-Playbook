#!/bin/bash

# Comprehensive test script for Platform Engineering Playbook
# This script runs all validation checks before allowing commits

set -e  # Exit on first error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Track overall status
FAILED=0

echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║     Platform Engineering Playbook - Test Suite                ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -e "${BOLD}Running: ${test_name}${NC}"
    echo -e "${YELLOW}Command: ${test_command}${NC}"
    echo ""

    if eval "$test_command"; then
        echo -e "${GREEN}✓ ${test_name} passed${NC}"
        echo ""
        return 0
    else
        echo -e "${RED}✗ ${test_name} failed${NC}"
        echo ""
        FAILED=1
        return 1
    fi
}

# Test 1: Validate MDX/Markdown syntax
run_test "MDX/Markdown Validation" \
    "node scripts/validate-mdx.js"

# Test 2: TypeScript type checking
if [ -f "tsconfig.json" ]; then
    run_test "TypeScript Type Check" \
        "npm run typecheck"
else
    echo -e "${YELLOW}⚠ Skipping TypeScript check (no tsconfig.json)${NC}"
    echo ""
fi

# Test 3: Docusaurus build (production build to catch all issues)
run_test "Docusaurus Production Build" \
    "npm run build"

# Test 4: Check for large files (>1MB)
echo -e "${BOLD}Checking for large files...${NC}"
LARGE_FILES=$(find docs blog static -type f -size +1M 2>/dev/null || true)
if [ -n "$LARGE_FILES" ]; then
    echo -e "${YELLOW}⚠ Warning: Found large files (>1MB):${NC}"
    echo "$LARGE_FILES"
    echo ""
else
    echo -e "${GREEN}✓ No large files found${NC}"
    echo ""
fi

# Test 5: Check for TODO/FIXME in staged files (only in git repos)
if [ -d ".git" ]; then
    echo -e "${BOLD}Checking for TODO/FIXME in staged files...${NC}"
    STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(md|mdx|ts|tsx|js|jsx)$' || true)
    if [ -n "$STAGED_FILES" ]; then
        TODO_COUNT=$(echo "$STAGED_FILES" | xargs grep -n "TODO\|FIXME" 2>/dev/null | wc -l || echo 0)
        if [ "$TODO_COUNT" -gt 0 ]; then
            echo -e "${YELLOW}⚠ Warning: Found $TODO_COUNT TODO/FIXME comments in staged files${NC}"
            echo "$STAGED_FILES" | xargs grep -n "TODO\|FIXME" 2>/dev/null || true
            echo ""
        else
            echo -e "${GREEN}✓ No TODO/FIXME comments in staged files${NC}"
            echo ""
        fi
    else
        echo -e "${YELLOW}⚠ No staged files to check${NC}"
        echo ""
    fi
fi

# Test 6: Verify podcast metadata integrity (if podcasts exist)
if [ -d "docs/podcasts" ]; then
    echo -e "${BOLD}Checking podcast metadata integrity...${NC}"
    PODCAST_ERRORS=0

    # Check that each podcast script has corresponding metadata
    for script in docs/podcasts/scripts/*.txt; do
        if [ -f "$script" ]; then
            basename=$(basename "$script" .txt)
            # Remove episode number prefix if present (e.g., 00001-)
            metadata_name=$(echo "$basename" | sed 's/^[0-9]\{5\}-//')
            metadata_file="docs/podcasts/metadata/${metadata_name}.json"

            if [ ! -f "$metadata_file" ]; then
                echo -e "${RED}✗ Missing metadata for $script${NC}"
                PODCAST_ERRORS=$((PODCAST_ERRORS + 1))
            fi
        fi
    done

    if [ $PODCAST_ERRORS -eq 0 ]; then
        echo -e "${GREEN}✓ All podcast metadata files present${NC}"
        echo ""
    else
        echo -e "${RED}✗ Found $PODCAST_ERRORS podcast metadata issues${NC}"
        echo ""
        FAILED=1
    fi
fi

# Summary
echo -e "${CYAN}${BOLD}════════════════════════════════════════════════════════════════${NC}"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ All tests passed! Ready to commit.${NC}"
    echo -e "${CYAN}${BOLD}════════════════════════════════════════════════════════════════${NC}"
    exit 0
else
    echo -e "${RED}${BOLD}✗ Some tests failed. Please fix the issues before committing.${NC}"
    echo -e "${CYAN}${BOLD}════════════════════════════════════════════════════════════════${NC}"
    exit 1
fi
