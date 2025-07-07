import os
import fnmatch
import yaml
import argparse
import re

def find_mxr_files(data_dir='_data'):
    """
    Returns a list of the 8 module .yml files plus match_together_questions.yml and multiple_answer_questions.yml for unique question counting.
    """
    module_files = [
        'm1r5_practice.yml',
        'm1r5_comprehensive.yml',
        'm2r5_practice.yml',
        'm2r5_comprehensive.yml',
        'm3r5_practice.yml',
        'm3r5_comprehensive.yml',
        'm4r5_practice.yml',
        'm4r5_comprehensive.yml',
        'match_together_questions.yml',
        'multiple_answer_questions.yml',
    ]
    return [f for f in module_files if os.path.exists(os.path.join(data_dir, f))]

def count_unique_questions(files, count_only=False):
    # Map question text to the number of sets/files it appears in
    question_counts = {}
    for file in files:
        with open(os.path.join('_data', file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                for s in data.get('sets', []):
                    for question in s.get('questions', []):
                        text = question.get('text', '').strip()
                        if text:
                            question_counts[text] = question_counts.get(text, 0) + 1
    strictly_unique_questions = [q for q, c in question_counts.items() if c == 1]
    if count_only:
        print(len(strictly_unique_questions))
    else:
        print(f"Total strictly unique questions: {len(strictly_unique_questions)}")
        print("Strictly unique questions:")
        for q in strictly_unique_questions:
            print(f"- {q}")

def count_question_types(files):
    """
    Count all questions of each type across all modules, but for single and multiple answer questions, count only unique ones by their text.
    Question types:
    1. type: "multiple" OR answer is a list - Multiple answer questions (unique by text)
    2. type: "match" - Match together questions  
    3. else - Single answer questions (unique by text)
    Returns the total count for each type.
    """
    single_answer_texts = set()
    match_together_texts = set()
    multiple_answer_texts = set()
    for file in files:
        with open(os.path.join('_data', file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                for s in data.get('sets', []):
                    for question in s.get('questions', []):
                        question_type = question.get('type', '')
                        answer = question.get('answer')
                        text = question.get('text', '').strip()
                        if question_type == 'match':
                            if text:
                                match_together_texts.add(text)
                        elif question_type == 'multiple' or isinstance(answer, list):
                            if text:
                                multiple_answer_texts.add(text)
                        else:
                            if text:
                                single_answer_texts.add(text)
    return {
        'single_answer': len(single_answer_texts),
        'multiple_answer': len(multiple_answer_texts),
        'match_together': len(match_together_texts),
        'total': len(single_answer_texts) + len(multiple_answer_texts) + len(match_together_texts)
    }

def update_config_file(question_types, unique_count, total_questions):
    """Update _config.yml with question type counts, unique question count, and total_questions (all instances, including duplicates)"""
    config_file = '_config.yml'
    
    # Read current config
    with open(config_file, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    # Use regex to update all question type counts robustly
    config_content = re.sub(r'unique_questions:\s*\d+', f'unique_questions: {unique_count}', config_content)
    config_content = re.sub(r'single_answer_questions:\s*\d+', f'single_answer_questions: {question_types["single_answer"]}', config_content)
    config_content = re.sub(r'multiple_answer_questions:\s*\d+', f'multiple_answer_questions: {question_types["multiple_answer"]}', config_content)
    config_content = re.sub(r'match_together_questions:\s*\d+', f'match_together_questions: {question_types["match_together"]}', config_content)
    config_content = re.sub(r'total_questions:\s*\d+', f'total_questions: {total_questions}', config_content)
    
    # Write updated config
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)

if __name__ == "__main__":    
    files = find_mxr_files()
    question_types = count_question_types(files)
    # Compute all unique question texts (not just strictly unique)
    question_texts = set()
    total_questions = 0
    for file in files:
        with open(os.path.join('_data', file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                for s in data.get('sets', []):
                    for question in s.get('questions', []):
                        text = question.get('text', '').strip()
                        if text:
                            question_texts.add(text)
                        total_questions += 1
    unique_count = len(question_texts)
    update_config_file(question_types, unique_count, total_questions)
    print(f"Updated _config.yml with question types: {question_types}, unique questions: {unique_count}, and total questions: {total_questions}")    