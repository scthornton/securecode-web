#!/usr/bin/env python3
"""
Standardize csharp/c# language naming to 'csharp' throughout the dataset
"""

import json
from pathlib import Path

def main():
    data_dir = Path(__file__).parent.parent.parent / 'data'

    # Exclude backup/duplicate files
    exclude_patterns = ['_backup', '_before_', '_pre_', '_final_fix', '_archived']

    batch_files = []
    for f in sorted(data_dir.glob('*_batch_*.jsonl')):
        if any(pattern in f.name for pattern in exclude_patterns):
            continue
        batch_files.append(f)

    print(f"Checking {len(batch_files)} batch files for csharp/c# inconsistencies...\n")

    total_fixed = 0
    files_modified = []

    for batch_file in batch_files:
        examples = []
        modified = False

        with open(batch_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    example = json.loads(line)

                    # Check and fix lang field
                    lang = example.get('metadata', {}).get('lang', '')
                    if lang == 'c#':
                        example['metadata']['lang'] = 'csharp'
                        modified = True
                        total_fixed += 1
                        print(f"  Fixed: {batch_file.name} line {line_num}: 'c#' → 'csharp'")

                    examples.append(example)

                except json.JSONDecodeError as e:
                    print(f"  ERROR: {batch_file.name} line {line_num}: {e}")
                    continue

        # Write back if modified
        if modified:
            with open(batch_file, 'w') as f:
                for example in examples:
                    f.write(json.dumps(example) + '\n')
            files_modified.append(batch_file.name)

    print(f"\n{'='*60}")
    print("STANDARDIZATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total fixes: {total_fixed}")
    print(f"Files modified: {len(files_modified)}")

    if files_modified:
        print(f"\nModified files:")
        for fname in files_modified:
            print(f"  - {fname}")
    else:
        print("\n✓ No inconsistencies found")

if __name__ == '__main__':
    main()
