import os

# Unicode characters to remove (BOM, LRM, RLM, etc.)
HIDDEN_CHARS = ['\ufeff', '\u200e', '\u200f', '\u202a', '\u202b', '\u202c', '\u202d', '\u202e']

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Remove hidden characters from the first line (and all lines, just in case)
    cleaned_lines = []
    for line in lines:
        for hc in HIDDEN_CHARS:
            line = line.replace(hc, '')
        cleaned_lines.append(line)
    # Ensure the first line is exactly '---' if it was meant to be
    if cleaned_lines and cleaned_lines[0].strip() != '---':
        cleaned_lines[0] = cleaned_lines[0].lstrip(''.join(HIDDEN_CHARS)).lstrip()
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(cleaned_lines)
    print(f"Cleaned: {filepath}")

def process_directory(directory, extensions=('.html',)):
    for filename in os.listdir(directory):
        if filename.endswith(extensions):
            clean_file(os.path.join(directory, filename))

if __name__ == "__main__":
    process_directory('pages') 