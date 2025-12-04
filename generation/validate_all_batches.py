"""
Validate all generated example batches
"""

import json
import sys
from pathlib import Path
from validators import DatasetValidator

def validate_batch(batch_name, data_file):
    """Validate a single batch"""
    print(f"\n{'='*60}")
    print(f"Validating: {batch_name}")
    print(f"{'='*60}")

    # Load examples
    examples = []
    with open(data_file, 'r') as f:
        for line in f:
            examples.append(json.loads(line))

    # Validate each example
    schema_path = Path(__file__).parent.parent / 'schema.json'
    validator = DatasetValidator(schema_path)

    results = []
    for example in examples:
        result = validator.validate_example(example)
        results.append(result)

        status = "✓ PASSED" if result.passed else "✗ FAILED"
        print(f"\n{status}: {example['id']}")
        print(f"  Language: {example['metadata']['lang']}")
        print(f"  Subcategory: {example['metadata']['subcategory']}")
        print(f"  Turns: {len(example['conversations'])}")

        # Show check results compactly
        checks_summary = []
        for check, status in result.checks.items():
            if status == "passed":
                checks_summary.append(f"✓{check[:8]}")
            elif status == "failed":
                checks_summary.append(f"✗{check[:8]}")

        print(f"  Checks: {' '.join(checks_summary)}")

        # Show issues if any
        if result.issues:
            print(f"  Issues ({len(result.issues)}):")
            for issue in result.issues[:3]:  # Show first 3
                print(f"    [{issue['severity']}] {issue['message'][:80]}")

    # Summary
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)

    print(f"\n{batch_name} Summary:")
    print(f"  Total: {len(results)}, Passed: {passed}, Failed: {failed}")
    print(f"  Pass Rate: {passed/len(results)*100:.1f}%")

    return passed, failed, len(results)

def main():
    data_dir = Path(__file__).parent.parent / 'data'

    batches = [
        ("Batch 001: SQL Injection", data_dir / 'sql_injection_batch_001.jsonl'),
        ("Batch 002: Command Injection", data_dir / 'command_injection_batch_002.jsonl'),
        ("Batch 003: XSS", data_dir / 'xss_batch_003.jsonl'),
        ("Batch 005: SQL Injection Expansion", data_dir / 'sql_injection_batch_005.jsonl'),
        ("Batch 006: NoSQL Injection", data_dir / 'nosql_injection_batch_006.jsonl'),
        ("Batch 007: Command Injection Expansion", data_dir / 'command_injection_batch_007.jsonl'),
        ("Batch 008: XSS Expansion Part 1", data_dir / 'xss_expansion_batch_008.jsonl'),
        ("Batch 009: Template Injection (SSTI) Part 1", data_dir / 'ssti_batch_009.jsonl'),
        ("Batch 010: SQL Injection Advanced", data_dir / 'sql_advanced_batch_010.jsonl'),
    ]

    total_passed = 0
    total_failed = 0
    total_examples = 0

    for batch_name, batch_file in batches:
        if not batch_file.exists():
            print(f"\n⚠ Skipping {batch_name} - file not found")
            continue

        passed, failed, count = validate_batch(batch_name, batch_file)
        total_passed += passed
        total_failed += failed
        total_examples += count

    # Overall summary
    print(f"\n{'='*60}")
    print("OVERALL SUMMARY")
    print(f"{'='*60}")
    print(f"Total Examples: {total_examples}")
    print(f"Passed: {total_passed} ({total_passed/total_examples*100:.1f}%)")
    print(f"Failed: {total_failed} ({total_failed/total_examples*100:.1f}%)")

    if total_failed > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
