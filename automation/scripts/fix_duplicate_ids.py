#!/usr/bin/env python3
"""
Fix Duplicate IDs in SecureCode v2.0 Dataset

This script regenerates unique IDs for all examples to resolve the critical
duplicate ID issue found in QA review.

New ID Format: {category}-{global_index:06d}-{content_hash:8}
Example: injection-000042-a3f5d8c9

Usage:
    python3 fix_duplicate_ids.py
    python3 fix_duplicate_ids.py --verify-only
"""

import json
import hashlib
import argparse
from pathlib import Path
from collections import Counter

def generate_content_hash(example):
    """Generate MD5 hash of conversation content for uniqueness."""
    content = json.dumps(example.get('conversations', []), sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()[:8]

def regenerate_ids(input_file, output_file, start_index=0):
    """
    Regenerate unique IDs for all examples in a file.

    Args:
        input_file: Path to input JSONL file
        output_file: Path to output JSONL file with fixed IDs
        start_index: Starting index for global ID numbering

    Returns:
        Tuple of (examples_processed, next_index)
    """
    examples = []

    # Read all examples
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))

    # Regenerate IDs
    current_index = start_index
    for example in examples:
        category = example['metadata']['category']
        content_hash = generate_content_hash(example)

        # New unique ID format
        new_id = f"{category}-{current_index:06d}-{content_hash}"
        example['id'] = new_id

        current_index += 1

    # Write fixed examples
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example) + '\n')

    return len(examples), current_index

def verify_uniqueness(file_paths):
    """
    Verify all IDs are unique across all files.

    Args:
        file_paths: List of JSONL file paths to check

    Returns:
        Tuple of (is_unique, duplicate_count, total_ids)
    """
    all_ids = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    example = json.loads(line)
                    all_ids.append(example['id'])

    id_counts = Counter(all_ids)
    duplicates = [(id, count) for id, count in id_counts.items() if count > 1]

    return len(duplicates) == 0, len(duplicates), len(all_ids)

def main():
    parser = argparse.ArgumentParser(description='Fix duplicate IDs in SecureCode v2.0')
    parser.add_argument('--verify-only', action='store_true',
                        help='Only verify uniqueness, do not fix')
    parser.add_argument('--input-dir', default='consolidated',
                        help='Input directory (default: consolidated)')
    parser.add_argument('--output-dir', default='consolidated_fixed',
                        help='Output directory (default: consolidated_fixed)')
    parser.add_argument('--in-place', action='store_true',
                        help='Fix files in place (overwrites originals)')

    args = parser.parse_args()

    base_path = Path('/Users/scott/perfecxion/datasets/securecode/v2')
    input_dir = base_path / args.input_dir

    splits = ['train', 'val', 'test']
    input_files = [input_dir / f'{split}.jsonl' for split in splits]

    # Verify all input files exist
    for file_path in input_files:
        if not file_path.exists():
            print(f"❌ Error: {file_path} not found")
            return 1

    if args.verify_only:
        print("VERIFICATION MODE - Checking ID uniqueness...")
        print("=" * 70)

        is_unique, dup_count, total = verify_uniqueness(input_files)

        if is_unique:
            print(f"✅ All {total} IDs are unique across all splits")
            return 0
        else:
            print(f"❌ Found {dup_count} duplicate IDs out of {total} total")
            print(f"   Unique IDs: {total - dup_count}")
            return 1

    # FIX MODE
    print("FIXING DUPLICATE IDs")
    print("=" * 70)

    # Create output directory
    if args.in_place:
        output_dir = input_dir
        print("⚠️  IN-PLACE MODE: Original files will be overwritten")
        print("Creating backups first...")

        # Create backups
        backup_dir = base_path / f'{args.input_dir}_backup'
        backup_dir.mkdir(exist_ok=True)

        for split in splits:
            src = input_dir / f'{split}.jsonl'
            dst = backup_dir / f'{split}.jsonl'
            import shutil
            shutil.copy2(src, dst)
            print(f"   Backed up {split}.jsonl")

        print(f"✅ Backups saved to {backup_dir}")
    else:
        output_dir = base_path / args.output_dir
        output_dir.mkdir(exist_ok=True)
        print(f"Output directory: {output_dir}")

    print()

    # Process each split with continuous indexing
    global_index = 0
    total_processed = 0

    for split in splits:
        input_file = input_dir / f'{split}.jsonl'
        output_file = output_dir / f'{split}.jsonl'

        print(f"Processing {split}.jsonl...")
        count, global_index = regenerate_ids(input_file, output_file, global_index)
        total_processed += count
        print(f"   ✅ Regenerated {count} IDs (indices {global_index-count} to {global_index-1})")

    print()
    print(f"TOTAL: Regenerated {total_processed} unique IDs")
    print()

    # Verify the fix worked
    print("Verifying uniqueness of fixed files...")
    output_files = [output_dir / f'{split}.jsonl' for split in splits]

    is_unique, dup_count, total = verify_uniqueness(output_files)

    if is_unique:
        print(f"✅ SUCCESS: All {total} IDs are now unique!")

        if not args.in_place:
            print()
            print("Next steps:")
            print(f"1. Review fixed files in: {output_dir}")
            print(f"2. If satisfied, replace original files:")
            print(f"   mv {output_dir}/*.jsonl {input_dir}/")
            print(f"3. Update metadata.json if needed")

        return 0
    else:
        print(f"❌ ERROR: Still have {dup_count} duplicates after fix")
        return 1

if __name__ == '__main__':
    exit(main())
