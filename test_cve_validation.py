#!/usr/bin/env python3
"""
CVE Validation Test Suite

Comprehensive tests for CVE format validation in SecureCode v2.0.
Tests cover edge cases, boundaries, real-world CVEs, and regression tests
for the original buggy regex pattern.

Run with:
    python test_cve_validation.py
    python test_cve_validation.py -v  # verbose

Author: Scott Thornton (scott@perfecxion.ai)
License: Apache 2.0
Version: 2.0
Date: 2025-12-15
"""

import unittest
import re
from datetime import datetime
from validate_contributing_compliance import validate_cve_format


def validate_cve_format_original_buggy(cve_id):
    """
    Original buggy implementation from paper (for regression testing).

    BUG: Accepts years 2026-2029 despite claiming to only accept 1999-2025.
    Pattern 20[0-2][0-9] matches 2000-2029, not 2000-2025.
    """
    if cve_id is None:
        return True, "Explicit null accepted"

    pattern = r'^CVE-(199[9]|20[0-2][0-9])-\d{1,5}$'
    if re.match(pattern, cve_id):
        return True, "Valid CVE format"

    return False, f"Invalid CVE format: {cve_id}"


class TestCVEValidation(unittest.TestCase):
    """Comprehensive test suite for CVE validation"""

    def test_null_values(self):
        """Test that None/null is accepted"""
        valid, msg = validate_cve_format(None)
        self.assertTrue(valid, f"None should be accepted: {msg}")
        self.assertIn("null", msg.lower())

    def test_empty_string_rejected(self):
        """Test that empty string is rejected (should use None instead)"""
        valid, msg = validate_cve_format("")
        self.assertFalse(valid, "Empty string should be rejected")

    def test_valid_cve_numbers(self):
        """Test valid CVE numbers across different years"""
        valid_cves = [
            "CVE-1999-1",          # Minimum year, minimum number
            "CVE-1999-0001",       # Minimum year with leading zeros
            "CVE-2000-12345",      # Valid with 5 digits
            "CVE-2010-5678",       # Mid-range year
            "CVE-2015-99999",      # Maximum CVE number
            "CVE-2020-1",          # Recent year (2020)
            "CVE-2021-12345",      # Recent year (2021)
            "CVE-2022-54321",      # Recent year (2022)
            "CVE-2023-12345",      # Recent year (2023)
            "CVE-2024-54321",      # Recent year (2024)
            "CVE-2025-1",          # Current year (2025)
        ]

        for cve in valid_cves:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertTrue(valid, f"Valid CVE rejected: {cve} - {msg}")

    def test_invalid_cve_formats(self):
        """Test various invalid CVE format patterns"""
        invalid_formats = [
            ("", "empty string"),
            ("CVE-2023", "missing CVE number"),
            ("2023-12345", "missing CVE prefix"),
            ("CVE-2023-", "missing number after dash"),
            ("CVE-23-12345", "two-digit year"),
            ("CVE-02023-12345", "five-digit year"),
            ("CVE-2023-123456", "six-digit CVE number"),
            ("CVE-2023-0", "CVE number zero"),
            ("CVE-2023-ABC", "non-numeric CVE number"),
            ("CVE 2023 12345", "spaces instead of dashes"),
            ("CVE_2023_12345", "underscores instead of dashes"),
            ("cve-2023-12345", "lowercase prefix (if case-sensitive)"),
        ]

        for cve, reason in invalid_formats:
            with self.subTest(cve=cve, reason=reason):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"Invalid CVE accepted: {cve} ({reason})")

    def test_year_too_early(self):
        """Test that years before 1999 are rejected"""
        invalid_years = [
            "CVE-1998-12345",
            "CVE-1990-1",
            "CVE-1900-99999",
        ]

        for cve in invalid_years:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"Pre-1999 CVE accepted: {cve}")
                self.assertIn("1999", msg, f"Error message should mention 1999: {msg}")

    def test_year_boundary_1999(self):
        """Test that 1999 (first CVE year) is accepted"""
        valid, msg = validate_cve_format("CVE-1999-1")
        self.assertTrue(valid, f"CVE-1999-1 should be valid: {msg}")

    def test_current_year(self):
        """Test that current year is accepted"""
        current_year = datetime.now().year
        cve = f"CVE-{current_year}-12345"
        valid, msg = validate_cve_format(cve)
        self.assertTrue(valid, f"Current year CVE should be valid: {cve} - {msg}")

    def test_next_year_accepted(self):
        """Test that next year is accepted (for upcoming CVE assignments)"""
        next_year = datetime.now().year + 1
        cve = f"CVE-{next_year}-12345"
        valid, msg = validate_cve_format(cve)
        self.assertTrue(valid, f"Next year CVE should be valid: {cve} - {msg}")

    def test_distant_future_rejected(self):
        """Test that years beyond next year are rejected"""
        current_year = datetime.now().year
        distant_future_years = [current_year + 2, current_year + 5, current_year + 10]

        for year in distant_future_years:
            cve = f"CVE-{year}-12345"
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"Distant future CVE accepted: {cve}")
                self.assertIn(str(year), msg, f"Error should mention the year: {msg}")

    def test_cve_number_minimum(self):
        """Test that CVE number 1 is accepted"""
        valid, msg = validate_cve_format("CVE-2023-1")
        self.assertTrue(valid, f"CVE number 1 should be valid: {msg}")

    def test_cve_number_zero_rejected(self):
        """Test that CVE number 0 is rejected"""
        valid, msg = validate_cve_format("CVE-2023-0")
        self.assertFalse(valid, "CVE number 0 should be rejected")
        self.assertIn("1", msg.lower(), f"Error should mention minimum of 1: {msg}")

    def test_cve_number_maximum(self):
        """Test that CVE number 99999 is accepted"""
        valid, msg = validate_cve_format("CVE-2023-99999")
        self.assertTrue(valid, f"CVE number 99999 should be valid: {msg}")

    def test_cve_number_too_large(self):
        """Test that CVE numbers > 99999 are rejected"""
        invalid_numbers = [
            "CVE-2023-100000",  # Just over limit
            "CVE-2023-999999",  # Way over limit
        ]

        for cve in invalid_numbers:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"Oversized CVE number accepted: {cve}")
                self.assertIn("99999", msg, f"Error should mention 99999 limit: {msg}")

    def test_leading_zeros_accepted(self):
        """Test that CVE numbers with leading zeros are accepted"""
        valid_with_zeros = [
            "CVE-2023-00001",     # 5 digits with leading zeros
            "CVE-2023-01234",     # 5 digits with one leading zero
            "CVE-2023-0001",      # 4 digits with leading zeros
            "CVE-2023-001",       # 3 digits with leading zeros
            "CVE-2023-01",        # 2 digits with leading zero
        ]

        for cve in valid_with_zeros:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertTrue(valid, f"Leading zeros rejected: {cve} - {msg}")

    def test_real_world_cves(self):
        """Test real-world high-profile CVE examples"""
        real_cves = [
            ("CVE-2021-44228", "Log4Shell"),
            ("CVE-2022-22965", "Spring4Shell"),
            ("CVE-2023-23397", "Microsoft Outlook"),
            ("CVE-2024-3094", "XZ Utils backdoor"),
            ("CVE-2014-0160", "Heartbleed"),
            ("CVE-2017-5638", "Apache Struts (Equifax breach)"),
            ("CVE-2020-1472", "Zerologon"),
            ("CVE-2019-0708", "BlueKeep"),
        ]

        for cve, name in real_cves:
            with self.subTest(cve=cve, name=name):
                valid, msg = validate_cve_format(cve)
                self.assertTrue(valid, f"Real CVE rejected: {cve} ({name}) - {msg}")

    def test_type_validation(self):
        """Test that non-string types are rejected"""
        invalid_types = [
            (123, int),
            (12.34, float),
            (True, bool),
            (['CVE-2023-1'], list),
            ({'cve': 'CVE-2023-1'}, dict),
        ]

        for value, type_name in invalid_types:
            with self.subTest(value=value, type=type_name):
                valid, msg = validate_cve_format(value)
                self.assertFalse(valid, f"Non-string type accepted: {type_name}")
                self.assertIn("string", msg.lower(), f"Error should mention type: {msg}")

    def test_regression_original_bug(self):
        """
        Regression test: Verify that the original buggy regex accepted 2026-2029.
        This confirms the bug was real and our fix addresses it.
        """
        if datetime.now().year >= 2026:
            self.skipTest("Test only valid before 2026")

        buggy_accepts_future = [
            "CVE-2026-12345",
            "CVE-2027-12345",
            "CVE-2028-12345",
            "CVE-2029-12345",
        ]

        for cve in buggy_accepts_future:
            with self.subTest(cve=cve):
                # Original buggy version should accept these (the bug)
                buggy_valid, _ = validate_cve_format_original_buggy(cve)
                self.assertTrue(buggy_valid,
                              f"Original regex should accept (bug): {cve}")

                # Fixed version should reject these
                fixed_valid, _ = validate_cve_format(cve)
                self.assertFalse(fixed_valid,
                               f"Fixed version should reject future year: {cve}")

    def test_original_bug_boundary_2025(self):
        """Test that both versions accept 2025"""
        cve = "CVE-2025-12345"

        # Both versions should accept 2025
        buggy_valid, _ = validate_cve_format_original_buggy(cve)
        fixed_valid, _ = validate_cve_format(cve)

        self.assertTrue(buggy_valid, f"Original should accept 2025: {cve}")
        self.assertTrue(fixed_valid, f"Fixed should accept 2025: {cve}")

    def test_various_number_lengths(self):
        """Test CVE numbers with different digit lengths (1-5 digits)"""
        valid_lengths = [
            ("CVE-2023-1", 1),
            ("CVE-2023-12", 2),
            ("CVE-2023-123", 3),
            ("CVE-2023-1234", 4),
            ("CVE-2023-12345", 5),
        ]

        for cve, length in valid_lengths:
            with self.subTest(cve=cve, length=length):
                valid, msg = validate_cve_format(cve)
                self.assertTrue(valid, f"{length}-digit CVE rejected: {cve} - {msg}")

    def test_case_sensitivity(self):
        """Test that CVE prefix must be uppercase"""
        lowercase_variants = [
            "cve-2023-12345",      # All lowercase
            "Cve-2023-12345",      # Only first letter capitalized
            "cVe-2023-12345",      # Mixed case
        ]

        for cve in lowercase_variants:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"Lowercase CVE accepted: {cve}")

    def test_whitespace_handling(self):
        """Test that whitespace around CVE is rejected"""
        whitespace_variants = [
            " CVE-2023-12345",     # Leading space
            "CVE-2023-12345 ",     # Trailing space
            " CVE-2023-12345 ",    # Both
            "CVE-2023- 12345",     # Space in number
            "CVE- 2023-12345",     # Space after prefix
        ]

        for cve in whitespace_variants:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"CVE with whitespace accepted: '{cve}'")

    def test_special_characters_rejected(self):
        """Test that special characters in CVE number are rejected"""
        special_char_variants = [
            "CVE-2023-12345!",
            "CVE-2023-12345#",
            "CVE-2023-12.345",
            "CVE-2023-12,345",
        ]

        for cve in special_char_variants:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"CVE with special chars accepted: {cve}")


