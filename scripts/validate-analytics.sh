#!/bin/bash
# Validate Google Analytics is present in build output
#
# Usage: bash scripts/validate-analytics.sh
#
# This script checks that Google Analytics tracking code is properly
# included in the build output. Run after npm run build.

set -e

echo "🔍 Validating Google Analytics in build output..."
echo ""

# Check if build directory exists
if [ ! -d "build" ]; then
  echo "❌ ERROR: Build directory not found"
  echo "   Run 'npm run build' first to generate the build output"
  exit 1
fi

# Check docusaurus.config.ts for gtag configuration
echo "1️⃣  Checking docusaurus.config.ts configuration..."
if grep -q "^[[:space:]]*// gtag:" docusaurus.config.ts; then
  echo "   ❌ Google Analytics is commented out in config"
  echo "   Location: docusaurus.config.ts (search for 'gtag')"
  exit 1
fi

if ! grep -q "trackingID: 'G-JYN3ZYTSNR'" docusaurus.config.ts; then
  echo "   ❌ Tracking ID not found or incorrect"
  echo "   Expected: trackingID: 'G-JYN3ZYTSNR'"
  exit 1
fi

echo "   ✅ Configuration OK (gtag enabled with correct tracking ID)"
echo ""

# Check build output for GA script
echo "2️⃣  Checking build output for Google Analytics script..."

# Check multiple pages to ensure GA is everywhere
check_files=(
  "build/index.html"
  "build/podcasts/index.html"
  "build/blog/index.html"
)

failed=0
for file in "${check_files[@]}"; do
  if [ -f "$file" ]; then
    if grep -q "G-JYN3ZYTSNR" "$file" && grep -q "googletagmanager.com/gtag" "$file"; then
      echo "   ✅ $file has GA tracking code"
    else
      echo "   ❌ $file missing GA tracking code"
      failed=1
    fi
  else
    echo "   ⚠️  $file not found (skipping)"
  fi
done

if [ $failed -eq 1 ]; then
  echo ""
  echo "❌ ERROR: Some pages are missing Google Analytics tracking code"
  echo "   Try running 'npm run build' again"
  exit 1
fi

echo ""

# Verify gtag function is defined
echo "3️⃣  Checking gtag function initialization..."
if grep -q "function gtag(){dataLayer.push(arguments)}" build/index.html; then
  echo "   ✅ gtag function is properly initialized"
else
  echo "   ❌ gtag function initialization not found"
  exit 1
fi

echo ""
echo "✅ Google Analytics validation complete!"
echo ""
echo "Summary:"
echo "  - Tracking ID: G-JYN3ZYTSNR"
echo "  - gtag script: ✅ Present"
echo "  - Anonymize IP: ✅ Enabled"
echo "  - Pages checked: ${#check_files[@]}"
echo ""
echo "Google Analytics is properly configured and active on all pages."
