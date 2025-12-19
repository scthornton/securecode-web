#!/usr/bin/env python3
"""
SecureCode v2.0 - Contributing Compliance Validator (Version 2)

Comprehensive validation framework for SecureCode v2.0 dataset quality assurance.
Validates dataset examples for compliance with all SecureCode v2.0 standards:

Core Validators:
- Structure validation (4-turn conversation format)
- CVE format validation (CVE-YYYY-NNNN+ or null)
- Language tag validation (supported languages only)
- Content length validation (minimum character thresholds)
- OWASP category validation (valid categories only)
- Severity validation (CRITICAL/HIGH/MEDIUM/LOW)
- Incident grounding (required when cve_id is null)

Enhanced Validators:
- Turn 2 sections (vulnerable/attack/secure code)
- Turn 4 operational (logging/monitoring keywords)
- Example ID presence

Usage:
    python validate_contributing_compliance_v2.py <dataset_file.jsonl>
    python validate_contributing_compliance_v2.py consolidated/train.jsonl --strict
    python validate_contributing_compliance_v2.py consolidated/train.jsonl --report report.json
    python validate_contributing_compliance_v2.py consolidated/train.jsonl --verbose

Exit Codes:
    0: All validations passed
    1: One or more validations failed (or warnings in strict mode)

Author: Scott Thornton (scott@perfecxion.ai)
License: Apache 2.0
Version: 2.0
Date: 2025-12-15
"""

import json
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


# ============================================================================
# CONFIGURATION
# ============================================================================

# Supported programming languages
SUPPORTED_LANGUAGES = {
    'python', 'javascript', 'java', 'php', 'csharp', 'c#',
    'ruby', 'go', 'typescript', 'rust', 'kotlin', 'yaml',
    'c', 'c++', 'cpp', 'swift', 'bash', 'shell', 'sql'
}

# Valid OWASP categories (2025 Top 10 + custom)
VALID_OWASP_CATEGORIES = {
    'A01:2025-Broken Access Control',
    'A02:2025-Security Misconfiguration',
    'A03:2025-Software Supply Chain Failures',
    'A04:2025-Cryptographic Failures',
    'A05:2025-Injection',
    'A06:2025-Insecure Design',
    'A07:2025-Authentication Failures',
    'A08:2025-Software and Data Integrity Failures',
    'A09:2025-Security Logging and Monitoring Failures',
    'AI/ML Security Threats',  # Custom category for AI security
    'Unknown'  # For edge cases
}

# Valid severity levels (matching CVSS)
VALID_SEVERITIES = {'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'}

# Content length minimums (characters)
USER_TURN_MIN_LENGTH = 50
ASSISTANT_TURN_MIN_LENGTH = 100

# Turn 2 expected sections (for enhanced validation)
TURN2_EXPECTED_SECTIONS = {
    'vulnerable', 'attack', 'secure', 'why this is dangerous',
    'security controls', 'key security controls'
}

# Turn 4 operational keywords (for enhanced validation)
TURN4_OPERATIONAL_KEYWORDS = {
    'logging', 'monitoring', 'detection', 'alert', 'audit',
    'siem', 'log', 'metrics', 'observability', 'trace'
}


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class ValidationResult(Enum):
    """Validation result status"""
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    SKIP = "SKIP"


@dataclass
class ValidationReport:
    """Single validation check result"""
    check_name: str
    result: ValidationResult
    message: str
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'check_name': self.check_name,
            'result': self.result.value,
            'message': self.message,
            'details': self.details
        }


@dataclass
class ExampleValidationResult:
    """Validation result for a single example"""
    example_id: str
    index: int
    overall_result: ValidationResult
    checks: List[ValidationReport] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'example_id': self.example_id,
            'index': self.index,
            'overall_result': self.overall_result.value,
            'checks': [check.to_dict() for check in self.checks]
        }

    def has_failures(self) -> bool:
        """Check if example has any failures"""
        return any(check.result == ValidationResult.FAIL for check in self.checks)

    def has_warnings(self) -> bool:
        """Check if example has any warnings"""
        return any(check.result == ValidationResult.WARN for check in self.checks)


