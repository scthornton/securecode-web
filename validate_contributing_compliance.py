#!/usr/bin/env python3
"""
SecureCode v2.0 - Contributing Compliance Validator

Validates dataset examples for compliance with SecureCode v2.0 standards:
- Structure validation (4-turn conversation format)
- Metadata validation (required fields present)
- CVE format validation (CVE-YYYY-NNNNN or null)
- Language tag validation (supported languages only)
- Content quality validation (minimum length requirements)

Usage:
    python validate_contributing_compliance.py <dataset_file.jsonl>
    python validate_contributing_compliance.py consolidated/train.jsonl

Author: Scott Thornton (scott@perfecxion.ai)
License: Apache 2.0
Version: 2.0
Date: 2025-12-15
"""

import json
import re
import sys
from datetime import datetime
from typing import Tuple, Dict, List, Any
from pathlib import Path


# Supported programming languages
SUPPORTED_LANGUAGES = {
    'python', 'javascript', 'java', 'php', 'csharp',
    'ruby', 'go', 'typescript', 'rust', 'kotlin', 'yaml'
}

# Valid OWASP categories (2025)
VALID_OWASP_CATEGORIES = {
    'A01:2025-Broken Access Control',
    'A02:2025-Security Misconfiguration',
    'A03:2025-Software Supply Chain Failures',
    'A04:2025-Cryptographic Failures',
    'A05:2025-Injection',
    'A06:2025-Insecure Design',
    'A07:2025-Authentication Failures',
    'A08:2025-Software and Data Integrity Failures',
    'A09:2025-Security Logging and Monitoring Failures',
    'AI/ML Security Threats',  # Custom category
    'Unknown'  # For edge cases
}

# Valid severity levels
VALID_SEVERITIES = {'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'}


