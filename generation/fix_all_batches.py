#!/usr/bin/env python3
"""
Comprehensive fix script for all 10 failing examples across batches 003, 005, and 006.

Fixes:
- Batch 003 (XSS): ES6 module syntax, innerHTML security issues
- Batch 005 (SQL Injection): Python syntax errors, Java class wrappers, ES6 modules, C# language code
- Batch 006 (NoSQL Injection): JavaScript and Python syntax errors
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
import shutil

# Define batch files
BATCH_FILES = {
    '003': '/Users/scott/perfecxion/datasets/securecode/v2/data/xss_batch_003.jsonl',
    '005': '/Users/scott/perfecxion/datasets/securecode/v2/data/sql_injection_batch_005.jsonl',
    '006': '/Users/scott/perfecxion/datasets/securecode/v2/data/nosql_injection_batch_006.jsonl',
}

# Define fixes for each example
FIXES = {
    # Batch 003 - XSS
    'xss-000001': ['fix_es6_modules', 'fix_innerHTML_security'],
    'xss-000002': ['fix_es6_modules', 'fix_javascript_syntax'],  # JSX + ES6

    # Batch 005 - SQL Injection
    'sql-injection-000006': ['fix_python_syntax'],
    'sql-injection-000007': ['fix_java_class_wrapper'],
    'sql-injection-000008': ['fix_es6_modules'],
    'sql-injection-000010': ['fix_java_class_wrapper'],
    'sql-injection-000012': ['fix_csharp_lang'],
    'sql-injection-000014': ['fix_python_syntax'],

    # Batch 006 - NoSQL Injection
    'sql-injection-000016': ['fix_javascript_syntax'],
    'sql-injection-000018': ['fix_python_syntax'],
}


def backup_file(filepath):
    """Create a backup of the file with timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{filepath}.backup_{timestamp}"
    shutil.copy2(filepath, backup_path)
    print(f"✓ Created backup: {backup_path}")
    return backup_path


def fix_es6_modules(code_block):
    """
    Fix ES6 module syntax issues by:
    1. Commenting out import statements
    2. Wrapping top-level await in async IIFE
    """
    if not code_block:
        return code_block

    # Comment out ES6 imports
    # Match: import ... from '...';
    code_block = re.sub(
        r'^(import\s+.+?from\s+[\'"].+?[\'"];?\s*)$',
        r'// \1',
        code_block,
        flags=re.MULTILINE
    )

    # Check if there's top-level await
    if re.search(r'^\s*const\s+\w+\s*=\s*await\s+', code_block, re.MULTILINE):
        # Find the usage section (typically starts with "// Usage" comment)
        usage_match = re.search(r'(// Usage.*?)(\n(?:```|$))', code_block, re.DOTALL)
        if usage_match:
            usage_section = usage_match.group(1)

            # Wrap in async IIFE
            wrapped_usage = '// Usage (wrapped in async IIFE for top-level await)\n(async () => {\n'

            # Indent the usage code
            usage_lines = usage_section.replace('// Usage\n', '').split('\n')
            for line in usage_lines:
                if line.strip():
                    wrapped_usage += '    ' + line + '\n'
                else:
                    wrapped_usage += '\n'

            wrapped_usage += '})().catch(console.error);'

            # Replace in code block
            code_block = code_block.replace(usage_match.group(1), wrapped_usage)

    return code_block


