#!/bin/bash
# Advanced injection: Add a robust translation JS snippet to all HTML files in ArisEdu Project Folder
TRANSLATE_JS='<script>\n(function(){\n  const translations = {\n    "Settings": "设置", "Appearance": "外观", "Account": "账户", "Notifications": "通知", "Search": "搜索", "Homepage": "首页", "Courses": "课程", "Play": "玩", "Preferences": "偏好设置", "Dark Mode": "深色模式", "Enable Dark Mode": "启用深色模式", "Language:": "语言:", "Color Theme:": "主题颜色:", "Email:": "邮箱:", "Password:": "密码:", "Notification Settings": "通知设置", "Email Notifications": "邮件通知", "Push Notifications": "推送通知"\n  };\n  function translateNode(node) {\n    if (node.nodeType === 3) {\n      let text = node.nodeValue;\n      Object.keys(translations).forEach(function(en) {\n        text = text.replace(new RegExp(en, "g"), translations[en]);\n      });\n      node.nodeValue = text;\n    } else if (node.nodeType === 1 && node.childNodes.length) {\n      for (let i = 0; i < node.childNodes.length; i++) {\n        translateNode(node.childNodes[i]);\n      }\n    }\n  }\n  function translateAll() {\n    if (localStorage.getItem("arisEduLanguage") === "chinese") {\n      translateNode(document.body);\n    }\n  }\n  window.addEventListener("DOMContentLoaded", translateAll);\n})();\n</script>'

find "./ArisEdu Project Folder" -type f -name "*.html" | while read file; do
  if ! grep -q "translateNode" "$file"; then
    # Insert before </body> using awk for multiline safety
    awk -v js="$TRANSLATE_JS" '/<\/body>/ {print js; print $0; next} {print}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
  fi
done

echo "Advanced Chinese translation script injected into all HTML files."