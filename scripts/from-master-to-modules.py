import os
import glob
import yaml
import sys

# Allow specifying a target data directory for testing
if len(sys.argv) > 1:
    DATA_DIR = sys.argv[1]
else:
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '_data')

MASTER_FILE = os.path.join(DATA_DIR, 'master_questions_set.yml')
MODULES = ['m1r5', 'm2r5', 'm3r5', 'm4r5']

# Patterns
practice_pattern = '{module}_practice.yml'
comprehensive_pattern = '{module}_comprehensive.yml'

def file_exists(pattern):
    """Check if any file matching the pattern exists in DATA_DIR."""
    return bool(glob.glob(os.path.join(DATA_DIR, pattern)))

def write_module_file(filename, questions):
    with open(os.path.join(DATA_DIR, filename), 'w', encoding='utf-8') as f:
        yaml.dump(questions, f, allow_unicode=True, sort_keys=False)

def main():
    # Load master questions
    master_file_path = os.path.join(DATA_DIR, 'master_questions_set.yml')
    if not os.path.exists(master_file_path):
        print(f"master_questions_set.yml not found in {DATA_DIR}")
        return
    with open(master_file_path, 'r', encoding='utf-8') as f:
        questions = yaml.safe_load(f)

    for module in MODULES:
        # Practice file
        practice_file = practice_pattern.format(module=module)
        if not file_exists(practice_file):
            print(f'Creating {practice_file}')
            write_module_file(practice_file, questions)
        else:
            print(f'{practice_file} already exists, skipping.')

        # Comprehensive file
        comprehensive_file = comprehensive_pattern.format(module=module)
        if not file_exists(comprehensive_file):
            print(f'Creating {comprehensive_file}')
            write_module_file(comprehensive_file, questions)
        else:
            print(f'{comprehensive_file} already exists, skipping.')

if __name__ == '__main__':
    main()
