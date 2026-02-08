import os
import re
import shutil

# Root directory for Chemistry Lessons
ROOT_DIR = r"ChemistryLessons"

# JS to inject
JS_INJECTION = r"""
<script>
  window.togglePracticesPanel = function(button) {
    if (!button) return;
    const menu = button.closest('.Practices-menu') || button.closest('.side-buttons'); 
    if (!menu) return;
    const panel = menu.querySelector('.Practices-panel');
    if (!panel) return;
    const isOpen = panel.classList.toggle('is-open');
    panel.setAttribute('aria-hidden', (!isOpen).toString());
  };

  function attachPracticeListeners() {
      document.querySelectorAll('.view-other-Practices').forEach((button) => {
      button.addEventListener('click', (event) => {
        event.preventDefault();
        window.togglePracticesPanel(button);
      });
    });
  }


  window.toggleToSummary = function(event) {
    if (event) event.preventDefault();
    const lessonView = document.getElementById('lesson-content-view');
    const practiceView = document.getElementById('practice-content-view');
    const summaryView = document.getElementById('summary-content-view');
    
    if (lessonView) lessonView.style.display = 'none';
    if (practiceView) practiceView.style.display = 'none';
    if (summaryView) summaryView.style.display = 'block';
    
    // Update Back Button
    const backBtn = document.getElementById('back-button');
    if (backBtn) {
        // Store original text if not already stored
        if (!backBtn.dataset.originalText) {
            backBtn.dataset.originalText = backBtn.innerText;
        }
        
        // Get the lesson name for the back button, e.g. "Lesson 2.1"
        // Try to parse from title or use generic
        const title = document.title;
        const lessonMatch = title.match(/Lesson\s+\d+\.\d+/);
        const lessonName = lessonMatch ? lessonMatch[0] : "Lesson";
        
        backBtn.innerText = "← Back to " + lessonName;
        
        // Clone to clear previous listeners
        const newBackBtn = backBtn.cloneNode(true);
        if (backBtn.parentNode) {
            backBtn.parentNode.replaceChild(newBackBtn, backBtn);
            newBackBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (summaryView) summaryView.style.display = 'none';
                if (lessonView) lessonView.style.display = 'block';
                
                // Restore original Back Button behavior for Unit
                const restoreBtn = newBackBtn.cloneNode(true);
                newBackBtn.parentNode.replaceChild(restoreBtn, newBackBtn);
                
                // We need to know where the unit page is. 
                // Usually it is ChemistryUnitXMeasure.html or similar.
                // We can just reload the page to be safe if we don't know the unit link, 
                // BUT the original back button had a listener or href.
                // Let's try to extract the original HREF from the HTML source if possible, 
                // but since we are replacing the logic, we might need a smart way to go back.
                // Actually, the original back button usually changes window.location.href.
                // We should probably just reload to be safe or try to go back in history?
                // No, the original listener is gone.
                // Let's assume the user wants to go to the Unit page.
                // Best bet: finding the unit file name from the path.
                
                // Simpler approach: Just reload the page? No, that stays on Lesson.
                // We need the Unit Hub link.
                // In Lesson 1.1 logic, we hardcoded 'ChemistryUnit1Matter.html'.
                // Here we can try to guess or just use history.back() if safe?
                // Let's try to grab the Unit text from the original button text?
                // "Back to Unit 1"
                
                // Re-read strictly:
                // The original code had: window.location.href = '/ArisEdu Project Folder/ChemistryLessons/Unit2/ChemicalUnit2.html' (example)
                // We can't easily parse that strictly from js logic without parsing the original file content.
                // HOWEVER, we can just grab the 'href' if it was an <a> tag?
                // The original back button is often a <button> with a JS listener.
                
                // Let's rely on the fact that we are just hiding/showing divs. 
                // Initial state: Lesson View visible.
                // If we hit back from Summary -> Show Lesson View.
                // Now we are at Lesson View. The "Back" button should do what it originally did.
                // Problem: We replaced the node, so we lost the original event listener!
                
                // FIX: Instead of replacing the node when going back to lesson, we should 
                // RE-ADD the original listener? Or just reload the page?
                // Reloading is safe but slow.
                // Better: When initializing initJS, we can store the original click handler? No, can't easily extracting allow.
                
                // ALTERNATIVE: Don't replace the button node. Just change onclick.
                // But the original might be addEventListener.
                
                // OK, strategy: In the Python script, I will extract the original Back Button Logic (href) 
                // and inject it into a variable `window.originalBackLink`.
                if (window.originalBackLink) {
                    restoreBtn.innerText = "← Back to Unit"; 
                    restoreBtn.addEventListener('click', () => {
                        window.location.href = window.originalBackLink;
                    });
                } else {
                     restoreBtn.innerText = "← Back";
                     restoreBtn.addEventListener('click', () => history.back());
                }
            });
        }
    }
    
    window.scrollTo(0, 0);
  };

  window.toggleToPractice = function(event) {
    if (event) event.preventDefault();
    const lessonView = document.getElementById('lesson-content-view');
    const practiceView = document.getElementById('practice-content-view');
    const summaryView = document.getElementById('summary-content-view');

    if (lessonView) lessonView.style.display = 'none';
    if (summaryView) summaryView.style.display = 'none';
    if (practiceView) practiceView.style.display = 'block';
    
    // Initialize flashcards if not already done
    if (typeof initFlashcards === 'function') {
        try {
            initFlashcards();
        } catch (err) {
            console.error("Error initializing flashcards:", err);
        }
    }

    // Update Back Button
    const backBtn = document.getElementById('back-button');
    if (backBtn) {
        backBtn.innerText = "← Back to Summary";
        const newBackBtn = backBtn.cloneNode(true);
        if (backBtn.parentNode) {
            backBtn.parentNode.replaceChild(newBackBtn, backBtn);
            newBackBtn.addEventListener('click', (e) => {
                e.preventDefault();
                window.toggleToSummary(e);
            });
        }
    }
    window.scrollTo(0, 0);
  };
  
</script>
"""

