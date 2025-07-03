import os
import fnmatch
import yaml
import argparse
import re

def find_mxr_files(data_dir='_data'):
    """
    Returns a list of files in the given directory matching the pattern m?r?_*.
    """
    pattern = 'm?r?_*'
    return [f for f in os.listdir(data_dir) if fnmatch.fnmatch(f, pattern)]

def count_unique_questions(files, count_only=False):
    unique_questions = set()
    for file in files:
        with open(os.path.join('_data', file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            for s in data.get('sets', []):
                for question in s.get('questions', []):
                    text = question.get('text', '').strip()
                    if text:
                        unique_questions.add(text)
    if count_only:
        print(len(unique_questions))
    else:
        print(f"Total unique questions: {len(unique_questions)}")

def count_question_types(files):
    """
    Count all types of unique questions across all modules.
    Question types:
    1. type: "multiple" - Multiple answer questions
    2. type: "match" - Match together questions  
    3. no type - Single answer questions
    """
    single_answer_questions = set()
    multiple_answer_questions = set()
    match_together_questions = set()
    
    for file in files:
        with open(os.path.join('_data', file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            for s in data.get('sets', []):
                for question in s.get('questions', []):
                    question_text = question.get('text', '').strip()
                    if question_text:  # Only count questions with text
                        question_type = question.get('type', '')
                        if question_type == 'multiple':
                            multiple_answer_questions.add(question_text)
                        elif question_type == 'match':
                            match_together_questions.add(question_text)
                        else:
                            single_answer_questions.add(question_text)
    
    return {
        'single_answer': len(single_answer_questions),
        'multiple_answer': len(multiple_answer_questions),
        'match_together': len(match_together_questions),
        'total': len(single_answer_questions) + len(multiple_answer_questions) + len(match_together_questions)
    }

def update_config_file(question_types):
    """Update _config.yml with question type counts"""
    config_file = '_config.yml'
    
    # Read current config
    with open(config_file, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    # Use regex to update all question type counts robustly
    config_content = re.sub(r'unique_questions:\s*\d+', f'unique_questions: {question_types["total"]}', config_content)
    config_content = re.sub(r'single_answer_questions:\s*\d+', f'single_answer_questions: {question_types["single_answer"]}', config_content)
    config_content = re.sub(r'multiple_answer_questions:\s*\d+', f'multiple_answer_questions: {question_types["multiple_answer"]}', config_content)
    config_content = re.sub(r'match_together_questions:\s*\d+', f'match_together_questions: {question_types["match_together"]}', config_content)
    
    # Write updated config
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument('--count-only', action='store_true', help='Print only the count as an integer')
    parser.add_argument('--update-config', action='store_true', help='Update _config.yml with question type counts')
    args = parser.parse_args()
    
    files = find_mxr_files()
    
    if args.update_config:
        question_types = count_question_types(files)
        update_config_file(question_types)
        print(f"Updated _config.yml with question types: {question_types}")
    else:
        count_unique_questions(files, count_only=args.count_only)    