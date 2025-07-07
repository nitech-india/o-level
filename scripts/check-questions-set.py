import os
import fnmatch
import yaml
from collections import Counter
from collections import defaultdict
import argparse

def find_mxr_files(data_dir='_data'):
    """
    Returns a list of files in the given directory matching the pattern m?r?_*.
    """
    pattern = 'm?r?_*'
    return [f for f in os.listdir(data_dir) if fnmatch.fnmatch(f, pattern)]

def check_explanation(question):
    if 'explanation' not in question or question['explanation'] == '':
        print(f"No explanation: {question.get('text', '[No text field]')}")

def check_choices(question):
    if 'choices' not in question or question['choices'] == '':
        print(f"No choices: {question.get('text', '[No text field]')}")

def check_answer(question):
    if 'answer' not in question or question['answer'] == '':
        print(f"No answer: {question.get('text', '[No text field]')}")

def check_topic(question):
    if 'topic' not in question or question['topic'] == '':
        print(f"No topic: {question.get('text', '[No text field]')}")

def discrpency_check(file, data_dir):
    with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
        data = yaml.safe_load(f)
        if isinstance(data, dict) and 'sets' in data:
            sets = data['sets']
        elif isinstance(data, list):
            sets = [{'questions': data}]
        else:
            sets = []
        for s in sets:
            for question in s.get('questions', []):
                check_explanation(question)
                check_choices(question)
                check_answer(question)
                check_topic(question)

def summarize_total_questions(files, data_dir):
    total_questions = 0
    for file in files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                total_questions += len(s.get('questions', []))
    print(f"Total questions: {total_questions}")

def summarize_questions_by_topic(files, data_dir):
    topic_counter = Counter()
    for file in files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                for question in s.get('questions', []):
                    topic = question.get('topic', '[No topic]')
                    topic_counter[topic] += 1
    print("Questions by topic:")
    for topic, count in topic_counter.items():
        print(f"  {topic}: {count}")

def summarize_questions_by_module(files, data_dir):
    module_counter = {}
    for file in files:
        count = 0
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                count += len(s.get('questions', []))
        module_counter[file] = count
    print("Questions by module (file):")
    for module, count in module_counter.items():
        print(f"  {module}: {count}")

def summarize_questions_by_set(files, data_dir):
    print("Questions by set:")
    for file in files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                set_id = s.get('id', '[No id]')
                set_name = s.get('name', '[No name]')
                count = len(s.get('questions', []))
                print(f"  {file} | Set {set_id} ({set_name}): {count}")

def summarize_subtotal_by_pattern(files, pattern, label=None, data_dir='_data'):
    subtotal = 0
    set_count = 0
    matching_files = [f for f in files if fnmatch.fnmatch(f.lower(), pattern.lower())]
    for file in matching_files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                set_count += 1
                subtotal += len(s.get('questions', []))
    label = label or pattern
    print(f"{label} - {set_count} Sets and {subtotal} Questions")

def summarize_total_sets_and_questions(files, data_dir):
    total_sets = 0
    total_questions = 0
    for file in files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                total_sets += 1
                total_questions += len(s.get('questions', []))
    print(f"{total_sets} Practice Sets {total_questions} Total Questions")

def find_duplicate_questions(files, data_dir):
    question_map = defaultdict(list)  # text -> list of (file, set_id, set_name)
    for file in files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                set_id = s.get('id', '[No id]')
                set_name = s.get('name', '[No name]')
                for question in s.get('questions', []):
                    text = question.get('text', '').strip()
                    if text:
                        question_map[text].append((file, set_id, set_name))
    print("Duplicate questions (exact text match):")
    found = False
    for text, locations in question_map.items():
        if len(locations) > 1:
            found = True
            print(f"\nQ: {text}")
            for file, set_id, set_name in locations:
                print(f"  - {file} | Set {set_id} ({set_name})")
    if not found:
        print("No duplicates found.")

def summarize_duplicates_by_file(files, data_dir):
    question_map = defaultdict(list)  # text -> list of (file, set_id, set_name)
    for file in files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                set_id = s.get('id', '[No id]')
                set_name = s.get('name', '[No name]')
                for question in s.get('questions', []):
                    text = question.get('text', '').strip()
                    if text:
                        question_map[text].append((file, set_id, set_name))
    # Count duplicates per file
    file_duplicate_count = defaultdict(int)
    for text, locations in question_map.items():
        if len(locations) > 1:
            for file, set_id, set_name in locations:
                file_duplicate_count[file] += 1
    print("Duplicate questions summary (file-wise):")
    for file in files:
        print(f"{file}: {file_duplicate_count[file]} duplicate questions")

def count_unique_questions(files, data_dir):
    unique_questions = set()
    for file in files:
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
                for question in s.get('questions', []):
                    text = question.get('text', '').strip()
                    if text:
                        unique_questions.add(text)
    print(f"Total unique questions: {len(unique_questions)}")

def count_question_types(files, data_dir):
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
        with open(os.path.join(data_dir, file), 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'sets' in data:
                sets = data['sets']
            elif isinstance(data, list):
                sets = [{'questions': data}]
            else:
                sets = []
            for s in sets:
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
    
    single_answer_count = len(single_answer_questions)
    multiple_answer_count = len(multiple_answer_questions)
    match_together_count = len(match_together_questions)
    total_questions = single_answer_count + multiple_answer_count + match_together_count
    
    print("Question Types Summary (Unique Questions):")
    print(f"  Single Answer Questions: {single_answer_count}")
    print(f"  Multiple Answer Questions: {multiple_answer_count}")
    print(f"  Match Together Questions: {match_together_count}")
    print(f"  Total Unique Questions: {total_questions}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', default='_data', help='Directory to scan for question files')
    args = parser.parse_args()
    data_dir = args.data_dir
    files = find_mxr_files(data_dir)
    summarize_subtotal_by_pattern(files, pattern='m1r5_*', label='M1-R5', data_dir=data_dir)
    summarize_subtotal_by_pattern(files, pattern='m2r5_*', label='M2-R5', data_dir=data_dir)
    summarize_subtotal_by_pattern(files, pattern='m3r5_*', label='M3-R5', data_dir=data_dir)
    summarize_subtotal_by_pattern(files, pattern='m4r5_*', label='M4-R5', data_dir=data_dir)
    summarize_total_sets_and_questions(files, data_dir)
    count_question_types(files, data_dir)
