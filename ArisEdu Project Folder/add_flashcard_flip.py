import os
import re

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # 1. Add perspective to flashcard-game div if missing
        def add_perspective(match):
            tag = match.group(0)
            if 'perspective:' in tag:
                return tag
            
            # Insert perspective into style
            if 'style="' in tag:
                return tag.replace('style="', 'style="perspective:1000px;')
            else:
                return tag.replace('class="flashcard-game"', 'class="flashcard-game" style="perspective:1000px;"')

        new_content = re.sub(r'<div class="flashcard-game"[^>]*>', add_perspective, content)
        if new_content != content:
            changed = True
            content = new_content
            # print(f"Added perspective to {os.path.basename(file_path)}")

        # 2. Update JS Logic
        # The new JS code
        new_js_code = """
      let isFlipping = false;
      flashcardDiv.addEventListener('click', () => {
          if (isFlipping) return;
          isFlipping = true;
          
          flashcardDiv.style.transition = "transform 0.15s ease-in, background 0.2s, color 0.2s";
          flashcardDiv.style.transform = "rotateY(90deg)";
          
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
              
              flashcardDiv.style.transition = "transform 0.15s ease-out, background 0.2s, color 0.2s";
              flashcardDiv.style.transform = "rotateY(0deg)";
              
              setTimeout(() => {
                  isFlipping = false;
              }, 150);
          }, 150);
      });"""

        # Regex to find the OLD block
        regex_pattern = re.compile(
             r"flashcardDiv\.addEventListener\('click', \(\) => \{\s+"
             r"const idx = flashcardOrder\[currentFlashcard\];\s+"
             r"if \(!showingAnswer\) \{.+?"
             r"\} else \{.+?"
             r"\}\s+"
             r"\}\);", 
             re.DOTALL
        )
         
        if regex_pattern.search(content):
             content = regex_pattern.sub(new_js_code.strip(), content)
             changed = True
             print(f"Updated JS in {os.path.basename(file_path)}")

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