@dataclass
class DatasetValidationSummary:
    """Summary of dataset validation results"""
    total_examples: int
    passed: int
    failed: int
    warnings: int
    failures_by_check: Dict[str, int] = field(default_factory=dict)
    warnings_by_check: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

    @property
    def pass_rate(self) -> float:
        """Calculate pass rate (0.0 to 1.0)"""
        if self.total_examples == 0:
            return 0.0
        return self.passed / self.total_examples


# ============================================================================
# CORE VALIDATORS
# ============================================================================

def validate_structure(example: Dict[str, Any]) -> ValidationReport:
    """
    Validates 4-turn conversation structure.

    Checks:
    - 'messages' or 'conversations' field exists
    - Exactly 4 turns present
    - Turn roles alternate: user, assistant, user, assistant
    - Each turn has required fields (role/from and content/value)

    Args:
        example: Dataset example dictionary

    Returns:
        ValidationReport with result and details
    """
    # Check for messages field (multiple possible formats)
    if 'messages' in example:
        messages = example['messages']
        role_key = 'role'
        content_key = 'content'
    elif 'conversations' in example:
        # Alternative format: conversations with turn/from/value
        conversations = example['conversations']
        # Convert to messages format for validation
        messages = []
        for conv in conversations:
            role = 'user' if conv.get('from') == 'human' else 'assistant'
            messages.append({'role': role, 'content': conv.get('value', '')})
        role_key = 'role'
        content_key = 'content'
    else:
        return ValidationReport(
            check_name='structure',
            result=ValidationResult.FAIL,
            message="Missing 'messages' or 'conversations' field"
        )

    # Check turn count
    if len(messages) != 4:
        return ValidationReport(
            check_name='structure',
            result=ValidationResult.FAIL,
            message=f"Expected 4 turns, found {len(messages)}",
            details={'turn_count': len(messages)}
        )

    # Validate turn roles
    expected_roles = ['user', 'assistant', 'user', 'assistant']
    errors = []

    for i, (msg, expected_role) in enumerate(zip(messages, expected_roles)):
        turn_num = i + 1

        if role_key not in msg:
            errors.append(f"Turn {turn_num} missing '{role_key}' field")
            continue

        actual_role = msg[role_key]
        # Handle 'human' -> 'user' mapping
        if actual_role == 'human':
            actual_role = 'user'

        if actual_role != expected_role:
            errors.append(
                f"Turn {turn_num} has role '{msg[role_key]}', "
                f"expected '{expected_role}'"
            )

        if content_key not in msg:
            errors.append(f"Turn {turn_num} missing '{content_key}' field")

    if errors:
        return ValidationReport(
            check_name='structure',
            result=ValidationResult.FAIL,
            message="; ".join(errors),
            details={'errors': errors}
        )

    return ValidationReport(
        check_name='structure',
        result=ValidationResult.PASS,
        message="Structure valid: 4 turns with correct roles"
    )


