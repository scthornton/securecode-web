import json
import re
from collections import defaultdict


def analyze_sampled_examples(file_path):
    results = {
        'total_examples': 0,
        'structural_issues': [],
        'missing_fields': defaultdict(int),
        'conversation_lengths': defaultdict(int),
        'languages': defaultdict(int),
        'categories': defaultdict(int),
        'severities': defaultdict(int),
        'owasp_categories': defaultdict(int),
        'validation_status': defaultdict(int),
        'real_world_context': 0,
        'cve_present': 0,
        'code_blocks': 0,
        'syntax_issues': [],
        'security_accuracy_issues': [],
        'completeness_issues': []
    }

    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                example = json.loads(line.strip())
                results['total_examples'] += 1

                # Structural validity
                required_fields = ['id', 'metadata',
                                   'context', 'conversations', 'validation']
                for field in required_fields:
                    if field not in example:
                        results['missing_fields'][field] += 1
                        results['structural_issues'].append(
                            f"Line {line_num}: Missing {field}")

                if 'conversations' in example:
                    conv_len = len(example['conversations'])
                    results['conversation_lengths'][conv_len] += 1

                    # Check for 4 conversations
                    if conv_len != 4:
                        results['completeness_issues'].append(
                            f"Line {line_num}: Has {conv_len} conversations, expected 4")

                    # Check conversation structure
                    for i, conv in enumerate(example['conversations']):
                        if 'turn' not in conv or 'from' not in conv or 'value' not in conv:
                            results['structural_issues'].append(
                                f"Line {line_num}: Conversation {i+1} missing required fields")

                # Metadata analysis
                if 'metadata' in example:
                    meta = example['metadata']
                    results['languages'][meta.get('lang', 'unknown')] += 1
                    results['categories'][meta.get('category', 'unknown')] += 1
                    results['severities'][meta.get('severity', 'unknown')] += 1
                    results['owasp_categories'][meta.get(
                        'owasp_2021', 'unknown')] += 1

                # Context analysis
                if 'context' in example:
                    if 'real_world_incident' in example['context'] and example['context']['real_world_incident']:
                        results['real_world_context'] += 1
                    if 'cve' in example['context'] and example['context']['cve']:
                        results['cve_present'] += 1

                # Validation status
                if 'validation' in example:
                    val = example['validation']
                    for key in ['syntax_check', 'security_review', 'code_execution']:
                        status = val.get(key, 'unknown')
                        results['validation_status'][f"{key}:{status}"] += 1

                # Code blocks count (rough estimate)
                all_text = json.dumps(example)
                code_blocks = len(re.findall(
                    r'```[\w]*\n.*?```', all_text, re.DOTALL))
                results['code_blocks'] += code_blocks

                # Basic syntax check for code blocks
                code_pattern = r'```(\w+)?\n(.*?)\n```'
                for match in re.finditer(code_pattern, all_text, re.DOTALL):
                    lang = match.group(1) or 'unknown'
                    code = match.group(2)
                    # Very basic checks
                    if lang.lower() in ['python', 'py']:
                        if 'def ' in code and not code.strip().endswith(':'):
                            results['syntax_issues'].append(
                                f"Line {line_num}: Python function without colon")
                    elif lang.lower() in ['javascript', 'js']:
                        if 'function' in code and not '(' in code:
                            results['syntax_issues'].append(
                                f"Line {line_num}: JS function syntax issue")

            except json.JSONDecodeError as e:
                results['structural_issues'].append(
                    f"Line {line_num}: JSON decode error: {e}")

    return results


if __name__ == "__main__":
    results = analyze_sampled_examples('sampled_train.jsonl')
    print(json.dumps(results, indent=2))
