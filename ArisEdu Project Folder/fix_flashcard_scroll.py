import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False

        # Regex to find the flashcard-game div and append overflow:hidden
        # It currently looks like: class="flashcard-game" style="...perspective:1000px;"
        
        def add_overflow(match):
            tag = match.group(0)
            if 'overflow:hidden' in tag or 'overflow: hidden' in tag:
                return tag
            
            # Append to style
            if 'style="' in tag:
                # We want to be careful not to break the style string
                # We can just replace the perspective part since we know it's there from previous step
                if 'perspective:1000px;' in tag:
                    return tag.replace('perspective:1000px;', 'perspective:1000px;overflow:hidden;')
                else:
                    # Fallback if previous script added it differently
                    return tag.replace('style="', 'style="overflow:hidden;')
            else:
                return tag

        # We target the specific div we modified before
        new_content = re.sub(r'<div class="flashcard-game"[^>]*>', add_overflow, content)
        
        if new_content != content:
            changed = True
            content = new_content
            print(f"Added overflow:hidden to {os.path.basename(file_path)}")

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    root_dir = "ChemistryLessons"
    for unit in os.listdir(root_dir):
        unit_path = os.path.join(root_dir, unit)
        if os.path.isdir(unit_path):
            files = os.listdir(unit_path)
            for file in files:
                if file.endswith(".html") and "Summary" not in file and "Practice" not in file:
                    process_file(os.path.join(unit_path, file))
    print("Optimization complete.")

if __name__ == "__main__":
    main()
