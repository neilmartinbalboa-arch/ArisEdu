import os
import re

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

# Rocket SVG
ROCKET_SVG = """<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));">
  <!-- Left Fin -->
  <path d="M18 42 L 8 58 L 22 58 L 24 48 Z" fill="#ef4444" stroke="#991b1b" stroke-width="1.5" stroke-linejoin="round"/>
  <!-- Right Fin -->
  <path d="M46 42 L 56 58 L 42 58 L 40 48 Z" fill="#ef4444" stroke="#991b1b" stroke-width="1.5" stroke-linejoin="round"/>
  <!-- Main Body -->
  <ellipse cx="32" cy="32" rx="14" ry="28" fill="#e2e8f0" stroke="#475569" stroke-width="2"/>
  <!-- Window -->
  <circle cx="32" cy="24" r="7" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
  <circle cx="33" cy="22" r="2.5" fill="white" opacity="0.6"/>
  <!-- Engine Flame -->
  <path d="M26 56 Q 32 72 38 56" fill="#f59e0b" stroke="#d97706" stroke-width="1"/>
  <path d="M29 56 Q 32 66 35 56" fill="#fef3c7"/>
</svg>"""

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # Regex to match the climb-player div and replace it entirely
        # We look for <div id="climb-player" ... > ... </div>
        # This covers the robot SVG we put in earlier.
        pattern = r'<div id="climb-player"[^>]*>.*?</div>'
        
        # New style (same as last time, ensures 80x80)
        new_style = 'position:absolute; bottom:35%; left:50%; transform:translateX(-50%); width:80px; height:80px; transition: bottom 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index: 5;'
        new_div = f'<div id="climb-player" style="{new_style}">{ROCKET_SVG}</div>'
        
        match = re.search(pattern, content, re.DOTALL)
        if match:
             # Check if it's already the Rocket (look for specific rocket color or path d)
             # The robot had fill="#60a5fa". The rocket has fill="#ef4444" (for fins) and fill="#e2e8f0" (body).
             # Let's just check if unique rocket part exists
             if 'rx="14" ry="28"' not in match.group(0): # Unique to ellipse in rocket
                 content = content.replace(match.group(0), new_div)
                 updated = True

        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated character in {os.path.basename(filepath)}")
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".html"):
                if update_file(os.path.join(root, file)):
                    count += 1
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    main()
