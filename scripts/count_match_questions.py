import os
import yaml

def count_match_questions():
    """
    Count total match questions and how many have answer fields.
    """
    data_dir = '_data'
    count_total = 0
    count_with_answer = 0
    
    # Get all m*r* files
    files = [f for f in os.listdir(data_dir) if f.startswith('m') and f.endswith('.yml')]
    comprehensive_files = [f for f in os.listdir(data_dir) if f.endswith('_comprehensive.yml')]
    all_files = files + comprehensive_files
    
    for file in all_files:
        file_path = os.path.join(data_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if data and 'sets' in data:
                for s in data['sets']:
                    for q in s.get('questions', []):
                        if q.get('type') == 'match':
                            count_total += 1
                            if 'answer' in q:
                                count_with_answer += 1
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    print(f'Total match questions: {count_total}')
    print(f'Match questions with answer field: {count_with_answer}')
    print(f'Match questions missing answer field: {count_total - count_with_answer}')

if __name__ == "__main__":
    count_match_questions() 