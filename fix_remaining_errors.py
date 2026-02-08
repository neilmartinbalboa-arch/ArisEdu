import os
import re

ROOT_DIR = r"c:\Users\Peter\ArisEdu-1\ArisEdu"

def fix_remaining_files():
    count_listener = 0
    count_textcontent = 0
    
    # Pattern to find the Play Button listener (multiline)
    play_btn_pattern = re.compile(
        r"document\.getElementById\('play-button'\)\.addEventListener\('click',\s*\(\)\s*=>\s*\{[\s\S]*?\}\);", 
        re.MULTILINE
    )

    # Pattern for textContent assignment
    # Matches: document.getElementById('play-button').textContent = labels.play;
    # allowing for some whitespace variation
    text_content_pattern = re.compile(
        r"document\.getElementById\('play-button'\)\.textContent\s*=\s*labels\.play;?"
    )

    for root, dirs, files in os.walk(ROOT_DIR):
        # exclusions (folders)
        if ".git" in dirs:
            dirs.remove(".git")
        if ".venv" in dirs:
            dirs.remove(".venv")
        if ".vscode" in dirs:
            dirs.remove(".vscode")

        for file in files:
            # check extension OR specific filename 'vidRubric'
            if file.endswith(".html") or file == "vidRubric":
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    
                    # 1. Remove Play Button Listener
                    if play_btn_pattern.search(new_content):
                        new_content = play_btn_pattern.sub("", new_content)
                        # clean up empty lines left behind if desired, but not strictly necessary for functionality
                        count_listener += 1
                    
                    # 2. Remove textContent assignment
                    if text_content_pattern.search(new_content):
                        new_content = text_content_pattern.sub("", new_content)
                        count_textcontent += 1

                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed {file}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Fixed Listener in {count_listener} files")
    print(f"Fixed textContent in {count_textcontent} files")

if __name__ == "__main__":
    fix_remaining_files()
