#!/bin/bash
# Main execution script for generating all 910 remaining examples
# Estimated time: 6-12 hours
# Estimated cost: $60-100

set -e  # Exit on error

echo "========================================"
echo "SecureCode v2.0 - Full Generation"
echo "========================================"
echo ""
echo "This will generate 910 examples using AI APIs"
echo "Estimated time: 6-12 hours"
echo "Estimated cost: $60-100"
echo ""

# Check for API keys
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "ERROR: No API keys found"
    echo ""
    echo "Set API keys:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo "  export OPENAI_API_KEY='your-key-here'"
    echo ""
    exit 1
fi

echo "✓ API keys found"
echo ""

# Confirm execution
read -p "Continue with full generation? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

# Create logs directory
mkdir -p automation/logs

# Log file
LOGFILE="automation/logs/generation_$(date +%Y%m%d_%H%M%S).log"
echo "Logging to: $LOGFILE"
echo ""

# ========================================
# PHASE 1: Complete A03 Injection (50 examples)
# ========================================

echo "========================================"
echo "PHASE 1: Injection Category (50 examples)"
echo "========================================"
echo ""

# Batch 011: XSS Expansion Part 2 (OpenAI - simpler patterns)
echo "Generating Batch 011: XSS Expansion Part 2..."
python3 automation/scripts/api_generator.py \
    --batch 011 \
    --provider openai \
    --parallel 3 \
    2>&1 | tee -a $LOGFILE

# Batch 012: NoSQL + Command Advanced (Claude - complex)
echo "Generating Batch 012: NoSQL + Command Advanced..."
python3 automation/scripts/api_generator.py \
    --batch 012 \
    --provider claude \
    --parallel 2 \
    2>&1 | tee -a $LOGFILE

# Batch 013: XML/XXE (Claude - complex)
echo "Generating Batch 013: XML/XXE Injection..."
python3 automation/scripts/api_generator.py \
    --batch 013 \
    --provider claude \
    --parallel 2 \
    2>&1 | tee -a $LOGFILE

# Batch 014: Template + XSS Final (Claude)
echo "Generating Batch 014: Template + XSS Final..."
python3 automation/scripts/api_generator.py \
    --batch 014 \
    --provider claude \
    --parallel 2 \
    2>&1 | tee -a $LOGFILE

# Batch 015: SQL + LDAP Final (Claude)
echo "Generating Batch 015: SQL + LDAP Final..."
python3 automation/scripts/api_generator.py \
    --batch 015 \
    --provider claude \
    --parallel 2 \
    2>&1 | tee -a $LOGFILE

echo "✓ Phase 1 complete (50 injection examples)"
echo ""

# ========================================
# PHASE 2: Authentication Failures (150 examples)
# ========================================

echo "========================================"
echo "PHASE 2: Authentication Failures (150 examples)"
echo "========================================"
echo ""

# Batches 016-025: Auth failures (Claude - critical security)
for batch_num in {016..025}; do
    echo "Generating Batch $batch_num: Authentication Failures..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider claude \
        --parallel 3 \
        2>&1 | tee -a $LOGFILE

    # Small delay between batches
    sleep 10
done

# Batches 026-030: Simpler auth patterns (OpenAI)
for batch_num in {026..030}; do
    echo "Generating Batch $batch_num: Authentication Failures..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider openai \
        --parallel 4 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 2 complete (150 auth examples)"
echo ""

# ========================================
# PHASE 3: Broken Access Control (150 examples)
# ========================================

echo "========================================"
echo "PHASE 3: Broken Access Control (150 examples)"
echo "========================================"
echo ""

# Batches 031-045: Access control (Claude)
for batch_num in {031..045}; do
    echo "Generating Batch $batch_num: Broken Access Control..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider claude \
        --parallel 3 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 3 complete (150 access control examples)"
echo ""

# ========================================
# PHASE 4: Security Misconfiguration (120 examples)
# ========================================

echo "========================================"
echo "PHASE 4: Security Misconfiguration (120 examples)"
echo "========================================"
echo ""

