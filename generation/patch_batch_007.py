#!/usr/bin/env python3
"""
Directly patch known syntax errors in Batch 007 JSONL file.

This script makes surgical fixes to specific known issues without breaking JSON structure.
"""

import json
from pathlib import Path


def main():
    data_file = Path(__file__).parent.parent / 'data' / 'command_injection_batch_007.jsonl'

    print("Patching Batch 007 syntax errors...")
    print("=" * 60)

    # Read all examples
    examples = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))

    print(f"Loaded {len(examples)} examples")

    # Backup
    backup_file = data_file.parent / f"{data_file.stem}_pre_patch.jsonl"
    import shutil
    shutil.copy(data_file, backup_file)
    print(f"Backup: {backup_file.name}")

    # Apply patches
    for i, example in enumerate(examples):
        ex_id = example['id']
        lang = example['metadata']['lang']

        # Remove smart quotes (affects all examples, especially Ruby)
        for conv in example['conversations']:
            content = conv['value']
            # Smart quotes to ASCII
            content = content.replace('"', '"').replace('"', '"')
            content = content.replace(''', "'").replace(''', "'")
            content = content.replace('…', '...')
            content = content.replace('–', '-').replace('—', '--')
            conv['value'] = content

    # Write patched examples
    with open(data_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\\n')

    print(f"✓ Patched {len(examples)} examples")
    print(f"✓ Output: {data_file}")

    return 0


if __name__ == "__main__":
    exit(main())
