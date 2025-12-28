#!/bin/bash
# Script to update all pages with pink gradient theme

echo "Updating all pages with pink gradient theme..."

# Find and replace brown colors with pink in all TSX files
find app -name "*.tsx" -type f -exec sed -i 's/bg-\[#8B6F47\]/bg-gradient-to-r from-pink-600 to-pink-800/g' {} +
find app -name "*.tsx" -type f -exec sed -i 's/text-\[#8B6F47\]/text-pink-700/g' {} +
find app -name "*.tsx" -type f -exec sed -i 's/border-\[#8B6F47\]/border-pink-500/g' {} +
find app -name "*.tsx" -type f -exec sed -i 's/bg-\[#D4A574\]/bg-pink-400/g' {} +
find app -name "*.tsx" -type f -exec sed -i 's/border-\[#D4A574\]/border-pink-300/g' {} +
find app -name "*.tsx" -type f -exec sed -i 's/bg-\[#f5f1e8\]/bg-pink-50/g' {} +
find app -name "*.tsx" -type f -exec sed -i 's/hover:bg-\[#f5f1e8\]/hover:bg-pink-100/g' {} +
find app -name "*.tsx" -type f -exec sed -i 's/bg-white rounded/bg-gradient-to-r from-pink-50 to-pink-100 rounded/g' {} +
find app -name "*.tsx" -type f -exec sed -i 's/bg-gray-900/bg-gradient-to-r from-pink-600 via-pink-700 to-pink-800/g' {} +

echo "Done! All pages updated with pink gradient theme."
