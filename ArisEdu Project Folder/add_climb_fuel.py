import os
import re

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

# Fuel Bar HTML
FUEL_BAR_HTML = """                 <!-- Fuel Bar -->
                 <div id="climb-fuel-container" style="position:absolute; bottom:2rem; left:2rem; width:20px; height:200px; background:rgba(255,255,255,0.3); border:2px solid #334155; border-radius:10px; overflow:hidden; z-index:10; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div id="climb-fuel-fill" style="position:absolute; bottom:0; left:0; width:100%; height:50%; background:linear-gradient(to top, #f59e0b, #ef4444); transition: height 0.5s ease;"></div>
                    <div style="position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-weight:bold; font-size:0.8rem; color:#334155; white-space:nowrap;">FUEL</div>
                 </div>"""

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        updated = False

        # 1. Inject HTML
        # Insert inside the Game Area, before the Player
        # Search for: <!-- Player -->
        if 'id="climb-fuel-container"' not in content:
            marker = '<!-- Player -->'
            if marker in content:
                content = content.replace(marker, FUEL_BAR_HTML + '\n                 ' + marker)
                updated = True

        # 2. Add Logic
        # Need to init fuel variable and update logic
        
        # Init variable in JS
        if 'let climbFuel = 50;' not in content:
             vars_marker = 'let currentQuestion = null;'
             if vars_marker in content:
                 content = content.replace(vars_marker, vars_marker + '\n    let climbFuel = 50;')
                 # Note: updated is handled at write time, but let's track separately? 
                 # Actually content is being mutated, so if updated was True earlier, it's fine.
                 # If not, set it here.
                 if not updated: updated = True
        
        # Start Game: Reset Fuel
        if 'climbFuel = 50;' not in content: # Check if reset exists
            reset_marker = 'climbLevel = 1;'
            if reset_marker in content:
                 content = content.replace(reset_marker, reset_marker + '\n        climbFuel = 50;')
                 if not updated: updated = True
                 
        # Update Dispaly: Update Fuel UI
        if 'updateFuelDisplay();' not in content:
             display_marker = 'updatePlayerPos();' # Called in updateDisplay
             if display_marker in content:
                 content = content.replace(display_marker, display_marker + '\n        updateFuelDisplay();')
                 if not updated: updated = True
                 
        # Handle Answer: Increase Fuel
        if 'climbFuel = Math.min(100, climbFuel + 20);' not in content:
             # Look for correct answer logic
             if 'climbScore += 10;' in content:
                 content = content.replace('climbScore += 10;', 'climbScore += 10;\n            climbFuel = Math.min(100, climbFuel + 20);')
                 if not updated: updated = True

        # Add updateFuelDisplay function
        func_marker = 'function updatePlayerPos() {'
        if 'function updateFuelDisplay()' not in content and func_marker in content:
             new_func = """    function updateFuelDisplay() {
        const fill = document.getElementById('climb-fuel-fill');
        if(fill) fill.style.height = `${climbFuel}%`;
    }
    
    """
             content = content.replace(func_marker, new_func + func_marker)
             if not updated: updated = True

        # 3. Add Depletion Logic (Optional but requested "make it a fuel bar")
        # I'll enable a very slow burn to make it feel like "Fuel"
        # 0.1% per tick?
        
        if 'climbFuel -= 0.1;' not in content:
             game_loop_marker = 'playerPosition -= FALL_RATE * climbLevel;'
             if game_loop_marker in content:
                 content = content.replace(game_loop_marker, game_loop_marker + '\n        climbFuel = Math.max(0, climbFuel - 0.1);')
                 if not updated: updated = True

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
