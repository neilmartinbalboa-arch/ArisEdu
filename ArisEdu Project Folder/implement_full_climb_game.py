import os
import re

# The HTML for the Climb Game UI
CLIMB_GAME_HTML = """        <div id="climb-game-ui" style="display:none; height: 100%; display:flex; flex-direction:column; position:relative; overflow:hidden; background-color: #e2e8f0; border-radius: 1rem; min-height: 500px;">
            <!-- Moving Background (The Ladder) -->
            <div id="climb-ladder-bg" style="position:absolute; top:0; left:0; width:100%; height:200%; background: repeating-linear-gradient(180deg, #94a3b8 0, #94a3b8 2px, transparent 2px, transparent 40px); opacity:0.3; animation: slideLadder 10s linear infinite;"></div>
            
            <!-- Header / Status -->
            <div style="z-index:10; padding:1rem; background:rgba(255,255,255,0.95); display:flex; justify-content:space-between; align-items:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <span id="climb-score" style="font-weight: bold; color: #334155;">Score: 0</span>
                <span id="climb-level" style="font-weight: bold; color: #334155;">Level: 1</span>
                <button onclick="exitClimbGame()" style="background:#ef4444; color:white; border:none; padding: 0.5rem 1rem; border-radius: 0.5rem; cursor:pointer; font-weight: 600;">Exit</button>
            </div>

            <!-- Game Area -->
            <div style="flex:1; position:relative; width:100%; overflow:hidden;">
                 <!-- Player -->
                 <div id="climb-player" style="position:absolute; bottom:10%; left:50%; transform:translateX(-50%); font-size:4rem; transition: bottom 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index: 5; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">🧗</div>
                 <!-- Goal Line -->
                 <div id="climb-goal" style="position:absolute; top:0; width:100%; height: 5px; background: #22c55e; box-shadow: 0 0 10px #22c55e; z-index:4;"></div>
            </div>

            <!-- Interaction Area (Question) -->
            <div id="climb-interaction" style="z-index:20; background:white; padding:1.5rem; border-top:4px solid #cbd5e1; min-height: 200px; display:flex; flex-direction:column; justify-content:center;">
                <div id="climb-start-screen" style="text-align:center;">
                    <h3 style="color:#1e293b; margin-top:0;">Ready to Climb?</h3>
                    <p style="color:#64748b; margin-bottom:1.5rem;">Answer correctly to climb up against the moving ladder!</p>
                    <button onclick="startClimbGame()" style="background:#0f172a; color:white; padding:0.75rem 2rem; border:none; border-radius:0.5rem; cursor:pointer; font-weight:600; font-size:1.1rem; transition: background 0.2s;">Start Climbing</button>
                </div>
                
                <div id="climb-question-area" style="display:none; text-align:center; width:100%; max-width:600px; margin:0 auto;">
                    <p id="climb-question-text" style="font-weight:bold; margin-bottom:1.5rem; font-size:1.1rem; color: #1e293b; line-height:1.5;"></p>
                    <div id="climb-options" style="display:grid; gap:0.75rem; grid-template-columns: 1fr;">
                        <!-- Buttons injected here -->
                    </div>
                    <div id="climb-feedback" style="margin-top:1rem; height:1.5rem; font-weight:bold;"></div>
                </div>

                <div id="climb-game-over" style="display:none; text-align:center;">
                    <h3 id="climb-result-title" style="font-size: 1.5rem; margin-bottom: 0.5rem;">Game Over!</h3>
                    <p id="climb-final-score" style="color:#64748b; margin-bottom: 1.5rem;"></p>
                    <button onclick="startClimbGame()" style="background:#10b981; color:white; padding:0.75rem 2rem; border:none; border-radius:0.5rem; cursor:pointer; font-weight:600;">Play Again</button>
                </div>
            </div>
            
            <style>
                @keyframes slideLadder {
                    from { background-position: 0 0; }
                    to { background-position: 0 40px; } /* Moves down 40px (one rung spacing) */
                }
                .climb-option-btn {
                    background: #f1f5f9;
                    border: 2px solid #e2e8f0;
                    padding: 0.75rem;
                    border-radius: 0.5rem;
                    cursor: pointer;
                    font-size: 1rem;
                    color: #334155;
                    transition: all 0.2s;
                    text-align: left;
                }
                .climb-option-btn:hover {
                    background: #e2e8f0;
                    border-color: #cbd5e1;
                }
            </style>
        </div>"""

