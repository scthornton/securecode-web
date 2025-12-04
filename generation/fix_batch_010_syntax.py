#!/usr/bin/env python3
"""Fix syntax errors in Batch 010 examples 025 and 027"""

import json
import re
from pathlib import Path

def fix_example_025(example):
    """Fix WAF bypass payloads - change from Python code blocks to SQL/text blocks"""
    for conv in example['conversations']:
        if conv['from'] == 'assistant':
            # Fix the WAF bypass techniques by changing code fence language
            # from python to sql for payload examples
            value = conv['value']

            # Pattern: code blocks with single-quoted payloads that aren't valid Python
            # Change these specific blocks from ```python to ```sql
            if '**1. URL Encoding**:' in value:
                # These are payload examples, not Python code
                value = value.replace(
                    '**1. URL Encoding**:\n```python\n# Normal payload (blocked):\n\' OR \'1\'=\'1',
                    '**1. URL Encoding**:\n```sql\n# Normal payload (blocked):\n\' OR \'1\'=\'1'
                )

            if '**2. Double URL Encoding**:' in value:
                value = value.replace(
                    '**2. Double URL Encoding**:\n```python\n# Double encoded:',
                    '**2. Double URL Encoding**:\n```sql\n# Double encoded:'
                )

            if '**3. Case Variation**:' in value:
                value = value.replace(
                    '**3. Case Variation**:\n```python\n# Mixed case:',
                    '**3. Case Variation**:\n```sql\n# Mixed case:'
                )

            if '**4. Comment Obfuscation**:' in value:
                value = value.replace(
                    '**4. Comment Obfuscation**:\n```python\n# Inline comments:',
                    '**4. Comment Obfuscation**:\n```sql\n# Inline comments:'
                )

            if '**5. Whitespace Alternatives**:' in value:
                value = value.replace(
                    '**5. Whitespace Alternatives**:\n```python\n# Tabs, newlines instead of spaces:',
                    '**5. Whitespace Alternatives**:\n```sql\n# Tabs, newlines instead of spaces:'
                )

            if '**6. Function-based Obfuscation**:' in value:
                value = value.replace(
                    '**6. Function-based Obfuscation**:\n```python\n# Using CHAR() to build strings:',
                    '**6. Function-based Obfuscation**:\n```sql\n# Using CHAR() to build strings:'
                )

            conv['value'] = value

    return example

def fix_example_027(example):
    """Add missing class constants to Java example"""
    for conv in example['conversations']:
        if conv['from'] == 'assistant' and 'VULNERABLE CODE' in conv['value']:
            value = conv['value']

            # Add DB constants at the top of Java code blocks
            if 'public class UserProfileService {' in value and 'DB_URL' not in value[:value.index('public class')]:
                # Find the Java code block and add constants
                value = value.replace(
                    '```java\nimport java.sql.*;\n\npublic class UserProfileService {',
                    '''```java
import java.sql.*;

public class UserProfileService {
    private static final String DB_URL = "jdbc:postgresql://localhost/appdb";
    private static final String USER = "appuser";
    private static final String PASS = "password";'''
                )

            conv['value'] = value

    return example

def main():
    input_file = Path(__file__).parent.parent / 'data' / 'sql_advanced_batch_010.jsonl'

    examples = []
    with open(input_file, 'r') as f:
        for line in f:
            example = json.loads(line)

            if example['id'] == 'sql-injection-000025':
                print(f"Fixing {example['id']}: WAF bypass payload code blocks")
                example = fix_example_025(example)

            elif example['id'] == 'sql-injection-000027':
                print(f"Fixing {example['id']}: Adding Java class constants")
                example = fix_example_027(example)

            examples.append(example)

    # Write back
    with open(input_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\nFixed {len(examples)} examples")

if __name__ == '__main__':
    main()
