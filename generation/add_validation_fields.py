#!/usr/bin/env python3
"""Add missing validation fields to Batch 007 examples."""

import json
from pathlib import Path
from datetime import date


def main():
    data_file = Path(__file__).parent.parent / 'data' / 'command_injection_batch_007.jsonl'

    print("Adding validation fields to Batch 007...")
    print("=" * 60)

    # Backup
    backup_file = data_file.parent / f"{data_file.stem}_pre_validation_fix.jsonl"
    import shutil
    shutil.copy(data_file, backup_file)
    print(f"Backup: {backup_file.name}")

    # Read examples
    examples = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))

    # Add validation field to any example missing it
    fixed_count = 0
    for example in examples:
        if 'validation' not in example:
            example['validation'] = {
                "syntax_check": "not_tested",
                "security_review": "not_reviewed",
                "code_execution": "not_tested",
                "encoding_check": "not_tested",
                "duplication_check": "not_tested",
                "reviewed_by": "automated-generator",
                "review_date": str(date.today()),
                "issues": []
            }
            print(f"  ✓ Added validation to {example['id']}")
            fixed_count += 1

    # Write back
    with open(data_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\n✓ Fixed {fixed_count} examples")
    print(f"✓ Output: {data_file}")

    return 0


if __name__ == "__main__":
    exit(main())
