import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # Pattern matches the existing nextFlashcardBtn click handler
        old_code_pattern = re.compile(
            r"nextFlashcardBtn\.addEventListener\('click', \(\) => \{\s+"
            r"currentFlashcard = \(currentFlashcard \+ 1\) % flashcardOrder\.length;\s+"
            r"updateFlashcard\(\);\s+"
            r"\}\);",
            re.DOTALL
        )

        new_code = """
        nextFlashcardBtn.addEventListener('click', () => {
          if (isFlipping) return;
          isFlipping = true;

          // Swipe Left Animation
          flashcardDiv.style.transition = "transform 0.25s ease-in, opacity 0.25s ease-in";
          flashcardDiv.style.transform = "translateX(-120%) rotate(-10deg)";
          flashcardDiv.style.opacity = "0";

          setTimeout(() => {
              currentFlashcard = (currentFlashcard + 1) % flashcardOrder.length;
              updateFlashcard();
              
              // Reset to right side (hidden)
              flashcardDiv.style.transition = "none";
              flashcardDiv.style.transform = "translateX(120%) rotate(10deg)";
              
              // Force reflow
              void flashcardDiv.offsetWidth;
              
              // Animate in from right
              flashcardDiv.style.transition = "transform 0.25s ease-out, opacity 0.25s ease-out, background 0.2s, color 0.2s";
              flashcardDiv.style.transform = "translateX(0) rotate(0)";
              flashcardDiv.style.opacity = "1";
              
              setTimeout(() => {
                  isFlipping = false;
              }, 250);
          }, 250);
        });"""

        if old_code_pattern.search(content):
            content = old_code_pattern.sub(new_code.strip(), content)
            changed = True
            print(f"Added swipe animation to {os.path.basename(file_path)}")

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
    print("Swipe animation update complete.")

if __name__ == "__main__":
    main()
