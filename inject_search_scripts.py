import os

# The directory where the search scripts are located (relative to the script execution or absolute)
# We assume this script is run from 'c:\Users\Peter\ArisEdu-1\ArisEdu'
SEARCH_DATA_FILENAME = "search_data.js"
SEARCH_LOGIC_FILENAME = "search_logic.js"

ROOT_DIR = os.path.join(os.getcwd(), "ArisEdu Project Folder")

def inject_scripts():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                # Calculate relative path from this html file to the root where js files are
                # The JS files are at c:\Users\Peter\ArisEdu-1\ArisEdu
                # The current file is at 'root'
                
                # We need to go up from 'root' to 'c:\Users\Peter\ArisEdu-1\ArisEdu'
                # os.path.relpath('c:\Users\Peter\ArisEdu-1\ArisEdu', root)
                
                script_dir = os.getcwd() # c:\Users\Peter\ArisEdu-1\ArisEdu
                rel_path_to_scripts = os.path.relpath(script_dir, root)
                
                # Normalize path separators to forward slashes for HTML
                rel_path_to_data = os.path.join(rel_path_to_scripts, SEARCH_DATA_FILENAME).replace("\\", "/")
                rel_path_to_logic = os.path.join(rel_path_to_scripts, SEARCH_LOGIC_FILENAME).replace("\\", "/")
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if SEARCH_DATA_FILENAME in content:
                    print(f"Skipping {file} - already injected")
                    continue
                
                # Insert before </body>
                if "</body>" in content:
                    injection = f'\n    <!-- ArisEdu Global Search -->\n    <script src="{rel_path_to_data}"></script>\n    <script src="{rel_path_to_logic}"></script>\n'
                    new_content = content.replace("</body>", injection + "</body>")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Injected into {file}")
                    count += 1
                else:
                    print(f"Skipping {file} - no body tag")

    print(f"Total files injected: {count}")

if __name__ == "__main__":
    inject_scripts()
