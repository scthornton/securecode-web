#!/usr/bin/env python3
"""
Analyze all failing examples across batches 003, 005, 006.
Generate a comprehensive fix plan.
"""

import subprocess
import re


def main():
    print("Analyzing All Failing Examples")
    print("=" * 80)

    # Run validation
    result = subprocess.run(
        ['python3', 'validate_all_batches.py'],
        capture_output=True,
        text=True,
        cwd='/Users/scott/perfecxion/datasets/securecode/v2/generation'
    )

    output = result.stdout

    # Extract failures
    failures = []
    current_batch = None

    for line in output.split('\n'):
        if 'Validating: Batch' in line:
            current_batch = line.split('Validating: ')[1]

        if '✗ FAILED:' in line:
            # Extract example ID
            match = re.search(r'FAILED: ([\w-]+)', line)
            if match:
                ex_id = match.group(1)
                failures.append({'batch': current_batch, 'id': ex_id, 'errors': []})

        # Collect error messages for current failure
        if failures and '[ERROR]' in line:
            error = line.strip()
            failures[-1]['errors'].append(error)

    # Print summary
    print(f"\nTotal Failing Examples: {len(failures)}\n")

    # Group by batch
    batches = {}
    for failure in failures:
        batch = failure['batch']
        if batch not in batches:
            batches[batch] = []
        batches[batch].append(failure)

    # Print organized report
    for batch_name, batch_failures in sorted(batches.items()):
        print(f"\n{batch_name}")
        print("-" * 80)
        print(f"Failures: {len(batch_failures)}\n")

        for failure in batch_failures:
            print(f"  {failure['id']}")
            for error in failure['errors'][:3]:  # First 3 errors
                print(f"    {error}")
            print()

    # Categorize errors
    print("\n" + "=" * 80)
    print("ERROR CATEGORIZATION")
    print("=" * 80)

    error_types = {}
    for failure in failures:
        for error in failure['errors']:
            # Categorize error
            if 'ES module' in error or 'ES6' in error or 'import' in error:
                error_type = 'ES6_MODULE_SYNTAX'
            elif 'Schema validation failed' in error:
                error_type = 'SCHEMA_VALIDATION'
            elif 'Syntax error' in error:
                error_type = 'CODE_SYNTAX'
            elif 'innerHTML' in error or 'XSS risk' in error:
                error_type = 'SECURITY_PATTERN'
            elif 'No code blocks' in error:
                error_type = 'MISSING_CODE'
            else:
                error_type = 'OTHER'

            if error_type not in error_types:
                error_types[error_type] = []

            error_types[error_type].append({
                'id': failure['id'],
                'batch': failure['batch'],
                'error': error
            })

    for error_type, occurrences in sorted(error_types.items()):
        print(f"\n{error_type}: {len(occurrences)} occurrences")
        # Show unique examples affected
        unique_ids = set(occ['id'] for occ in occurrences)
        print(f"  Affected examples: {', '.join(sorted(unique_ids))}")

    # Generate fix recommendations
    print("\n" + "=" * 80)
    print("FIX RECOMMENDATIONS")
    print("=" * 80)

    if 'ES6_MODULE_SYNTAX' in error_types:
        print("\n1. ES6 Module Syntax Issues:")
        affected = set(occ['id'] for occ in error_types['ES6_MODULE_SYNTAX'])
        print(f"   Affected: {', '.join(sorted(affected))}")
        print("   Fix: Wrap top-level await in async IIFE (like we did for 033)")

    if 'SCHEMA_VALIDATION' in error_types:
        print("\n2. Schema Validation Issues:")
        affected = set(occ['id'] for occ in error_types['SCHEMA_VALIDATION'])
        print(f"   Affected: {', '.join(sorted(affected))}")
        print("   Fix: Add missing required fields (created, validated, etc.)")

    if 'SECURITY_PATTERN' in error_types:
        print("\n3. Security Pattern Issues:")
        affected = set(occ['id'] for occ in error_types['SECURITY_PATTERN'])
        print(f"   Affected: {', '.join(sorted(affected))}")
        print("   Fix: Replace innerHTML with textContent or use DOMPurify")

    if 'MISSING_CODE' in error_types:
        print("\n4. Missing Code Blocks:")
        affected = set(occ['id'] for occ in error_types['MISSING_CODE'])
        print(f"   Affected: {', '.join(sorted(affected))}")
        print("   Fix: Verify code fence markers (```language)")

    print("\n" + "=" * 80)
    print(f"Total fixes needed: {len(failures)} examples")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    exit(main())