def fix_innerHTML_security(code_block):
    """
    Fix innerHTML security issues in 'secure' code:
    Replace innerHTML with textContent where appropriate in sanitized contexts.
    """
    if not code_block:
        return code_block

    # Look for patterns where innerHTML is used with sanitized content
    # This is actually safe AFTER DOMPurify, so we'll add a comment explaining
    # Instead of replacing, add explanatory comment

    # Pattern: commentElement.innerHTML = cleanComment;  // Safe after DOMPurify
    code_block = re.sub(
        r'(\s+)(commentSpan\.innerHTML\s*=\s*cleanComment;)(\s*)(//.*)?$',
        r'\1\2  // Safe: sanitized by DOMPurify\3',
        code_block,
        flags=re.MULTILINE
    )

    # Pattern: commentElement.innerHTML = safeComment;
    code_block = re.sub(
        r'(\s+)(commentElement\.innerHTML\s*=\s*safeComment;)(\s*)(//.*)?$',
        r'\1\2  // Safe: sanitized content\3',
        code_block,
        flags=re.MULTILINE
    )

    return code_block


def fix_python_syntax(code_block):
    """
    Fix common Python syntax errors:
    1. Unterminated string literals in SQL comments
    2. Unbalanced parentheses/brackets
    3. HTTP requests in Python code blocks (should be separate)
    """
    if not code_block:
        return code_block

    # Fix 1: sql-injection-000006 - Unterminated string + raw SQL
    # Problem: WHERE category = '' UNION SELECT... --'
    # Also, the SQL query is shown as raw text (not in a Python string)
    # Solution: Comment out the SQL query demonstration
    if "UNION SELECT" in code_block and "FROM users" in code_block:
        # Replace the inline SQL with a comment-based version
        code_block = re.sub(
            r"(WHERE category = .* UNION SELECT .* FROM users )--'",
            r"\1-- (SQL injection payload)",
            code_block
        )

        # Also comment out raw SQL queries (lines that start with SELECT, WHERE, etc.)
        code_block = re.sub(
            r'^(SELECT .+)$',
            r'# SQL: \1',
            code_block,
            flags=re.MULTILINE
        )
        code_block = re.sub(
            r'^(FROM .+)$',
            r'# SQL: \1',
            code_block,
            flags=re.MULTILINE
        )
        code_block = re.sub(
            r'^(WHERE .+)$',
            r'# SQL: \1',
            code_block,
            flags=re.MULTILINE
        )
        code_block = re.sub(
            r'^(AND .+)$',
            r'# SQL: \1',
            code_block,
            flags=re.MULTILINE
        )

    # Fix 2: sql-injection-000014 - HTTP request in Python code block
    # Problem: GET /search?q=<payload> is not valid Python
    # Solution: Convert to comment or remove
    code_block = re.sub(
        r'^(GET /.*?)$',
        r'# HTTP Request: \1',
        code_block,
        flags=re.MULTILINE
    )

    # Fix 3: sql-injection-000018 - Mismatched brackets
    # Problem: methods='POST'] should be methods=['POST']
    code_block = re.sub(
        r"methods='POST'\]",
        r"methods=['POST']",
        code_block
    )

    # Also fix the inverse case
    code_block = re.sub(
        r"methods=\['POST'\)",
        r"methods=['POST']",
        code_block
    )

    return code_block


def fix_java_class_wrapper(code_block):
    """
    Wrap Java code snippets in proper class declarations if missing.
    """
    if not code_block:
        return code_block

    # Check if already has a class declaration
    if re.search(r'^\s*(public\s+)?class\s+\w+', code_block, re.MULTILINE):
        return code_block

    # Check if it's a complete snippet (has imports, etc.)
    has_imports = 'import ' in code_block
    has_main = 'public static void main' in code_block or 'public void ' in code_block

    # If it's just a method snippet, wrap it
    if not has_main and not has_imports:
        # It's likely a method - wrap in a class
        lines = code_block.split('\n')
        indented_lines = ['    ' + line if line.strip() else line for line in lines]

        wrapped = 'public class Example {\n'
        wrapped += '\n'.join(indented_lines)
        wrapped += '\n}'

        return wrapped

    return code_block


def fix_csharp_lang(metadata):
    """
    Fix C# language code in metadata from 'csharp' to 'c#'.
    """
    if metadata.get('lang') == 'csharp':
        metadata['lang'] = 'c#'
    return metadata


