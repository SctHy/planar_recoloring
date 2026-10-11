#!/usr/bin/env python3
"""Compatibility entry point for the complete adjacent-pair reader."""
import sys
from certificate_core import run_cli
from verify_adjacent_pairs import check_adjacent_pairs

if __name__ == "__main__":
    sys.exit(run_cli(check_adjacent_pairs, __doc__))
