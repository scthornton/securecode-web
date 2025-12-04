#!/usr/bin/env python3
"""
Fix xss-000043 Vue component syntax.
"""

import json
import re
from pathlib import Path
import shutil


def fix_vue_component_syntax(code):
    """Fix Vue component object literal syntax for validation."""

    # Convert method shorthand to full property syntax
    # async mounted() { → mounted: async function() {
    code = re.sub(r'(\s+)async\s+(\w+)\s*\(\)\s*\{', r'\1\2: async function() {', code)

    # Regular method shorthand: methods() { → methods: function() {
    code = re.sub(r'(\s+)(\w+)\s*\(\)\s*\{(?!\s*return)', r'\1\2: function() {', code)

    # Make sure data: function() stays as is (already fixed)

    # Remove any remaining problematic syntax - wrap entire object in const
    if code.strip().startswith('{') and 'name:' in code:
        # Add const declaration
        code = 'const VueComponent = ' + code

    return code


def main():
    data_file = Path(__file__).parent.parent / 'data' / 'xss_expansion_batch_008.jsonl'

    print("Fixing xss-000043 Vue component...")
    print("=" * 60)

    # Backup
    backup_file = data_file.parent / f"{data_file.stem}_pre_043_fix.jsonl"
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

                # Fix Vue component syntax
                fixed_code = fix_vue_component_syntax(code)

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

    # Show Batch 008 summary
    lines = result.stdout.split('\n')

    for i, line in enumerate(lines):
        if 'xss-000043' in line:
            # Show this example and next 5 lines
            for j in range(7):
                if i + j < len(lines):
                    print(lines[i + j])
            break

    # Show batch summary
    print("\n" + "=" * 60)
    for line in lines:
        if 'Batch 008' in line and 'Summary' in line:
            # Print this and next 3 lines
            idx = lines.index(line)
            for j in range(4):
                if idx + j < len(lines):
                    print(lines[idx + j])
            break

    # Overall
    print("\n" + "=" * 60)
    for line in lines:
        if any(x in line for x in ['OVERALL SUMMARY', 'Total Examples:', 'Passed:', 'Failed:']):
            print(line)

    return 0


if __name__ == "__main__":
    exit(main())
