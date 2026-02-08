import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False

        # 1. Inject Climb Game Container
        # We look for <div class="Practice-actions" and insert before it.
        # But we need to make sure we are inside #practice-content-view's diagram-card?
        # Typically "Practice-actions" is unique enough in these files.
        
        if 'id="climb-game-container"' not in content:
            climb_html = """
        <div id="climb-game-container" style="display:none; width:100%; text-align:center; padding: 2rem;">
            <h3>Climb Game</h3>
            <p>Welcome to the Climb! (Game content coming soon)</p>
            <div style="font-size: 3rem; margin: 2rem;">🧗</div>
        </div>
"""
            # Find the actions div
            pattern = re.compile(r'(<div class="Practice-actions")', re.IGNORECASE)
            search = pattern.search(content)
            if search:
                # Insert before
                content = content[:search.start()] + climb_html + content[search.start():]
                changed = True
                print(f"Injected Climb container into {os.path.basename(file_path)}")

        # 2. Inject JS Logic
        # We need a script that handles the switching.
        # We check if we already injected it.
        js_signature = "window.switchToClimb = function()"
        
        js_code = """
<script>
  window.switchToClimb = function() {
    const flashcardGame = document.querySelector('.flashcard-game');
    const climbGame = document.getElementById('climb-game-container');
    if(flashcardGame) flashcardGame.style.display = 'none';
    if(climbGame) climbGame.style.display = 'block';
  };

  window.switchToFlashcards = function() {
    const flashcardGame = document.querySelector('.flashcard-game');
    const climbGame = document.getElementById('climb-game-container');
    if(flashcardGame) flashcardGame.style.display = 'flex';
    if(climbGame) climbGame.style.display = 'none';
  };

  document.addEventListener('DOMContentLoaded', () => {
    // Attach listeners to practice menu items
    
    // Climb Link
    document.querySelectorAll('a[href="#climb"]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        window.switchToClimb();
        // Close menu if possible
        if (window.togglePracticesPanel && el.closest('.Practices-menu')) {
             const btn = el.closest('.Practices-menu').querySelector('.view-other-Practices');
             if(btn) window.togglePracticesPanel(btn);
        }
      });
    });

    // Flashcard Link
    document.querySelectorAll('a[href="#flashcard-game"]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        window.switchToFlashcards();
        // Close menu if possible
         if (window.togglePracticesPanel && el.closest('.Practices-menu')) {
             const btn = el.closest('.Practices-menu').querySelector('.view-other-Practices');
             if(btn) window.togglePracticesPanel(btn);
        }
      });
    });
  });
</script>
"""
        if js_signature not in content:
            # Append before closing body
            body_end = content.rfind("</body>")
            if body_end != -1:
                content = content[:body_end] + js_code + content[body_end:]
                changed = True
                print(f"Injected Climb JS into {os.path.basename(file_path)}")

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
    print("Climb Game implementation complete.")

if __name__ == "__main__":
    main()
