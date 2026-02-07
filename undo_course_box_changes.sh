#!/bin/bash
# Undo course-box and selector changes in all PhysicsLesson*.html files

find './ArisEdu Project Folder/PhysicsLessons/' -type f -name 'PhysicsLesson*.html' | while read file; do
  # Remove course-box structure and restore original lesson layout if present
  # Replace <a href="#"><div class="course-box">Lesson ...</div></a> with nothing (or original content if known)
  perl -pi -e 's#<a href="#"><div class="course-box">Lesson [0-9]+[^<]*</div></a>##g' "$file"
  # Remove injected course-box CSS if present
  perl -pi -e 's#<style>.*course-box.*?</style>##gs' "$file"
  echo "Checked and reverted course-box changes in: $file"
done