def validate_cve_format(cve_id: Any) -> ValidationReport:
    """
    Validates CVE format: CVE-YYYY-NNNN+

    CORRECTED VERSION: Accepts CVE IDs with 4+ digit numbers (no maximum).
    This fixes the original bug that limited CVE numbers to 5 digits.

    Accepts:
    - None/null (explicit null for incidents without CVE assignments)
    - CVE-YYYY-NNNN+ where:
        - YYYY is 1999 to (current_year + 1)
        - NNNN is 4+ digits (1000-9999999...)

    Examples:
    - CVE-2024-1234 (valid: 4 digits)
    - CVE-2024-12345 (valid: 5 digits)
    - CVE-2024-1000000 (valid: 7 digits)
    - CVE-2024-123 (invalid: only 3 digits)

    Args:
        cve_id: CVE identifier (string or None)

    Returns:
        ValidationReport with result and details
    """
    if cve_id is None:
        return ValidationReport(
            check_name='cve_format',
            result=ValidationResult.PASS,
            message="Explicit null accepted (no CVE assigned)"
        )

    if not isinstance(cve_id, str):
        return ValidationReport(
            check_name='cve_format',
            result=ValidationResult.FAIL,
            message=f"CVE must be string or null, got {type(cve_id).__name__}",
            details={'type': type(cve_id).__name__, 'value': str(cve_id)}
        )

    # CORRECTED: CVE format with 4+ digits (no maximum)
    # Pattern: CVE-YYYY-NNNN where NNNN is 4 or more digits
    pattern = r'^CVE-(\d{4})-(\d{4,})$'
    match = re.match(pattern, cve_id)

    if not match:
        return ValidationReport(
            check_name='cve_format',
            result=ValidationResult.FAIL,
            message=f"Invalid CVE format: '{cve_id}' (expected CVE-YYYY-NNNN with 4+ digits)",
            details={'cve_id': cve_id, 'pattern': 'CVE-YYYY-NNNN (4+ digits)'}
        )

    year = int(match.group(1))
    cve_number = int(match.group(2))

    # Year range validation (CVE program started in 1999)
    if year < 1999:
        return ValidationReport(
            check_name='cve_format',
            result=ValidationResult.FAIL,
            message=f"Invalid CVE year: {year} (CVE program started in 1999)",
            details={'year': year, 'min_year': 1999}
        )

    # Allow current year + 1 for upcoming CVE assignments
    current_year = datetime.now().year
    max_year = current_year + 1

    if year > max_year:
        return ValidationReport(
            check_name='cve_format',
            result=ValidationResult.FAIL,
            message=f"Invalid CVE year: {year} (future year beyond {max_year})",
            details={'year': year, 'max_year': max_year}
        )

    return ValidationReport(
        check_name='cve_format',
        result=ValidationResult.PASS,
        message=f"Valid CVE format: {cve_id}",
        details={'year': year, 'cve_number': cve_number}
    )


def validate_metadata(example: Dict[str, Any]) -> ValidationReport:
    """
    Validates metadata completeness and correctness.

    Checks for both old and new metadata formats:
    - Old format: fields at root level
    - New format: fields in 'metadata' and 'context' objects

    Required fields:
    - owasp_category (or metadata.owasp_2025 or context.owasp_category)
    - cve_id (or context.cve)
    - severity (or metadata.severity)
    - language (or metadata.lang)
    - incident_year (or context.year)
    - business_impact (or context.business_impact)

    Args:
        example: Dataset example dictionary

    Returns:
        ValidationReport with result and details
    """
    errors = []

    # Helper function to get field from multiple possible locations
    def get_field(field_mappings: List[Tuple[str, ...]]) -> Optional[Any]:
        """Try multiple paths to find a field value"""
        for path in field_mappings:
            value = example
            for key in path:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    value = None
                    break
            if value is not None:
                return value
        return None

    # OWASP category
    owasp = get_field([
        ('owasp_category',),
        ('metadata', 'owasp_2025'),
        ('context', 'owasp_category')
    ])
    if owasp is None:
        errors.append("Missing OWASP category")
    elif owasp not in VALID_OWASP_CATEGORIES:
        errors.append(f"Invalid OWASP category: '{owasp}'")

    # CVE ID (can be null, but should exist OR have incident grounding)
    cve = get_field([
        ('cve_id',),
        ('context', 'cve')
    ])
    # If CVE field doesn't exist, check for incident grounding
    has_cve_field = 'cve_id' in example or 'cve' in example.get('context', {})
    has_incident_grounding = (
        'incident_grounding' in example or
        'real_world_incident' in example.get('context', {})
    )
    if not has_cve_field and not has_incident_grounding:
        errors.append("Missing cve_id field (or incident_grounding if no CVE)")

    # Severity
    severity = get_field([
        ('severity',),
        ('metadata', 'severity')
    ])
    if severity is None:
        errors.append("Missing severity")
    elif severity.upper() not in VALID_SEVERITIES:
        errors.append(f"Invalid severity: '{severity}' (must be CRITICAL/HIGH/MEDIUM/LOW)")

    # Language
    language = get_field([
        ('language',),
        ('metadata', 'lang')
    ])
    if language is None:
        errors.append("Missing language")

    # Incident year (accept from multiple locations)
    incident_year = get_field([
        ('incident_year',),
        ('context', 'year'),
        ('metadata', 'year')
    ])
    # Incident year is optional if we have created date instead
    if incident_year is None:
        # Check if we have a created date instead
        created = get_field([
            ('metadata', 'created'),
            ('created',)
        ])
        if created:
            # Extract year from created date if it's in ISO format
            try:
                if isinstance(created, str) and len(created) >= 4:
                    incident_year = int(created[:4])
            except (ValueError, TypeError):
                pass

    if incident_year is not None:
        if not isinstance(incident_year, int):
            errors.append(f"incident_year must be integer, got {type(incident_year).__name__}")
        elif not (2000 <= incident_year <= datetime.now().year + 1):
            errors.append(f"Invalid incident_year: {incident_year} (must be 2000-{datetime.now().year + 1})")

    # Business impact
    business_impact = get_field([
        ('business_impact',),
        ('context', 'business_impact'),
        ('context', 'impact')
    ])
    if business_impact is None:
        errors.append("Missing business_impact")

    if errors:
        return ValidationReport(
            check_name='metadata',
            result=ValidationResult.FAIL,
            message="; ".join(errors),
            details={'errors': errors}
        )

    return ValidationReport(
        check_name='metadata',
        result=ValidationResult.PASS,
        message="Metadata complete and valid"
    )