class TestCVEValidationEdgeCases(unittest.TestCase):
    """Additional edge case tests"""

    def test_unicode_characters(self):
        """Test that unicode characters are rejected"""
        unicode_variants = [
            "CVE-2023-１２３４５",  # Full-width digits
            "CVE-②⓪②③-12345",      # Circled numbers
            "CVE-2023-𝟙𝟚𝟛𝟜𝟝",      # Mathematical bold digits
        ]

        for cve in unicode_variants:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"Unicode CVE accepted: {cve}")

    def test_sql_injection_attempt(self):
        """Test that SQL injection attempts are rejected"""
        sql_injection_attempts = [
            "CVE-2023-1'; DROP TABLE cves;--",
            "CVE-2023-1 OR 1=1",
        ]

        for cve in sql_injection_attempts:
            with self.subTest(cve=cve):
                valid, msg = validate_cve_format(cve)
                self.assertFalse(valid, f"SQL injection accepted: {cve}")

    def test_year_2000_boundary(self):
        """Test the year 2000 boundary (Y2K edge case)"""
        valid, msg = validate_cve_format("CVE-2000-1")
        self.assertTrue(valid, f"Year 2000 rejected: {msg}")

    def test_maximum_realistic_cve(self):
        """Test maximum realistic CVE (highest year, highest number)"""
        next_year = datetime.now().year + 1
        cve = f"CVE-{next_year}-99999"
        valid, msg = validate_cve_format(cve)
        self.assertTrue(valid, f"Maximum realistic CVE rejected: {cve} - {msg}")


def run_tests():
    """Run all tests with verbose output"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestCVEValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestCVEValidationEdgeCases))

    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED")
        return 0
    else:
        print("\n✗ TESTS FAILED")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
