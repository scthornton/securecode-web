#!/usr/bin/env python3
"""Fix validation fields in Batch 010"""

import json
from pathlib import Path

def fix_validation(example):
    """Fix validation field to match schema"""
    example['validation'] = {
        "syntax_check": "not_tested",
        "security_review": "not_reviewed",
        "code_execution": "not_tested",
        "encoding_check": "not_tested",
        "duplication_check": "not_tested",
        "reviewed_by": "automated-generator",
        "review_date": example['validation']['review_date'],
        "issues": []
    }
    return example

def main():
    input_file = Path(__file__).parent.parent / 'data' / 'sql_advanced_batch_010.jsonl'

    examples = []
    with open(input_file, 'r') as f:
        for line in f:
            example = json.loads(line)
            example = fix_validation(example)
            examples.append(example)

    # Write back
    with open(input_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"Fixed validation fields for {len(examples)} examples")

if __name__ == '__main__':
    main()