def fix_javascript_syntax(code_block, block_info=None):
    """
    Fix JavaScript syntax errors:
    1. React JSX code (not pure JS) - change language to 'jsx'
    2. HTTP requests in JS code blocks
    """
    if not code_block:
        return code_block, None

    # Fix 1: sql-injection-000016 - HTTP request in JavaScript code block
    # Problem: GET /api/products?category=... is not valid JS
    # Solution: Convert to comment
    code_block = re.sub(
        r'^(GET /.*?)$',
        r'// HTTP Request: \1',
        code_block,
        flags=re.MULTILINE
    )

    # Fix 2: xss-000002 - React JSX is not pure JavaScript
    # Check if this is JSX (has <Component> syntax or JSX patterns)
    has_jsx = bool(re.search(r'<[A-Z]\w+[^>]*>', code_block) or
                   re.search(r'<div|<span|<strong', code_block))

    # If it has JSX with function components or return statements, suggest language change
    suggested_lang = None
    if has_jsx and ('return (' in code_block or 'function ' in code_block):
        suggested_lang = 'jsx'  # Signal to change language code
        # Also add a comment
        if '// JSX' not in code_block and '// Note: This is JSX' not in code_block:
            code_block = '// JSX - React syntax (requires Babel transpilation)\n' + code_block

    return code_block, suggested_lang


def extract_code_blocks(text):
    """
    Extract code blocks from markdown text.
    Returns list of (start_pos, end_pos, language, code) tuples.
    """
    pattern = r'```(\w+)?\n(.*?)```'
    blocks = []

    for match in re.finditer(pattern, text, re.DOTALL):
        lang = match.group(1) or ''
        code = match.group(2)
        blocks.append({
            'start': match.start(),
            'end': match.end(),
            'lang': lang,
            'code': code,
            'full_match': match.group(0)
        })

    return blocks


def apply_code_fixes(text, fix_functions):
    """
    Apply fix functions to code blocks in markdown text.
    """
    blocks = extract_code_blocks(text)

    # Process in reverse order to maintain positions
    for block in reversed(blocks):
        original_code = block['code']
        fixed_code = original_code
        new_lang = block['lang']  # May be changed for JSX

        # JavaScript-related languages
        js_langs = ['javascript', 'typescript', 'js', 'ts']

        # Apply each fix function
        for fix_func in fix_functions:
            if fix_func == 'fix_es6_modules' and block['lang'] in js_langs:
                fixed_code = fix_es6_modules(fixed_code)
            elif fix_func == 'fix_innerHTML_security' and block['lang'] in js_langs:
                fixed_code = fix_innerHTML_security(fixed_code)
            elif fix_func == 'fix_python_syntax' and block['lang'] == 'python':
                fixed_code = fix_python_syntax(fixed_code)
            elif fix_func == 'fix_java_class_wrapper' and block['lang'] == 'java':
                fixed_code = fix_java_class_wrapper(fixed_code)
            elif fix_func == 'fix_javascript_syntax' and block['lang'] in js_langs:
                result = fix_javascript_syntax(fixed_code, block)
                if isinstance(result, tuple):
                    fixed_code, suggested_lang = result
                    if suggested_lang:
                        new_lang = suggested_lang
                else:
                    fixed_code = result

        # Replace in text if changed or language changed
        if fixed_code != original_code or new_lang != block['lang']:
            new_block = f"```{new_lang}\n{fixed_code}```"
            text = text[:block['start']] + new_block + text[block['end']:]

    return text


