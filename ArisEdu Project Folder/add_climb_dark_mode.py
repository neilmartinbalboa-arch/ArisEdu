import os

ROOT_DIR = r"C:\Users\Peter\ArisEdu-1\ArisEdu\ArisEdu Project Folder\ChemistryLessons"

DARK_MODE_CSS = """
                /* Dark Mode Support */
                body.dark-mode #climb-game-ui { background-color: #0f172a !important; }
                body.dark-mode #climb-ladder-bg { background-image: repeating-linear-gradient(180deg, #334155 0, #334155 2px, transparent 2px, transparent 40px) !important; opacity: 0.2 !important; }
                body.dark-mode #climb-header { background: rgba(15, 23, 42, 0.95) !important; box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important; }
                body.dark-mode #climb-score, body.dark-mode #climb-level { color: #e2e8f0 !important; }
                body.dark-mode #climb-interaction { background: #1e293b !important; border-top-color: #334155 !important; }
                body.dark-mode #climb-start-screen h3, body.dark-mode #climb-game-over h3 { color: #f8fafc !important; }
                body.dark-mode #climb-start-screen p, body.dark-mode #climb-game-over p, body.dark-mode #climb-question-text { color: #cbd5e1 !important; }
                body.dark-mode .climb-option-btn { background: #334155 !important; border-color: #475569 !important; color: #e2e8f0 !important; }
                body.dark-mode .climb-option-btn:hover { background: #475569 !important; border-color: #64748b !important; }
                body.dark-mode #climb-fullscreen-btn { background: rgba(30, 41, 59, 0.9) !important; }
                body.dark-mode #climb-fullscreen-btn svg { stroke: #e2e8f0 !important; }
"""

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        updated = False

        # 1. Add ID to header to make styling easier
        header_search = '<div style="z-index:10; padding:1rem; background:rgba(255,255,255,0.95);'
        header_replace = '<div id="climb-header" style="z-index:10; padding:1rem; background:rgba(255,255,255,0.95);'
        
        if header_search in content:
            content = content.replace(header_search, header_replace)
            updated = True
        elif '<div id="climb-header"' in content:
            # Already has ID, good
            pass

        # 2. Inject CSS
        # Check if we already injected the dark mode css
        if "body.dark-mode #climb-game-ui" not in content:
            # Insert before the closing style tag for the climb game
            # We look for the last </style> inside the climb-game-ui container specifically if possible
            # But since it's unique enough (inside the inject string), let's just find the closing tag for the climb styles
            
            # The climb styles end with:
            #     border-color: #cbd5e1;
            # }
            # </style>
            
            style_end_marker = """
                .climb-option-btn:hover {
                    background: #e2e8f0;
                    border-color: #cbd5e1;
                }
            </style>"""
            
            # We can replace just the closing tag to be safe
            target = "</style>"
            # But wait, there are other style tags in the document.
            # We need to target the one we added.
            # Let's target by a unique string in our CSS
            unique_css = ".climb-option-btn:hover {"
            
            idx = content.find(unique_css)
            if idx != -1:
                # Find the next </style> after this
                style_end_idx = content.find("</style>", idx)
                if style_end_idx != -1:
                    # Insert before it
                    content = content[:style_end_idx] + DARK_MODE_CSS + content[style_end_idx:]
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
