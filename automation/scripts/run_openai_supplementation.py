#!/usr/bin/env python3
"""
Run OpenAI supplementation batches (201-222) to add language diversity
"""

import subprocess
import sys
from pathlib import Path
import time

def main():
    """Run OpenAI supplementation batches"""
    script_path = Path(__file__).parent / 'run_all_batches.py'

    print("=" * 80)
    print("STARTING OPENAI SUPPLEMENTATION")
    print("=" * 80)
    print("\nGenerating batches 201-222 (196 examples)")
    print("Provider: OpenAI GPT-5.1")
    print("Focus: TypeScript, Ruby, C#, Rust, Kotlin, PHP")
    print("\nEstimated time: 6-8 hours")
    print("=" * 80)
    print()

    # Read the run_all_batches.py and modify for batches 201-222
    with open(script_path, 'r') as f:
        content = f.read()

    # Create temporary modified version
    modified_content = content.replace(
        'START_BATCH = 16',
        'START_BATCH = 201'
    ).replace(
        'END_BATCH = 107',
        'END_BATCH = 222'
    ).replace(
        "PROVIDER = 'claude'",
        "PROVIDER = 'openai'"
    ).replace(
        "generation_plan_expanded.yaml",
        "openai_supplementation_plan.yaml"
    )

    temp_script = Path(__file__).parent / 'run_openai_temp.py'
    with open(temp_script, 'w') as f:
        f.write(modified_content)

    print("Starting OpenAI batch generation...")
    print("Check logs at: automation/logs/batch_run_openai_*.log\n")

    # Run the modified script
    try:
        subprocess.run([sys.executable, str(temp_script)], check=True)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Progress saved.")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    finally:
        # Clean up temp file
        if temp_script.exists():
            temp_script.unlink()

    print("\n" + "=" * 80)
    print("OPENAI SUPPLEMENTATION COMPLETE")
    print("=" * 80)
    return 0

if __name__ == '__main__':
    sys.exit(main())
