#!/bin/bash
# Fix links in HTML files from PhysicsUnitXLessonY to PhysicsLessonX.Y

find . -type f -name "*.html" | while read file; do
  sed -i -E 's/PhysicsUnit([0-9]+)Lesson([0-9]+)/PhysicsLesson\1.\2/g' "$file"
  echo "Updated links in: $file"
done