# The JavaScript Game Engine
CLIMB_GAME_JS = """
<script>
// Climb Game Logic
(function() {
    let climbScore = 0;
    let climbLevel = 1;
    let playerPosition = 10; // percent from bottom
    let isGameRunning = false;
    let gameLoopId = null;
    let currentQuestion = null;
    
    // Config
    const WIN_HEIGHT = 90; // percent
    const CLIMB_STEP = 15; // percent
    const FALL_RATE = 0.05; // percent per tick (simulates moving ladder)
    const TICK_RATE = 20; // ms
    
    window.initClimbGame = function() {
        const ui = document.getElementById('climb-game-ui');
        if(ui) ui.style.display = 'flex';
    }

    window.exitClimbGame = function() {
        const ui = document.getElementById('climb-game-ui');
        if(ui) ui.style.display = 'none';
        isGameRunning = false;
        if(gameLoopId) clearInterval(gameLoopId);
        window.switchToFlashcards();
    }

    window.startClimbGame = function() {
        // Reset State
        climbScore = 0;
        climbLevel = 1;
        playerPosition = 10;
        isGameRunning = true;
        
        document.getElementById('climb-start-screen').style.display = 'none';
        document.getElementById('climb-game-over').style.display = 'none';
        document.getElementById('climb-question-area').style.display = 'block';
        
        updateDisplay();
        nextClimbQuestion();
        
        // Start "Ladder Going Down" Mechanics
        if(gameLoopId) clearInterval(gameLoopId);
        gameLoopId = setInterval(gameLoop, TICK_RATE);
    }
    
    function gameLoop() {
        if(!isGameRunning) return;
        
        // Ladder moves down, so character moves down relative to viewport if they don't climb
        // Or simply: Gravity pulls them down
        playerPosition -= FALL_RATE * climbLevel; // Faster at higher levels?
        
        if (playerPosition <= 0) {
            endGame(false);
        }
        
        updatePlayerPos();
    }
    
    function updateDisplay() {
        document.getElementById('climb-score').innerText = `Score: ${climbScore}`;
        document.getElementById('climb-level').innerText = `Level: ${climbLevel}`;
        updatePlayerPos();
    }
    
    function updatePlayerPos() {
        const player = document.getElementById('climb-player');
        if(player) player.style.bottom = `${Math.max(0, playerPosition)}%`;
    }
    
    function nextClimbQuestion() {
        const feedback = document.getElementById('climb-feedback');
        feedback.innerText = '';
        feedback.className = '';
        
        if (!window.lessonFlashcards || window.lessonFlashcards.length === 0) {
            document.getElementById('climb-question-text').innerText = "No flashcards found for this lesson!";
            return;
        }
        
        // Pick random question
        const qIdx = Math.floor(Math.random() * window.lessonFlashcards.length);
        currentQuestion = window.lessonFlashcards[qIdx];
        
        document.getElementById('climb-question-text').innerText = currentQuestion.question;
        
        // Generate Distractors
        const options = [currentQuestion.answer];
        
        // Try to get 2 unique distractors
        const maxDistractors = Math.min(2, window.lessonFlashcards.length - 1);
        const usedIndices = new Set([qIdx]);
        
        while(options.length < 1 + maxDistractors) {
            const dIdx = Math.floor(Math.random() * window.lessonFlashcards.length);
            if(!usedIndices.has(dIdx)) {
                options.push(window.lessonFlashcards[dIdx].answer);
                usedIndices.add(dIdx);
            }
        }
        
        // Shuffle Options
        for (let i = options.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [options[i], options[j]] = [options[j], options[i]];
        }
        
        // Render Options
        const optionsContainer = document.getElementById('climb-options');
        optionsContainer.innerHTML = '';
        
        options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = 'climb-option-btn';
            btn.innerText = opt;
            btn.onclick = () => handleClimbAnswer(opt);
            optionsContainer.appendChild(btn);
        });
    }
    
    function handleClimbAnswer(selected) {
        if(!isGameRunning) return;
        
        const feedback = document.getElementById('climb-feedback');
        
        if(selected === currentQuestion.answer) {
            // Correct
            climbScore += 10;
            playerPosition += CLIMB_STEP;
            feedback.innerText = "Correct! Climbing up...";
            feedback.style.color = "#16a34a";
            
            // Level Up logic
            if(climbScore > 0 && climbScore % 50 === 0) {
                climbLevel++;
                playerPosition += 5; // Bonus boost
            }
            
            if(playerPosition >= WIN_HEIGHT) {
                endGame(true);
                return;
            }
            
        } else {
            // Incorrect
            playerPosition -= 5; // Slip down
            feedback.innerText = "Oops! Slipping down...";
            feedback.style.color = "#dc2626";
        }
        
        updateDisplay();
        
        // Disable buttons temporarily
        const btns = document.querySelectorAll('.climb-option-btn');
        btns.forEach(b => b.disabled = true);
        
        setTimeout(() => {
            nextClimbQuestion();
        }, 1000);
    }
    
    function endGame(win) {
        isGameRunning = false;
        clearInterval(gameLoopId);
        
        document.getElementById('climb-question-area').style.display = 'none';
        const gameOverScreen = document.getElementById('climb-game-over');
        gameOverScreen.style.display = 'block';
        
        const title = document.getElementById('climb-result-title');
        const msg = document.getElementById('climb-final-score');
        
        if(win) {
            title.innerText = "🎉 You Reached the Top! 🎉";
            title.style.color = "#16a34a";
            msg.innerText = `Final Score: ${climbScore} | Level Reached: ${climbLevel}`;
        } else {
            title.innerText = "Game Over!";
            title.style.color = "#dc2626";
            msg.innerText = `You fell off the ladder! Final Score: ${climbScore}`;
        }
    }
})();
</script>
"""

