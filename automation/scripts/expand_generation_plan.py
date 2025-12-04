#!/usr/bin/env python3
"""
Expand batch ranges in generation plan to individual batch definitions
"""

import yaml
from pathlib import Path
from typing import List, Dict, Any

def expand_batch_range(batch: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Expand a batch range definition into individual batch definitions."""
    batch_id = batch['batch_id']

    # Check if it's a range (e.g., "016-025")
    if '-' in batch_id and len(batch_id.split('-')) == 2:
        start, end = batch_id.split('-')
        start_num = int(start)
        end_num = int(end)
        batch_count = end_num - start_num + 1

        # Calculate examples per batch
        total_examples = batch['count']
        examples_per_batch = total_examples // batch_count

        # Distribute techniques across batches
        techniques = batch['techniques']
        techniques_per_batch = len(techniques) // batch_count

        individual_batches = []

        for i in range(batch_count):
            batch_num = start_num + i
            batch_id_str = f"{batch_num:03d}"

            # Distribute techniques
            technique_start = i * techniques_per_batch
            technique_end = (i + 1) * techniques_per_batch if i < batch_count - 1 else len(techniques)
            batch_techniques = techniques[technique_start:technique_end]

            # Create individual batch
            individual_batch = {
                'batch_id': batch_id_str,
                'name': f"{batch['name']} - Batch {batch_num}",
                'category': batch['category'],
                'subcategory': batch['subcategory'],
                'count': examples_per_batch,
                'provider': batch['provider'],
                'languages': batch['languages'],
                'techniques': batch_techniques
            }

            # Add breakdown if it exists
            if 'breakdown' in batch:
                individual_batch['breakdown'] = batch['breakdown']

            individual_batches.append(individual_batch)

        return individual_batches
    else:
        # Already an individual batch
        return [batch]

def expand_plan(input_path: Path, output_path: Path):
    """Expand the full generation plan."""
    with open(input_path, 'r') as f:
        plan = yaml.safe_load(f)

    expanded_batches = []

    for batch in plan['batches']:
        individual_batches = expand_batch_range(batch)
        expanded_batches.extend(individual_batches)

    # Update the plan
    plan['batches'] = expanded_batches

    # Update statistics
    plan['statistics']['current_complete'] = 150  # Batches 001-015
    plan['statistics']['remaining'] = 850

    # Write expanded plan
    with open(output_path, 'w') as f:
        yaml.dump(plan, f, default_flow_style=False, sort_keys=False, width=120)

    print(f"Expanded {len(plan['batches'])} individual batch definitions")
    print(f"Output written to: {output_path}")

    # Print summary
    print("\nExpanded batches:")
    for i, batch in enumerate(expanded_batches[:20], 1):
        print(f"  {batch['batch_id']}: {batch['name']} ({batch['count']} examples, {batch['provider']})")
    if len(expanded_batches) > 20:
        print(f"  ... and {len(expanded_batches) - 20} more")

if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent
    input_path = base_dir / 'config' / 'generation_plan.yaml'
    output_path = base_dir / 'config' / 'generation_plan_expanded.yaml'

    expand_plan(input_path, output_path)