def validate_structure(example: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates 4-turn conversation structure.

    Args:
        example: Dataset example dictionary

    Returns:
        Tuple of (is_valid, message)
    """
    if 'messages' not in example:
        return False, "Missing 'messages' field"

    messages = example['messages']

    if len(messages) != 4:
        return False, f"Expected 4 turns, found {len(messages)}"

    # Validate turn roles
    expected_roles = ['user', 'assistant', 'user', 'assistant']
    for i, (msg, expected_role) in enumerate(zip(messages, expected_roles)):
        if 'role' not in msg:
            return False, f"Turn {i+1} missing 'role' field"

        if msg['role'] != expected_role:
            return False, f"Turn {i+1} has role '{msg['role']}', expected '{expected_role}'"

        if 'content' not in msg:
            return False, f"Turn {i+1} missing 'content' field"

    return True, "Structure valid"


def validate_metadata_complete(example: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates that all required metadata fields are present.

    Args:
        example: Dataset example dictionary

    Returns:
        Tuple of (is_valid, message)
    """
    required_fields = [
        'owasp_category',
        'cve_id',
        'severity',
        'language',
        'incident_year',
        'business_impact'
    ]

    missing_fields = [field for field in required_fields if field not in example]

    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    # Validate OWASP category
    if example['owasp_category'] not in VALID_OWASP_CATEGORIES:
        return False, f"Invalid OWASP category: {example['owasp_category']}"

    # Validate severity
    if example['severity'] not in VALID_SEVERITIES:
        return False, f"Invalid severity: {example['severity']} (must be one of {VALID_SEVERITIES})"

    # Validate incident year
    if not isinstance(example['incident_year'], int):
        return False, f"incident_year must be integer, got {type(example['incident_year'])}"

    if not (2017 <= example['incident_year'] <= datetime.now().year):
        return False, f"Invalid incident_year: {example['incident_year']} (must be 2017-{datetime.now().year})"

    return True, "Metadata complete"


def validate_cve_format(cve_id: Any) -> Tuple[bool, str]:
    """
    Validates CVE format: CVE-YYYY-NNNNN

    Accepts:
        - None/null (explicit null for incidents without CVE assignments)
        - CVE-YYYY-NNNNN where:
            - YYYY is 1999 to (current_year + 1)
            - NNNNN is 1-99999

    Args:
        cve_id: CVE identifier (string or None)

    Returns:
        Tuple of (is_valid, message)
    """
    if cve_id is None:
        return True, "Explicit null accepted"

    if not isinstance(cve_id, str):
        return False, f"CVE must be string or null, got {type(cve_id)}"

    # Basic format validation
    pattern = r'^CVE-(\d{4})-(\d{1,5})$'
    match = re.match(pattern, cve_id)

    if not match:
        return False, f"Invalid CVE format: {cve_id} (expected CVE-YYYY-NNNNN)"

    year = int(match.group(1))
    cve_number = int(match.group(2))

    # Year range validation (CVE program started in 1999)
    if year < 1999:
        return False, f"Invalid CVE year: {year} (CVE program started in 1999)"

    # Allow current year + 1 for upcoming CVE assignments
    current_year = datetime.now().year
    max_year = current_year + 1

    if year > max_year:
        return False, f"Invalid CVE year: {year} (future year beyond {max_year})"

    # CVE number range validation (1-99999)
    if cve_number < 1:
        return False, f"Invalid CVE number: {cve_number} (must be >= 1)"

    if cve_number > 99999:
        return False, f"Invalid CVE number: {cve_number} (must be <= 99999)"

    return True, "Valid CVE format"


def validate_language(language: str) -> Tuple[bool, str]:
    """
    Validates programming language tag.

    Args:
        language: Programming language string

    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(language, str):
        return False, f"Language must be string, got {type(language)}"

    if language.lower() in SUPPORTED_LANGUAGES:
        return True, "Valid language tag"

    return False, f"Unsupported language: {language} (supported: {sorted(SUPPORTED_LANGUAGES)})"


def validate_content_length(example: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates minimum content length for conversation turns.

    User turns: minimum 50 characters
    Assistant turns: minimum 100 characters

    Args:
        example: Dataset example dictionary

    Returns:
        Tuple of (is_valid, message)
    """
    user_min = 50  # characters
    assistant_min = 100  # characters

    messages = example.get('messages', [])

    if len(messages) != 4:
        return False, "Cannot validate content length without 4 turns"

    errors = []

    # Turn 1 (user): minimum 50 chars
    if len(messages[0]['content']) < user_min:
        errors.append(f"Turn 1 below {user_min} chars ({len(messages[0]['content'])} chars)")

    # Turn 2 (assistant): minimum 100 chars
    if len(messages[1]['content']) < assistant_min:
        errors.append(f"Turn 2 below {assistant_min} chars ({len(messages[1]['content'])} chars)")

    # Turn 3 (user): minimum 50 chars
    if len(messages[2]['content']) < user_min:
        errors.append(f"Turn 3 below {user_min} chars ({len(messages[2]['content'])} chars)")

    # Turn 4 (assistant): minimum 100 chars
    if len(messages[3]['content']) < assistant_min:
        errors.append(f"Turn 4 below {assistant_min} chars ({len(messages[3]['content'])} chars)")

    if errors:
        return False, "; ".join(errors)

    return True, "Content length valid"


def validate_example(example: Dict[str, Any], index: int = 0) -> Tuple[bool, Dict[str, Tuple[bool, str]]]:
    """
    Validates a complete example against all compliance requirements.

    Args:
        example: Dataset example dictionary
        index: Example index (for error reporting)

    Returns:
        Tuple of (all_passed, results_dict)
    """
    results = {
        'structure': validate_structure(example),
        'metadata': validate_metadata_complete(example),
        'cve_format': validate_cve_format(example.get('cve_id')),
        'language': validate_language(example.get('language', '')),
        'content_length': validate_content_length(example)
    }

    # Example passes only if all checks pass
    all_passed = all(result[0] for result in results.values())

    return all_passed, results


def validate_dataset(filepath: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Validates entire dataset file.

    Args:
        filepath: Path to JSONL dataset file
        verbose: Print detailed progress

    Returns:
        Dictionary with validation statistics and failures
    """
    if not Path(filepath).exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    if verbose:
        print(f"Loading dataset: {filepath}")

    examples = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                examples.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid JSON on line {line_num}: {e}")
                sys.exit(1)

    if verbose:
        print(f"Loaded {len(examples)} examples\n")
        print("="*80)
        print("VALIDATION STARTED")
        print("="*80)

    # Track statistics
    stats = {
        'total': len(examples),
        'passed': 0,
        'failed': 0,
        'structure_failures': 0,
        'metadata_failures': 0,
        'cve_format_failures': 0,
        'language_failures': 0,
        'content_length_failures': 0
    }

    failures = []

    # Validate each example
    for idx, example in enumerate(examples):
        if verbose and (idx % 100 == 0 or idx == len(examples) - 1):
            print(f"Progress: {idx + 1}/{len(examples)} ({(idx + 1) * 100 // len(examples)}%)")

        passed, results = validate_example(example, idx)

        if passed:
            stats['passed'] += 1
        else:
            stats['failed'] += 1

            # Track failure types
            for check_name, (check_passed, message) in results.items():
                if not check_passed:
                    stats[f'{check_name}_failures'] += 1

            # Record failure details
            failures.append({
                'index': idx,
                'results': {k: v[1] for k, v in results.items()},
                'example_preview': {
                    'cve_id': example.get('cve_id'),
                    'language': example.get('language'),
                    'severity': example.get('severity')
                }
            })

    # Print results
    if verbose:
        print("\n" + "="*80)
        print("VALIDATION COMPLETE")
        print("="*80)
        print(f"\nTotal Examples: {stats['total']}")
        print(f"Passed: {stats['passed']} ({stats['passed'] * 100 // stats['total']}%)")
        print(f"Failed: {stats['failed']} ({stats['failed'] * 100 // stats['total']}%)")

        if stats['failed'] > 0:
            print("\n" + "-"*80)
            print("FAILURE BREAKDOWN")
            print("-"*80)
            print(f"Structure failures: {stats['structure_failures']}")
            print(f"Metadata failures: {stats['metadata_failures']}")
            print(f"CVE format failures: {stats['cve_format_failures']}")
            print(f"Language failures: {stats['language_failures']}")
            print(f"Content length failures: {stats['content_length_failures']}")

            print("\n" + "-"*80)
            print(f"FIRST 10 FAILURES (of {len(failures)})")
            print("-"*80)

            for i, failure in enumerate(failures[:10], 1):
                print(f"\n{i}. Example #{failure['index']}")
                print(f"   CVE: {failure['example_preview'].get('cve_id')}")
                print(f"   Language: {failure['example_preview'].get('language')}")
                print(f"   Failures:")
                for check_name, message in failure['results'].items():
                    if not message.startswith("Valid") and not message.startswith("Explicit"):
                        print(f"     - {check_name}: {message}")

    return {
        'statistics': stats,
        'failures': failures,
        'compliance_rate': stats['passed'] / stats['total'] if stats['total'] > 0 else 0
    }


def main():
    """Main entry point for CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python validate_contributing_compliance.py <dataset_file.jsonl>")
        print("\nExample:")
        print("  python validate_contributing_compliance.py consolidated/train.jsonl")
        sys.exit(1)

    filepath = sys.argv[1]
    results = validate_dataset(filepath, verbose=True)

    # Save detailed results
    output_file = f"{Path(filepath).stem}_validation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n\nDetailed results saved to: {output_file}")

    # Exit with error code if validation failed
    if results['statistics']['failed'] > 0:
        print("\n⚠️  VALIDATION FAILED - Fix issues before contribution")
        sys.exit(1)
    else:
        print("\n✓ VALIDATION PASSED - All examples comply with standards")
        sys.exit(0)


if __name__ == '__main__':
    main()
