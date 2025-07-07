import os

def convert_to_utf8_no_bom_and_lf(filepath):
    # Read the file as bytes, decode with 'utf-8-sig' to remove BOM if present
    with open(filepath, 'rb') as f:
        content = f.read().decode('utf-8-sig')
    # Convert all line endings to LF
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    # Write back as UTF-8 (no BOM)
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print(f"Converted: {filepath}")

def process_directory(directory, extensions=('.html',)):
    for filename in os.listdir(directory):
        if filename.endswith(extensions):
            convert_to_utf8_no_bom_and_lf(os.path.join(directory, filename))

if __name__ == "__main__":
    # Change this to your pages directory if needed
    process_directory('pages') 