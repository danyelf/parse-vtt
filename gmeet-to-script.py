import webvtt
from datetime import datetime
import sys


def time_to_timedelta(time_str): 
    time_format = "%H:%M:%S.%f" 
    return datetime.strptime(time_str, time_format) - datetime.strptime("00:00:00.000", time_format)

def fix_vtt_format(lines):
    fixed_lines = []
    i = 0;
    while( i < len(lines) ):
        line = lines[i]
        if line.strip() == '-' and i + 1 < len(lines) and lines[i + 1].strip() == '':
            # Skip the next blank line
            i = i + 1;
        fixed_lines.append(line)
        i = i + 1;
    return ''.join( fixed_lines )

file = sys.argv[1]
# We are ussing google meet-like captions
# a single "caption text" looks like:
# (speaker)\nline
vtt_data = open(file).readlines()

vtt_string = fix_vtt_format( vtt_data )

caps = []
for caption in webvtt.from_string( vtt_string ):
    caps.append( {
        "start": caption.start,
        "end": caption.end,
        "text": caption.text
    })

# Function to convert time string to timedelta
def time_to_timedelta(time_str):
    time_format = "%H:%M:%S.%f"
    return datetime.strptime(time_str, time_format) - datetime.strptime("00:00:00.000", time_format)

# Split and consolidate statements
consolidated_data = {}
for entry in caps:
    text_blocks = entry["text"].split("\n-\n")
    for block in text_blocks:
        start = entry["start"]
        end = entry["end"]
        name, statement = block.split(")\n")
        name = name[1:]  # Remove leading '('
        if name not in consolidated_data:
            consolidated_data[name] = []
        consolidated_data[name].append({"start": start, "end": end, "text": statement.strip()})

# Merge adjacent time blocks
for name in consolidated_data:
    merged_entries = []
    previous_entry = None
    for entry in consolidated_data[name]:
        if previous_entry and time_to_timedelta(previous_entry["end"]) == time_to_timedelta(entry["start"]):
            previous_entry["end"] = entry["end"]
            previous_entry["text"] += " " + entry["text"]
        else:
            if previous_entry:
                merged_entries.append(previous_entry)
            previous_entry = entry
    if previous_entry:
        merged_entries.append(previous_entry)
    consolidated_data[name] = merged_entries

# Interleave conversations with less aggressive merging
interleaved_data = []
for name, entries in consolidated_data.items():
    for entry in entries:
        interleaved_data.append({"start": entry["start"], "end": entry["end"], "name": name, "text": entry["text"]})

# Sort interleaved data by start time
interleaved_data.sort(key=lambda x: time_to_timedelta(x["start"]))

# Print the interleaved conversation with mid-response interjections
for i in range(len(interleaved_data)):
    current_entry = interleaved_data[i]
    next_entry = interleaved_data[i + 1] if i + 1 < len(interleaved_data) else None
    
    print(f"{current_entry['start']} - {current_entry['end']} ({current_entry['name']}): {current_entry['text']}")
    
    if next_entry and time_to_timedelta(current_entry["end"]) < time_to_timedelta(next_entry["start"]):
        continue
    if next_entry and next_entry["name"] != current_entry["name"] and time_to_timedelta(current_entry["end"]) == time_to_timedelta(next_entry["start"]):
        print(f"{next_entry['start']} - {next_entry['end']} ({next_entry['name']}): {next_entry['text']}")