def validate_language(example: Dict[str, Any]) -> ValidationReport:
    """
    Validates programming language tag.

    Args:
        example: Dataset example dictionary

    Returns:
        ValidationReport with result and details
    """
    # Get language from multiple possible locations
    language = None
    if 'language' in example:
        language = example['language']
    elif 'metadata' in example and 'lang' in example['metadata']:
        language = example['metadata']['lang']

    if language is None:
        return ValidationReport(
            check_name='language',
            result=ValidationResult.FAIL,
            message="Missing language field"
        )

    if not isinstance(language, str):
        return ValidationReport(
            check_name='language',
            result=ValidationResult.FAIL,
            message=f"Language must be string, got {type(language).__name__}",
            details={'type': type(language).__name__}
        )

    lang_lower = language.lower()
    if lang_lower in SUPPORTED_LANGUAGES:
        return ValidationReport(
            check_name='language',
            result=ValidationResult.PASS,
            message=f"Valid language: {language}"
        )

    return ValidationReport(
        check_name='language',
        result=ValidationResult.FAIL,
        message=f"Unsupported language: '{language}'",
        details={
            'language': language,
            'supported': sorted(SUPPORTED_LANGUAGES)
        }
    )


def validate_content_length(example: Dict[str, Any]) -> ValidationReport:
    """
    Validates minimum content length for conversation turns.

    RENAMED from 'content_quality' to be honest about what this checks.
    This validator only measures character count, NOT semantic quality.

    Thresholds:
    - User turns: minimum 50 characters
    - Assistant turns: minimum 100 characters

    Args:
        example: Dataset example dictionary

    Returns:
        ValidationReport with result and details
    """
    # Get messages from either format
    if 'messages' in example:
        messages = example['messages']
        content_key = 'content'
    elif 'conversations' in example:
        messages = [
            {'content': conv.get('value', '')}
            for conv in example['conversations']
        ]
        content_key = 'content'
    else:
        return ValidationReport(
            check_name='content_length',
            result=ValidationResult.FAIL,
            message="Cannot validate content length: missing messages/conversations"
        )

    if len(messages) != 4:
        return ValidationReport(
            check_name='content_length',
            result=ValidationResult.FAIL,
            message=f"Cannot validate content length: expected 4 turns, found {len(messages)}"
        )

    errors = []
    lengths = []

    # Turn 1 (user): minimum 50 chars
    turn1_len = len(messages[0].get(content_key, ''))
    lengths.append(turn1_len)
    if turn1_len < USER_TURN_MIN_LENGTH:
        errors.append(
            f"Turn 1 below {USER_TURN_MIN_LENGTH} chars ({turn1_len} chars)"
        )

    # Turn 2 (assistant): minimum 100 chars
    turn2_len = len(messages[1].get(content_key, ''))
    lengths.append(turn2_len)
    if turn2_len < ASSISTANT_TURN_MIN_LENGTH:
        errors.append(
            f"Turn 2 below {ASSISTANT_TURN_MIN_LENGTH} chars ({turn2_len} chars)"
        )

    # Turn 3 (user): minimum 50 chars
    turn3_len = len(messages[2].get(content_key, ''))
    lengths.append(turn3_len)
    if turn3_len < USER_TURN_MIN_LENGTH:
        errors.append(
            f"Turn 3 below {USER_TURN_MIN_LENGTH} chars ({turn3_len} chars)"
        )

    # Turn 4 (assistant): minimum 100 chars
    turn4_len = len(messages[3].get(content_key, ''))
    lengths.append(turn4_len)
    if turn4_len < ASSISTANT_TURN_MIN_LENGTH:
        errors.append(
            f"Turn 4 below {ASSISTANT_TURN_MIN_LENGTH} chars ({turn4_len} chars)"
        )

    if errors:
        return ValidationReport(
            check_name='content_length',
            result=ValidationResult.FAIL,
            message="; ".join(errors),
            details={'turn_lengths': lengths, 'errors': errors}
        )

    return ValidationReport(
        check_name='content_length',
        result=ValidationResult.PASS,
        message="Content length valid for all turns",
        details={'turn_lengths': lengths}
    )


