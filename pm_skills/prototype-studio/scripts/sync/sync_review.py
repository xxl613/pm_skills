#!/usr/bin/env python3
"""Build an offline review view from explicit source documents; never infer PRD semantics."""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

PACKAGE = Path(__file__).resolve().parents[2]
ASSETS = PACKAGE / "assets" / "review-shell"
START = "<!-- prototype-studio:review:start -->"
END = "<!-- prototype-studio:review:end -->"
BLOCK = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("File references must be non-empty strings")
    parts = urlsplit(relative)
    if parts.scheme or parts.netloc or parts.path.startswith("/"):
        raise ValueError(f"Expected a project-relative file: {relative}")
    path = (root / unquote(parts.path)).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"Missing or out-of-project file: {relative}")
    return path


def route_key(path: str) -> tuple:
    route = urlsplit(path)
    return (posixpath.normpath(unquote(route.path)), tuple(sorted(parse_qsl(route.query, keep_blank_values=True))), unquote(route.fragment))


def read_sources(root: Path) -> tuple[dict, dict[str, str], list[Path]]:
    sources: dict[str, str] = {}
    docs = {}
    for filename in ("pages.json", "data.json", "decisions.json"):
        path = local_file(root, filename)
        raw = path.read_bytes()
        sources[filename] = sha(raw)
        docs[filename] = json.loads(raw)
        if not isinstance(docs[filename], dict) or docs[filename].get("schemaVersion") != 1:
            raise ValueError(f"{filename}: schemaVersion must be 1")
    catalog = docs["pages.json"]
    if not isinstance(catalog.get("projectId"), str) or not catalog["projectId"].strip():
        raise ValueError("pages.json: projectId is required")
    if not isinstance(catalog.get("title"), str) or not catalog["title"].strip():
        raise ValueError("pages.json: title is required")
    if not isinstance(catalog.get("pages"), list):
        raise ValueError("pages.json: pages must be a list (an empty list is valid for an unbuilt project)")
    objects = docs["data.json"].get("objects")
    decisions = docs["decisions.json"].get("decisions")
    if not isinstance(objects, list) or not isinstance(decisions, list):
        raise ValueError("data.objects and decisions.decisions must be lists")
    object_ids = {item["id"] for item in objects}
    ids, routes, html_files, output_pages = set(), set(), set(), []
    for page in catalog["pages"]:
        for key in ("id", "title", "path", "prd"):
            if not isinstance(page.get(key), str) or not page[key].strip():
                raise ValueError(f"Page has no {key}: {page.get('id', '(unnamed)')}")
        if page["id"] in ids or route_key(page["path"]) in routes:
            raise ValueError(f"Duplicate page id or route: {page['id']}")
        ids.add(page["id"])
        routes.add(route_key(page["path"]))
        html_path = local_file(root, page["path"])
        if html_path.suffix.lower() != ".html":
            raise ValueError(f"Page must reference HTML: {page['path']}")
        html_files.add(html_path)
        prd_path = local_file(root, page["prd"])
        if prd_path.suffix.lower() != ".md":
            raise ValueError(f"PRD must be Markdown: {page['prd']}")
        prd = prd_path.read_text(encoding="utf-8")
        if not prd.strip():
            raise ValueError(f"Empty page PRD: {page['prd']}")
        sources[prd_path.relative_to(root).as_posix()] = sha(prd_path.read_bytes())
        if not isinstance(page.get("dataObjects"), list) or any(x not in object_ids for x in page["dataObjects"]):
            raise ValueError(f"Unknown or missing dataObjects: {page['id']}")
        status = page.get("status", {})
        if any(type(status.get(k)) is not bool for k in ("implemented", "verified", "userReviewed")):
            raise ValueError(f"Three independent boolean status values required: {page['id']}")
        if status["userReviewed"] and not str(page.get("userReviewEvidence", "")).strip():
            raise ValueError(f"userReviewed requires actual user evidence: {page['id']}")
        output_pages.append({**page, "prdMarkdown": prd})
    sources = dict(sorted(sources.items()))
    performance_fields = {}
    for obj in objects:
        for field in obj.get("fields", []):
            decision_id = field.get("source", {}).get("performanceDecisionId")
            if decision_id:
                performance_fields.setdefault(decision_id, []).append(obj["id"] + "." + field["id"])
    payload = {"schemaVersion": 1, "projectId": catalog["projectId"], "title": catalog["title"],
               "fixtureOnly": docs["data.json"].get("fixtureOnly", False), "pages": output_pages,
               "sourceHash": sha(json.dumps(sources, sort_keys=True).encode()), "sources": sources,
               "decisions": decisions, "performanceFields": performance_fields}
    return payload, sources, sorted(html_files)


