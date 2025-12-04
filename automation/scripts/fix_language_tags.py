#!/usr/bin/env python3
"""
Fix invalid language tags to comply with CONTRIBUTING.md
Valid languages: python, javascript, java, go, php, csharp, typescript, ruby, rust, kotlin
"""

import json
from pathlib import Path

# Language mapping per CONTRIBUTING.md
LANGUAGE_MAPPING = {
    'docker': 'yaml',  # Dockerfile configs → YAML
    'kubernetes': 'yaml',  # K8s manifests → YAML
    'vue': 'javascript',  # Vue.js → JavaScript
    'react': 'javascript',  # React → JavaScript
    'angular': 'typescript',  # Angular → TypeScript
    'bash': 'python',  # Shell scripts → Python (closest match)
    'shell': 'python',  # Shell scripts → Python
}

VALID_LANGUAGES = {
    'python', 'javascript', 'java', 'go', 'php', 'csharp',
    'typescript', 'ruby', 'rust', 'kotlin'
}

def fix_language_tag(example):
    """
    Fix language metadata to use valid values
    """
    metadata = example.get('metadata', {})
    lang = metadata.get('lang', '').lower()

    if not lang:
        return False, None

    if lang in VALID_LANGUAGES:
        return False, None

    # Check if needs mapping
    if lang in LANGUAGE_MAPPING:
        new_lang = LANGUAGE_MAPPING[lang]
        metadata['lang'] = new_lang
        return True, f"Mapped '{lang}' → '{new_lang}'"

    # Unknown invalid language
    return False, f"UNMAPPED: '{lang}' (needs manual review)"

def process_file(file_path):
    """Process a single JSONL file"""
    print(f"\nProcessing: {file_path.name}")

    examples = []
    fixed_count = 0
    unmapped = []

    with open(file_path) as f:
        for line_num, line in enumerate(f, 1):
            example = json.loads(line)
            was_fixed, reason = fix_language_tag(example)

            if was_fixed:
                fixed_count += 1
                if 'UNMAPPED' not in reason:
                    if fixed_count <= 10:
                        print(f"  ✓ {example.get('id', f'line_{line_num}')}: {reason}")
                else:
                    unmapped.append((example.get('id'), reason))

            examples.append(example)

    # Write back
    with open(file_path, 'w') as f:
        for example in examples:
            f.write(json.dumps(example) + '\n')

    if unmapped:
        print(f"  ⚠️  {len(unmapped)} unmapped languages need manual review")
        for ex_id, msg in unmapped[:5]:
            print(f"     {ex_id}: {msg}")

    print(f"  Fixed {fixed_count}/{len(examples)} examples")
    return fixed_count, len(examples), unmapped

def main():
    print("="*80)
    print("LANGUAGE TAG FIX")
    print("="*80)
    print("\nFixing language tags to comply with CONTRIBUTING.md...")
    print(f"Valid languages: {', '.join(sorted(VALID_LANGUAGES))}\n")

    # Process data files
    data_dir = Path(__file__).parent.parent.parent / 'data'
    batch_files = sorted(data_dir.glob('*_batch_*.jsonl'))

    total_fixed = 0
    total_examples = 0
    all_unmapped = []

    for batch_file in batch_files:
        fixed, total, unmapped = process_file(batch_file)
        total_fixed += fixed
        total_examples += total
        all_unmapped.extend(unmapped)

    # Process consolidated files
    consolidated_dir = Path(__file__).parent.parent.parent / 'consolidated'
    for split_file in ['train.jsonl', 'val.jsonl', 'test.jsonl']:
        split_path = consolidated_dir / split_file
        if split_path.exists():
            fixed, total, unmapped = process_file(split_path)
            total_fixed += fixed
            total_examples += total
            all_unmapped.extend(unmapped)

    print("\n" + "="*80)
    print(f"COMPLETE: Fixed {total_fixed} language tags across {total_examples} examples")

    if all_unmapped:
        print(f"\n⚠️  {len(all_unmapped)} examples need manual language review")
        print("First 10:")
        for ex_id, msg in all_unmapped[:10]:
            print(f"   {ex_id}: {msg}")
    else:
        print("\n✅ All language tags now valid!")

    print("="*80)

if __name__ == '__main__':
    main()
