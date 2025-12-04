#!/bin/bash
# Test API generation with a small batch
# This helps verify API keys and configuration before full generation

set -e  # Exit on error

echo "========================================"
echo "SecureCode v2.0 - API Generation Test"
echo "========================================"
echo ""

# Check for API keys
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "ERROR: No API keys found"
    echo ""
    echo "Set one of:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo "  export OPENAI_API_KEY='your-key-here'"
    echo ""
    exit 1
fi

# Determine which provider to test
PROVIDER="claude"
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "✓ Found ANTHROPIC_API_KEY"
    PROVIDER="claude"
elif [ -n "$OPENAI_API_KEY" ]; then
    echo "✓ Found OPENAI_API_KEY"
    PROVIDER="openai"
fi

echo "Testing with provider: $PROVIDER"
echo ""

# Test 1: Dry run to verify configuration
echo "Test 1: Dry run (verifying configuration)"
echo "----------------------------------------"
python3 automation/scripts/api_generator.py \
    --batch 011 \
    --provider $PROVIDER \
    --dry-run

echo ""
echo "✓ Configuration valid"
echo ""

# Test 2: Generate 2 examples
echo "Test 2: Generate 2 examples (real API calls)"
echo "---------------------------------------------"
echo "This will cost ~$0.50 in API fees"
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Temporarily modify generation plan to generate only 2 examples
    python3 << 'PYTHON_SCRIPT'
import yaml
from pathlib import Path

# Load generation plan
config_file = Path('automation/config/generation_plan.yaml')
with open(config_file, 'r') as f:
    plan = yaml.safe_load(f)

# Modify batch 011 to generate only 2 examples
for batch in plan['batches']:
    if batch['batch_id'] == '011':
        batch['count'] = 2
        break

# Save test version
test_config = Path('automation/config/generation_plan_test.yaml')
with open(test_config, 'w') as f:
    yaml.dump(plan, f)

print("Created test configuration: 2 examples only")
PYTHON_SCRIPT

    # Temporarily replace config
    mv automation/config/generation_plan.yaml automation/config/generation_plan_backup.yaml
    mv automation/config/generation_plan_test.yaml automation/config/generation_plan.yaml

    # Generate
    python3 automation/scripts/api_generator.py \
        --batch 011 \
        --provider $PROVIDER

    # Restore original config
    mv automation/config/generation_plan.yaml automation/config/generation_plan_test.yaml
    mv automation/config/generation_plan_backup.yaml automation/config/generation_plan.yaml

    echo ""
    echo "✓ Test generation complete"
    echo ""

    # Validate generated examples
    echo "Test 3: Validate generated examples"
    echo "------------------------------------"
    python3 generation/validate_all_batches.py

    echo ""
    echo "========================================"
    echo "✓ ALL TESTS PASSED"
    echo "========================================"
    echo ""
    echo "You're ready to run full generation:"
    echo "  ./automation/scripts/run_generation.sh"
    echo ""
else
    echo "Test cancelled"
    exit 0
fi
