#!/usr/bin/env python3
"""Register a user-selected, already self-contained folder as a versioned standard."""
import argparse
import shutil
import sys
from pathlib import Path

from standard_lib import check_package, digest, inside, read_json, references, validate_definition, write_json


def register(source, definition_path, registry):
    source, registry = Path(source).resolve(), Path(registry).resolve()
    definition = read_json(Path(definition_path))
    validate_definition(definition)
    if not source.is_dir():
        raise ValueError("source must be an existing self-contained directory")
    destination = registry / definition["id"] / definition["version"]
    if destination.exists():
        raise ValueError(f"version already exists; choose a new version: {destination}")
    if destination.is_relative_to(source):
        raise ValueError("registry must not be inside the source directory")
    files = sorted(p for p in source.rglob("*") if p.is_file())
    if not files or any(p.is_symlink() for p in source.rglob("*")):
        raise ValueError("source must contain files and may not contain symlinks")
    if (source / "pack.json").exists():
        raise ValueError("source already contains pack.json; use a clean component source folder")
    errors, _ = references(source)
    if errors:
        raise ValueError("source is not self-contained:\n" + "\n".join(errors))
    for entry in definition["examples"]:
        name = entry["path"] if isinstance(entry, dict) else entry
        if not inside(source, name).is_file():
            raise ValueError(f"missing example: {name}")
    for name in definition.get("specification", {}).get("files", []):
        if not inside(source, name).is_file():
            raise ValueError(f"missing specification: {name}")
    records = [{"path": str(p.relative_to(source)), "sha256": digest(p),
                "source_path": str(p), "source_sha256": digest(p), "changes": "copied unchanged"} for p in files]
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    write_json(destination / "pack.json", {**definition, "format_version": 1, "files": records})
    result = check_package(destination)
    result["package"] = str(destination)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--definition", required=True)
    parser.add_argument("--registry", required=True)
    args = parser.parse_args()
    try:
        import json
        result = register(args.source, args.definition, args.registry)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    except (ValueError, OSError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
