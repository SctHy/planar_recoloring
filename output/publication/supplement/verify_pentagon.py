#!/usr/bin/env python3
"""Compatibility entry point for the complete protected-pentagon reader."""
import sys
from certificate_core import run_cli
from verify_protected_pentagons import check_pentagons

if __name__ == "__main__":
    sys.exit(run_cli(check_pentagons, __doc__))
