import os

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        updated = False

        # Target string
        target = 'playerPosition -= FALL_RATE * climbLevel;'
        
        # New logic
        # We use a compact generic replacement to avoid messing up indentation too much, 
        # though we should try to match indentation.
        # The surrounding code usually has 8 spaces indentation.
        
        new_logic = """let effectiveFall = FALL_RATE * climbLevel;
        if (climbFuel <= 0) effectiveFall *= 2;
        playerPosition -= effectiveFall;"""

        if target in content:
            # Check if we already did this (look for effectiveFall)
            if 'effectiveFall' not in content:
                content = content.replace(target, new_logic)
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
