#!/usr/bin/env python3
"""
Final fix for example 033 JavaScript - wrap top-level await in async IIFE.
"""

import json
import re
from pathlib import Path


def fix_top_level_await(code):
    """Wrap top-level await statements in async IIFE for node compatibility."""

    # Check if code has top-level await (outside functions/classes)
    # Look for await at the start of lines that aren't inside a function

    # If we find usage examples with await at top level, wrap the entire usage section
    if re.search(r'^\s*await\s+', code, re.MULTILINE):
        # Find the usage section (usually at the end)
        # Pattern: // Usage or similar comment, followed by await statements

        # Simple approach: wrap everything after "// Usage" in an async IIFE
        parts = re.split(r'(//\s*Usage.*?\n)', code, maxsplit=1, flags=re.DOTALL)

        if len(parts) == 3:
            before_usage = parts[0]
            usage_comment = parts[1]
            usage_code = parts[2]

            # Wrap usage code in async IIFE
            wrapped_usage = f"""{usage_comment}
(async () => {{
{usage_code}
}})().catch(console.error);
"""
            return before_usage + wrapped_usage

    return code


def fix_example_033(example):
    """Fix JavaScript example 033 - wrap top-level await."""
    for conv in example['conversations']:
        if conv.get('from') != 'assistant':
            continue

        content = conv['value']

        # Find all JavaScript code blocks
        pattern = r'(```(?:javascript|js)\n)(.*?)(```)'

        def replacer(match):
            prefix = match.group(1)
            code = match.group(2)
            suffix = match.group(3)

            # Fix top-level await
            fixed_code = fix_top_level_await(code)

            return prefix + fixed_code + suffix

        content = re.sub(pattern, replacer, content, flags=re.DOTALL)
        conv['value'] = content

    return example


def main():
    data_file = Path(__file__).parent.parent / 'data' / 'command_injection_batch_007.jsonl'

    print("Final fix for example 033...")
    print("=" * 60)

    # Backup
    backup_file = data_file.parent / f"{data_file.stem}_pre_033_final.jsonl"
    import shutil
    shutil.copy(data_file, backup_file)
    print(f"Backup: {backup_file.name}\n")

    # Read examples
    examples = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))

    # Fix example 033
    for example in examples:
        if example['id'] == 'sql-injection-000033':
            example = fix_example_033(example)
            print(f"✓ Fixed {example['id']}: Wrapped top-level await in async IIFE")

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
        text=True
    )

    # Show Batch 007 summary
    for line in result.stdout.split('\n'):
        if 'Batch 007' in line or 'Pass Rate:' in line:
            print(line)

    return 0


if __name__ == "__main__":
    exit(main())
