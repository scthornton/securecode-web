#!/usr/bin/env python3
"""
SecureCode v2.0: OWASP 2025 Migration Validation Script

Validates that migration from OWASP 2021 to 2025 was successful.

Usage:
    python validate_owasp_migration.py

Author: Dataset Integrity Expert
Date: 2025-12-16
"""

import json
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple

# Expected post-migration distribution (from actual dataset analysis)
EXPECTED_DISTRIBUTION = {
    "A01:2025-Broken Access Control": 224,
    "A02:2025-Security Misconfiguration": 134,
    "A03:2025-Software Supply Chain Failures": 85,
    "A04:2025-Cryptographic Failures": 115,
    "A05:2025-Injection": 125,
    "A06:2025-Insecure Design": 84,
    "A07:2025-Authentication Failures": 199,
    "A08:2025-Software and Data Integrity Failures": 80,
    "A09:2025-Security Logging and Monitoring Failures": 59,
    "AI/ML Security Threats": 50,
    "Unknown": 60,
}

EXPECTED_TOTAL = 1215
EXPECTED_COUNTS = {
    "train": 989,
    "val": 122,
    "test": 104,
}

BASE_DIR = Path(__file__).parent.parent / "consolidated"
FILES = {
    "train": BASE_DIR / "train.jsonl",
    "val": BASE_DIR / "val.jsonl",
    "test": BASE_DIR / "test.jsonl",
}


class ValidationResults:
    """Track validation results"""
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.errors = []
        self.warnings = []

    def pass_test(self, test_name: str):
        self.tests_passed += 1
        print(f"✓ {test_name}")

    def fail_test(self, test_name: str, reason: str):
        self.tests_failed += 1
        self.errors.append(f"{test_name}: {reason}")
        print(f"✗ {test_name}: {reason}")

    def warn(self, warning: str):
        self.warnings.append(warning)
        print(f"⚠  {warning}")

    def print_summary(self):
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")
        print(f"Warnings: {len(self.warnings)}")

        if self.errors:
            print("\nFAILURES:")
            for error in self.errors:
                print(f"  ✗ {error}")

        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠  {warning}")

        status = "PASSED" if self.tests_failed == 0 else "FAILED"
        emoji = "✅" if self.tests_failed == 0 else "❌"
        print(f"\n{emoji} VALIDATION {status}")


def validate_file_structure(filepath: Path, results: ValidationResults) -> Dict:
    """Validate file exists and has correct structure"""
    stats = {
        "entries": 0,
        "has_owasp_2021": 0,  # Should be 0 after migration
        "has_owasp_2025": 0,  # Should equal entries after migration
        "categories": Counter(),
    }

    if not filepath.exists():
        results.fail_test(f"File exists: {filepath.name}", "File not found")
        return stats

    results.pass_test(f"File exists: {filepath.name}")

    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line)
                stats["entries"] += 1

                metadata = entry.get('metadata', {})

                # Check for old field (should be removed)
                if 'owasp_2021' in metadata:
                    stats["has_owasp_2021"] += 1

                # Check for new field (should exist)
                if 'owasp_2025' in metadata:
                    stats["has_owasp_2025"] += 1
                    category = metadata['owasp_2025']
                    stats["categories"][category] += 1

            except json.JSONDecodeError as e:
                results.fail_test(
                    f"JSON integrity: {filepath.name} line {line_num}",
                    f"Parse error: {e}"
                )

    return stats


def validate_field_migration(stats: Dict, filename: str, results: ValidationResults):
    """Validate field migration was successful"""
    entries = stats["entries"]

    # All entries should have owasp_2025
    if stats["has_owasp_2025"] == entries:
        results.pass_test(f"All entries have owasp_2025: {filename}")
    else:
        results.fail_test(
            f"All entries have owasp_2025: {filename}",
            f"{stats['has_owasp_2025']}/{entries} entries have field"
        )

    # No entries should have owasp_2021
    if stats["has_owasp_2021"] == 0:
        results.pass_test(f"No entries have owasp_2021: {filename}")
    else:
        results.fail_test(
            f"No entries have owasp_2021: {filename}",
            f"{stats['has_owasp_2021']} entries still have old field"
        )


