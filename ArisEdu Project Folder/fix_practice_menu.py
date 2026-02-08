import os
import re

# The Correct CSS from Lesson 1.1
FIXED_MENU_CSS = """
    /* Fixed Practices Menu CSS */
    .Practices-menu {
      position: relative;
      display: inline-block;
    }
    
    .Practices-panel {
      width: 12rem;
      min-height: 3rem;
      background: #0f172a;
      border: 2px solid #334155;
      border-radius: 0.75rem;
      position: absolute;
      right: 0;
      bottom: calc(100% + 0.5rem);
      z-index: 50; /* Increased z-index */
      opacity: 0;
      transform: scale(0.95);
      transform-origin: bottom right;
      visibility: hidden;
      pointer-events: none;
      padding: 0.6rem;
      transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    .Practices-panel.is-open {
      opacity: 1;
      visibility: visible;
      pointer-events: auto;
      transform: scale(1);
    }

    .Practices-panel-item {
      margin-bottom: 0.5rem;
    }
    
    .Practices-panel a {
      display: block;
      color: #e2e8f0;
      text-decoration: none;
      padding: 0.5rem;
      border-radius: 0.25rem;
      font-size: 0.9rem;
      font-weight: 500;
      transition: background-color 0.2s;
    }

    .Practices-panel a:hover {
      background: rgba(255, 255, 255, 0.1);
      color: white;
    }
"""

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Inject CSS if likely needed
        # We check if .Practices-panel is mentioned, but we want to OVERRIDE it.
        # We'll just append our fixed CSS to the last </style> tag.
        # Check if we already injected it (to avoid dupes if run twice)
        if "/* Fixed Practices Menu CSS */" not in content:
            if "</style>" in content:
                # Replace the last </style> with css + </style>
                # Python's replace replaces ALL by default, we want the LAST one.
                # rfind finds the last index.
                last_style_idx = content.rfind("</style>")
                if last_style_idx != -1:
                    content = content[:last_style_idx] + FIXED_MENU_CSS + "\n" + content[last_style_idx:]
                    changed = True
                    print(f"Injected CSS into {os.path.basename(file_path)}")

        # 2. Ensure Toggle Function Exists
        # Check if window.togglePracticesPanel is defined
        if "window.togglePracticesPanel =" not in content and "function togglePracticesPanel" not in content:
            # We need to inject it.
            # Look for suitable script end.
            body_end = content.rfind("</body>")
            if body_end != -1:
                js_injection = """
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
    
  // Ensure listeners are attached if not using inline onclick
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.view-other-Practices').forEach((button) => {
      button.addEventListener('click', (event) => {
        event.preventDefault();
        window.togglePracticesPanel(button);
      });
    });
  });
</script>
"""
                content = content[:body_end] + js_injection + content[body_end:]
                changed = True
                print(f"Injected JS into {os.path.basename(file_path)}")

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
            for file in os.listdir(unit_path):
                if file.endswith(".html") and "Summary" not in file and "Practice" not in file:
                    process_file(os.path.join(unit_path, file))

if __name__ == "__main__":
    main()
