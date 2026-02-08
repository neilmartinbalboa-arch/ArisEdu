import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # Regex to find the Practice Panel Items
        # We look for the Flashcard Game item and verify we haven't already added Climb
        
        flashcard_item_pattern = re.compile(
            r'(<div class="Practices-panel-item">\s*<a href="#flashcard-game">Flashcard Game</a>\s*</div>)',
            re.DOTALL
        )
        
        if '<a href="#climb">Climb</a>' not in content:
            # We want to insert the Climb option AFTER the Flashcard Game item.
            
            climb_option = """
              <div class="Practices-panel-item">
                <a href="#climb">Climb</a>
              </div>"""
              
            def replacer(match):
                return match.group(1) + climb_option

            new_content = flashcard_item_pattern.sub(replacer, content)
            
            if new_content != content:
                content = new_content
                changed = True
                print(f"Added 'Climb' option to {os.path.basename(file_path)}")
        
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