def extract_content(file_path, start_marker, end_marker=None):
    """Simple extraction helper."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex or substring find
        # For Summary: <div class="lesson-notes"> ... </div>
        # But we want the whole diagram-card or just contents?
        # Lesson 1.1 extracted the content of `.diagram-card` usually.
        # Let's try to extract specific divs.
        
        return content
    except FileNotFoundError:
        return None

def process_lesson(unit_dir, lesson_file):
    lesson_path = os.path.join(unit_dir, lesson_file)
    
    # Identify companions
    base_name = os.path.splitext(lesson_file)[0]
    summary_file = base_name + "Summary.html"
    practice_file = base_name + "Practice.html"
    
    summary_path = os.path.join(unit_dir, summary_file)
    practice_path = os.path.join(unit_dir, practice_file)
    
    if not (os.path.exists(summary_path) and os.path.exists(practice_path)):
        print(f"Skipping {lesson_file}: Missing companions.")
        return

    print(f"Processing {lesson_file}...")
    
    # Read Main Lesson
    with open(lesson_path, 'r', encoding='utf-8', errors='replace') as f:
        main_content = f.read()
        
    if 'id="lesson-content-view"' in main_content:
        print(f"Skipping {lesson_file}: Already converted.")
        return

    # Extract Back Button Link to preserve unit navigation
    # specific pattern: window.location.href = '/ArisEdu Project Folder/ChemistryLessons/Unit2/Lesson 2.1.html';
    # Wait, inside the Practice file it points to Lesson.
    # Inside the MAIN file, the back button points to UNIT.
    # Pattern: document.getElementById('back-button').addEventListener('click', () => { window.location.href = '...'; });
    back_link_match = re.search(r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]", main_content)
    # This match might be the one for "settings" or "logout" if we aren't careful.
    # Let's look for the one near 'back-button'.
    back_link = ""
    back_btn_block = re.search(r"document\.getElementById\('back-button'\)\.addEventListener\('click',\s*\(\)\s*=>\s*{([^}]+)}", main_content)
    if back_btn_block:
        block_content = back_btn_block.group(1)
        href_match = re.search(r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]", block_content)
        if href_match:
            back_link = href_match.group(1)
            
    # Read/Extract Summary
    with open(summary_path, 'r', encoding='utf-8', errors='replace') as f:
        sum_content = f.read()
    
    # Try different content patterns for Summary
    summary_html = "<p>Summary content not found.</p>"
    
    # 1. Lesson Notes
    sum_notes_match = re.search(r'(<div class="lesson-notes">.*?</div>)', sum_content, re.DOTALL)
    if sum_notes_match:
        summary_html = sum_notes_match.group(1)
    else:
        # 2. Diagram Placeholder
        sum_place_match = re.search(r'(<div class="diagram-placeholder">.*?</div>)', sum_content, re.DOTALL)
        if sum_place_match:
            summary_html = sum_place_match.group(1)
        else:
             # 3. Everything in diagram-card BEFORE summary-actions
             # <div class="diagram-card"> (CONTENT) <div class="summary-actions">
             card_match = re.search(r'<div class="diagram-card">\s*(.*?)\s*<div class="summary-actions">', sum_content, re.DOTALL)
             if card_match:
                 summary_html = card_match.group(1)

    # Read/Extract Practice
    with open(practice_path, 'r', encoding='utf-8', errors='replace') as f:
        prac_content = f.read()

    # Extract Flashcard HTML
    # Look for <div class="flashcard-game" ...> ... </div>
    # This is tricky with nested divs.
    # However, the structure seems quite standard.
    # <div class="flashcard-game" ...> [content] </div>
    # We can try to grab from <div class="flashcard-game" to the closing </div> of that tree.
    # Or just Regex greedily until <div class="Practice-actions">?
    
    prac_game_match = re.search(r'(<div class="flashcard-game".*?</div>)\s*<div class="Practice-actions"', prac_content, re.DOTALL)
    if not prac_game_match:
        # Try looser match
        prac_game_match = re.search(r'(<div class="flashcard-game".*?Shuffle\s*</button>\s*</div>\s*</div>)', prac_content, re.DOTALL)
        
    flashcard_html = ""
    if prac_game_match:
        flashcard_html = prac_game_match.group(1)
    else:
        print(f"Warning: Could not find .flashcard-game in {practice_file}")
        flashcard_html = "<p>Practice content could not be parsed.</p>"

    # Extract Flashcard JS Array
    # const flashcards = [ ... ];
    flashcards_js_match = re.search(r'(const flashcards\s*=\s*\[.*?\];)', prac_content, re.DOTALL)
    flashcards_js = ""
    if flashcards_js_match:
        flashcards_js = flashcards_js_match.group(1)
    else:
        print(f"Warning: Could not extract flashcards array from {practice_file}")

    # Build New CSS
    # We need to make sure we include the Practice/Summary CSS if it's unique.
    # Usually it's in the <style> tag.
    # We can perform a naive copy of the style block from Practice.
    style_match = re.search(r'<style>(.*?)</style>', prac_content, re.DOTALL)
    extra_css = ""
    if style_match:
        extra_css = style_match.group(1)
        # Filter commonly repeated css?
        # For now, just append it. It might duplicate but that's okay.

    # CONSTRUCT NEW HTML
    
    # 1. Inject CSS
    if extra_css:
         main_content = main_content.replace('</style>', extra_css + '\n</style>', 1)
         
    # 2. Wrap Main Content
    # Find <main class="main-container">
    # We want to replace <main ...> [CONTENT] </main>
    # with <main ...> <div id="lesson-content-view"> [CONTENT] </div> [HIDDEN DIVS] </main>
    
    main_start = re.search(r'<main class="main-container">', main_content)
    main_end = re.search(r'</main>', main_content)
    
    if main_start and main_end:
        start_idx = main_start.end()
        end_idx = main_end.start()
        
        inner_html = main_content[start_idx:end_idx]
        
        # 3. Update "Next Up" Button in inner_html
        # Replace href="...Summary.html" with onclick="toggleToSummary(event)"
        # Regex for valid summary link
        summary_link_pattern = re.compile(r'<a\s+class="side-button"\s+href="[^"]*Summary\.html">Next Up: Summary</a>')
        inner_html = summary_link_pattern.sub(r'<button class="side-button" onclick="toggleToSummary(event)">Next Up: Summary</button>', inner_html)
        
        # Summary View HTML
        summary_view = f"""
    <!-- Embedded Summary View -->
    <div id="summary-content-view" style="display: none;">
        <h2 class="page-title">{base_name.replace('_', ' ')} Summary</h2>
        <div class="diagram-card">
          {summary_html}
          <div class="summary-actions">
            <button class="side-button" onclick="toggleToPractice(event)">Next Up: Play</button>
          </div>
        </div>
    </div>
