#!/bin/bash
# Update lesson button text style in all PhysicsLesson*.html files

for file in ./ArisEdu\ Project\ Folder/PhysicsLessons/Unit*/PhysicsLesson*.html; do
  if [ -f "$file" ]; then
    # Remove existing .course-box a style and add the new style
    sed -i '/.course-box a {/,+5d' "$file"
    sed -i '/.course-box {/a \
.course-box a {\n  text-decoration: none;\n  color: #ffffff;\n  font-size: 1.125rem;\n  font-weight: 600;\n  display: block;\n}\n.course-box a:hover {\n  color: #ffffff;\n}\n' "$file"
    echo "Updated lesson button text style in: $file"
  fi
done
