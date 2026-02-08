import os
import re

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Target the climb-game-ui div line specifically
        # Pattern looks for id="climb-game-ui" ... min-height: 500px;
        # We replace the min-height part.
        
        # It's safer to read line by line or use a precise regex if the file is huge, 
        # but read() is fine for these file sizes.
        
        # We look for the specific style attribute part
        if 'id="climb-game-ui"' in content and 'height: 80rem;' in content:
            new_content = content.replace('height: 80rem;', 'height: 64rem;')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated height in {os.path.basename(filepath)}")
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