"""

        # Practice View HTML
        # Need to include the "Other practices" menu HTML too?
        # The Lesson 1.1 file has it.
        # We can just hardcode a generic one or try to extract it.
        # Lesson 2.1 practice has it.
        
        practice_view = f"""
    <!-- Embedded Practice View -->
    <div id="practice-content-view" style="display: none;">
      <h2 class="page-title">{base_name.replace('_', ' ')} Practice</h2>
      <div class="diagram-card">
        {flashcard_html}
        <div class="Practice-actions" style="margin-top:2rem;display:flex;justify-content:flex-end;width:100%;">
          <div class="Practices-menu" style="position:relative;">
            <button class="side-button view-other-Practices" type="button" onclick="window.togglePracticesPanel(this)">Other practices</button>
            <div class="Practices-panel" aria-hidden="true">
              <div class="Practices-panel-item">
                <a href="#flashcard-game">Flashcard Game</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
"""

        new_inner = f"""
    <div id="lesson-content-view">
{inner_html}
    </div>
{summary_view}
{practice_view}
"""
        main_content = main_content[:start_idx] + new_inner + main_content[end_idx:]
        
    # 4. Inject JS
    # We need to inject the Flashcard Array into the initFlashcards function logic
    # The JS_INJECTION constant has `initFlashcards();` call inside `toggleToPractice`
    # But it needs the definition of `initFlashcards` with the specific array.
    
    flashcard_init_script = f"""
