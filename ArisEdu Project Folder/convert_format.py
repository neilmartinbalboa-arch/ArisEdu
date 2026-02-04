#!/usr/bin/env python3
import re

# Read the file
with open('c:\\Users\\Peter\\ARISedu\\test.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Color mapping based on difficulty/value
color_map = {
    # Difficulty colors
    'Easy': '#90EE90',
    'Medium-Easy': '#FFFFE0',
    'Medium': '#FFD700',
    'Medium-High': '#FFA500',
    'Medium-Hard': '#FF6347',
    'Hard': '#FF0000',
    'High': '#FF4500',
    
    # Length colors
    'Fast': '#87CEEB',
    'Medium-Fast': '#ADFF2F',
    'Long': '#FF4500',
    'Medium-Long': '#FFA500',
    'Medium-Slow': '#FFD700',
    'Slow': '#FF4500',
    
    # Other colors
    'Very Fast': '#DA70D6',
    'Low': '#ADD8E6',
    'Medium-Low': '#90EE90',
}

def get_color(value):
    """Get color code for a value"""
    if value in color_map:
        return color_map[value]
    return '#FFD700'  # Default yellow if not found

def convert_row(match):
    """Convert a single-line row to multi-line format with colors"""
    full_row = match.group(0)
    
    # Extract cells
    cells = re.findall(r'<td[^>]*>([^<]*)</td>', full_row)
    if len(cells) < 7:
        return full_row  # If not enough cells, return as is
    
    title = cells[0]
    lesson_id = cells[1]
    creator = cells[2]
    difficulty = cells[3]
    detail = cells[4]
    length = cells[5]
    pace = cells[6]
    
    # Add YouTube link to title if not already present
    if '<a href=' not in title and '<a ' not in title:
        title_text = title.replace('⭐', '').strip()
        star = ' ⭐' if '⭐' in title else ''
        title = f'<a href="https://www.youtube.com" target="_blank">{title_text}</a>{star}'
    
    # Get colors for each value
    diff_color = get_color(difficulty)
    detail_color = get_color(detail)
    length_color = get_color(length)
    pace_color = get_color(pace)
    
    # Build multi-line format
    new_row = f'''  <tr><td>{title}</td><td>{lesson_id}</td><td>{creator}</td>
    <td style="background:{diff_color}">{difficulty}</td>
    <td style="background:{detail_color}">{detail}</td>
    <td style="background:{length_color}">{length}</td>
    <td style="background:{pace_color}">{pace}</td></tr>'''
    
    return new_row

# Find all single-line rows (starting after line 159, excluding the already converted first row)
# Pattern: <tr><td>...7 cells...</td></tr> all on one line
pattern = r'    <tr><td>(?!<a href)([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td></tr>'

# Replace all matching rows
result = re.sub(pattern, convert_row, content)

# Write back
with open('c:\\Users\\Peter\\ARISedu\\test.html', 'w', encoding='utf-8') as f:
    f.write(result)

print("Conversion complete!")