def validate_incident_grounding(example: Dict[str, Any]) -> ValidationReport:
    """
    Validates incident grounding requirement.

    When cve_id is null, the example must have incident_grounding field
    to ensure the security issue is based on a real-world incident.

    Args:
        example: Dataset example dictionary

    Returns:
        ValidationReport with result and details
    """
    # Get CVE ID
    cve = None
    if 'cve_id' in example:
        cve = example['cve_id']
    elif 'context' in example and 'cve' in example['context']:
        cve = example['context']['cve']

    # If CVE exists, incident grounding is optional
    if cve is not None:
        return ValidationReport(
            check_name='incident_grounding',
            result=ValidationResult.SKIP,
            message="Skipped: CVE ID present, incident grounding optional"
        )

    # CVE is null, check for incident grounding
    grounding = None
    if 'incident_grounding' in example:
        grounding = example['incident_grounding']
    elif 'context' in example:
        if 'incident_grounding' in example['context']:
            grounding = example['context']['incident_grounding']
        elif 'real_world_incident' in example['context']:
            grounding = example['context']['real_world_incident']

    if grounding is None or (isinstance(grounding, str) and len(grounding.strip()) == 0):
        return ValidationReport(
            check_name='incident_grounding',
            result=ValidationResult.FAIL,
            message="Missing incident_grounding (required when cve_id is null)",
            details={'cve_id': None}
        )

    return ValidationReport(
        check_name='incident_grounding',
        result=ValidationResult.PASS,
        message="Incident grounding present",
        details={'grounding_length': len(str(grounding))}
    )


# ============================================================================
# ENHANCED VALIDATORS (Nice to Have)
# ============================================================================

