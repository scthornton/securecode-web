#!/usr/bin/env python3
import json
import re
from pathlib import Path

# Find a SQL injection example in Python
train_path = Path('/Users/scott/perfecxion/datasets/securecode/v2/consolidated/train.jsonl')

with open(train_path, 'r') as f:
    for line in f:
        example = json.loads(line)
        metadata = example.get('metadata', {})

        if metadata.get('subcategory') == 'sql' and metadata.get('lang') == 'python':
            print('=' * 80)
            print('SQL INJECTION EXAMPLE:', example['id'])
            print('=' * 80)
            print('CVE:', example['context'].get('cve', 'N/A'))
            print('Impact:', example['context'].get('impact', 'N/A')[:150])
            print()

            # Extract vulnerable code from second conversation turn
            turn2 = example['conversations'][1]['value']
            code_blocks = re.findall(r'```(\w+)\n(.*?)```', turn2, re.DOTALL)

            if code_blocks:
                print('VULNERABLE CODE BLOCK #1:')
                print('-' * 80)
                lang, code = code_blocks[0]
                print(f'Language: {lang}\n')
                print(code[:800])

                if len(code_blocks) > 1:
                    print('\n\nSECURE CODE BLOCK (from later in conversation):')
                    print('-' * 80)
                    # Get secure version from later turn
                    turn4 = example['conversations'][3]['value'] if len(example['conversations']) > 3 else turn2
                    secure_blocks = re.findall(r'```(\w+)\n(.*?)```', turn4, re.DOTALL)
                    if secure_blocks:
                        lang, code = secure_blocks[0]
                        print(f'Language: {lang}\n')
                        print(code[:800])

            break  # Just show first example
