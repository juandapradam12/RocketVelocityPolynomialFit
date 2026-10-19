#!/usr/bin/env python3
"""Thin wrapper so the use case can be run without installing the package."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rocket_velocity.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
