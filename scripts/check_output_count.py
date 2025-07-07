import yaml

def check_output_counts():
    """
    Check how many questions are in the output files.
    """
    try:
        # Check match questions
        with open('_data/match_together_questions.yml', 'r', encoding='utf-8') as f:
            match_data = yaml.safe_load(f)
        match_count = len(match_data['sets'][0]['questions'])
        print(f'Match questions in output: {match_count}')
        
        # Check multiple answer questions
        with open('_data/multiple_answer_questions.yml', 'r', encoding='utf-8') as f:
            multiple_data = yaml.safe_load(f)
        multiple_count = len(multiple_data['sets'][0]['questions'])
        print(f'Multiple answer questions in output: {multiple_count}')
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_output_counts() 