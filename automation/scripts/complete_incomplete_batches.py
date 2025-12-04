#!/usr/bin/env python3
"""
Complete incomplete batches by generating missing examples
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from api_generator import SecureCodeGenerator
import json
import yaml
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_incomplete_batches():
    """Load list of incomplete batches"""
    incomplete = [
        {'batch_id': '004', 'current': 1, 'needed': 9},
        {'batch_id': '020', 'current': 7, 'needed': 3},
        {'batch_id': '030', 'current': 8, 'needed': 2},
        {'batch_id': '057', 'current': 9, 'needed': 1},
        {'batch_id': '069', 'current': 6, 'needed': 4},
        {'batch_id': '074', 'current': 9, 'needed': 1},
        {'batch_id': '096', 'current': 9, 'needed': 1},
        {'batch_id': '099', 'current': 8, 'needed': 2},
        {'batch_id': '101', 'current': 8, 'needed': 2},
        {'batch_id': '102', 'current': 9, 'needed': 1},
    ]
    return incomplete

def complete_batch(generator, batch_id, current_count, needed_count):
    """Complete a single batch by generating missing examples"""

    # Load generation plan
    config_dir = Path(__file__).parent.parent / 'config'
    with open(config_dir / 'generation_plan_expanded.yaml', 'r') as f:
        plan = yaml.safe_load(f)

    # Find batch config
    batch_config = None
    for batch in plan['batches']:
        if batch['batch_id'] == batch_id:
            batch_config = batch
            break

    if not batch_config:
        logger.error(f"Batch {batch_id} not found in generation plan")
        return False

    logger.info(f"\n{'='*60}")
    logger.info(f"Completing Batch {batch_id}")
    logger.info(f"{'='*60}")
    logger.info(f"Current: {current_count}/10")
    logger.info(f"Generating: {needed_count} additional examples")
    logger.info(f"Category: {batch_config['category']}")
    logger.info(f"Subcategory: {batch_config['subcategory']}")

    # Load existing examples to get the next ID number
    data_dir = Path(__file__).parent.parent.parent / 'data'
    batch_files = list(data_dir.glob(f'*_batch_{batch_id}.jsonl'))

    if not batch_files:
        logger.error(f"Could not find batch file for batch {batch_id}")
        return False

    batch_file = batch_files[0]

    # Get existing IDs to determine starting number
    existing_examples = []
    with open(batch_file) as f:
        for line in f:
            existing_examples.append(json.loads(line))

    start_num = current_count + 1

    # Generate missing examples
    new_examples = []
    languages = batch_config['languages']

    for i in range(needed_count):
        example_num = start_num + i
        lang = languages[example_num % len(languages)]

        logger.info(f"\nGenerating example {example_num} ({lang})")

        example = generator.generate_example(
            batch_config=batch_config,
            example_num=example_num,
            language=lang,
            max_retries=3
        )

        if example:
            new_examples.append(example)
            logger.info(f"✓ Generated {example['id']}")
        else:
            logger.error(f"✗ Failed to generate example {example_num}")

    if new_examples:
        # Append to existing batch file
        with open(batch_file, 'a') as f:
            for example in new_examples:
                f.write(json.dumps(example) + '\n')

        logger.info(f"\n✓ Added {len(new_examples)} examples to {batch_file.name}")
        logger.info(f"Batch {batch_id} now has {current_count + len(new_examples)}/10 examples")
        return True
    else:
        logger.error(f"\n✗ Failed to generate any examples for batch {batch_id}")
        return False

def main():
    """Main completion process"""
    logger.info("Starting incomplete batch completion process...")

    incomplete_batches = load_incomplete_batches()
    total_needed = sum(b['needed'] for b in incomplete_batches)

    logger.info(f"\nIncomplete batches: {len(incomplete_batches)}")
    logger.info(f"Total missing examples: {total_needed}")

    # Initialize generator
    generator = SecureCodeGenerator(
        provider='claude'
    )

    completed = 0
    failed = 0

    for batch in incomplete_batches:
        success = complete_batch(
            generator,
            batch['batch_id'],
            batch['current'],
            batch['needed']
        )

        if success:
            completed += 1
        else:
            failed += 1

    logger.info(f"\n{'='*60}")
    logger.info("COMPLETION SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Batches completed: {completed}/{len(incomplete_batches)}")
    logger.info(f"Batches failed: {failed}")
    logger.info(f"Total examples generated: {total_needed - failed}")  # Rough estimate

if __name__ == '__main__':
    main()
