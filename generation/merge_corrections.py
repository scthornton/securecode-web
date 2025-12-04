#!/usr/bin/env python3
"""
Merge corrected examples back into Batch 007.

Replaces examples 026, 027, 028, 031, 032, 033, 034 with corrected versions.
Keeps examples 029, 030, 035 (which already passed validation).
"""

import json
from pathlib import Path


def main():
    data_dir = Path(__file__).parent.parent / 'data'

    original_file = data_dir / 'command_injection_batch_007.jsonl'
    corrections_file = data_dir / 'batch_007_corrections.jsonl'
    output_file = original_file  # Will overwrite

    print("Merging Batch 007 corrections...")
    print("=" * 60)

    # Read original examples
    original_examples = {}
    with open(original_file, 'r', encoding='utf-8') as f:
        for line in f:
            ex = json.loads(line)
            original_examples[ex['id']] = ex

    print(f"Loaded {len(original_examples)} original examples")

    # Read corrections
    corrections = {}
    with open(corrections_file, 'r', encoding='utf-8') as f:
        for line in f:
            ex = json.loads(line)
            corrections[ex['id']] = ex

    print(f"Loaded {len(corrections)} corrected examples")

    # Backup original
    backup_file = data_dir / f"{original_file.stem}_pre_merge.jsonl"
    import shutil
    shutil.copy(original_file, backup_file)
    print(f"Backup: {backup_file.name}")

    # Merge: use corrections for IDs that exist in corrections, else use original
    merged = {}
    for ex_id in sorted(original_examples.keys()):
        if ex_id in corrections:
            merged[ex_id] = corrections[ex_id]
            print(f"  ✓ Replaced {ex_id} with corrected version")
        else:
            merged[ex_id] = original_examples[ex_id]
            print(f"  → Kept original {ex_id}")

    # Write merged file (sorted by ID)
    with open(output_file, 'w', encoding='utf-8') as f:
        for ex_id in sorted(merged.keys()):
            f.write(json.dumps(merged[ex_id], ensure_ascii=False) + '\n')

    print(f"\n✓ Merged {len(merged)} examples")
    print(f"✓ Output: {output_file}")
    print(f"\nNext: Run validation with 'python3 validate_all_batches.py'")

    return 0


if __name__ == "__main__":
    exit(main())
