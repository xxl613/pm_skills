#!/usr/bin/env python3
"""Verify package inventory, local references and pinned component usage."""
import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "components"))
from standard_lib import check_package, digest, inside, read_json


class Frames(HTMLParser):
    def __init__(self):
        super().__init__()
        self.frames = []

    def handle_starttag(self, tag, attrs):
        if tag == "iframe":
            self.frames.append(dict(attrs))


def check_project(root):
    root = Path(root).resolve()
    errors, reports = [], []
    lock = read_json(root / "standard-usage.json")
    for usage in lock["usages"]:
        pack = inside(root, usage["package"])
        report = check_package(pack)
        reports.append(report)
        errors.extend(report["errors"])
        if digest(pack / "pack.json") != usage["pack_sha256"]:
            errors.append(f"manifest lock drift: {usage['id']}@{usage['version']}")
        if (report["id"], report["version"]) != (usage["id"], usage["version"]):
            errors.append("package identity differs from usage lock")
        if usage["mode"] == "isolated-frame":
            parser = Frames()
            parser.feed(inside(root, usage["page"]).read_text(encoding="utf-8"))
            matching = [f for f in parser.frames if f.get("id") == usage["scope"]]
            if len(matching) != 1 or matching[0].get("src") != usage["src"] or matching[0].get("data-standard") != f"{usage['id']}@{usage['version']}":
                errors.append(f"component mount drift: {usage['page']}#{usage['scope']}")
            destination = (inside(root, usage["page"]).parent / usage["src"]).resolve()
            if destination != inside(pack, usage["entry"]):
                errors.append(f"component mount points outside its locked entry: {usage['page']}")
    return {"ok": not errors, "usages": len(lock["usages"]), "packages": reports, "errors": errors,
            "limits": ["File and mount checks do not prove live interaction or visual fidelity."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pack")
    group.add_argument("--project")
    args = parser.parse_args()
    try:
        report = check_package(Path(args.pack).resolve()) if args.pack else check_project(args.project)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1
    except (ValueError, OSError, KeyError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
