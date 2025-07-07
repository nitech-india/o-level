import os
import fnmatch
import yaml
from collections import Counter
from collections import defaultdict
import argparse
import random

def find_mxr_files(data_dir='_data'):
    """
    Returns a list of files in the given directory matching the pattern m?r?_*.
    """
    pattern = 'm?r?_comprehensive.yml'
    files = [f for f in os.listdir(data_dir) if fnmatch.fnmatch(f, pattern)]
    pattern = 'm?r?_practice.yml'
    files.extend([f for f in os.listdir(data_dir) if fnmatch.fnmatch(f, pattern)])
    pattern = 'match_together_questions.yml'
    files.extend([f for f in os.listdir(data_dir) if fnmatch.fnmatch(f, pattern)])
    pattern = 'multiple_answer_questions.yml'
    files.extend([f for f in os.listdir(data_dir) if fnmatch.fnmatch(f, pattern)])
    files.sort()
    return files


def read_yaml_file(file):
    with open(file, 'r', encoding='utf-8-sig') as f:
        return yaml.safe_load(f)

def write_yaml_file(file, data):
    with open(file, 'w', encoding='utf-8-sig') as f:
        yaml.dump(data, f, allow_unicode=True)

def shuffle_questions(files, data_dir='_data'):
    for file in files:
        file_path = os.path.join(data_dir, file)
        data = read_yaml_file(file_path)
        modified = False
        if isinstance(data, dict) and 'sets' in data:
            for s in data['sets']:
                if 'questions' in s and isinstance(s['questions'], list):
                    for q in s['questions']:
                        if 'choices' in q:
                            if isinstance(q['choices'], dict):
                                # Shuffle dict items and reconstruct dict
                                items = list(q['choices'].items())
                                random.shuffle(items)
                                q['choices'] = dict(items)
                            elif isinstance(q['choices'], list):
                                random.shuffle(q['choices'])
                    random.shuffle(s['questions'])
                    modified = True
            if modified:
                write_yaml_file(file_path, data)
        elif isinstance(data, list):
            for q in data:
                if 'choices' in q:
                    if isinstance(q['choices'], dict):
                        items = list(q['choices'].items())
                        random.shuffle(items)
                        q['choices'] = dict(items)
                    elif isinstance(q['choices'], list):
                        random.shuffle(q['choices'])
            random.shuffle(data)
            write_yaml_file(file_path, data)
        # else: do nothing if structure is not recognized

if __name__ == "__main__":
    files = find_mxr_files()
    shuffle_questions(files)
