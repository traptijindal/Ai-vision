def extract_general_notes(text):
    """Extracts General Notes section from text."""
    # This is a heuristic approach, assuming the section title
    # and content format.
    notes = []
    for line in text.split('\n'):
        if "GENERAL SHEET NOTES" in line.upper():
            notes_start = text.find(line)
            # Find the end of the notes section. This might need refinement.
            notes_end = text.find("KEYNOTES", notes_start)
            if notes_end == -1:
                notes_end = len(text)
            notes.append(text[notes_start:notes_end])
    return "\n".join(notes)

# def extract_lighting_schedule(text):
#     """Extracts lighting schedule table from text."""
#     # Assuming a fixed table structure.
#     start_keywords = ["TYPE MARK", "TYPE MARR"]
#     end_keywords = ["NTS", "SCHEDULE"]
    
#     schedule_text = ""
#     start_found = False
    
#     for line in text.split('\n'):
#         if any(keyword in line for keyword in start_keywords):
#             start_found = True
        
#         if start_found:
#             schedule_text += line + "\n"
        
#         if any(keyword in line for keyword in end_keywords) and start_found:
#             break
            
#     # Simple parsing into a list of dictionaries
#     schedule_data = []
#     lines = schedule_text.strip().split('\n')
#     if len(lines) > 1:
#         headers = [h.strip() for h in lines[0].split(',') if h.strip()]
#         for line in lines[1:]:
#             parts = [p.strip() for p in line.split(',') if p.strip()]
#             if parts and len(parts) == len(headers):
#                 row_dict = dict(zip(headers, parts))
#                 schedule_data.append(row_dict)
    
#     return schedule_data

# In src/data_extractor.py

import re

def extract_lighting_schedule(text):
    """
    Extracts and parses the lighting schedule table from text.
    It's more robust now to handle OCR errors and different table formats.
    """
    schedule_data = []
    # Using regex to find the table headers
    match = re.search(r'(TYPE MARK|TYPE MARR).*', text, re.IGNORECASE)
    if not match:
        return schedule_data

    headers_line = match.group(0)
    text_after_headers = text[match.end():]
    
    # Split by lines and clean up to create a table structure
    lines = text_after_headers.strip().split('\n')
    headers = [h.strip() for h in headers_line.split(',') if h.strip()]

    # Assuming a fixed number of columns for the table
    num_cols = len(headers)
    for line in lines:
        parts = [p.strip() for p in line.split(',') if p.strip()]
        if len(parts) >= num_cols:
            row_dict = dict(zip(headers, parts[:num_cols]))
            schedule_data.append(row_dict)
    
    # Clean up empty dictionaries that might result from poor parsing
    schedule_data = [row for row in schedule_data if row.get('TYPE MARK')]

    return schedule_data

def count_emergency_lights_from_schedule(lighting_schedule):
    """
    Counts emergency lights based on TYPE MARK and DESCRIPTION.
    """
    emergency_counts = {
        "total_emergency_lights": 0,
        "2x4_recessed_led_luminaire": 0,
        "wallpack_with_photocell": 0,
        "other_emergency_fixtures": []
    }
    
    for item in lighting_schedule:
        type_mark = item.get('TYPE MARK', '').strip()
        description = item.get('DESCRIPTION', '').lower()
        
        # Count all fixtures with 'E' suffix
        if type_mark and type_mark.endswith('E'):
            emergency_counts['total_emergency_lights'] += 1
            if '2\' x 4\' recessed' in description:
                emergency_counts['2x4_recessed_led_luminaire'] += 1
            else:
                emergency_counts['other_emergency_fixtures'].append(type_mark)

        # Count fixture 'W' based on General Notes
        if type_mark == 'W':
            emergency_counts['wallpack_with_photocell'] += 1
            emergency_counts['total_emergency_lights'] += 1

    return emergency_counts