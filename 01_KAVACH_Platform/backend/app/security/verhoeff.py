"""
Verhoeff algorithm implementation for validating Aadhaar national identification numbers.

The Verhoeff algorithm is a checksum formula for error detection developed by Jacobus Verhoeff.
It uses the dihedral group D_5 (symmetries of a regular pentagon) and is capable of detecting:
  1. All single-digit transcription errors.
  2. All adjacent digit transposition errors.
  3. Most twin, jump twin, and jump transposition errors.

UIDAI Aadhaar specification:
  - Total length: exactly 12 numeric digits.
  - Leading digit: MUST NOT start with 0 or 1 (valid initial digits: 2 through 9).
  - Checksum: The 12th digit is the Verhoeff check digit computed over the first 11 digits.
"""

from typing import Union, Dict, Any
import re

# Dihedral group D_5 multiplication table
VERHOEFF_D = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
)

# Permutation table
VERHOEFF_P = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
)

# Multiplicative inverse table
VERHOEFF_INV = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)


def validate_verhoeff(num_str: Union[str, int]) -> bool:
    """
    Validate a numeric string using the Verhoeff algorithm.
    Returns True if the check digit matches, False otherwise.
    """
    s = str(num_str).strip()
    if not s.isdigit() or len(s) == 0:
        return False
    c = 0
    for i, char in enumerate(reversed(s)):
        c = VERHOEFF_D[c][VERHOEFF_P[i % 8][int(char)]]
    return c == 0


def generate_verhoeff_check_digit(num_str: Union[str, int]) -> int:
    """
    Calculate the Verhoeff check digit for a string of numbers.
    For an 11-digit Aadhaar prefix, returns the 12th check digit.
    """
    s = str(num_str).strip()
    if not s.isdigit() or len(s) == 0:
        raise ValueError(f"Expected numeric string, got: {num_str}")
    c = 0
    for i, char in enumerate(reversed(s)):
        c = VERHOEFF_D[c][VERHOEFF_P[(i + 1) % 8][int(char)]]
    return VERHOEFF_INV[c]


def validate_aadhaar_candidate(candidate: str) -> Dict[str, Any]:
    """
    Validate an Aadhaar candidate string (formatted or unformatted).
    Enforces UIDAI constraints:
      1. Exactly 12 digits.
      2. Leading digit cannot be '0' or '1' (valid range: 2-9).
      3. Verhoeff checksum must equal 0.

    Returns a dict:
      {
        "is_valid_aadhaar": bool,
        "digits": str,
        "reject_reason": Optional[str],
        "is_possible_id": bool
      }
    """
    digits = re.sub(r"\D", "", candidate)
    if len(digits) != 12:
        return {
            "is_valid_aadhaar": False,
            "digits": digits,
            "reject_reason": f"Invalid length ({len(digits)} digits, expected 12)",
            "is_possible_id": False,
        }

    # UIDAI Rule 1: Cannot start with 0 or 1
    if digits[0] in ("0", "1"):
        return {
            "is_valid_aadhaar": False,
            "digits": digits,
            "reject_reason": f"Invalid leading digit '{digits[0]}' (UIDAI rejects leading 0 or 1)",
            "is_possible_id": True,
        }

    # UIDAI Rule 2: Verhoeff checksum
    if not validate_verhoeff(digits):
        return {
            "is_valid_aadhaar": False,
            "digits": digits,
            "reject_reason": "Failed Verhoeff checksum validation",
            "is_possible_id": True,
        }

    return {
        "is_valid_aadhaar": True,
        "digits": digits,
        "reject_reason": None,
        "is_possible_id": False,
    }
