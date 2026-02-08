import os

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        updated = False
        
        # 1. Update Player Start Position (affects both 'let' declaration and reset logic)
        # Changing from 10% to 35% from bottom
        if 'playerPosition = 10;' in content:
            content = content.replace('playerPosition = 10;', 'playerPosition = 35;')
            updated = True
            
        # 2. Update Fall Rate (Ladder Speed)
        # Changing from 0.05% per tick to 0.02% per tick (much slower)
        if 'const FALL_RATE = 0.05;' in content:
            content = content.replace('const FALL_RATE = 0.05;', 'const FALL_RATE = 0.02;')
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
