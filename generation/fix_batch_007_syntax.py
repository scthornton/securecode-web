#!/usr/bin/env python3
"""
Fix syntax errors in Batch 007 JSONL file.

Issues to fix:
1. Unbalanced braces in Python code blocks (dict/set syntax)
2. Ruby encoding issues (smart quotes)
3. Java code syntax errors
4. JavaScript code syntax errors
"""

import json
import re
from pathlib import Path


def fix_python_dict_syntax(content):
    """Fix unbalanced braces in Python dictionaries and sets."""
    # This is a targeted fix for the specific patterns causing issues

    # Fix: {{'Name', 'FullName'} -> {{'Name', 'FullName'}}
    content = re.sub(
        r"(\{\{['\"][\w]+['\"],\s*['\"][\w]+['\"])\}([,\s]*\n)",
        r"\1}}\2",
        content
    )

    # Fix missing closing braces in nested dicts
    # Pattern: 'optional': {{'Description', 'NoPassword'},
    # Should be: 'optional': {{'Description', 'NoPassword'}},
    content = re.sub(
        r"('optional':\s*\{\{[^}]+)\},",
        r"\1}},",
        content
    )

    # Fix: 'required': {{'Name', 'FullName'},
    # Should be: 'required': {{'Name', 'FullName'}},
    content = re.sub(
        r"('required':\s*\{\{[^}]+)\},",
        r"\1}},",
        content
    )

    return content


def fix_ruby_encoding(content):
    """Replace smart quotes and other non-ASCII characters with ASCII equivalents."""
    # Smart quotes to regular quotes
    content = content.replace('"', '"').replace('"', '"')
    content = content.replace(''', "'").replace(''', "'")
    content = content.replace('…', '...')
    content = content.replace('–', '-').replace('—', '--')

    return content


def fix_java_syntax(content):
    """Fix Java code syntax errors."""
    # Fix double braces in Java code (should be single braces for actual code)
    # This is tricky because we need to preserve JSON escaping but fix Java code

    # Pattern: new HashSet<String>\n {{\n should be new HashSet<String>() {{\n
    content = re.sub(
        r'(new HashSet<String>)\s*\n\s*(\{\{)',
        r'\1() \2',
        content
    )

    # Fix: new ProcessStartInfo\n {{ should have no space issues
    # Most Java issues are from the conversion - let's check the actual structure

    return content


def fix_javascript_syntax(content):
    """Fix JavaScript code syntax errors."""
    # Most JavaScript issues are from line breaks in strings
    # Fix: const dangerous = [';', '&', '|', '
    # Should be: const dangerous = [';', '&', '|', ...

    # Fix incomplete string literals split across lines
    content = re.sub(
        r"const dangerous = \[([^\]]+)\n",
        r"const dangerous = [\1];\\n",
        content
    )

    return content


def fix_example(example):
    """Fix syntax issues in a single example."""
    lang = example.get('metadata', {}).get('lang', '')

    # Fix conversations content
    for conv in example.get('conversations', []):
        if 'value' in conv:
            content = conv['value']

            # Apply language-specific fixes
            if lang == 'python':
                content = fix_python_dict_syntax(content)
            elif lang == 'ruby':
                content = fix_ruby_encoding(content)
            elif lang == 'java':
                content = fix_java_syntax(content)
            elif lang == 'javascript':
                content = fix_javascript_syntax(content)

            # Apply general fixes
            content = fix_ruby_encoding(content)  # Fix smart quotes everywhere

            conv['value'] = content

    return example


def main():
    """Fix all syntax errors in Batch 007."""
    data_file = Path(__file__).parent.parent / 'data' / 'command_injection_batch_007.jsonl'

    if not data_file.exists():
        print(f"Error: {data_file} not found")
        return 1

    print("Fixing Batch 007 syntax errors...")
    print("=" * 60)

    # Read all examples
    examples = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            example = json.loads(line)
            examples.append(example)

    print(f"Loaded {len(examples)} examples")

    # Fix each example
    fixed_examples = []
    for i, example in enumerate(examples, 1):
        ex_id = example.get('id', f'example-{i}')
        lang = example.get('metadata', {}).get('lang', 'unknown')
        print(f"Fixing {ex_id} ({lang})...")

        fixed = fix_example(example)
        fixed_examples.append(fixed)

    # Write fixed examples back
    backup_file = data_file.parent / f"{data_file.stem}_before_fix.jsonl"

    # Backup original
    import shutil
    shutil.copy(data_file, backup_file)
    print(f"\\nBackup created: {backup_file.name}")

    # Write fixed version
    with open(data_file, 'w', encoding='utf-8') as f:
        for example in fixed_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\\n')

    print(f"✓ Fixed {len(fixed_examples)} examples")
    print(f"✓ Output: {data_file}")
    print("\\nNext: Run validation with 'python3 validate_all_batches.py'")

    return 0


if __name__ == "__main__":
    exit(main())
