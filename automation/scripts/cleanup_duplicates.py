#!/usr/bin/env python3
"""
Clean up duplicate batch files by archiving backups and variants
"""

from pathlib import Path
import shutil
import re
from collections import defaultdict

def main():
    data_dir = Path(__file__).parent.parent.parent / 'data'
    archive_dir = data_dir / '_archived_duplicates'
    archive_dir.mkdir(exist_ok=True)

    # Find all batch files
    batch_files = list(data_dir.glob('*_batch_*.jsonl'))

    # Group by batch number
    batch_groups = defaultdict(list)
    for f in batch_files:
        match = re.search(r'batch_(\d+)', f.name)
        if match:
            batch_num = int(match.group(1))
            batch_groups[batch_num].append(f)

    # Identify duplicates and primary files
    print("Identifying duplicate files...\n")

    duplicates_to_archive = []
    exclude_patterns = ['_backup', '_before_', '_pre_', '_final_fix']

    for batch_num, files in sorted(batch_groups.items()):
        if len(files) > 1:
            # Find the primary file (without suffix patterns)
            primary = None
            others = []

            for f in files:
                if any(pattern in f.name for pattern in exclude_patterns):
                    others.append(f)
                else:
                    if primary is None:
                        primary = f
                    else:
                        # If multiple files without patterns, keep the larger one
                        if f.stat().st_size > primary.stat().st_size:
                            others.append(primary)
                            primary = f
                        else:
                            others.append(f)

            if others:
                print(f"Batch {batch_num:03d}:")
                print(f"  Keeping: {primary.name}")
                print(f"  Archiving: {len(others)} duplicate(s)")
                for other in others:
                    print(f"    - {other.name}")
                duplicates_to_archive.extend(others)
                print()

    # Archive duplicates
    if duplicates_to_archive:
        print(f"\nArchiving {len(duplicates_to_archive)} duplicate files...")
        for f in duplicates_to_archive:
            dest = archive_dir / f.name
            shutil.move(str(f), str(dest))
            print(f"  ✓ Archived: {f.name}")

        print(f"\n✓ Archived {len(duplicates_to_archive)} files to {archive_dir}")
    else:
        print("✓ No duplicates found")

if __name__ == '__main__':
    main()
