import os

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        updated = False

        # 1. Add spacePressed variable
        if 'let isGameRunning = false;' in content and 'let spacePressed' not in content:
            content = content.replace('let isGameRunning = false;', 'let isGameRunning = false; let spacePressed = false;')
            updated = True

        # 2. Add Event Listeners
        # We hook into where existing vars are declared to ensure it's inside the scope
        if "if(e.code === 'Space') spacePressed = true;" not in content:
            # Safest anchor is `let currentQuestion = null;`
            anchor = 'let currentQuestion = null;'
            if anchor in content:
                listeners = """let currentQuestion = null;
    document.addEventListener('keydown', (e) => { if(e.code === 'Space') { spacePressed = true; if(isGameRunning) e.preventDefault(); } });
    document.addEventListener('keyup', (e) => { if(e.code === 'Space') spacePressed = false; });"""
                content = content.replace(anchor, listeners)
                updated = True

        # 3. Update gameLoop to include Boost Logic
        # Anchor: "if(!isGameRunning) return;"
        # We check if we already added the boost logic
        if 'if(spacePressed && climbFuel > 0)' not in content:
            loop_anchor = 'if(!isGameRunning) return;'
            boost_logic = """if(!isGameRunning) return;
        if(spacePressed && climbFuel > 0) {
            playerPosition += 0.5;
            climbFuel = Math.max(0, climbFuel - 0.2);
            if(typeof updateFuelDisplay === 'function') updateFuelDisplay();
            if(playerPosition >= WIN_HEIGHT) { endGame(true); return; }
        }"""
            if loop_anchor in content:
                content = content.replace(loop_anchor, boost_logic)
                updated = True

        # 4. Modify handleClimbAnswer (Remove automatic climb, update text)
        # 4a. Update Text
        if '"Correct! Climbing up..."' in content:
            content = content.replace('"Correct! Climbing up..."', '"Correct! Adding fuel..."')
            updated = True
        
        # 4b. Disable automatic climb
        # Look for: playerPosition += CLIMB_STEP;
        if 'playerPosition += CLIMB_STEP;' in content:
            content = content.replace('playerPosition += CLIMB_STEP;', '// playerPosition += CLIMB_STEP; // Disabled for manual boost')
            updated = True
            
        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated mechanics in {os.path.basename(filepath)}")
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