def validate_turn2_sections(example: Dict[str, Any]) -> ValidationReport:
    """
    Enhanced validation: Check for expected sections in Turn 2.

    Turn 2 should contain vulnerable code, attack payload, and secure code
    sections to provide comprehensive security education.

    Args:
        example: Dataset example dictionary

    Returns:
        ValidationReport with result and details (WARN if missing)
    """
    # Get Turn 2 content
    if 'messages' in example:
        if len(example['messages']) < 2:
            return ValidationReport(
                check_name='turn2_sections',
                result=ValidationResult.SKIP,
                message="Skipped: insufficient turns"
            )
        turn2_content = example['messages'][1].get('content', '')
    elif 'conversations' in example:
        if len(example['conversations']) < 2:
            return ValidationReport(
                check_name='turn2_sections',
                result=ValidationResult.SKIP,
                message="Skipped: insufficient turns"
            )
        turn2_content = example['conversations'][1].get('value', '')
    else:
        return ValidationReport(
            check_name='turn2_sections',
            result=ValidationResult.SKIP,
            message="Skipped: no messages found"
        )

    turn2_lower = turn2_content.lower()

    # Check for expected sections
    found_sections = []
    missing_sections = []

    for section in TURN2_EXPECTED_SECTIONS:
        if section in turn2_lower:
            found_sections.append(section)

    # We want at least 2-3 of the expected sections
    if len(found_sections) < 2:
        return ValidationReport(
            check_name='turn2_sections',
            result=ValidationResult.WARN,
            message=f"Turn 2 may be missing standard sections (found {len(found_sections)}: {found_sections})",
            details={'found_sections': found_sections}
        )

    return ValidationReport(
        check_name='turn2_sections',
        result=ValidationResult.PASS,
        message=f"Turn 2 contains expected sections ({len(found_sections)} found)",
        details={'found_sections': found_sections}
    )


def validate_turn4_operational(example: Dict[str, Any]) -> ValidationReport:
    """
    Enhanced validation: Check for operational security content in Turn 4.

    Turn 4 should address operational concerns like logging, monitoring,
    and detection to provide production-ready security guidance.

    Args:
        example: Dataset example dictionary

    Returns:
        ValidationReport with result and details (WARN if missing)
    """
    # Get Turn 4 content
    if 'messages' in example:
        if len(example['messages']) < 4:
            return ValidationReport(
                check_name='turn4_operational',
                result=ValidationResult.SKIP,
                message="Skipped: insufficient turns"
            )
        turn4_content = example['messages'][3].get('content', '')
    elif 'conversations' in example:
        if len(example['conversations']) < 4:
            return ValidationReport(
                check_name='turn4_operational',
                result=ValidationResult.SKIP,
                message="Skipped: insufficient turns"
            )
        turn4_content = example['conversations'][3].get('value', '')
    else:
        return ValidationReport(
            check_name='turn4_operational',
            result=ValidationResult.SKIP,
            message="Skipped: no messages found"
        )

    turn4_lower = turn4_content.lower()

    # Check for operational keywords
    found_keywords = []
    for keyword in TURN4_OPERATIONAL_KEYWORDS:
        if keyword in turn4_lower:
            found_keywords.append(keyword)

    if len(found_keywords) < 2:
        return ValidationReport(
            check_name='turn4_operational',
            result=ValidationResult.WARN,
            message=f"Turn 4 may lack operational security guidance (found {len(found_keywords)} keywords)",
            details={'found_keywords': found_keywords}
        )

    return ValidationReport(
        check_name='turn4_operational',
        result=ValidationResult.PASS,
        message=f"Turn 4 contains operational security guidance ({len(found_keywords)} keywords)",
        details={'found_keywords': found_keywords}
    )


def validate_example_id(example: Dict[str, Any]) -> ValidationReport:
    """
    Enhanced validation: Check for example ID presence.

    Having unique IDs helps with dataset management and debugging.

    Args:
        example: Dataset example dictionary

    Returns:
        ValidationReport with result and details (WARN if missing)
    """
    example_id = example.get('id')

    if example_id is None or (isinstance(example_id, str) and len(example_id.strip()) == 0):
        return ValidationReport(
            check_name='example_id',
            result=ValidationResult.WARN,
            message="Missing example ID (recommended for dataset management)"
        )

    return ValidationReport(
        check_name='example_id',
        result=ValidationResult.PASS,
        message=f"Example ID present: {example_id}",
        details={'id': example_id}
    )


# ============================================================================
# VALIDATION ORCHESTRATION
# ============================================================================