def performance_markdown(payload: dict) -> str:
    lines = ["# 性能与生成成本确认表", "", "本表由 decisions.json 与 data.json 派生。未提供的测量不填估计数字；脚本不代表用户确认。", "",
             "| 决策 | 字段 | 触发 | 频率 | 影响 | 替代方案 | 证据类型 | 测量证据 | 高成本 | 决定 | 用户证据 |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    records = [item for item in payload["decisions"] if item["kind"] == "performance"]
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    for item in records:
        cost = item.get("performance", {})
        values = [item["id"], ", ".join(payload["performanceFields"].get(item["id"], [])) or "页面级能力",
                  cost.get("trigger", "待补充"), cost.get("frequency", "待补充"), cost.get("impact", "待评估"),
                  cost.get("alternative", "待评估"), cost.get("measurement", "unknown"), cost.get("evidence", "尚无测量证据"),
                  "是" if cost.get("highCost") else "否", item["status"] + ": " + item.get("answer", "待用户确认"), item.get("evidence", "尚无用户确认")]
        lines.append("| " + " | ".join(map(cell, values)) + " |")
    if not records:
        lines.extend(["", "尚无性能决策记录；这不自动证明产品不存在高成本能力。应在交付验收中检查 AI 调用、大文件和高频刷新。"])
    return "\n".join(lines) + "\n"


def desired_block(root: Path, page: Path) -> str:
    import os
    prefix = Path(os.path.relpath(root / "_review", page.parent)).as_posix()
    return (f'{START}\n<link rel="stylesheet" href="{prefix}/review-shell.css">\n'
            f'<script defer src="{prefix}/review-data.js"></script>\n'
            f'<script defer src="{prefix}/review-shell.js"></script>\n{END}')


def injected_text(root: Path, page: Path) -> str:
    current = page.read_text(encoding="utf-8")
    block = desired_block(root, page)
    if current.count(START) != current.count(END):
        raise ValueError(f"Unbalanced review markers: {page}")
    if BLOCK.search(current):
        if len(BLOCK.findall(current)) != 1:
            raise ValueError(f"Multiple review blocks: {page}")
        return BLOCK.sub(lambda _: block, current)
    match = re.search(r"</body\s*>", current, re.I)
    if not match:
        raise ValueError(f"Cannot inject without </body>: {page}")
    return current[:match.start()] + block + "\n" + current[match.start():]


def synchronize(root: Path, check: bool = False, inject: bool = False) -> dict:
    root = root.expanduser().resolve()
    payload, sources, html_files = read_sources(root)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    generated = {"review-data.js": ("window.PROTOTYPE_REVIEW_DATA = " + encoded + ";\n").encode(),
                 "performance-review.md": performance_markdown(payload).encode()}
    for name in ("review-shell.js", "review-shell.css"):
        generated[name] = (ASSETS / name).read_bytes()
    manifest = {"schemaVersion": 1, "sourceHash": payload["sourceHash"], "sources": sources,
                "generated": {name: sha(value) for name, value in generated.items()}}
    generated["source-manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    updates = {}
    for name, value in generated.items():
        target = root / "_review" / name
        if not target.exists() or target.read_bytes() != value:
            updates[target] = value
    for page in html_files:
        has_block = START in page.read_text(encoding="utf-8")
        if inject or has_block:
            expected = injected_text(root, page)
            if expected != page.read_text(encoding="utf-8"):
                if not check and not inject:
                    raise ValueError(f"Review block needs repair; rerun with --inject: {page}")
                updates[page] = expected.encode()
    changes = [path.relative_to(root).as_posix() for path in updates]
    if check and changes:
        raise ValueError("Stale or missing generated review artifacts: " + ", ".join(changes))
    if not check:
        for path, value in updates.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)
    return {"ok": True, "project": str(root), "pages": len(payload["pages"]),
            "sourceHash": payload["sourceHash"], "changed": changes, "check": check,
            "injected": inject, "note": "Freshness checks source documents; semantic code/PRD agreement requires review."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--check", action="store_true", help="Read-only freshness check")
    parser.add_argument("--inject", action="store_true", help="Add/repair the managed review block in registered HTML")
    args = parser.parse_args()
    try:
        print(json.dumps(synchronize(args.project, args.check, args.inject), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
