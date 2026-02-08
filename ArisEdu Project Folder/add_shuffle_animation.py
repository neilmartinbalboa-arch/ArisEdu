import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # Pattern for existing shuffle logic
        # It handles variable whitespace
        old_pattern = re.compile(
            r"shuffleFlashcardBtn\.addEventListener\('click', \(\) => \{\s+"
            r"function shuffleArray\(array\) \{.+?\}"
            r"\s+flashcardOrder = shuffleArray\(flashcardOrder\);\s+"
            r"currentFlashcard = 0;\s+"
            r"updateFlashcard\(\);\s+"
            r"\}\);",
            re.DOTALL
        )

        new_code = """
        shuffleFlashcardBtn.addEventListener('click', () => {
          if (isFlipping) return;
          isFlipping = true;

          // 1. Shuffle Data
          function shuffleArray(array) {
            let arr = array.slice();
            for (let i = arr.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
            return arr;
          }
          flashcardOrder = shuffleArray(flashcardOrder);
          currentFlashcard = 0;

          // 2. Visual Scramble Animation
          const container = flashcardDiv.parentElement;
          if (getComputedStyle(container).position === 'static') {
              container.style.position = 'relative';
          }

          // Create clones to simulate a deck being mixed
          const numClones = 3;
          const clones = [];

          flashcardDiv.style.transition = 'all 0.3s ease';
          flashcardDiv.style.zIndex = '10';

          for (let i = 0; i < numClones; i++) {
              const clone = flashcardDiv.cloneNode(true);
              clone.removeAttribute('id');
              clone.style.position = 'absolute';
              clone.style.left = flashcardDiv.offsetLeft + 'px';
              clone.style.top = flashcardDiv.offsetTop + 'px';
              clone.style.width = flashcardDiv.offsetWidth + 'px';
              clone.style.height = flashcardDiv.offsetHeight + 'px';
              clone.style.zIndex = '5';
              clone.style.transition = 'all 0.3s ease';
              clone.style.opacity = '1';
              
              // Remove duplicate IDs from children
              clone.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
              
              container.appendChild(clone);
              clones.push(clone);
          }

          // Trigger Scatter
          requestAnimationFrame(() => {
              // Shake main card
              flashcardDiv.style.transform = `translate(${Math.random()*30-15}px, ${Math.random()*30-15}px) rotate(${Math.random()*10-5}deg)`;

              // Scatter clones randomly
              clones.forEach((clone) => {
                  const x = (Math.random() * 120 - 60);
                  const y = (Math.random() * 80 - 40);
                  const rot = (Math.random() * 40 - 20);
                  clone.style.transform = `translate(${x}px, ${y}px) rotate(${rot}deg) scale(0.95)`;
                  clone.style.opacity = '0.8';
                  clone.style.boxShadow = '0 10px 20px rgba(0,0,0,0.2)';
              });
          });

          // Converge and Cleanup
          setTimeout(() => {
             updateFlashcard();

             flashcardDiv.style.transform = 'translate(0,0) rotate(0deg)';
             clones.forEach(clone => {
                 clone.style.transform = 'translate(0,0) rotate(0) scale(1)';
                 clone.style.opacity = '0';
             });

             setTimeout(() => {
                 clones.forEach(c => c.remove());
                 flashcardDiv.style.zIndex = '';
                 isFlipping = false;
             }, 300);
          }, 300);
        });"""

        if old_pattern.search(content):
            content = old_pattern.sub(new_code.strip(), content)
            changed = True
            print(f"Added shuffle animation to {os.path.basename(file_path)}")

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
    print("Shuffle animation update complete.")

if __name__ == "__main__":
    main()