def fix_example(example_id, example):
    """
    Apply appropriate fixes to an example based on its ID.
    """
    if example_id not in FIXES:
        return example, False

    fix_functions = FIXES[example_id]
    modified = False

    print(f"\n  Fixing {example_id}...")
    print(f"    Applying fixes: {', '.join(fix_functions)}")

    # Fix metadata if needed
    if 'fix_csharp_lang' in fix_functions:
        old_lang = example['metadata'].get('lang')
        example['metadata'] = fix_csharp_lang(example['metadata'])
        new_lang = example['metadata'].get('lang')
        if old_lang != new_lang:
            print(f"    ✓ Changed language: {old_lang} -> {new_lang}")
            modified = True

    # Fix code in conversations
    for conversation in example.get('conversations', []):
        if 'value' in conversation:
            original_value = conversation['value']
            fixed_value = apply_code_fixes(original_value, fix_functions)

            if fixed_value != original_value:
                conversation['value'] = fixed_value
                modified = True

                # Count changes
                original_blocks = extract_code_blocks(original_value)
                fixed_blocks = extract_code_blocks(fixed_value)
                print(f"    ✓ Fixed {len(original_blocks)} code block(s) in turn {conversation.get('turn', '?')}")

    return example, modified


def process_batch(batch_id, filepath):
    """
    Process a single batch file and apply fixes.
    """
    print(f"\n{'='*70}")
    print(f"Processing Batch {batch_id}: {Path(filepath).name}")
    print(f"{'='*70}")

    # Read all examples
    examples = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))

    print(f"Loaded {len(examples)} examples")

    # Apply fixes
    fixed_count = 0
    for example in examples:
        example_id = example.get('id')
        if example_id in FIXES:
            example, modified = fix_example(example_id, example)
            if modified:
                fixed_count += 1

    # Write back
    if fixed_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            for example in examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')

        print(f"\n✓ Fixed {fixed_count} example(s) in batch {batch_id}")
    else:
        print(f"\n! No changes made to batch {batch_id}")

    return fixed_count


def validate_syntax(filepath, batch_id):
    """
    Run basic syntax validation on the batch file.
    """
    print(f"\nValidating batch {batch_id}...")

    try:
        # Check JSON validity
        with open(filepath, 'r', encoding='utf-8') as f:
            line_num = 0
            for line in f:
                line_num += 1
                if line.strip():
                    try:
                        json.loads(line)
                    except json.JSONDecodeError as e:
                        print(f"  ✗ JSON error on line {line_num}: {e}")
                        return False

        print(f"  ✓ All {line_num} lines are valid JSON")
        return True

    except Exception as e:
        print(f"  ✗ Validation error: {e}")
        return False


def main():
    print("="*70)
    print("Comprehensive Batch Fixer")
    print("Fixing 10 failing examples across batches 003, 005, and 006")
    print("="*70)

    # Create backups
    print("\n" + "="*70)
    print("Creating backups...")
    print("="*70)

    backups = {}
    for batch_id, filepath in BATCH_FILES.items():
        if Path(filepath).exists():
            backups[batch_id] = backup_file(filepath)
        else:
            print(f"✗ File not found: {filepath}")
            return 1

    # Process each batch
    total_fixed = 0
    for batch_id, filepath in BATCH_FILES.items():
        fixed_count = process_batch(batch_id, filepath)
        total_fixed += fixed_count

    # Validate all batches
    print("\n" + "="*70)
    print("Validation")
    print("="*70)

    all_valid = True
    for batch_id, filepath in BATCH_FILES.items():
        if not validate_syntax(filepath, batch_id):
            all_valid = False

    # Summary
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    print(f"Total examples fixed: {total_fixed}")
    print(f"Validation status: {'✓ PASSED' if all_valid else '✗ FAILED'}")

    if backups:
        print("\nBackup files created:")
        for batch_id, backup_path in backups.items():
            print(f"  Batch {batch_id}: {backup_path}")

    # Success
    if all_valid:
        print("\n✓ All fixes applied successfully!")
        print("\nNext steps:")
        print("  1. Run validation script: python comprehensive_qa.py")
        print("  2. Check pass rates for batches 003, 005, 006")
        return 0
    else:
        print("\n✗ Some validations failed. Check errors above.")
        print("  Backups are available if you need to restore.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
