#!/usr/bin/env python3
"""
Batch Runner - Process all remaining batches sequentially
Generates batches 012-101 (900 examples total)
"""

import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
START_BATCH = 16  # Resume from batch 016
END_BATCH = 107  # Updated to match expanded plan (batches 016-107)
PROVIDER = 'claude'
SCRIPT_PATH = Path(__file__).parent / 'api_generator.py'
LOGS_DIR = Path(__file__).parent.parent / 'logs'
DATA_DIR = Path(__file__).parent.parent.parent / 'data'

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

class BatchRunner:
    def __init__(self):
        self.start_time = datetime.now()
        self.completed_batches = []
        self.failed_batches = []
        self.total_examples = 0
        self.total_api_calls = 0
        self.total_retries = 0
        self.total_cost = 0.0

    def run_batch(self, batch_num):
        """Run a single batch and return success status"""
        batch_id = f"{batch_num:03d}"
        log_file = LOGS_DIR / f"batch_{batch_id}_run.log"

        print(f"\n{'='*70}")
        print(f"Starting Batch {batch_id}")
        print(f"{'='*70}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Log file: {log_file}")

        try:
            # Run the batch
            cmd = [
                'python3',
                str(SCRIPT_PATH),
                '--batch', batch_id,
                '--provider', PROVIDER
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout per batch
            )

            # Write log file
            with open(log_file, 'w') as f:
                f.write(result.stdout)
                if result.stderr:
                    f.write("\n\nSTDERR:\n")
                    f.write(result.stderr)

            # Parse results from output
            success = "FINAL STATISTICS" in result.stdout

            if success:
                # Extract statistics
                for line in result.stdout.split('\n'):
                    if 'Successful:' in line and '(' in line:
                        # Extract count like "Successful: 10 (100.0%)"
                        parts = line.split(':')[1].strip().split()
                        self.total_examples += int(parts[0])
                    elif 'Total API Calls:' in line:
                        self.total_api_calls += int(line.split(':')[1].strip())
                    elif 'Total Retries:' in line:
                        self.total_retries += int(line.split(':')[1].strip())
                    elif 'Estimated Cost:' in line:
                        cost_str = line.split('$')[1].strip()
                        self.total_cost += float(cost_str)

                self.completed_batches.append(batch_id)
                print(f"✓ Batch {batch_id} completed successfully")
                return True
            else:
                self.failed_batches.append(batch_id)
                print(f"✗ Batch {batch_id} failed")
                print(f"Check log: {log_file}")
                return False

        except subprocess.TimeoutExpired:
            print(f"✗ Batch {batch_id} timed out after 30 minutes")
            self.failed_batches.append(batch_id)
            return False
        except Exception as e:
            print(f"✗ Batch {batch_id} error: {e}")
            self.failed_batches.append(batch_id)
            return False

    def print_progress(self, current_batch):
        """Print overall progress statistics"""
        elapsed = datetime.now() - self.start_time
        completed = len(self.completed_batches)
        total_batches = END_BATCH - START_BATCH + 1

        print(f"\n{'='*70}")
        print(f"PROGRESS UPDATE")
        print(f"{'='*70}")
        print(f"Completed batches: {completed}/{total_batches}")
        print(f"Failed batches: {len(self.failed_batches)}")
        print(f"Total examples generated: {self.total_examples}")
        print(f"Total API calls: {self.total_api_calls}")
        print(f"Total retries: {self.total_retries}")
        print(f"Total cost: ${self.total_cost:.2f}")
        print(f"Elapsed time: {elapsed}")

        if completed > 0:
            avg_time = elapsed / completed
            remaining = total_batches - completed
            eta = avg_time * remaining
            print(f"Average time per batch: {avg_time}")
            print(f"Estimated time remaining: {eta}")
        print(f"{'='*70}\n")

    def run_all(self):
        """Run all batches from START_BATCH to END_BATCH"""
        print(f"\n{'#'*70}")
        print(f"BATCH PROCESSING STARTED")
        print(f"{'#'*70}")
        print(f"Batches: {START_BATCH:03d} to {END_BATCH:03d}")
        print(f"Total batches: {END_BATCH - START_BATCH + 1}")
        print(f"Expected examples: {(END_BATCH - START_BATCH + 1) * 10}")
        print(f"Provider: {PROVIDER}")
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*70}\n")

        for batch_num in range(START_BATCH, END_BATCH + 1):
            success = self.run_batch(batch_num)

            # Print progress every 5 batches
            if batch_num % 5 == 0 or not success:
                self.print_progress(batch_num)

            # Brief pause between batches to avoid rate limiting
            if batch_num < END_BATCH:
                time.sleep(2)

        # Final summary
        self.print_final_summary()

    def print_final_summary(self):
        """Print final summary of all batch processing"""
        elapsed = datetime.now() - self.start_time

        print(f"\n{'#'*70}")
        print(f"BATCH PROCESSING COMPLETE")
        print(f"{'#'*70}")
        print(f"Total batches processed: {len(self.completed_batches) + len(self.failed_batches)}")
        print(f"Successful: {len(self.completed_batches)}")
        print(f"Failed: {len(self.failed_batches)}")
        print(f"\nTotal examples generated: {self.total_examples}")
        print(f"Total API calls: {self.total_api_calls}")
        print(f"Total retries: {self.total_retries}")
        print(f"Total cost: ${self.total_cost:.2f}")
        print(f"\nTotal elapsed time: {elapsed}")
        print(f"Average time per batch: {elapsed / max(len(self.completed_batches), 1)}")

        if self.failed_batches:
            print(f"\n⚠ Failed batches: {', '.join(self.failed_batches)}")
            print(f"You can rerun failed batches individually using:")
            for batch_id in self.failed_batches:
                print(f"  python3 {SCRIPT_PATH} --batch {batch_id} --provider {PROVIDER}")
        else:
            print(f"\n✓ All batches completed successfully!")

        print(f"{'#'*70}\n")

        # Write summary to file
        summary_file = LOGS_DIR / f"batch_run_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(summary_file, 'w') as f:
            f.write(f"Batch Processing Summary\n")
            f.write(f"========================\n\n")
            f.write(f"Batches: {START_BATCH:03d} to {END_BATCH:03d}\n")
            f.write(f"Successful: {len(self.completed_batches)}\n")
            f.write(f"Failed: {len(self.failed_batches)}\n")
            f.write(f"Total examples: {self.total_examples}\n")
            f.write(f"Total API calls: {self.total_api_calls}\n")
            f.write(f"Total retries: {self.total_retries}\n")
            f.write(f"Total cost: ${self.total_cost:.2f}\n")
            f.write(f"Elapsed time: {elapsed}\n\n")

            if self.failed_batches:
                f.write(f"Failed batches: {', '.join(self.failed_batches)}\n")

        print(f"Summary saved to: {summary_file}")

if __name__ == '__main__':
    runner = BatchRunner()
    try:
        runner.run_all()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        runner.print_final_summary()
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        runner.print_final_summary()
        sys.exit(1)
