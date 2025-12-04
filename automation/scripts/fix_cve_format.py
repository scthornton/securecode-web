#!/usr/bin/env python3
"""
Fix CVE format issues: Change 'N/A - description' patterns to null
Per CONTRIBUTING.md: CVE should be CVE-YYYY-NNNNN format or null/"N/A"
"""

import json
from pathlib import Path
import re

def fix_cve_field(example):
    """
    Fix CVE field to comply with CONTRIBUTING.md standards
    """
    context = example.get('context', {})
    cve = context.get('cve', '')

    # If CVE is "N/A - description" pattern, set to null
    if cve and isinstance(cve, str):
        if cve.startswith('N/A -') or cve.startswith('N/A:') or (cve == 'N/A'):
            context['cve'] = None
            return True, f"Changed '{cve[:50]}' to null"
        elif not re.match(r'^CVE-\d{4}-\d+$', cve):
            # Invalid CVE format that isn't N/A pattern
            context['cve'] = None
            return True, f"Invalid format '{cve[:30]}', changed to null"

    return False, None

def process_file(file_path):
    """Process a single JSONL file"""
    print(f"\nProcessing: {file_path.name}")

    examples = []
    fixed_count = 0

    with open(file_path) as f:
        for line_num, line in enumerate(f, 1):
            example = json.loads(line)
            was_fixed, reason = fix_cve_field(example)

            if was_fixed:
                fixed_count += 1
                if fixed_count <= 5:  # Show first 5
                    print(f"  ✓ {example.get('id', f'line_{line_num}')}: {reason}")

            examples.append(example)

    # Write back
    with open(file_path, 'w') as f:
        for example in examples:
            f.write(json.dumps(example) + '\n')

    print(f"  Fixed {fixed_count}/{len(examples)} examples")
    return fixed_count, len(examples)

def main():
    print("="*80)
    print("CVE FORMAT FIX")
    print("="*80)
    print("\nFixing CVE fields to comply with CONTRIBUTING.md standards...")
    print("Pattern: 'N/A - description' → null\n")

    # Process data files
    data_dir = Path(__file__).parent.parent.parent / 'data'
    batch_files = sorted(data_dir.glob('*_batch_*.jsonl'))

    total_fixed = 0
    total_examples = 0

    for batch_file in batch_files:
        fixed, total = process_file(batch_file)
        total_fixed += fixed
        total_examples += total

    # Process consolidated files
    consolidated_dir = Path(__file__).parent.parent.parent / 'consolidated'
    for split_file in ['train.jsonl', 'val.jsonl', 'test.jsonl']:
        split_path = consolidated_dir / split_file
        if split_path.exists():
            fixed, total = process_file(split_path)
            total_fixed += fixed
            total_examples += total

    print("\n" + "="*80)
    print(f"COMPLETE: Fixed {total_fixed} CVE fields across {total_examples} total examples")
    print("="*80)

if __name__ == '__main__':
    main()
