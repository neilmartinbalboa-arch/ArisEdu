import os

ROOT_DIR = r"ChemistryLessons"

CSS_TO_INJECT = """
    /* Embedded Summary Styles - Injected for Layout Fixes */
    .lesson-notes {
      margin-top: 1.5rem;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 1rem;
      padding: 1.5rem 1.75rem;
      box-shadow: 0 10px 18px rgba(15, 23, 42, 0.12);
      color: #0f172a;
    }

    .lesson-notes h3 {
      font-size: 1.2rem;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 0.5rem;
    }

    .lesson-notes p {
      margin-bottom: 1rem;
      color: #1e293b;
    }

    .lesson-notes ul {
      margin: 0 0 1.25rem 1.25rem;
      color: #1e293b;
      list-style: disc;
    }

    .lesson-notes li {
      margin-bottom: 0.35rem;
    }
    
    .diagram-card {
      background: rgba(255, 255, 255, 0.95);
      border-radius: 1rem;
      padding: 1.5rem;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      margin-top: 1.5rem;
      position: relative;
    }

    body.dark-mode .lesson-notes {
      background: #0f172a;
      border: 1px solid #1e293b;
      box-shadow: 0 10px 18px rgba(2, 6, 23, 0.35);
      color: #e2e8f0;
    }

    body.dark-mode .lesson-notes h3 {
      color: #f8fafc;
    }

    body.dark-mode .lesson-notes p,
    body.dark-mode .lesson-notes ul {
      color: #e2e8f0;
    }

    body.dark-mode .diagram-card {
      background: rgba(15, 23, 42, 0.85);
    }
    
    .diagram-placeholder {
      border: 2px dashed rgba(59, 130, 246, 0.6);
      border-radius: 0.75rem;
      padding: 2.5rem;
      text-align: center;
      color: #475569;
    }

    body.dark-mode .diagram-placeholder {
      color: #cbd5e1;
      border-color: rgba(148, 163, 184, 0.6);
    }
    
    /* Ensures Next Up: Play button is aligned to bottom right */
    .summary-actions {
      margin-top: 1.5rem;
      display: flex;
      justify-content: flex-end;
      gap: 0.75rem;
      flex-wrap: wrap;
    }
"""

def inject_styles(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        if '.summary-actions' in content and 'justify-content: flex-end' in content:
            print(f"Skipping {file_path}: Styles already present.")
            return

        # Find the last closing style tag
        if '</style>' in content:
            # We want to inject before the last style tag closure, to ensure it overrides or appends correctly
            # Or we can just find any </style> tag.
            # Usually the main style block is the big one.
            # Let's replace the FIRST occurrence of </style> inside the <head> usually?
            # Or simply the last one found.
            
            # Simple approach: Replace the last </style>
            parts = content.rsplit('</style>', 1)
            if len(parts) == 2:
                new_content = parts[0] + CSS_TO_INJECT + '\n</style>' + parts[1]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
            else:
                print(f"Warning: No </style> tag found in {file_path}")
        else:
             print(f"Warning: No </style> tag found in {file_path}")
             
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    if not os.path.exists(ROOT_DIR):
        print("Root dir not found")
        return

    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.startswith("Lesson") and file.endswith(".html"):
                inject_styles(os.path.join(root, file))

if __name__ == "__main__":
    main()
