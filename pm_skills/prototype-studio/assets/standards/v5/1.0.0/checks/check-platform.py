#!/usr/bin/env python3
"""Reject cross-platform shell mixing in V5 prototype HTML files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


MOBILE_REQUIRED = ("v5m-screen", "name=\"viewport\"")
MOBILE_FORBIDDEN = ("v5-nav", "v5-drawer", "_viewport-fit.js", "--v5-content-max")
DESKTOP_REQUIRED_ANY = ("v5-app", "v5-shell", "v5-portal", "v5-chat", "v5-nav")
DESKTOP_FORBIDDEN = ("v5m-screen", "v5m-safe", "v5m-sheet", "Home Indicator")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_mobile(path: Path) -> list[str]:
    html = read(path)
    errors = [f"missing {token}" for token in MOBILE_REQUIRED if token not in html]
    errors.extend(f"forbidden {token}" for token in MOBILE_FORBIDDEN if token in html)
    return errors


def check_desktop(path: Path) -> list[str]:
    html = read(path)
    errors = []
    if not any(token in html for token in DESKTOP_REQUIRED_ANY):
        errors.append("missing desktop v5 shell marker")
    errors.extend(f"forbidden {token}" for token in DESKTOP_FORBIDDEN if token in html)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mobile", nargs="*", default=[])
    parser.add_argument("--desktop", nargs="*", default=[])
    args = parser.parse_args()
    failures = []
    for value in args.mobile:
        path = Path(value)
        failures.extend(f"{path}: {message}" for message in check_mobile(path))
    for value in args.desktop:
        path = Path(value)
        failures.extend(f"{path}: {message}" for message in check_desktop(path))
    if failures:
        print("\n".join(failures))
        return 1
    print(f"platform check passed: {len(args.mobile)} mobile, {len(args.desktop)} desktop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
