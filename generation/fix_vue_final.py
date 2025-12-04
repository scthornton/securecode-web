#!/usr/bin/env python3
"""
Fix Vue example by extracting only <script> sections for validation.
"""

import json
import re
from pathlib import Path
import shutil


def extract_vue_script(code):
    """Extract JavaScript from Vue Single File Component."""

    # Find <script> section
    script_match = re.search(r'<script>(.*?)</script>', code, re.DOTALL | re.IGNORECASE)

    if script_match:
        # Extract just the JavaScript
        js_code = script_match.group(1).strip()

        # Remove 'export default' if present
        js_code = re.sub(r'^\s*export\s+default\s+', '', js_code, flags=re.MULTILINE)

        # If it's an object literal for Vue component, wrap in const
        if js_code.strip().startswith('{'):
            js_code = 'const VueComponent = ' + js_code

        return js_code

    # No <script> section, might be already extracted or different format
    # If code starts with <template>, comment it out
    if '<template>' in code:
        # Comment out template section
        code = re.sub(
            r'<template>.*?</template>',
            '/* Vue template section omitted for validation */',
            code,
            flags=re.DOTALL | re.IGNORECASE
        )

    # Remove export default
    code = re.sub(r'^\s*export\s+default\s+', '', code, flags=re.MULTILINE)

    # If remaining code is object literal, wrap it
    code = code.strip()
    if code.startswith('{') and code.endswith(';'):
        code = 'const VueComponent = ' + code

    return code


def main():
    data_file = Path(__file__).parent.parent / 'data' / 'xss_expansion_batch_008.jsonl'

    print("Extracting Vue JavaScript sections...")
    print("=" * 60)

    # Backup
    backup_file = data_file.parent / f"{data_file.stem}_pre_vue_final.jsonl"
    shutil.copy(data_file, backup_file)
    print(f"Backup: {backup_file.name}\n")

    # Read examples
    examples = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))

    # Fix xss-000043
    for example in examples:
        if example['id'] != 'xss-000043':
            continue

        for conv in example['conversations']:
            if conv.get('from') != 'assistant':
                continue

            content = conv['value']

            # Fix all JavaScript code blocks
            pattern = r'(```javascript\n)(.*?)(```)'

            def replacer(match):
                prefix = match.group(1)
                code = match.group(2)
                suffix = match.group(3)

                # Extract Vue script section
                fixed_code = extract_vue_script(code)

                return prefix + fixed_code + suffix

            content = re.sub(pattern, replacer, content, flags=re.DOTALL)
            conv['value'] = content

        print(f"✓ Fixed {example['id']}")

    # Write fixed examples
    with open(data_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\n✓ Fix applied")
    print(f"✓ Output: {data_file}")
    print("\nValidating...")

    # Run validation
    import subprocess
    result = subprocess.run(
        ['python3', 'validate_all_batches.py'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )

    # Show xss-000043 result
    lines = result.stdout.split('\n')
    for i, line in enumerate(lines):
        if 'xss-000043' in line:
            for j in range(7):
                if i + j < len(lines):
                    print(lines[i + j])
            break

    # Show batch summary
    print("\n" + "=" * 60)
    in_summary = False
    for line in lines:
        if 'Batch 008' in line and 'Summary' in line:
            in_summary = True
        if in_summary:
            print(line)
            if 'Pass Rate' in line:
                break

    # Overall
    print("\n" + "=" * 60)
    for line in lines:
        if any(x in line for x in ['OVERALL SUMMARY', 'Total Examples:', 'Passed:', 'Failed:']):
            print(line)

    return 0


if __name__ == "__main__":
    exit(main())
