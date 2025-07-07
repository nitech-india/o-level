import os
import yaml
from collections import OrderedDict

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '_data')
OUTPUT_FILE = os.path.join(DATA_DIR, 'breadcrumbs.yml')

# Mapping for module codes to URL slugs and display names
def get_module_map():
    return OrderedDict([
        ('m1r5', {
            'title': 'IT Tools',
            'slug': 'm1r5',
            'practice_slug': 'm1r5-practice',
            'comprehensive_slug': 'm1r5-comprehensive',
        }),
        ('m2r5', {
            'title': 'Web Design',
            'slug': 'm2r5',
            'practice_slug': 'm2r5-practice',
            'comprehensive_slug': 'm2r5-comprehensive',
        }),
        ('m3r5', {
            'title': 'Programming in Python',
            'slug': 'm3r5',
            'practice_slug': 'm3r5-practice',
            'comprehensive_slug': 'm3r5-comprehensive',
        }),
        ('m4r5', {
            'title': 'IoT',
            'slug': 'm4r5',
            'practice_slug': 'm4r5-practice',
            'comprehensive_slug': 'm4r5-comprehensive',
        }),
    ])

# Helper to load YAML safely
def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_sets_from_file(path):
    data = load_yaml(path)
    sets = data.get('sets', [])
    return sets

def build_breadcrumbs():
    module_map = get_module_map()
    children = []

    # Modules
    for mod_key, mod_info in module_map.items():
        mod_children = []
        # Practice sets
        practice_file = f'{mod_key}_practice.yml'
        practice_path = os.path.join(DATA_DIR, practice_file)
        practice_sets = get_sets_from_file(practice_path) if os.path.exists(practice_path) else []
        practice_set_nodes = []
        for s in practice_sets:
            set_name = s.get('name', f'Practice Set {s.get("id")}' )
            set_id = s.get('id')
            url = f'/{mod_info["slug"]}/{mod_info["practice_slug"]}/{mod_info["practice_slug"]}-{set_id}/'
            practice_set_nodes.append({
                'title': set_name,
                'url': url
            })
        mod_children.append({
            'title': 'Practice Sets',
            'url': f'/{mod_info["slug"]}/{mod_info["practice_slug"]}/',
            'children': practice_set_nodes
        })
        # Comprehensive sets
        comp_file = f'{mod_key}_comprehensive.yml'
        comp_path = os.path.join(DATA_DIR, comp_file)
        comp_sets = get_sets_from_file(comp_path) if os.path.exists(comp_path) else []
        comp_set_nodes = []
        for s in comp_sets:
            set_id = s.get('id')
            url = f'/{mod_info["slug"]}/{mod_info["comprehensive_slug"]}/{mod_info["comprehensive_slug"]}-{set_id}/'
            comp_set_nodes.append({
                'title': f'Practice Set {set_id}',
                'url': url
            })
        mod_children.append({
            'title': 'Comprehensive Sets',
            'url': f'/{mod_info["slug"]}/{mod_info["comprehensive_slug"]}/',
            'children': comp_set_nodes
        })
        children.append({
            'title': mod_info['title'],
            'url': f'/{mod_info["slug"]}/',
            'children': mod_children
        })

    # Question types
    # Match Together
    match_file = 'match_together_questions.yml'
    match_path = os.path.join(DATA_DIR, match_file)
    match_sets = get_sets_from_file(match_path) if os.path.exists(match_path) else []
    match_nodes = []
    for s in match_sets:
        set_name = s.get('name', f'Match Together Questions ({s.get("id")})')
        set_id = s.get('id')
        url = f'/question-types/match-together-questions/match-together-questions-{set_id}/'
        match_nodes.append({
            'title': set_name,
            'url': url
        })
    children.append({
        'title': 'Match Together Questions',
        'url': '/question-types/match-together-questions/',
        'children': match_nodes
    })
    # Multiple Answer
    multi_file = 'multiple_answer_questions.yml'
    multi_path = os.path.join(DATA_DIR, multi_file)
    multi_sets = get_sets_from_file(multi_path) if os.path.exists(multi_path) else []
    multi_nodes = []
    for s in multi_sets:
        set_name = s.get('name', 'Multiple Answer Questions')
        set_id = s.get('id')
        url = f'/question-types/multiple-answer-questions/multiple-answer-questions-{set_id}/'
        multi_nodes.append({
            'title': set_name,
            'url': url
        })
    children.append({
        'title': 'Multiple Answer Questions',
        'url': '/question-types/multiple-answer-questions/',
        'children': multi_nodes
    })

    # Home root
    root = [{
        'title': 'Home',
        'url': '/',
        'children': children
    }]
    return root

def main():
    breadcrumbs = build_breadcrumbs()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.safe_dump(breadcrumbs, f, allow_unicode=True, sort_keys=False)
    print(f'Breadcrumbs YAML written to {OUTPUT_FILE}')

if __name__ == '__main__':
    main() 