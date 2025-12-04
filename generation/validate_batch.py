"""
Validate generated examples using the validation framework
"""

import json
import sys
from pathlib import Path
from validators import DatasetValidator

def main():
    # Load schema
    schema_path = Path(__file__).parent.parent / 'schema.json'
    validator = DatasetValidator(schema_path)

    # Load examples
    data_file = Path(__file__).parent.parent / 'data' / 'sql_injection_batch_001.jsonl'

    if not data_file.exists():
        print(f"Error: {data_file} not found")
        sys.exit(1)

    examples = []
    with open(data_file, 'r') as f:
        for line in f:
            examples.append(json.loads(line))

    print(f"Validating {len(examples)} examples...")
    print("=" * 60)

    # Validate each example
    results = []
    for example in examples:
        result = validator.validate_example(example)
        results.append(result)

        status = "✓ PASSED" if result.passed else "✗ FAILED"
        print(f"\n{status}: {example['id']}")
        print(f"  Language: {example['metadata']['lang']}")
        print(f"  Subcategory: {example['metadata']['subcategory']}")
        print(f"  Turns: {len(example['conversations'])}")

        # Show check results
        for check, status in result.checks.items():
            symbol = "✓" if status == "passed" else ("✗" if status == "failed" else "○")
            print(f"    {symbol} {check}: {status}")

        # Show issues if any
        if result.issues:
            print(f"  Issues ({len(result.issues)}):")
            for issue in result.issues:
                severity = issue['severity']
                print(f"    [{severity}] {issue['message']}")

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)

    print(f"Total examples: {len(results)}")
    print(f"Passed: {passed} ({passed/len(results)*100:.1f}%)")
    print(f"Failed: {failed} ({failed/len(results)*100:.1f}%)")

    # Save validation report
    report_file = Path(__file__).parent.parent / 'validation' / 'reports' / 'batch_001_report.json'
    report_file.parent.mkdir(parents=True, exist_ok=True)

    report = {
        'total': len(results),
        'passed': passed,
        'failed': failed,
        'pass_rate': passed / len(results) * 100,
        'results': [r.to_dict() for r in results]
    }

    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n✓ Validation report saved to: {report_file}")

    # Exit with error code if any failed
    if failed > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
