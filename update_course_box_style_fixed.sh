#!/bin/bash
# Fixed script to update lesson selector buttons to match PhysicsUnit1.html course-box style

COURSE_BOX_CSS='<style>\n.course-box {\n  background: linear-gradient(#3b82f6 0%, #10b981 50%, #8b5cf6 100%);\n  border-radius: 0.75rem;\n  padding: 1.5rem;\n  text-align: center;\n  transition: all 0.3s ease;\n  cursor: pointer;\n  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);\n  color: #ffffff;\n}\n.course-box:hover {\n  transform: translateY(-4px);\n  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);\n  background: linear-gradient(#3b82f6 0%, #10b981 50%, #8b5cf6 100%);\n  filter: brightness(1.05);\n}\n.course-box a {\n  text-decoration: none;\n  color: #ffffff;\n  font-size: 1.125rem;\n  font-weight: 600;\n  display: block;\n}\n.course-box a:hover {\n  color: #ffffff;\n}\nbody.dark-mode .course-box {\n  background: linear-gradient(135deg, #3b82f6 0%, #10b981 50%, #8b5cf6 100%);\n  color: #e2e8f0;\n  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.45);\n}\nbody.dark-mode .course-box a {\n  color: #e2e8f0;\n}\nbody.dark-mode .course-box a:hover {\n  color: #38bdf8;\n}\n</style>'

find './ArisEdu Project Folder/PhysicsLessons/' -type f -name 'PhysicsLesson*.html' | while read file; do
  # Replace lesson selector divs/buttons with course-box structure
  perl -pi -e 's#<button[^>]*>(Lesson [0-9]+[^<]*)</button>#<a href="#"><div class="course-box">$1</div></a>#g' "$file"
  perl -pi -e 's#<div[^>]*class="lesson-selector"[^>]*>(Lesson [0-9]+[^<]*)</div>#<a href="#"><div class="course-box">$1</div></a>#g' "$file"
  # Inject CSS if not present
  grep -q 'course-box' "$file" || sed -i "1s#^#$COURSE_BOX_CSS\n#" "$file"
  echo "Updated course-box style in: $file"
done
