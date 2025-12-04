#!/bin/bash

# Move interim/duplicate docs to archive
mv CLEANUP_SUMMARY.md docs/archive/
mv COMPARISON_v1_vs_v2.md docs/archive/
mv COMPREHENSIVE_ASSESSMENT_REPORT.md docs/archive/
mv CONTRIBUTING_COMPLIANCE_STATUS.md docs/archive/
mv DATASET_DESIGN.md docs/archive/
mv FULL_DATASET_PLAN.md docs/archive/
mv PROJECT_DESCRIPTION.md docs/archive/
mv PROJECT_SUMMARY.md docs/archive/
mv QA_REPORT.md docs/archive/
mv QUICK_FIX_GUIDE.md docs/archive/
mv QUICK_START.md docs/archive/
mv REVIEW_PROMPT.md docs/archive/

# Move analysis reports
mv analysis/*.md docs/reports/ 2>/dev/null || true
mv analysis/*.json docs/reports/ 2>/dev/null || true

# Keep these in root:
# - README.md (will recreate)
# - CONTRIBUTING.md
# - FINAL_COMPLIANCE_REPORT.md
# - LICENSE (will create)
# - CITATION.bib (will create)

echo "Documentation reorganized"