def validate_example(example: Dict[str, Any], index: int,
                     enable_enhanced: bool = True) -> ExampleValidationResult:
    """
    Validates a complete example against all compliance requirements.

    Args:
        example: Dataset example dictionary
        index: Example index (for error reporting)
        enable_enhanced: Enable enhanced (nice-to-have) validators

    Returns:
        ExampleValidationResult with all check results
    """
    example_id = example.get('id', f'index_{index}')
    checks = []

    # Core validators (required)
    checks.append(validate_structure(example))
    checks.append(validate_cve_format(
        example.get('cve_id') or
        (example.get('context', {}).get('cve') if 'context' in example else None)
    ))
    checks.append(validate_metadata(example))
    checks.append(validate_language(example))
    checks.append(validate_content_length(example))
    checks.append(validate_incident_grounding(example))

    # Enhanced validators (nice-to-have)
    if enable_enhanced:
        checks.append(validate_turn2_sections(example))
        checks.append(validate_turn4_operational(example))
        checks.append(validate_example_id(example))

    # Determine overall result
    has_failures = any(check.result == ValidationResult.FAIL for check in checks)
    has_warnings = any(check.result == ValidationResult.WARN for check in checks)

    if has_failures:
        overall_result = ValidationResult.FAIL
    elif has_warnings:
        overall_result = ValidationResult.WARN
    else:
        overall_result = ValidationResult.PASS

    return ExampleValidationResult(
        example_id=example_id,
        index=index,
        overall_result=overall_result,
        checks=checks
    )


def validate_dataset(
    filepath: str,
    verbose: bool = True,
    strict: bool = False,
    enable_enhanced: bool = True
) -> Tuple[DatasetValidationSummary, List[ExampleValidationResult]]:
    """
    Validates entire dataset file.

    Args:
        filepath: Path to JSONL dataset file
        verbose: Print detailed progress
        strict: Treat warnings as failures
        enable_enhanced: Enable enhanced (nice-to-have) validators

    Returns:
        Tuple of (summary, list of failed/warned examples)
    """
    if not Path(filepath).exists():
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if verbose:
        print(f"Loading dataset: {filepath}")

    # Load examples
    examples = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                examples.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid JSON on line {line_num}: {e}", file=sys.stderr)
                sys.exit(1)

    if verbose:
        print(f"Loaded {len(examples)} examples\n")
        print("=" * 80)
        print("VALIDATION STARTED")
        print("=" * 80)

    # Initialize summary
    summary = DatasetValidationSummary(
        total_examples=len(examples),
        passed=0,
        failed=0,
        warnings=0
    )

    failed_or_warned_results = []

    # Validate each example
    for idx, example in enumerate(examples):
        if verbose and (idx % 100 == 0 or idx == len(examples) - 1):
            progress = (idx + 1) * 100 // len(examples)
            print(f"Progress: {idx + 1}/{len(examples)} ({progress}%)")

        result = validate_example(example, idx, enable_enhanced=enable_enhanced)

        # Count results
        if result.has_failures():
            summary.failed += 1
            failed_or_warned_results.append(result)
        elif result.has_warnings():
            summary.warnings += 1
            if strict:
                summary.failed += 1  # In strict mode, warnings count as failures
            failed_or_warned_results.append(result)
        else:
            summary.passed += 1

        # Track failure/warning counts by check
        for check in result.checks:
            if check.result == ValidationResult.FAIL:
                summary.failures_by_check[check.check_name] = \
                    summary.failures_by_check.get(check.check_name, 0) + 1
            elif check.result == ValidationResult.WARN:
                summary.warnings_by_check[check.check_name] = \
                    summary.warnings_by_check.get(check.check_name, 0) + 1

    return summary, failed_or_warned_results