<script>
  let flashcardsInitialized = false;
  window.initFlashcards = function() {{
      if (flashcardsInitialized) return;
      
      {flashcards_js}
      
      let currentFlashcard = 0;
      let flashcardOrder = [...Array(flashcards.length).keys()];
      
      const flashcardContent = document.getElementById('flashcard-content');
      const flashcardDiv = document.getElementById('flashcard');
      const nextFlashcardBtn = document.getElementById('next-flashcard');
      const prevFlashcardBtn = document.getElementById('prev-flashcard');
      const shuffleFlashcardBtn = document.getElementById('shuffle-flashcard');
      
      if (!flashcardContent || !flashcardDiv) return;

      let showingAnswer = false;

      function updateFlashcard() {{
          showingAnswer = false;
          const idx = flashcardOrder[currentFlashcard];
          const text = flashcards[idx].question;
          flashcardContent.textContent = text;
          autoAdjustFontSize(text);
      }}

      function autoAdjustFontSize(text) {{
          if (!flashcardContent) return;
          let baseSize = 1.25; 
          let minSize = 0.8; 
          let maxSize = 2.5; 
          let length = text.length;
          let size = baseSize;
          if (length < 60) size = maxSize;
          else if (length < 120) size = 1.5;
          else if (length < 200) size = 1.1;
          else size = minSize;
          flashcardContent.style.fontSize = size + 'rem';
      }}

      flashcardDiv.addEventListener('click', () => {{
          const idx = flashcardOrder[currentFlashcard];
          if (!showingAnswer) {{
            const answer = flashcards[idx].answer;
            flashcardContent.textContent = answer;
            autoAdjustFontSize(answer);
            showingAnswer = true;
          }} else {{
            const question = flashcards[idx].question;
            flashcardContent.textContent = question;
            autoAdjustFontSize(question);
            showingAnswer = false;
          }}
      }});
      
      if (nextFlashcardBtn) nextFlashcardBtn.addEventListener('click', () => {{
          currentFlashcard = (currentFlashcard + 1) % flashcardOrder.length;
          updateFlashcard();
      }});
      
      if (prevFlashcardBtn) prevFlashcardBtn.addEventListener('click', () => {{
          currentFlashcard = (currentFlashcard - 1 + flashcardOrder.length) % flashcardOrder.length;
          updateFlashcard();
      }});
      
      if (shuffleFlashcardBtn) shuffleFlashcardBtn.addEventListener('click', () => {{
          function shuffleArray(array) {{
            let arr = array.slice();
            for (let i = arr.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }}
            return arr;
          }}
          flashcardOrder = shuffleArray(flashcardOrder);
          currentFlashcard = 0;
          updateFlashcard();
      }});

      updateFlashcard();
      flashcardsInitialized = true;
  }};
</script>
"""
    
    # Inject Back Link Global Variable
    if back_link:
        back_link_script = f"<script> window.originalBackLink = '{back_link}'; </script>"
        main_content = main_content.replace('</body>', back_link_script + '\n</body>')

    # Append Scripts
    main_content = main_content.replace('</body>', JS_INJECTION + '\n' + flashcard_init_script + '\n</body>')
    
    # Write back
    with open(lesson_path, 'w', encoding='utf-8') as f:
        f.write(main_content)
        
    print(f"Successfully converted {lesson_file}")
    
    # Delete helpers
    os.remove(summary_path)
    os.remove(practice_path)
    print("Deleted companion files.")

def main():
    if not os.path.exists(ROOT_DIR):
        print("Root dir not found")
        return

    # Walk directories
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.startswith("Lesson") and file.endswith(".html") and not file.endswith("Summary.html") and not file.endswith("Practice.html"):
                process_lesson(root, file)

if __name__ == "__main__":
    main()
