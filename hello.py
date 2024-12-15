import webvtt
import json
from datetime import datetime, timedelta

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

# We are ussing google meet-like captions
# a single "caption text" looks like:
# (speaker)\nline
x = 10
vtt_data = open('sample.vtt').readlines()

vtt_string = fix_vtt_format( vtt_data )

caps = []
for caption in webvtt.from_string( vtt_string ):
    caps.append( {
        "start": caption.start,
        "end": caption.end,
        "text": caption.text
    })

print( json.dumps( caps [0:10] )) 

# my goal is to create an array of 
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

# Interleave conversations
interleaved_data = []
for name, entries in consolidated_data.items():
    for entry in entries:
        interleaved_data.append({"start": entry["start"], "end": entry["end"], "name": name, "text": entry["text"]})

# Sort interleaved data by start time
interleaved_data.sort(key=lambda x: time_to_timedelta(x["start"]))

for entry in interleaved_data:
    print(f"{entry['start']} - {entry['end']} ({entry['name']}): {entry['text']}")