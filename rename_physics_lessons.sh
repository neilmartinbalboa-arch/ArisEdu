#!/bin/bash
# Rename PhysicsUnitXLessonY* to PhysicsLessonX.Y*

for unit in {1..11}; do
  find . -type f -name "PhysicsUnit${unit}Lesson*.*" | while read file; do
    lesson=$(echo "$file" | sed -E "s/.*PhysicsUnit${unit}Lesson([0-9]+).*/\1/")
    newfile=$(echo "$file" | sed -E "s/PhysicsUnit${unit}Lesson${lesson}/PhysicsLesson${unit}.${lesson}/")
    mv "$file" "$newfile"
    echo "Renamed: $file -> $newfile"
  done
done
