#!/usr/bin/env python3
"""
Consolidate SecureCode v2.0 dataset into train/test/val splits
Uses stratified sampling to maintain OWASP category and language distribution
"""

import json
import random
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict

def load_all_examples() -> List[Dict]:
    """Load all examples from data directory, excluding duplicates"""
    data_dir = Path(__file__).parent.parent.parent / 'data'

    # Exclude archived duplicates
    examples = []
    for f in sorted(data_dir.glob('*_batch_*.jsonl')):
        # Skip archived duplicates
        if '_archived' in str(f):
            continue

        with open(f) as file:
            for line in file:
                try:
                    example = json.loads(line)
                    examples.append(example)
                except json.JSONDecodeError as e:
                    print(f"ERROR parsing {f.name}: {e}")

    return examples

def stratified_split(examples: List[Dict], train_pct=0.70, val_pct=0.15, test_pct=0.15):
    """
    Perform stratified split by OWASP category and language

    Args:
        examples: List of all examples
        train_pct: Training set percentage (default 70%)
        val_pct: Validation set percentage (default 15%)
        test_pct: Test set percentage (default 15%)

    Returns:
        Tuple of (train, val, test) example lists
    """
    # Group by category
    by_category = defaultdict(list)
    for ex in examples:
        category = ex.get('metadata', {}).get('category', 'unknown')
        by_category[category].append(ex)

    train_set = []
    val_set = []
    test_set = []

    random.seed(42)  # For reproducibility

    # Split each category proportionally
    for category, cat_examples in by_category.items():
        # Shuffle within category
        random.shuffle(cat_examples)

        n = len(cat_examples)
        train_end = int(n * train_pct)
        val_end = train_end + int(n * val_pct)

        train_set.extend(cat_examples[:train_end])
        val_set.extend(cat_examples[train_end:val_end])
        test_set.extend(cat_examples[val_end:])

    # Shuffle final sets
    random.shuffle(train_set)
    random.shuffle(val_set)
    random.shuffle(test_set)

    return train_set, val_set, test_set

def analyze_split_distribution(split_name: str, examples: List[Dict]):
    """Analyze and print distribution statistics for a split"""
    print(f"\n{split_name} Set:")
    print(f"  Total: {len(examples)} examples")

    # Category distribution
    categories = Counter(ex.get('metadata', {}).get('category', 'unknown') for ex in examples)
    print(f"\n  Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        pct = count / len(examples) * 100
        print(f"    {cat:30s}: {count:4d} ({pct:5.1f}%)")

    # Language distribution
    languages = Counter(ex.get('metadata', {}).get('lang', 'unknown') for ex in examples)
    print(f"\n  Top Languages:")
    for lang, count in sorted(languages.items(), key=lambda x: -x[1])[:10]:
        pct = count / len(examples) * 100
        print(f"    {lang:15s}: {count:4d} ({pct:5.1f}%)")

    # Severity distribution
    severities = Counter(ex.get('metadata', {}).get('severity', 'unknown') for ex in examples)
    print(f"\n  Severity:")
    for sev, count in sorted(severities.items(), key=lambda x: -x[1]):
        pct = count / len(examples) * 100
        print(f"    {sev:10s}: {count:4d} ({pct:5.1f}%)")

def save_split(split_name: str, examples: List[Dict], output_dir: Path):
    """Save split to JSONL file"""
    output_file = output_dir / f"{split_name}.jsonl"

    with open(output_file, 'w') as f:
        for example in examples:
            f.write(json.dumps(example) + '\n')

    print(f"\n✓ Saved {len(examples)} examples to {output_file}")

def main():
    """Main consolidation process"""
    print("=" * 80)
    print("SECURECODE v2.0 DATASET CONSOLIDATION")
    print("=" * 80)

    # Load all examples
    print("\nLoading dataset...")
    examples = load_all_examples()
    print(f"Loaded {len(examples)} total examples")

    # Perform stratified split
    print("\nPerforming stratified split (70/15/15)...")
    train, val, test = stratified_split(examples, train_pct=0.70, val_pct=0.15, test_pct=0.15)

    # Analyze distributions
    print("\n" + "=" * 80)
    print("SPLIT ANALYSIS")
    print("=" * 80)
    analyze_split_distribution("Training", train)
    analyze_split_distribution("Validation", val)
    analyze_split_distribution("Test", test)

    # Save splits
    output_dir = Path(__file__).parent.parent.parent / 'consolidated'
    output_dir.mkdir(exist_ok=True)

    print("\n" + "=" * 80)
    print("SAVING SPLITS")
    print("=" * 80)

    save_split('train', train, output_dir)
    save_split('val', val, output_dir)
    save_split('test', test, output_dir)

    print("\n" + "=" * 80)
    print("CONSOLIDATION COMPLETE")
    print("=" * 80)
    print(f"\nOutput directory: {output_dir}")
    print(f"Files created:")
    print(f"  - train.jsonl ({len(train)} examples)")
    print(f"  - val.jsonl ({len(val)} examples)")
    print(f"  - test.jsonl ({len(test)} examples)")

    # Create metadata file
    metadata = {
        'dataset_name': 'SecureCode v2.0',
        'version': '2.0.0',
        'total_examples': len(examples),
        'splits': {
            'train': len(train),
            'val': len(val),
            'test': len(test)
        },
        'categories': list(Counter(ex.get('metadata', {}).get('category', 'unknown') for ex in examples).keys()),
        'languages': list(Counter(ex.get('metadata', {}).get('lang', 'unknown') for ex in examples).keys()),
        'split_strategy': 'stratified by OWASP category',
        'random_seed': 42
    }

    with open(output_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✓ Saved metadata to {output_dir / 'metadata.json'}")
    print("\nDataset ready for training!")

if __name__ == '__main__':
    main()
