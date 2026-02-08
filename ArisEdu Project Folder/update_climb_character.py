import os
import re

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

# New SVG player character (Robot)
PLAYER_SVG = """<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; drop-shadow(0 4px 6px rgba(0,0,0,0.3));">
  <rect x="16" y="14" width="32" height="26" rx="6" fill="#60a5fa" stroke="#2563eb" stroke-width="2"/>
  <rect x="22" y="22" width="6" height="6" rx="2" fill="white"/>
  <rect x="36" y="22" width="6" height="6" rx="2" fill="white"/>
  <path d="M 26 32 Q 32 36 38 32" stroke="#1e40af" stroke-width="2" fill="none"/>
  <rect x="12" y="25" width="4" height="10" rx="2" fill="#2563eb"/>
  <rect x="48" y="25" width="4" height="10" rx="2" fill="#2563eb"/>
  <rect x="24" y="40" width="16" height="12" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
  <line x1="32" y1="14" x2="32" y2="8" stroke="#475569" stroke-width="2"/>
  <circle cx="32" cy="6" r="3" fill="#ef4444"/>
</svg>"""

# New style for container: remove font-size, add width/height
# Current: style="position:absolute; bottom:35%; left:50%; transform:translateX(-50%); font-size:4rem; ..."
# New: style="position:absolute; bottom:35%; left:50%; transform:translateX(-50%); width:64px; height:64px; ..."

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # We need to replace the climb-player div AND its content
        # Pattern match specifically the id="climb-player" ... >...</div>
        
        # Regex to capture the style attribute content to preserve transition/z-index/filter if needed, 
        # or just hardcode the new style since we know what it is.
        # The previous script changed bottom:10% to bottom:35%.
        # So we should look for bottom:35%.
        
        # Let's perform a smart replace.
        # Find: <div id="climb-player" ... >🧗</div>
        # Replace with: <div id="climb-player" style="..." >PLAYER_SVG</div>
        
        # Construct regex
        # Note: the style string might vary slightly if previous scripts modified it differently, 
        # so allow for variations in style string.
        pattern = r'<div id="climb-player"[^>]*>.*?</div>'
        
        # New style string
        new_style = 'position:absolute; bottom:35%; left:50%; transform:translateX(-50%); width:80px; height:80px; transition: bottom 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index: 5;'
        new_div = f'<div id="climb-player" style="{new_style}">{PLAYER_SVG}</div>'
        
        match = re.search(pattern, content)
        if match:
             # Check if it's already the SVG (don't overwrite if it is)
             if '<svg' not in match.group(0):
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
