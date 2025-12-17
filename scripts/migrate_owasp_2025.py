#!/usr/bin/env python3
"""
SecureCode v2.0: OWASP Top 10:2021 → 2025 Migration Script

Migrates dataset metadata from OWASP 2021 to OWASP 2025 taxonomy.
- Renames field: metadata.owasp_2021 → metadata.owasp_2025
- Updates values per OWASP 2025 mapping
- Validates data integrity throughout process

Usage:
    python migrate_owasp_2025.py --dry-run          # Validate only, no changes
    python migrate_owasp_2025.py                    # Execute migration
    python migrate_owasp_2025.py --rollback         # Restore from backups

Author: Dataset Integrity Expert
Date: 2025-12-16
"""

import json
import sys
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import Dict, Tuple, List

# OWASP 2021 → 2025 Migration Mapping
OWASP_MIGRATION_MAP = {
    "A01:2021-Broken Access Control": "A01:2025-Broken Access Control",
    "A02:2021-Cryptographic Failures": "A04:2025-Cryptographic Failures",
    "A03:2021-Injection": "A05:2025-Injection",
    "A04:2021-Insecure Design": "A06:2025-Insecure Design",
    "A05:2021-Security Misconfiguration": "A02:2025-Security Misconfiguration",
    "A06:2021-Vulnerable and Outdated Components": "A03:2025-Software Supply Chain Failures",
    "A07:2021-Identification and Authentication Failures": "A07:2025-Identification and Authentication Failures",
    "A08:2021-Software and Data Integrity Failures": "A08:2025-Software and Data Integrity Failures",
    "A09:2021-Security Logging and Monitoring Failures": "A09:2025-Security Logging and Monitoring Failures",
    "A10:2021-Server-Side Request Forgery": "A01:2025-Broken Access Control",
    # Special categories pass through unchanged
    "AI/ML Security Threats": "AI/ML Security Threats",
    "Unknown": "Unknown"
}

# File paths (relative to repository root)
BASE_DIR = Path(__file__).parent.parent / "consolidated"
FILES = ["train.jsonl", "val.jsonl", "test.jsonl"]


class MigrationStats:
    """Track migration statistics"""
    def __init__(self):
        self.total_entries = 0
        self.migrated_entries = 0
        self.unchanged_entries = 0
        self.errors = []
        self.category_counts_before = Counter()
        self.category_counts_after = Counter()

    def print_summary(self):
        """Print migration summary"""
        print("\n" + "="*80)
        print("MIGRATION SUMMARY")
        print("="*80)
        print(f"Total entries processed: {self.total_entries}")
        print(f"Entries migrated: {self.migrated_entries}")
        print(f"Entries unchanged (AI/ML, Unknown): {self.unchanged_entries}")
        print(f"Errors encountered: {len(self.errors)}")

        if self.errors:
            print("\nERRORS:")
            for error in self.errors[:10]:  # Show first 10
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more")

        print("\n" + "="*80)
        print("CATEGORY DISTRIBUTION AFTER MIGRATION")
        print("="*80)
        for category in sorted(self.category_counts_after.keys()):
            count = self.category_counts_after[category]
            pct = (count / self.total_entries * 100) if self.total_entries > 0 else 0
            print(f"{category:60} {count:4} ({pct:5.1f}%)")


def migrate_entry(entry: dict, stats: MigrationStats) -> dict:
    """
    Migrate single entry from OWASP 2021 to 2025.

    Args:
        entry: JSON entry to migrate
        stats: Statistics tracker

    Returns:
        Migrated entry
    """
    stats.total_entries += 1

    # Extract current OWASP 2021 category
    owasp_2021 = entry.get('metadata', {}).get('owasp_2021')

    if not owasp_2021:
        stats.errors.append(f"Entry {entry.get('id', 'unknown')} missing owasp_2021 field")
        return entry

    stats.category_counts_before[owasp_2021] += 1

    # Apply mapping
    owasp_2025 = OWASP_MIGRATION_MAP.get(owasp_2021, owasp_2021)

    # Track if this is a real change or passthrough
    if owasp_2021 not in ['AI/ML Security Threats', 'Unknown']:
        stats.migrated_entries += 1
    else:
        stats.unchanged_entries += 1

    stats.category_counts_after[owasp_2025] += 1

    # Rename field and update value
    entry['metadata']['owasp_2025'] = owasp_2025
    del entry['metadata']['owasp_2021']

    return entry


def validate_file(filepath: Path) -> Tuple[bool, List[str], int]:
    """
    Validate JSONL file integrity.

    Args:
        filepath: Path to JSONL file

    Returns:
        Tuple of (is_valid, errors, entry_count)
    """
    errors = []
    entry_count = 0

    try:
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    entry = json.loads(line)
                    entry_count += 1

                    # Validate required fields
                    if 'metadata' not in entry:
                        errors.append(f"Line {line_num}: Missing 'metadata' field")
                    elif 'owasp_2021' not in entry['metadata']:
                        errors.append(f"Line {line_num}: Missing 'metadata.owasp_2021' field")

                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: JSON parse error - {e}")

    except FileNotFoundError:
        errors.append(f"File not found: {filepath}")
        return False, errors, 0

    is_valid = len(errors) == 0
    return is_valid, errors, entry_count


