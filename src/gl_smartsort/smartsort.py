\
"""
Smart sort a GL String.

This is a faithful Python port of `SmartSort.pm` (2012-11-14, Martin J. Maiers).

Behavior:
- Recursively sorts within each GL delimiter level in this precedence order:
  ^, |, +, ~, /
- Sorting is primarily by gene/locus (left of '*') lexicographically.
- Within a locus, allele fields are compared numerically (not lexically), after
  stripping any non-numeric suffix (e.g., "01:01N" -> "01:01").
- Missing allele-field components are treated as 0 for comparison.

Example:
    "A*01:103+A*01:11" -> "A*01:11+A*01:103"
"""

from __future__ import annotations

import re
from functools import cmp_to_key
from typing import Iterable, Tuple


_NUMERIC_ALLELE_RE = re.compile(r"([:\d]+)")


def _strip_allele(allele: str) -> str:
    """
    Mimic Perl stripAllele:
      return the first substring consisting only of digits/colons if present;
      otherwise return the original allele string.
    """
    m = _NUMERIC_ALLELE_RE.search(allele)
    return m.group(1) if m else allele


def _allele_fields(allele: str) -> Tuple[int, int, int, int]:
    """
    Return up to 4 numeric fields from an allele string, padding with 0s.

    Examples:
      "01:11"      -> (1, 11, 0, 0)
      "01:103"     -> (1, 103, 0, 0)
      "02:01:05"   -> (2, 1, 5, 0)
      "02:01:05:1" -> (2, 1, 5, 1)
      "01:01N"     -> (1, 1, 0, 0)  (suffix stripped)
    """
    s = _strip_allele(allele)
    parts = s.split(":") if ":" in s else [s]
    nums: list[int] = []
    for p in parts[:4]:
        # Defensive: empty segment -> 0
        if p == "":
            nums.append(0)
        else:
            try:
                nums.append(int(p))
            except ValueError:
                # If stripping didn't leave clean ints, treat as 0 (rare)
                nums.append(0)
    while len(nums) < 4:
        nums.append(0)
    return nums[0], nums[1], nums[2], nums[3]


def _split_locus(token: str) -> Tuple[str, str | None]:
    """
    Split "LOCUS*ALLELE" into (LOCUS, ALLELE). If no '*', allele is None.
    """
    if "*" not in token:
        return token, None
    loc, allele = token.split("*", 1)
    return loc, allele


def _cmp_byallele(a: str, b: str) -> int:
    """
    Comparator equivalent to Perl byallele.
    """
    a_loc, a_allele = _split_locus(a)
    b_loc, b_allele = _split_locus(b)

    if a_loc != b_loc:
        return -1 if a_loc < b_loc else 1

    # If either allele part missing, compare locus only (stable tie otherwise)
    if a_allele is None or b_allele is None:
        return 0

    a0, a1, a2, a3 = _allele_fields(a_allele)
    b0, b1, b2, b3 = _allele_fields(b_allele)

    if (a0, a1, a2, a3) < (b0, b1, b2, b3):
        return -1
    if (a0, a1, a2, a3) > (b0, b1, b2, b3):
        return 1
    return 0


def _smart_sort_level(glstring: str, delim: str) -> str:
    parts = [smart_sort(p) for p in glstring.split(delim)]
    parts.sort(key=cmp_to_key(_cmp_byallele))
    return delim.join(parts)


def smart_sort(glstring: str) -> str:
    """
    Canonicalize a GL string by recursively sorting across delimiters.

    Precedence (outermost first): ^, |, +, ~, /
    """
    # Preserve exact precedence from SmartSort.pm
    if "^" in glstring:
        return _smart_sort_level(glstring, "^")
    if "|" in glstring:
        return _smart_sort_level(glstring, "|")
    if "+" in glstring:
        return _smart_sort_level(glstring, "+")
    if "~" in glstring:
        return _smart_sort_level(glstring, "~")
    if "/" in glstring:
        return _smart_sort_level(glstring, "/")
    return glstring