def validate_entry_counts(all_stats: Dict[str, Dict], results: ValidationResults):
    """Validate entry counts match expectations"""
    for split, stats in all_stats.items():
        expected = EXPECTED_COUNTS[split]
        actual = stats["entries"]

        if actual == expected:
            results.pass_test(f"Entry count: {split}.jsonl ({actual} entries)")
        else:
            results.fail_test(
                f"Entry count: {split}.jsonl",
                f"Expected {expected}, got {actual}"
            )

    # Total count
    total = sum(s["entries"] for s in all_stats.values())
    if total == EXPECTED_TOTAL:
        results.pass_test(f"Total entry count ({total})")
    else:
        results.fail_test(
            "Total entry count",
            f"Expected {EXPECTED_TOTAL}, got {total}"
        )


def validate_category_distribution(all_stats: Dict[str, Dict], results: ValidationResults):
    """Validate OWASP 2025 category distribution"""
    # Combine all category counts
    combined = Counter()
    for stats in all_stats.values():
        combined.update(stats["categories"])

    print("\n" + "="*80)
    print("OWASP 2025 CATEGORY DISTRIBUTION")
    print("="*80)

    all_match = True
    for category in sorted(EXPECTED_DISTRIBUTION.keys()):
        expected = EXPECTED_DISTRIBUTION[category]
        actual = combined[category]

        status = "✓" if actual == expected else "✗"
        diff = actual - expected

        if actual == expected:
            print(f"{status} {category:60} {actual:4} (expected: {expected})")
        else:
            print(f"{status} {category:60} {actual:4} (expected: {expected}, diff: {diff:+d})")
            all_match = False

    # Check for unexpected categories
    unexpected = set(combined.keys()) - set(EXPECTED_DISTRIBUTION.keys())
    if unexpected:
        results.warn(f"Unexpected categories found: {unexpected}")
        for cat in unexpected:
            print(f"⚠  Unexpected: {cat:60} {combined[cat]:4}")

    if all_match:
        results.pass_test("Category distribution matches expectations")
    else:
        results.fail_test(
            "Category distribution",
            "Some categories have incorrect counts"
        )


def validate_sample_entries(results: ValidationResults):
    """Manually inspect sample entries from each file"""
    print("\n" + "="*80)
    print("SAMPLE ENTRY INSPECTION")
    print("="*80)

    for split, filepath in FILES.items():
        if not filepath.exists():
            continue

        with open(filepath, 'r') as f:
            # Read first entry
            entry = json.loads(f.readline())

            print(f"\n{split.upper()} - Entry ID: {entry.get('id', 'unknown')}")
            metadata = entry.get('metadata', {})

            # Check for old field
            if 'owasp_2021' in metadata:
                results.fail_test(
                    f"Sample entry check: {split}",
                    f"Entry {entry.get('id')} still has owasp_2021 field"
                )
                print(f"  ✗ Has owasp_2021: {metadata['owasp_2021']}")

            # Check for new field
            if 'owasp_2025' in metadata:
                print(f"  ✓ Has owasp_2025: {metadata['owasp_2025']}")
            else:
                results.fail_test(
                    f"Sample entry check: {split}",
                    f"Entry {entry.get('id')} missing owasp_2025 field"
                )
                print(f"  ✗ Missing owasp_2025 field")

    results.pass_test("Sample entry inspection completed")


def main():
    """Main validation workflow"""
    print("="*80)
    print("SecureCode v2.0: OWASP 2025 Migration Validation")
    print("="*80)

    results = ValidationResults()
    all_stats = {}

    # Validate each file
    print("\n" + "="*80)
    print("FILE STRUCTURE VALIDATION")
    print("="*80)

    for split, filepath in FILES.items():
        stats = validate_file_structure(filepath, results)
        all_stats[split] = stats
        validate_field_migration(stats, filepath.name, results)

    # Validate entry counts
    print("\n" + "="*80)
    print("ENTRY COUNT VALIDATION")
    print("="*80)
    validate_entry_counts(all_stats, results)

    # Validate category distribution
    validate_category_distribution(all_stats, results)

    # Sample entry inspection
    validate_sample_entries(results)

    # Print summary
    results.print_summary()

    # Exit with appropriate code
    exit(0 if results.tests_failed == 0 else 1)


if __name__ == "__main__":
    main()
