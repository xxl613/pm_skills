"""File-level standard packages; no DOM inference or HTML component extraction."""
from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def inside(root: Path, value: str) -> Path:
    candidate = (root / value).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes package: {value}")
    return candidate


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and name in {"src", "href", "poster"}:
                self.items.append((value, tag not in {"a", "area"}))
            if value and name == "style":
                self.items.extend((v, True) for v in css_urls(value))


def css_urls(text):
    return [m.group(2).strip() for m in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", text, re.S)]


def references(root: Path):
    errors, external = [], []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".css", ".js", ".mjs"}:
            continue
        content = path.read_text(encoding="utf-8")
        values = []
        if path.suffix == ".html":
            parser = References()
            parser.feed(content)
            values.extend(parser.items)
            for block in re.findall(r"<style\b[^>]*>(.*?)</style>", content, re.S | re.I):
                values.extend((v, True) for v in css_urls(block))
        elif path.suffix == ".css":
            values.extend((v, True) for v in css_urls(content))
            values.extend((v, True) for v in re.findall(r"@import\s+['\"]([^'\"]+)['\"]", content))
        else:
            values.extend((v, True) for v in re.findall(r"(?:import|from)\s*['\"]([^'\"]+)['\"]", content))
        for value, runtime in values:
            if not value or value.startswith(("#", "?", "data:", "blob:", "mailto:", "tel:")):
                continue
            if "${" in value or "{{" in value:
                continue  # Dynamic references require browser verification.
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                external.append({"file": str(path.relative_to(root)), "url": value, "runtime": runtime})
                if runtime:
                    errors.append(f"external runtime resource: {path.relative_to(root)} -> {value}")
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root.resolve()):
                errors.append(f"reference escapes package: {path.relative_to(root)} -> {value}")
            elif not destination.exists():
                errors.append(f"missing reference: {path.relative_to(root)} -> {value}")
    return errors, external


def validate_definition(definition):
    required = {"id", "version", "title", "platforms", "scope", "locked", "slots", "states", "examples", "source", "license"}
    missing = required - definition.keys()
    if missing:
        raise ValueError("missing definition fields: " + ", ".join(sorted(missing)))
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", definition["id"]):
        raise ValueError("id must use lowercase letters, digits and hyphens")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?", definition["version"]):
        raise ValueError("version must use major.minor.patch")
    for name in ("platforms", "locked", "states", "examples"):
        if not isinstance(definition[name], list) or not definition[name]:
            raise ValueError(f"{name} must be a nonempty list")
    if not isinstance(definition["slots"], list):
        raise ValueError("slots must be a list; [] explicitly means no customization")
    specification = definition.get("specification")
    if specification is not None:
        if (not isinstance(specification, dict) or not isinstance(specification.get("files"), list)
                or not specification["files"] or not all(isinstance(v, str) and v for v in specification["files"])
                or specification.get("entry") not in specification["files"]):
            raise ValueError("specification must declare a nonempty files list containing its entry")


def check_package(root: Path):
    errors = []
    manifest = read_json(root / "pack.json")
    validate_definition(manifest)
    listed = set()
    for record in manifest.get("files", []):
        name = record["path"]
        if name in listed:
            errors.append(f"duplicate manifest file: {name}")
        listed.add(name)
        try:
            path = inside(root, name)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.is_file():
            errors.append(f"missing file: {name}")
        elif digest(path) != record["sha256"]:
            errors.append(f"hash drift: {name}")
        if not record.get("source_sha256") or not record.get("source_path"):
            errors.append(f"missing origin provenance: {name}")
    actual = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p != root / "pack.json"}
    errors.extend(f"unregistered file: {name}" for name in sorted(actual - listed))
    if not listed:
        errors.append("package has no files")
    for entry in manifest["examples"]:
        name = entry["path"] if isinstance(entry, dict) else entry
        if name not in listed:
            errors.append(f"example not registered: {name}")
    specification = manifest.get("specification")
    if specification is not None:
        if not isinstance(specification, dict) or not isinstance(specification.get("files"), list):
            errors.append("specification must declare entry and files")
        else:
            for name in [specification.get("entry"), *specification["files"]]:
                if not isinstance(name, str) or name not in listed:
                    errors.append(f"specification file not registered: {name}")
    ref_errors, external = references(root)
    return {"ok": not (errors or ref_errors), "id": manifest["id"], "version": manifest["version"],
            "files": len(listed), "errors": errors + ref_errors, "external_links": external,
            "limits": ["Static local URL checks do not execute JavaScript or prove runtime behavior or pixel fidelity."]}
