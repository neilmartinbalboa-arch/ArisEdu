#!/usr/bin/env python3
import re

# Read the file
with open('c:\\Users\\Peter\\ARISedu\\test.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the table start (after header)
table_start = None
table_end = None
for i, line in enumerate(lines):
    if '<th>Video Topic</th>' in line:
        table_start = i + 1
    if '</table>' in line and table_start is not None:
        table_end = i
        break

print(f"Table starts at line {table_start}, ends at line {table_end}")

# Extract rows (each row starts with <tr> and ends with </tr>)
# But can span multiple lines
current_row = []
rows = []
in_row = False

for i in range(table_start, table_end):
    line = lines[i]
    
    if '<tr>' in line:
        in_row = True
        current_row = [line]
    elif in_row:
        current_row.append(line)
        if '</tr>' in line:
            rows.append(''.join(current_row))
            in_row = False
            current_row = []

print(f"Extracted {len(rows)} rows")

# Parse lesson numbers and sort
def get_lesson_number(row_text):
    """Extract lesson number for sorting"""
    # Look for pattern <td>1.1</td> or <td>12.3</td> etc
    match = re.search(r'<td>(\d+)\.(\d+)', row_text)
    if match:
        unit = int(match.group(1))
        lesson = int(match.group(2))
        return (unit, lesson)
    return (999, 999)

# Sort rows
sorted_rows = sorted(rows, key=get_lesson_number)

# Print first few for verification
print("\nFirst 5 sorted rows:")
for row in sorted_rows[:5]:
    lesson = get_lesson_number(row)
    title_match = re.search(r'>([^<]+)</a></td>', row)
    title = title_match.group(1) if title_match else "N/A"
    print(f"  {lesson}: {title}")

# Rebuild the file
new_lines = lines[:table_start] + sorted_rows + lines[table_end:]

with open('c:\\Users\\Peter\\ARISedu\\test.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\nFile sorted! Total rows: {len(sorted_rows)}")
