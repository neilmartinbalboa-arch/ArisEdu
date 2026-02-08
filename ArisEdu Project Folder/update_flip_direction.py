import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False

        # CSS Regex to replace transform styling in JS
        # We look for the block starting with 'let isFlipping = false;'
        
        # New pattern logic
        new_js_logic = """
        let isFlipping = false;
        flashcardDiv.addEventListener('click', () => {
          if (isFlipping) return;
          isFlipping = true;
          
          // Direction: Q->A (Bottom-to-Up = +1), A->Q (Up-to-Bottom = -1)
          const direction = !showingAnswer ? 1 : -1;
          
          flashcardDiv.style.transition = "transform 0.15s ease-in, background 0.2s, color 0.2s";
          flashcardDiv.style.transform = `rotateX(${90 * direction}deg)`;
          
          setTimeout(() => {
              const idx = flashcardOrder[currentFlashcard];
              if (!showingAnswer) {
                const answer = flashcards[idx].answer;
                flashcardContent.textContent = answer;
                autoAdjustFontSize(answer);
                showingAnswer = true;
              } else {
                const question = flashcards[idx].question;
                flashcardContent.textContent = question;
                autoAdjustFontSize(question);
                showingAnswer = false;
              }
              
              // Complete the full flip illusion
              flashcardDiv.style.transition = "none";
              flashcardDiv.style.transform = `rotateX(${-90 * direction}deg)`;
              
              // Force reflow
              void flashcardDiv.offsetWidth;
              
              flashcardDiv.style.transition = "transform 0.15s ease-out, background 0.2s, color 0.2s";
              flashcardDiv.style.transform = "rotateX(0deg)";
              
              setTimeout(() => {
                  isFlipping = false;
              }, 150);
          }, 150);
        });"""

        # We need a regex that matches the current implementation (rotateY)
        # It handles variable whitespace
        regex_pattern = re.compile(
            r"let isFlipping = false;\s+"
            r"flashcardDiv\.addEventListener\('click', \(\) => \{\s+"
            r"if \(isFlipping\) return;\s+"
            r"isFlipping = true;\s+"
            r"flashcardDiv\.style\.transition = [^;]+;\s+"
            r"flashcardDiv\.style\.transform = \"rotateY\(90deg\)\";\s+"
            r"setTimeout\(\(\) => \{.+?"
            r"flashcardDiv\.style\.transition = [^;]+;\s+"
            r"flashcardDiv\.style\.transform = \"rotateY\(0deg\)\";\s+"
            r"setTimeout\(\(\) => \{\s+"
            r"isFlipping = false;\s+"
            r"\}, 150\);\s+"
            r"\}, 150\);\s+"
            r"\}\);",
            re.DOTALL
        )
        
        if regex_pattern.search(content):
            content = regex_pattern.sub(new_js_logic.strip(), content)
            changed = True
            print(f"Updated flip direction in {os.path.basename(file_path)}")
        else:
            # Fallback for manual whitespace differences or slight variations
            # Let's try to match a slightly simpler pattern if the strict one fails
            # Search for the start and end of the event listener
            start_marker = "let isFlipping = false;\n"
            start_idx = content.find("let isFlipping = false;")
            if start_idx != -1:
                # Find the closing of this specific listener. 
                # It's inside initFlashcards, so we can look for the next "flashcardDiv.addEventListener" or "nextFlashcardBtn"?
                # The listener ends with });
                # and is followed by nextFlashcardBtn.addEventListener
                
                # Look for nextFlashcardBtn
                end_marker_idx = content.find("nextFlashcardBtn.addEventListener", start_idx)
                if end_marker_idx != -1:
                    # Backtrack to the closing }); of the previous block
                    # The block ends with });
                    block_end = content.rfind("});", start_idx, end_marker_idx)
                    if block_end != -1:
                         # Verification: Check if "rotateY" is in this block
                         block = content[start_idx:block_end+3]
                         if "rotateY" in block:
                             content = content[:start_idx] + new_js_logic.strip() + content[block_end+3:]
                             changed = True
                             print(f"Updated (fallback) flip direction in {os.path.basename(file_path)}")

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
    print("Update complete.")

if __name__ == "__main__":
    main()
