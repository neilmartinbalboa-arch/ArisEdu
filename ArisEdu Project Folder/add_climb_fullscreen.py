import os
import re

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

BUTTON_HTML = """            <button id="climb-fullscreen-btn" onclick="toggleClimbFullscreen()" style="position:absolute; bottom:1rem; right:1rem; z-index:50; background:rgba(255,255,255,0.9); border:none; border-radius:50%; width:3rem; height:3rem; cursor:pointer; box-shadow:0 4px 6px rgba(0,0,0,0.1); display:flex; align-items:center; justify-content:center; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'" title="Toggle Fullscreen">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2-2h3"/></svg>
            </button>
"""

JS_CODE = """
    window.toggleClimbFullscreen = function() {
        const elem = document.getElementById('climb-game-ui');
        if (!document.fullscreenElement) {
            if (elem.requestFullscreen) {
                elem.requestFullscreen().catch(err => {
                    console.error(`Error attempting to enable fullscreen: ${err.message}`);
                });
            } else if (elem.webkitRequestFullscreen) { /* Safari */
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) { /* IE11 */
                elem.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) { /* Safari */
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) { /* IE11 */
                document.msExitFullscreen();
            }
        }
    };
"""

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # 1. Inject Button
        if 'id="climb-game-ui"' in content and 'id="climb-fullscreen-btn"' not in content:
            # We look for the background comment to insert before
            marker = '<!-- Moving Background (The Ladder) -->'
            if marker in content:
                content = content.replace(marker, BUTTON_HTML + marker)
                updated = True
        
        # 2. Inject JS
        if 'window.toggleClimbFullscreen' not in content:
            marker = 'window.exitClimbGame = function() {'
            if marker in content:
                content = content.replace(marker, JS_CODE + marker)
                updated = True
                
        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {os.path.basename(filepath)}")
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
