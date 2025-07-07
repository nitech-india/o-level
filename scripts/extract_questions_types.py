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

def extract_and_append_questions_by_type(files, question_type, target_file, data_dir='_data'):
    """
    Extracts questions of a given type from sets in the given files and appends them to the target YAML file.
    """
    # Read the target YAML file
    target_path = os.path.join(data_dir, target_file)
    if os.path.exists(target_path):
        target_data = read_yaml_file(target_path)
    else:
        target_data = {'sets': [{'id': 1, 'name': '', 'duration_minutes': 0, 'questions': []}]}

    if not target_data or 'sets' not in target_data or not target_data['sets']:
        target_data = {'sets': [{'id': 1, 'name': '', 'duration_minutes': 0, 'questions': []}]}

    target_questions = target_data['sets'][0].get('questions', [])
    existing_texts = set(q.get('text') for q in target_questions if 'text' in q)

    for file in files:
        file_path = os.path.join(data_dir, file)
        data = read_yaml_file(file_path)
        if not data or 'sets' not in data:
            continue
        for s in data['sets']:
            for q in s.get('questions', []):
                if q.get('type') == question_type and q.get('text') not in existing_texts:
                    target_questions.append(q)
                    existing_texts.add(q.get('text'))
    target_data['sets'][0]['questions'] = target_questions
    write_yaml_file(target_path, target_data)

if __name__ == "__main__":
    files, comprehensive_files = find_mxr_files()
    # Extract 'multiple' type questions from all files (practice and comprehensive)
    extract_and_append_questions_by_type(files + comprehensive_files, 'multiple', 'multiple_answer_questions.yml')
    # Extract 'match' type questions from all files (practice and comprehensive)
    extract_and_append_questions_by_type(files + comprehensive_files, 'match', 'match_together_questions.yml')