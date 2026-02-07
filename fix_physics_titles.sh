#!/bin/bash
# Update lesson titles from "Unit X Lesson Y" to "Lesson X.Y"

find . -type f -name "*.html" | while read file; do
  sed -i -E 's/Unit ([0-9]+) Lesson ([0-9]+)/Lesson \1.\2/g' "$file"
  echo "Updated lesson titles in: $file"
done
