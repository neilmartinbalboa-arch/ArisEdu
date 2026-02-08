import os
import re

ROOT_DIR = r"c:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder"

def fix_files():
    count = 0
    # Pattern to find the Play Button listener (multiline)
    # Allows for varying whitespace
    play_btn_pattern = re.compile(
        r"document\.getElementById\('play-button'\)\.addEventListener\('click',\s*\(\)\s*=>\s*\{[\s\S]*?\}\);", 
        re.MULTILINE
    )

    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    
                    # Remove Play Button Listener
                    if play_btn_pattern.search(content):
                        new_content = play_btn_pattern.sub("", new_content)
                    
                    # Also checking for single line version just in case
                    # new_content = new_content.replace("document.getElementById('play-button').addEventListener('click', () => {});", "")

                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed {file}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    fix_files()
