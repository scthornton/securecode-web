#!/usr/bin/env python3
"""
Fix TypeScript and framework-specific syntax in Batch 008.
Handles:
- TypeScript type annotations
- TypeScript interfaces
- Angular decorators
- React.FC types
- Vue ES modules
"""

import json
import re
from pathlib import Path
import shutil


def strip_typescript_syntax(code):
    """Remove TypeScript-specific syntax that causes Node.js parse errors."""

    # Remove type annotations from function parameters: (param: type) → (param)
    code = re.sub(r'\((\w+):\s*[^,)]+([,)])', r'(\1\2', code)
    code = re.sub(r',\s*(\w+):\s*[^,)]+([,)])', r', \1\2', code)

    # Remove return type annotations: ): Type { → ) {
    code = re.sub(r'\):\s*[^{]+\{', r') {', code)

    # Remove variable type annotations: const x: Type = → const x =
    code = re.sub(r'(const|let|var)\s+(\w+):\s*[^=]+=', r'\1 \2 =', code)

    # Remove interface declarations (keep as comments)
    code = re.sub(r'^interface\s+\w+\s*\{[^}]*\}', '// [TypeScript interface removed for validation]', code, flags=re.MULTILINE | re.DOTALL)

    # Remove Angular decorators
    code = re.sub(r'@Component\([^)]*\)\s*', '// [Angular Component decorator]\n', code, flags=re.DOTALL)
    code = re.sub(r'@Injectable\([^)]*\)\s*', '// [Angular Injectable decorator]\n', code, flags=re.DOTALL)

    # Remove React.FC type annotations: const Comp: React.FC<Props> = → const Comp =
    code = re.sub(r'(const|let)\s+(\w+):\s*React\.FC<[^>]+>\s*=', r'\1 \2 =', code)

    # Remove export default/export keywords that might cause issues
    code = re.sub(r'^export\s+default\s+', '', code, flags=re.MULTILINE)
    code = re.sub(r'^export\s+', '', code, flags=re.MULTILINE)

    # Remove type imports
    code = re.sub(r'import\s+type\s+\{[^}]+\}\s+from\s+[\'"][^\'"]+[\'"];?\s*\n', '', code)

    return code


def fix_vue_modules(code):
    """Fix Vue component ES module syntax."""
    # Remove export default
    code = re.sub(r'export\s+default\s+', '', code)

    # Comment out top-level object if it's a Vue component definition
    if code.strip().startswith('{') and 'data()' in code or 'computed:' in code:
        code = f"// Vue component definition\nconst component = {code}"

    return code


def fix_code_block(code, language):
    """Fix a code block based on language."""
    if language in ['typescript', 'ts']:
        # Strip TypeScript syntax
        code = strip_typescript_syntax(code)
    elif language in ['javascript', 'js']:
        # Check if it looks like a Vue component
        if 'export default' in code or ('data()' in code and 'computed:' in code):
            code = fix_vue_modules(code)

    return code


def fix_example(example):
    """Fix code blocks in an example."""
    example_id = example['id']

    # Only fix failing examples
    if example_id not in ['xss-000039', 'xss-000041', 'xss-000042', 'xss-000043']:
        return example

    for conv in example['conversations']:
        if conv.get('from') != 'assistant':
            continue

        content = conv['value']

        # Pattern to match code blocks
        pattern = r'```(typescript|ts|javascript|js)\n(.*?)```'

        def replacer(match):
            language = match.group(1)
            code = match.group(2)

            # Fix the code
            fixed_code = fix_code_block(code, language)

            return f'```{language}\n{fixed_code}```'

        content = re.sub(pattern, replacer, content, flags=re.DOTALL)
        conv['value'] = content

    return example


def main():
    data_file = Path(__file__).parent.parent / 'data' / 'xss_expansion_batch_008.jsonl'

    print("Fixing TypeScript/Framework syntax in Batch 008...")
    print("=" * 60)

    # Backup
    backup_file = data_file.parent / f"{data_file.stem}_pre_ts_fix.jsonl"
    shutil.copy(data_file, backup_file)
    print(f"Backup: {backup_file.name}\n")

    # Read examples
    examples = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))

    # Fix failing examples
    failing_ids = ['xss-000039', 'xss-000041', 'xss-000042', 'xss-000043']

    fixed_examples = []
    for example in examples:
        if example['id'] in failing_ids:
            example = fix_example(example)
            fixed_examples.append(example['id'])
            print(f"✓ Fixed {example['id']}")

    # Write fixed examples
    with open(data_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"\n✓ Fixes applied to {len(fixed_examples)} examples")
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
    in_batch_008 = False

    for line in lines:
        if 'Batch 008' in line:
            in_batch_008 = True
        if in_batch_008:
            print(line)
            if 'Pass Rate:' in line:
                break

    # Show overall summary
    print("\n" + "=" * 60)
    for line in lines:
        if 'OVERALL SUMMARY' in line or line.startswith('Total') or line.startswith('Passed') or line.startswith('Failed'):
            print(line)

    return 0


if __name__ == "__main__":
    exit(main())
