#!/usr/bin/env python3
"""Copy one pinned standard and optionally fill an explicit iframe mount marker."""
import argparse
import html
import json
import os
import shutil
import sys
from pathlib import Path

from standard_lib import check_package, digest, inside, read_json, write_json


def install(pack, target, page=None, scope=None, entry=None, height=300):
    pack, target = Path(pack).resolve(), Path(target).resolve()
    report = check_package(pack)
    if not report["ok"]:
        raise ValueError("package failed checks: " + "; ".join(report["errors"]))
    manifest = read_json(pack / "pack.json")
    relative = Path("standards") / manifest["id"] / manifest["version"]
    destination = target / relative
    marker, page_path, page_text = None, None, None
    if any((page, scope, entry)):
        if not all((page, scope, entry)):
            raise ValueError("--page, --scope and --entry must be supplied together")
        if not inside(pack, entry).is_file() or not entry.endswith(".html"):
            raise ValueError("entry must be an existing self-contained HTML file")
        page_path = inside(target, page)
        page_text = page_path.read_text(encoding="utf-8")
        marker = f"<!-- STANDARD-MOUNT:{scope} -->"
        if page_text.count(marker) != 1:
            raise ValueError("page must contain exactly one explicit marker: " + marker)
    if destination.exists():
        if digest(destination / "pack.json") != digest(pack / "pack.json") or not check_package(destination)["ok"]:
            raise ValueError("installed version has drifted; it will not be overwritten")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(pack, destination)
    usage = {"id": manifest["id"], "version": manifest["version"], "package": relative.as_posix(),
             "pack_sha256": digest(pack / "pack.json"), "mode": "assets-only"}
    if page_path:
        url = Path(os.path.relpath(destination / entry, page_path.parent)).as_posix()
        element = (f'<iframe id="{html.escape(scope, quote=True)}" data-standard="{manifest["id"]}@{manifest["version"]}" '
                   f'src="{html.escape(url, quote=True)}" title="{html.escape(manifest["title"], quote=True)}" '
                   f'style="width:100%;height:{int(height)}px;border:0;display:block"></iframe>')
        page_path.write_text(page_text.replace(marker, element), encoding="utf-8")
        usage.update(mode="isolated-frame", page=page, scope=scope, entry=entry, src=url)
    lock_path = target / "standard-usage.json"
    lock = read_json(lock_path) if lock_path.exists() else {"format_version": 1, "usages": []}
    if usage not in lock["usages"]:
        lock["usages"].append(usage)
    write_json(lock_path, lock)
    return {"ok": True, "installed": str(destination), "usage": usage,
            "note": "iframe mode preserves CSS/JS isolation; copying fragments into host DOM requires deliberate manual integration and review"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--page")
    parser.add_argument("--scope")
    parser.add_argument("--entry")
    parser.add_argument("--height", type=int, default=300)
    args = parser.parse_args()
    try:
        print(json.dumps(install(**vars(args)), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