# Directory to traverse (adjust as needed)
ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Expose Flashcards
        # Look for "const flashcards = [ ... ];"
        # We need to find the closing bracket specifically for this variable.
        # Simple regex: find "const flashcards = [" then find the next ";".
        # Warning: This is fragile if there are semicolons inside the array strings. 
        # But looking at the file format, it seems consistent: array of objects.
        
        if "window.lessonFlashcards = flashcards;" not in content:
            # Find the position of 'const flashcards = ['
            match_start = content.find("const flashcards = [")
            if match_start != -1:
                # Find the matching closing bracket and semicolon
                # Assuming standard formatting, it ends with "];"
                # Let's search for "];" starting from match_start
                match_end = content.find("];", match_start)
                if match_end != -1:
                    insert_pos = match_end + 2
                    content = content[:insert_pos] + "\n        window.lessonFlashcards = flashcards; " + content[insert_pos:]
                    print(f"Exposed flashcards in {os.path.basename(filepath)}")
        
        # 2. Inject Game HTML Loop
        # Find the placeholder div
        placeholder_start = '<div id="climb-game-container" style="display:none; width:100%; text-align:center; padding: 2rem;">'
        if placeholder_start in content:
            # Find the end of this div
            # Simpler: Replace the EXACT placeholder block if it matches what we injected earlier.
            # The earlier injection was:
            # <div id="climb-game-container" style="display:none; width:100%; text-align:center; padding: 2rem;">
            #    <h3>Climb Game</h3>
            #    <p>Welcome to the Climb! (Game content coming soon)</p>
            #    <div style="font-size: 3rem; margin: 2rem;">🧗</div>
            # </div>
            
            # Use regex to replace the whole div block roughly
            pattern = r'<div id="climb-game-container"[\s\S]*?</div>'
            
            # We want to keep the outer container but replace Inner HTML? 
            # Actually, let's just replace the whole placeholder div with a new container div that wraps our Game UI
            # OR just put the game UI *inside* the existing div if we want to keep styling?
            # The Game UI string starts with <div id="climb-game-ui" ...>
            # So let's replace the whole placeholder block with:
            # <div id="climb-game-container" style="display:none; width:100%;"> + CLIMB_GAME_HTML + </div>
            
            replacement_html = '<div id="climb-game-container" style="display:none; width:100%;">' + CLIMB_GAME_HTML + '</div>'
            content = re.sub(pattern, replacement_html, content, count=1)
            print(f"Injected Game HTML in {os.path.basename(filepath)}")

        # 3. Update switchToClimb
        # We need to ensure initClimbGame is called
        if "window.initClimbGame()" not in content:
             content = content.replace("if(climbGame) climbGame.style.display = 'block';", 
                                       "if(climbGame) { climbGame.style.display = 'block'; if(window.initClimbGame) window.initClimbGame(); }")
        
        # 4. Inject Game JS
        # Check if already injected
        if "window.initClimbGame = function" not in content:
            # Append before closing body
            if "</body>" in content:
                content = content.replace("</body>", CLIMB_GAME_JS + "\n</body>")
                print(f"Appended Game JS in {os.path.basename(filepath)}")
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
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
    print(f"Updated {count} files.")

if __name__ == "__main__":
    main()
