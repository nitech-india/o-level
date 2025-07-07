import re

def fix_code_question(line):
    # Look for triple backtick code in the line
    m = re.match(r'text:\s*["\']?(.*)```python\s*(.*?)\s*```["\']?$', line)
    if m:
        question = m.group(1).strip()
        code = m.group(2).strip()
        # Split code into lines for proper indentation
        code_lines = code.split(';')
        code_block = '\n'.join(['  ' + l.strip() for l in code_lines if l.strip()])
        return f'text: |\n  {question}\n\n  ```python\n{code_block}\n  ```\n'
    return None

with open('_data/m3r5_practice.yml', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip().startswith('text:'):
        fixed = fix_code_question(line)
        if fixed:
            new_lines.append(fixed)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('_data/m3r5_practice_fixed.yml', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
