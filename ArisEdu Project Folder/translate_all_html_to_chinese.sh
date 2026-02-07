#!/bin/bash
# Translate all visible text in HTML files to Chinese if the setting is enabled
# This script assumes a translation function is available in JS and will inject a language check and translation logic into each HTML file.

LANG_SETTING="arisEduLanguage"
TRANSLATE_JS='
<script>
function translateToChinese() {
  if (localStorage.getItem("arisEduLanguage") === "chinese") {
    // Example: Replace common English phrases with Chinese
    document.body.innerHTML = document.body.innerHTML
      .replace(/Settings/g, "设置")
      .replace(/Appearance/g, "外观")
      .replace(/Account/g, "账户")
      .replace(/Notifications/g, "通知")
      .replace(/Search/g, "搜索")
      .replace(/Homepage/g, "首页")
      .replace(/Courses/g, "课程")
      .replace(/Play/g, "玩")
      .replace(/Preferences/g, "偏好设置")
      .replace(/Dark Mode/g, "深色模式")
      .replace(/Enable Dark Mode/g, "启用深色模式")
      .replace(/Language:/g, "语言:")
      .replace(/Color Theme:/g, "主题颜色:")
      .replace(/Email:/g, "邮箱:")
      .replace(/Password:/g, "密码:")
      .replace(/Notification Settings/g, "通知设置")
      .replace(/Email Notifications/g, "邮件通知")
      .replace(/Push Notifications/g, "推送通知");
  }
}
window.addEventListener("DOMContentLoaded", translateToChinese);
</script>
'

# List all HTML files in ArisEdu Project Folder
find "./ArisEdu Project Folder" -type f -name "*.html" | while read file; do
  # Only inject if not already present
  if ! grep -q "translateToChinese" "$file"; then
    # Insert translation JS before </body>
    sed -i "/<\/body>/i $TRANSLATE_JS" "$file"
  fi
done

echo "Chinese translation script injected into all HTML files."