def create_backup(filepath: Path) -> Path:
    """
    Create timestamped backup of file.

    Args:
        filepath: Path to file to backup

    Returns:
        Path to backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = filepath.with_suffix(f".jsonl.bak_{timestamp}")

    with open(filepath, 'r') as src, open(backup_path, 'w') as dst:
        dst.write(src.read())

    print(f"✓ Created backup: {backup_path.name}")
    return backup_path


def migrate_file(filepath: Path, dry_run: bool = False) -> MigrationStats:
    """
    Migrate entire JSONL file.

    Args:
        filepath: Path to JSONL file
        dry_run: If True, validate only without writing changes

    Returns:
        Migration statistics
    """
    stats = MigrationStats()

    print(f"\n{'='*80}")
    print(f"Processing: {filepath.name}")
    print(f"{'='*80}")

    # Validate file before processing
    print("Validating file integrity...")
    is_valid, errors, entry_count = validate_file(filepath)

    if not is_valid:
        print(f"✗ Validation FAILED ({len(errors)} errors):")
        for error in errors[:5]:
            print(f"  - {error}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more")
        return stats

    print(f"✓ Validation passed ({entry_count} entries)")

    if not dry_run:
        # Create backup
        backup_path = create_backup(filepath)

    # Process entries
    temp_path = filepath.with_suffix('.jsonl.tmp')

    try:
        with open(filepath, 'r') as infile, open(temp_path, 'w') as outfile:
            for line in infile:
                entry = json.loads(line)
                migrated = migrate_entry(entry, stats)

                if not dry_run:
                    outfile.write(json.dumps(migrated, ensure_ascii=False) + '\n')

        if not dry_run:
            # Replace original with migrated version
            temp_path.replace(filepath)
            print(f"✓ Migration complete: {stats.total_entries} entries processed")
        else:
            # Clean up temp file in dry-run mode
            temp_path.unlink()
            print(f"✓ Dry-run validation complete: {stats.total_entries} entries")

    except Exception as e:
        stats.errors.append(f"Migration failed: {e}")
        print(f"✗ Migration FAILED: {e}")

        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()

    return stats


def rollback_migration(filepath: Path):
    """
    Restore file from most recent backup.

    Args:
        filepath: Path to file to restore
    """
    # Find most recent backup
    backups = sorted(filepath.parent.glob(f"{filepath.stem}.jsonl.bak_*"), reverse=True)

    if not backups:
        print(f"✗ No backups found for {filepath.name}")
        return

    backup_path = backups[0]
    print(f"Restoring from backup: {backup_path.name}")

    # Restore backup
    with open(backup_path, 'r') as src, open(filepath, 'w') as dst:
        dst.write(src.read())

    print(f"✓ Restored {filepath.name} from {backup_path.name}")


def main():
    """Main migration workflow"""
    parser = argparse.ArgumentParser(
        description="Migrate SecureCode v2.0 from OWASP 2021 to 2025 taxonomy"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate migration without making changes'
    )
    parser.add_argument(
        '--rollback',
        action='store_true',
        help='Restore files from most recent backups'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        default=FILES,
        help='Specific files to migrate (default: all)'
    )

    args = parser.parse_args()

    print("="*80)
    print("SecureCode v2.0: OWASP Top 10:2021 → 2025 Migration")
    print("="*80)

    if args.rollback:
        print("\n⚠️  ROLLBACK MODE - Restoring from backups")
        for filename in args.files:
            filepath = BASE_DIR / filename
            rollback_migration(filepath)
        return

    if args.dry_run:
        print("\n🔍 DRY-RUN MODE - No changes will be made")
    else:
        print("\n⚠️  LIVE MODE - Files will be modified (backups created)")
        response = input("\nProceed with migration? (yes/no): ")
        if response.lower() != 'yes':
            print("Migration cancelled.")
            return

    # Process each file
    combined_stats = MigrationStats()

    for filename in args.files:
        filepath = BASE_DIR / filename

        if not filepath.exists():
            print(f"\n✗ File not found: {filepath}")
            continue

        stats = migrate_file(filepath, dry_run=args.dry_run)

        # Combine statistics
        combined_stats.total_entries += stats.total_entries
        combined_stats.migrated_entries += stats.migrated_entries
        combined_stats.unchanged_entries += stats.unchanged_entries
        combined_stats.errors.extend(stats.errors)
        combined_stats.category_counts_before.update(stats.category_counts_before)
        combined_stats.category_counts_after.update(stats.category_counts_after)

    # Print overall summary
    combined_stats.print_summary()

    if not args.dry_run and combined_stats.total_entries > 0:
        print("\n" + "="*80)
        print("MIGRATION COMPLETE")
        print("="*80)
        print(f"""
Next steps:
1. Verify migrated files manually (sample 5-10 entries)
2. Run: python scripts/validate_dataset.py
3. Update documentation:
   - README.md (OWASP taxonomy version)
   - dataset_card.md (metadata description)
4. Commit changes:
   git add consolidated/*.jsonl
   git commit -m "Migrate dataset from OWASP 2021 to 2025 taxonomy"

Backups created - can rollback with: python {Path(__file__).name} --rollback
        """)


if __name__ == "__main__":
    main()
