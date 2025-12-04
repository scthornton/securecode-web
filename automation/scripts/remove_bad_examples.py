#!/usr/bin/env python3
"""
Remove incomplete and non-working examples from dataset
"""

import json
from pathlib import Path
from collections import defaultdict

def check_example_validity(example):
    """
    Check if example is valid and complete
    Returns: (is_valid, issues)
    """
    issues = []

    # Check required top-level fields
    required_fields = ['id', 'metadata', 'context', 'conversations']
    for field in required_fields:
        if field not in example:
            issues.append(f"Missing field: {field}")
            return False, issues

    # Check metadata
    meta = example.get('metadata', {})
    required_meta = ['lang', 'category', 'subcategory', 'severity']
    for field in required_meta:
        if field not in meta or not meta[field]:
            issues.append(f"Missing or empty metadata.{field}")
            return False, issues

    # Check conversations
    convs = example.get('conversations', [])
    if len(convs) != 4:
        issues.append(f"Expected 4 conversations, got {len(convs)}")
        return False, issues

    for i, conv in enumerate(convs):
        if 'from' not in conv or 'value' not in conv:
            issues.append(f"Conversation {i+1} missing 'from' or 'value'")
            return False, issues
        if not conv['value'] or len(conv['value']) < 50:
            issues.append(f"Conversation {i+1} has insufficient content")
            return False, issues

    # Check context
    context = example.get('context', {})
    if not context.get('real_world_incident') or len(context.get('real_world_incident', '')) < 10:
        issues.append("Missing or weak real_world_incident")
        return False, issues

    if not context.get('impact') or len(context.get('impact', '')) < 20:
        issues.append("Missing or weak impact")
        return False, issues

    # Check for code blocks
    content = ' '.join([c.get('value', '') for c in convs])
    code_block_count = content.count('```')
    if code_block_count < 2:
        issues.append(f"Insufficient code blocks: {code_block_count} (expected 4+)")
        return False, issues

    # Passed all checks
    return True, []

def process_batch_file(batch_file):
    """
    Process a batch file, removing invalid examples
    Returns: (valid_count, removed_count, removed_ids)
    """
    valid_examples = []
    removed_examples = []

    with open(batch_file) as f:
        for line_num, line in enumerate(f, 1):
            try:
                example = json.loads(line)
                is_valid, issues = check_example_validity(example)

                if is_valid:
                    valid_examples.append(example)
                else:
                    removed_examples.append({
                        'id': example.get('id', f'unknown_line_{line_num}'),
                        'issues': issues
                    })
            except json.JSONDecodeError as e:
                removed_examples.append({
                    'id': f'parse_error_line_{line_num}',
                    'issues': [f"JSON parse error: {e}"]
                })

    # Rewrite file with only valid examples
    if removed_examples:
        with open(batch_file, 'w') as f:
            for example in valid_examples:
                f.write(json.dumps(example) + '\n')

    return len(valid_examples), len(removed_examples), removed_examples

def main():
    """Main cleanup process"""
    print("=" * 80)
    print("REMOVING INCOMPLETE AND NON-WORKING EXAMPLES")
    print("=" * 80)

    data_dir = Path(__file__).parent.parent.parent / 'data'

    # Process all batch files
    total_valid = 0
    total_removed = 0
    files_modified = 0
    all_removed = []

    batch_files = sorted([f for f in data_dir.glob('*_batch_*.jsonl') if '_archived' not in str(f)])

    print(f"\nProcessing {len(batch_files)} batch files...\n")

    for batch_file in batch_files:
        valid_count, removed_count, removed_examples = process_batch_file(batch_file)

        total_valid += valid_count
        total_removed += removed_count

        if removed_count > 0:
            files_modified += 1
            print(f"✓ {batch_file.name}: Kept {valid_count}, Removed {removed_count}")
            for removed in removed_examples:
                print(f"  ✗ {removed['id']}: {', '.join(removed['issues'])}")
                all_removed.append({
                    'file': batch_file.name,
                    'id': removed['id'],
                    'issues': removed['issues']
                })

    print("\n" + "=" * 80)
    print("CLEANUP SUMMARY")
    print("=" * 80)
    print(f"\nTotal valid examples: {total_valid}")
    print(f"Total removed: {total_removed}")
    print(f"Files modified: {files_modified}")
    print(f"Removal rate: {total_removed/(total_valid+total_removed)*100:.1f}%")

    if all_removed:
        print(f"\nRemoved examples:")
        for item in all_removed:
            print(f"  {item['file']} - {item['id']}")

    # Save removal log
    log_file = Path(__file__).parent.parent / 'logs' / 'removed_examples.json'
    with open(log_file, 'w') as f:
        json.dump({
            'total_removed': total_removed,
            'removed_examples': all_removed
        }, f, indent=2)

    print(f"\n✓ Saved removal log to {log_file}")

    print("\n" + "=" * 80)
    print("NEXT STEP: Regenerate consolidated splits")
    print("=" * 80)
    print("\nRun: python3 consolidate_dataset.py")

if __name__ == '__main__':
    main()
