#!/usr/bin/env python3
"""Final fixes for Batch 010 examples 025 and 027"""

import json
from pathlib import Path

def fix_example_025_final(example):
    """Fix all payload code blocks in example 025"""
    for i, conv in enumerate(example['conversations']):
        if conv['from'] == 'assistant':
            value = conv['value']

            # Fix the Polyglot Payloads section
            if '**7. Polyglot Payloads**' in value:
                value = value.replace(
                    '**7. Polyglot Payloads** (works across MySQL, PostgreSQL, MSSQL):\n```python',
                    '**7. Polyglot Payloads** (works across MySQL, PostgreSQL, MSSQL):\n```sql'
                )

            example['conversations'][i]['value'] = value

    return example

def fix_example_027_final(example):
    """Fix all Java code blocks to include class declaration properly"""
    for i, conv in enumerate(example['conversations']):
        if conv['from'] == 'assistant':
            value = conv['value']

            # Find all Java code blocks and ensure they have proper class context
            import re

            # Pattern to find Java code blocks
            java_blocks = list(re.finditer(r'```java\n(.*?)```', value, re.DOTALL))

            for match in reversed(java_blocks):  # Process in reverse to maintain positions
                block_content = match.group(1)

                # If this block has methods but no class wrapper, add one
                if ('public void' in block_content or 'public User' in block_content or 'private void' in block_content) and 'public class' not in block_content:
                    # Check if it needs DB constants
                    needs_constants = 'DriverManager.getConnection(DB_URL' in block_content

                    if needs_constants:
                        wrapped_content = f'''import java.sql.*;

public class UserProfileService {{
    private static final String DB_URL = "jdbc:postgresql://localhost/appdb";
    private static final String USER = "appuser";
    private static final String PASS = "password";

{block_content}
}}
'''
                    else:
                        wrapped_content = f'''import java.sql.*;

public class UserService {{
{block_content}
}}
'''

                    value = value[:match.start(1)] + wrapped_content + value[match.end(1):]

            example['conversations'][i]['value'] = value

    return example

def main():
    input_file = Path(__file__).parent.parent / 'data' / 'sql_advanced_batch_010.jsonl'

    examples = []
    with open(input_file, 'r') as f:
        for line in f:
            example = json.loads(line)

            if example['id'] == 'sql-injection-000025':
                print(f"Final fix for {example['id']}: Polyglot payloads code block")
                example = fix_example_025_final(example)

            elif example['id'] == 'sql-injection-000027':
                print(f"Final fix for {example['id']}: Wrapping Java methods in classes")
                example = fix_example_027_final(example)

            examples.append(example)

    # Write back
    with open(input_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\nFinal fixes applied to {len(examples)} examples")

if __name__ == '__main__':
    main()
