#!/bin/bash
# Run OpenAI batches 202-222 for language supplementation
# Total: 21 batches, 196 examples

# Set your OpenAI API key as an environment variable before running
# export OPENAI_API_KEY="your-key-here"
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable not set"
    exit 1
fi

echo "========================================"
echo "OpenAI Batch Generation - Batches 202-222"
echo "========================================"
echo "Start time: $(date)"
echo ""

# Counter for progress tracking
COMPLETED=0
FAILED=0
START_TIME=$(date +%s)

for batch in {202..222}; do
    echo ""
    echo "========================================"
    echo "Starting Batch $batch"
    echo "========================================"

    python3 api_generator.py --batch $batch --provider openai

    if [ $? -eq 0 ]; then
        COMPLETED=$((COMPLETED + 1))
        echo "✓ Batch $batch completed successfully"
    else
        FAILED=$((FAILED + 1))
        echo "✗ Batch $batch failed"
    fi

    # Progress update
    TOTAL_PROCESSED=$((COMPLETED + FAILED))
    echo ""
    echo "Progress: $TOTAL_PROCESSED/21 batches processed"
    echo "Completed: $COMPLETED | Failed: $FAILED"

    # Calculate ETA
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    if [ $TOTAL_PROCESSED -gt 0 ]; then
        AVG_TIME=$((ELAPSED / TOTAL_PROCESSED))
        REMAINING=$((21 - TOTAL_PROCESSED))
        ETA=$((AVG_TIME * REMAINING))
        echo "Average time per batch: $((AVG_TIME / 60)) minutes"
        echo "Estimated time remaining: $((ETA / 60)) minutes"
    fi
    echo ""

    # Brief pause between batches
    if [ $batch -lt 222 ]; then
        sleep 3
    fi
done

echo ""
echo "========================================"
echo "BATCH PROCESSING COMPLETE"
echo "========================================"
echo "End time: $(date)"
echo "Total processed: $((COMPLETED + FAILED))"
echo "Completed: $COMPLETED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -gt 0 ]; then
    echo "⚠ Some batches failed. Check logs for details."
else
    echo "✓ All batches completed successfully!"
fi