# Batches 046-057: Misconfigurations (OpenAI - simpler)
for batch_num in {046..057}; do
    echo "Generating Batch $batch_num: Security Misconfiguration..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider openai \
        --parallel 4 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 4 complete (120 misconfiguration examples)"
echo ""

# ========================================
# PHASE 5: Cryptographic Failures (100 examples)
# ========================================

echo "========================================"
echo "PHASE 5: Cryptographic Failures (100 examples)"
echo "========================================"
echo ""

# Batches 058-067: Crypto (Claude - precision needed)
for batch_num in {058..067}; do
    echo "Generating Batch $batch_num: Cryptographic Failures..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider claude \
        --parallel 2 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 5 complete (100 crypto examples)"
echo ""

# ========================================
# PHASE 6: Insecure Design (80 examples)
# ========================================

echo "========================================"
echo "PHASE 6: Insecure Design (80 examples)"
echo "========================================"
echo ""

# Batches 068-075: Design flaws (Claude)
for batch_num in {068..075}; do
    echo "Generating Batch $batch_num: Insecure Design..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider claude \
        --parallel 3 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 6 complete (80 design examples)"
echo ""

# ========================================
# PHASE 7: Vulnerable Components (80 examples)
# ========================================

echo "========================================"
echo "PHASE 7: Vulnerable Components (80 examples)"
echo "========================================"
echo ""

# Batches 076-083: Dependencies (OpenAI)
for batch_num in {076..083}; do
    echo "Generating Batch $batch_num: Vulnerable Components..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider openai \
        --parallel 4 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 7 complete (80 dependency examples)"
echo ""

# ========================================
# PHASE 8: Software/Data Integrity (80 examples)
# ========================================

echo "========================================"
echo "PHASE 8: Software/Data Integrity (80 examples)"
echo "========================================"
echo ""

# Batches 084-091: Integrity (Claude)
for batch_num in {084..091}; do
    echo "Generating Batch $batch_num: Integrity Failures..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider claude \
        --parallel 3 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 8 complete (80 integrity examples)"
echo ""

# ========================================
# PHASE 9: Logging/Monitoring (60 examples)
# ========================================

echo "========================================"
echo "PHASE 9: Logging/Monitoring (60 examples)"
echo "========================================"
echo ""

# Batches 092-097: Logging (OpenAI)
for batch_num in {092..097}; do
    echo "Generating Batch $batch_num: Logging Failures..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider openai \
        --parallel 4 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 9 complete (60 logging examples)"
echo ""

# ========================================
# PHASE 10: SSRF (50 examples)
# ========================================

echo "========================================"
echo "PHASE 10: SSRF (50 examples)"
echo "========================================"
echo ""

# Batches 098-102: SSRF (Claude)
for batch_num in {098..102}; do
    echo "Generating Batch $batch_num: SSRF..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider claude \
        --parallel 3 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 10 complete (50 SSRF examples)"
echo ""

# ========================================
# PHASE 11: AI/ML Security (150 examples)
# ========================================

echo "========================================"
echo "PHASE 11: AI/ML Security (150 examples)"
echo "========================================"
echo ""

# Batches 103-117: AI/ML (Claude - specialized)
for batch_num in {103..117}; do
    echo "Generating Batch $batch_num: AI/ML Security..."
    python3 automation/scripts/api_generator.py \
        --batch $batch_num \
        --provider claude \
        --parallel 2 \
        2>&1 | tee -a $LOGFILE

    sleep 10
done

echo "✓ Phase 11 complete (150 AI/ML examples)"
echo ""

# ========================================
# Final Validation
# ========================================

echo "========================================"
echo "Running Final Validation"
echo "========================================"
echo ""

python3 generation/validate_all_batches.py 2>&1 | tee -a $LOGFILE

echo ""
echo "========================================"
echo "✓ GENERATION COMPLETE!"
echo "========================================"
echo ""
echo "Total examples: 1,000"
echo "Log file: $LOGFILE"
echo ""
echo "Next steps:"
echo "  1. Review validation results"
echo "  2. Fix any failed examples"
echo "  3. Run final QA: python3 generation/comprehensive_qa.py"
echo ""
