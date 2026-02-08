import os
import json
import re

root_dir = r"c:\Users\Peter\ArisEdu-1\ArisEdu"
project_folder = "ArisEdu Project Folder"

search_index = []

print("Generating search index...")

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            
            # Skip templates or non-content files if necessary
            if "template" in file.lower() or "TODO" in file:
                continue
                
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue

            # Extract Title
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else file

            # Extract H1 or H2 as fallback title or description
            h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
            h1 = h1_match.group(1) if h1_match else ""
            
            # Clean up title
            display_title = title.replace(" - ArisEdu", "")
            if h1:
                # If H1 is very different from filename, use it, otherwise combining might be redundant
                # But kept as is per request logic
                display_title = f"{display_title} - {h1}"
            
            # Just filename if it looks nicer
            # Convert file name underscores to spaces
            file_clean = file.replace(".html", "").replace("_", " ")

            # Improve formatting: Split CamelCase and Numbers
            # 1. Insert space between lower char and upper char (e.g., "UnitMatter" -> "Unit Matter")
            file_clean = re.sub(r'([a-z])([A-Z])', r'\1 \2', file_clean)
            # 2. Insert space between letter and number (e.g., "Unit1" -> "Unit 1")
            file_clean = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', file_clean)
            # 3. Insert space between number and letter (e.g., "1Matter" -> "1 Matter"), avoiding decimals like 1.1
            file_clean = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', file_clean)
            
            # Collapse multiple spaces
            file_clean = re.sub(r'\s+', ' ', file_clean).strip()
            
            # Capitalize first letter of every word
            # file_clean = file_clean.title() # Optional, but might mess up things like "pH"
            
            # Determine relative URL
            # We need the path relative to the root for the link
            # But since pages are at different depths, absolute paths (from domain root) are safer if served, 
            # but for file system usage, we might need relative. 
            # Assuming typical web server structure:
            
            rel_path = os.path.relpath(path, root_dir)
            # If standard web server, replace \ with /
            url = "/" + rel_path.replace("\\", "/")
            
            # Extract basic text content for searching (simple regex to strip tags)
            # We'll take the first 500 characters of the body to keep index small
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
            body_text = ""
            if body_match:
                raw_body = body_match.group(1)
                # Remove scripts and styles
                raw_body = re.sub(r'<script.*?>.*?</script>', '', raw_body, flags=re.DOTALL)
                raw_body = re.sub(r'<style.*?>.*?</style>', '', raw_body, flags=re.DOTALL)
                # Strip HTML tags
                body_text = re.sub(r'<[^>]+>', ' ', raw_body)
                # Normalize whitespace
                body_text = ' '.join(body_text.split())
            
            # Determine final display values
            # Prefer the HTML title (display_title) for the main bold text
            # Use the cleaned filename as the subtitle/secondary info
            
            main_title = display_title
            sub_title = file_clean
            
            # If they are very similar, don't show both
            # Normalize for comparison
            if ''.join(e for e in main_title if e.isalnum()).lower() == ''.join(e for e in sub_title if e.isalnum()).lower():
                sub_title = ""
            
            entry = {
                "title": main_title,
                "subtitle": sub_title,
                "url": url,
                "content": body_text[:1000] # Limit content for search speed/size
            }
            
            search_index.append(entry)

# Write to JS file
js_content = f"const ARIS_EDU_SEARCH_INDEX = {json.dumps(search_index, indent=2)};"

output_path = os.path.join(root_dir, "search_data.js")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Search index generated with {len(search_index)} entries at {output_path}")
