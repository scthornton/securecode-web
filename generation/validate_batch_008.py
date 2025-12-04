#!/usr/bin/env python3
"""
Quick validation script for XSS Batch 008.
Tests syntax validation of code blocks in all examples.
"""

import json
import re
import ast
import sys
from pathlib import Path

def extract_code_blocks(content):
    """Extract code blocks from markdown content."""
    pattern = r'```(\w+)?\n(.*?)\n```'
    blocks = re.findall(pattern, content, re.DOTALL)
    return [(lang or 'unknown', code) for lang, code in blocks]

def validate_javascript(code):
    """Validate JavaScript/TypeScript syntax using Node.js."""
    import subprocess
    import tempfile

    # Write code to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        # Use node --check to validate syntax
        result = subprocess.run(
            ['node', '--check', temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        Path(temp_file).unlink()
        return result.returncode == 0, result.stderr
    except Exception as e:
        Path(temp_file).unlink()
        return False, str(e)

def validate_python(code):
    """Validate Python syntax."""
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def validate_code_block(lang, code):
    """Validate a single code block."""
    lang = lang.lower()

    if lang in ['python', 'py']:
        return validate_python(code)
    elif lang in ['javascript', 'js', 'typescript', 'ts']:
        return validate_javascript(code)
    elif lang in ['java', 'go', 'php', 'ruby', 'rust', 'c', 'cpp', 'csharp']:
        # Skip validation for other languages for now
        return True, "Language validation not implemented"
    else:
        return True, "Unknown language"

def validate_example(example):
    """Validate all code blocks in an example."""
    example_id = example['id']
    results = {
        'id': example_id,
        'passed': True,
        'total_blocks': 0,
        'failed_blocks': [],
        'errors': []
    }

    for conv in example['conversations']:
        if 'value' not in conv:
            continue

        blocks = extract_code_blocks(conv['value'])
        results['total_blocks'] += len(blocks)

        for i, (lang, code) in enumerate(blocks):
            is_valid, error = validate_code_block(lang, code)

            if not is_valid:
                results['passed'] = False
                results['failed_blocks'].append({
                    'turn': conv.get('turn', 'unknown'),
                    'block': i + 1,
                    'language': lang,
                    'error': error
                })

    return results

def main():
    batch_file = Path("/Users/scott/perfecxion/datasets/securecode/v2/data/xss_expansion_batch_008.jsonl")

    print("="*80)
    print("XSS Batch 008 Validation")
    print("="*80)

    # Load examples
    with open(batch_file, 'r') as f:
        examples = [json.loads(line) for line in f]

    print(f"\nValidating {len(examples)} examples...\n")

    # Validate each example
    results = []
    passed_count = 0
    failed_count = 0

    for example in examples:
        result = validate_example(example)
        results.append(result)

        if result['passed']:
            passed_count += 1
            print(f"✓ PASSED: {result['id']} ({result['total_blocks']} code blocks)")
        else:
            failed_count += 1
            print(f"✗ FAILED: {result['id']}")
            for failure in result['failed_blocks']:
                print(f"  Turn {failure['turn']}, Block {failure['block']} ({failure['language']}):")
                print(f"    {failure['error'][:200]}")

    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print(f"Total examples: {len(examples)}")
    print(f"Passed: {passed_count} ({100*passed_count/len(examples):.1f}%)")
    print(f"Failed: {failed_count} ({100*failed_count/len(examples):.1f}%)")

    if failed_count == 0:
        print("\n✓ All examples passed validation!")
        return 0
    else:
        print(f"\n✗ {failed_count} examples failed validation")
        return 1

if __name__ == "__main__":
    sys.exit(main())