def print_summary(
    summary: DatasetValidationSummary,
    failed_or_warned: List[ExampleValidationResult],
    strict: bool = False,
    max_failures_shown: int = 10
):
    """
    Print validation summary to console.

    Args:
        summary: Validation summary
        failed_or_warned: List of failed/warned examples
        strict: Strict mode (warnings treated as failures)
        max_failures_shown: Maximum number of failures to display
    """
    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print(f"\nTotal Examples: {summary.total_examples}")
    print(f"Passed: {summary.passed} ({summary.pass_rate * 100:.1f}%)")
    print(f"Failed: {summary.failed}")
    print(f"Warnings: {summary.warnings}" + (" (treated as failures)" if strict else ""))

    if summary.failures_by_check:
        print("\n" + "-" * 80)
        print("FAILURE BREAKDOWN BY CHECK")
        print("-" * 80)
        for check_name, count in sorted(summary.failures_by_check.items()):
            print(f"{check_name}: {count} failures")

    if summary.warnings_by_check:
        print("\n" + "-" * 80)
        print("WARNING BREAKDOWN BY CHECK")
        print("-" * 80)
        for check_name, count in sorted(summary.warnings_by_check.items()):
            print(f"{check_name}: {count} warnings")

    if failed_or_warned:
        print("\n" + "-" * 80)
        print(f"DETAILED FAILURES (showing first {max_failures_shown} of {len(failed_or_warned)})")
        print("-" * 80)

        for i, result in enumerate(failed_or_warned[:max_failures_shown], 1):
            print(f"\n{i}. Example #{result.index} ({result.example_id})")
            print(f"   Overall: {result.overall_result.value}")
            print(f"   Issues:")

            for check in result.checks:
                if check.result in (ValidationResult.FAIL, ValidationResult.WARN):
                    print(f"     [{check.result.value}] {check.check_name}: {check.message}")


def save_report(
    summary: DatasetValidationSummary,
    failed_or_warned: List[ExampleValidationResult],
    output_path: str
):
    """
    Save validation report to JSON file.

    Args:
        summary: Validation summary
        failed_or_warned: List of failed/warned examples
        output_path: Output file path
    """
    report = {
        'summary': summary.to_dict(),
        'failed_or_warned_examples': [
            result.to_dict() for result in failed_or_warned
        ]
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: {output_path}")


# ============================================================================
# CLI
# ============================================================================

def main():
    """Main entry point for CLI usage"""
    parser = argparse.ArgumentParser(
        description='SecureCode v2.0 Contributing Compliance Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s consolidated/train.jsonl
  %(prog)s consolidated/train.jsonl --strict
  %(prog)s consolidated/train.jsonl --report validation_report.json
  %(prog)s consolidated/train.jsonl --verbose --no-enhanced

Exit codes:
  0: All validations passed
  1: One or more validations failed
        """
    )

    parser.add_argument(
        'dataset',
        help='Path to JSONL dataset file'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as failures (strict mode)'
    )

    parser.add_argument(
        '--report',
        metavar='FILE',
        help='Save detailed JSON report to file'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='Print detailed progress (default: True)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress output'
    )

    parser.add_argument(
        '--no-enhanced',
        action='store_true',
        help='Disable enhanced (nice-to-have) validators'
    )

    parser.add_argument(
        '--max-failures',
        type=int,
        default=10,
        metavar='N',
        help='Maximum number of failures to display (default: 10)'
    )

    args = parser.parse_args()

    verbose = args.verbose and not args.quiet
    enable_enhanced = not args.no_enhanced

    # Validate dataset
    summary, failed_or_warned = validate_dataset(
        filepath=args.dataset,
        verbose=verbose,
        strict=args.strict,
        enable_enhanced=enable_enhanced
    )

    # Print summary
    print_summary(summary, failed_or_warned, strict=args.strict,
                  max_failures_shown=args.max_failures)

    # Save report if requested
    if args.report:
        save_report(summary, failed_or_warned, args.report)

    # Exit with appropriate code
    if args.strict:
        # In strict mode, any failures or warnings = exit 1
        exit_code = 0 if (summary.failed == 0 and summary.warnings == 0) else 1
    else:
        # In normal mode, only failures = exit 1
        exit_code = 0 if summary.failed == 0 else 1

    if exit_code == 0:
        print("\n✓ VALIDATION PASSED - All examples comply with standards")
    else:
        if args.strict and summary.warnings > 0:
            print("\n⚠️  VALIDATION FAILED - Fix failures and warnings before contribution (strict mode)")
        else:
            print("\n⚠️  VALIDATION FAILED - Fix failures before contribution")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
