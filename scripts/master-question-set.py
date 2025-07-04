import os
import fnmatch
import yaml

def find_mxr_files(data_dir='_data'):
    """
    Returns a list of files in the given directory matching the pattern m?r?_*.
    """
    pattern = 'm?r?_*.yml'
    comprehensive_pattern = 'm?r?_*_comprehensive.yml'
    files = [f for f in os.listdir(data_dir) if fnmatch.fnmatch(f, pattern)]
    comprehensive_files = [f for f in os.listdir(data_dir) if fnmatch.fnmatch(f, comprehensive_pattern)]
    return files, comprehensive_files


def read_yaml_file(file_path):
    """
    Reads a YAML file and returns its contents.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def write_yaml_file(file_path, data):
    """
    Writes data to a YAML file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)

def add_all_of_above_choice(files, data_dir='_data'):
    """
    Adds a new choice 'All of the above' (key: 'E') to all questions in all sets in the given files, if not already present.
    If the answer is a list and contains all choice keys (excluding 'E'), change answer to 'E'.
    """
    for file in files:
        file_path = os.path.join(data_dir, file)
        data = read_yaml_file(file_path)
        if not data or 'sets' not in data:
            continue
        changed = False
        for s in data['sets']:
            for q in s.get('questions', []):
                choices = q.get('choices')
                if isinstance(choices, dict):
                    # Add 'E' if not present
                    if 'E' not in choices:
                        choices['E'] = 'All of the above'
                        changed = True
                    # If answer is a list and matches all choice keys except 'E', set answer to 'E'
                    answer = q.get('answer')
                    choice_keys = set(choices.keys()) - {'E'}
                    if isinstance(answer, list) and set(answer) == choice_keys:
                        q['answer'] = 'E'
                        changed = True
        if changed:
            write_yaml_file(file_path, data)

if __name__ == "__main__":
    files, comprehensive_files = find_mxr_files()
    add_all_of_above_choice(files)
    add_all_of_above_choice(comprehensive_files)