#!/usr/bin/env python3
"""
Progress Monitor - Track batch generation progress in real-time
"""

import json
import os
from pathlib import Path
from datetime import datetime
import time

DATA_DIR = Path(__file__).parent.parent.parent / 'data'
LOGS_DIR = Path(__file__).parent.parent / 'logs'

def count_examples_in_file(filepath):
    """Count examples in a JSONL file"""
    try:
        with open(filepath, 'r') as f:
            return sum(1 for line in f if line.strip())
    except:
        return 0

def get_batch_status():
    """Get status of all batches"""
    # Expected batches: 001-010 (manual), 011-101 (automated)
    manual_batches = list(range(1, 11))  # 001-010
    auto_batches = list(range(11, 102))  # 011-101

    status = {
        'manual_complete': 0,
        'auto_complete': 0,
        'auto_in_progress': None,
        'total_examples': 0,
        'batches': []
    }

    # Check manual batches (already done)
    for i in manual_batches:
        # Check for various file patterns
        found = False
        for pattern in [
            f'*_batch_{i:03d}.jsonl',
            f'batch_{i:03d}.jsonl',
            f'*{i:03d}*.jsonl'
        ]:
            files = list(DATA_DIR.glob(pattern))
            if files:
                examples = count_examples_in_file(files[0])
                status['total_examples'] += examples
                status['manual_complete'] += 1
                status['batches'].append({
                    'id': f'{i:03d}',
                    'status': 'complete',
                    'examples': examples,
                    'file': files[0].name
                })
                found = True
                break

    # Check automated batches (011-101)
    for i in auto_batches:
        batch_id = f'{i:03d}'

        # Check for batch file
        batch_files = list(DATA_DIR.glob(f'*_batch_{batch_id}.jsonl'))

        if batch_files:
            examples = count_examples_in_file(batch_files[0])
            status['total_examples'] += examples

            if examples >= 10:
                status['auto_complete'] += 1
                status['batches'].append({
                    'id': batch_id,
                    'status': 'complete',
                    'examples': examples,
                    'file': batch_files[0].name
                })
            else:
                # In progress
                status['auto_in_progress'] = batch_id
                status['batches'].append({
                    'id': batch_id,
                    'status': 'in_progress',
                    'examples': examples,
                    'file': batch_files[0].name
                })
        else:
            # Check if batch is in progress (check logs)
            log_file = LOGS_DIR / f'batch_{batch_id}_run.log'
            if log_file.exists() and log_file.stat().st_size > 0:
                status['auto_in_progress'] = batch_id
                status['batches'].append({
                    'id': batch_id,
                    'status': 'in_progress',
                    'examples': 0,
                    'file': None
                })
                break  # Only one batch in progress at a time
            else:
                # Not started yet
                break

    return status

def parse_generation_log():
    """Parse the generation.log to get current status"""
    log_file = LOGS_DIR / 'generation.log'
    if not log_file.exists():
        return None

    # Read last 100 lines
    with open(log_file, 'r') as f:
        lines = f.readlines()[-100:]

    current_batch = None
    current_example = None
    current_lang = None

    for line in reversed(lines):
        if 'Batch' in line and '====' in line:
            # Found batch header like "Batch 012: NoSQL + Command Advanced"
            parts = line.split('Batch')[1].split(':')
            if parts:
                current_batch = parts[0].strip()
                break
        elif 'Generating example' in line:
            # Line like: "Generating example 5 (python) - attempt 1/3"
            if '(' in line and ')' in line:
                num_part = line.split('example')[1].split('(')[0].strip()
                lang_part = line.split('(')[1].split(')')[0].strip()
                current_example = int(num_part)
                current_lang = lang_part
                break

    return {
        'current_batch': current_batch,
        'current_example': current_example,
        'current_lang': current_lang
    }

def format_time_estimate(total_batches, completed_batches, avg_time_per_batch):
    """Format time estimate for remaining batches"""
    if completed_batches == 0:
        return "Calculating..."

    remaining = total_batches - completed_batches
    seconds_remaining = remaining * avg_time_per_batch

    hours = int(seconds_remaining // 3600)
    minutes = int((seconds_remaining % 3600) // 60)

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def display_progress():
    """Display comprehensive progress information"""
    status = get_batch_status()
    log_status = parse_generation_log()

    print("\n" + "="*80)
    print("SECUR ECODE v2.0 - BATCH GENERATION PROGRESS")
    print("="*80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Overall stats
    total_batches = 101  # 001-101
    completed = status['manual_complete'] + status['auto_complete']
    completion_pct = (completed / total_batches) * 100

    print(f"📊 OVERALL PROGRESS")
    print(f"   Batches: {completed}/{total_batches} ({completion_pct:.1f}%)")
    print(f"   Examples: {status['total_examples']}/1,010")
    print()

    # Manual vs Automated
    print(f"📝 MANUAL BATCHES (001-010)")
    print(f"   Complete: {status['manual_complete']}/10")
    print()

    print(f"🤖 AUTOMATED BATCHES (011-101)")
    print(f"   Complete: {status['auto_complete']}/91")
    print(f"   Remaining: {91 - status['auto_complete']}")

    if status['auto_in_progress']:
        print(f"   Current: Batch {status['auto_in_progress']}")

    print()

    # Current activity
    if log_status and log_status['current_batch']:
        print(f"⚡ CURRENT ACTIVITY")
        print(f"   Batch: {log_status['current_batch']}")
        if log_status['current_example']:
            print(f"   Example: {log_status['current_example']}/10 ({log_status['current_lang']})")
        print()

    # Time estimate (assume ~18 minutes per batch based on batch 011)
    if status['auto_complete'] > 0:
        avg_time = 18 * 60  # 18 minutes in seconds
        remaining_batches = 91 - status['auto_complete']
        eta = format_time_estimate(91, status['auto_complete'], avg_time)
        print(f"⏱️  ESTIMATED TIME REMAINING: {eta}")
        print()

    # Recent completions
    recent = [b for b in status['batches'] if b['status'] == 'complete'][-5:]
    if recent:
        print(f"✅ RECENTLY COMPLETED")
        for batch in recent:
            print(f"   Batch {batch['id']}: {batch['examples']} examples ({batch['file']})")
        print()

    # Cost estimate
    total_cost = status['total_examples'] * 0.11  # ~$0.11 per example
    estimated_total = 1010 * 0.11
    print(f"💰 COST ESTIMATE")
    print(f"   Current: ${total_cost:.2f}")
    print(f"   Projected total: ${estimated_total:.2f}")

    print("="*80)

if __name__ == '__main__':
    import sys

    # Check for --watch flag
    watch = '--watch' in sys.argv or '-w' in sys.argv

    if watch:
        print("Watching progress... (Ctrl+C to exit)\n")
        try:
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                display_progress()
                time.sleep(30)  # Update every 30 seconds
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
    else:
        display_progress()
