#!/usr/bin/env python3
"""Rebuild the V5 1.0.0 source snapshot from the specified local legacy skill."""
import argparse
import re
import shutil
import sys
from pathlib import Path

from standard_lib import check_package, digest, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="legacy v5-ux-rule directory; never modified")
    parser.add_argument("--registry", required=True)
    parser.add_argument("--specifications", required=True, help="reviewed current specification directory; copied into the new self-contained pack")
    args = parser.parse_args()
    source = Path(args.source).resolve()
    destination = Path(args.registry).resolve() / "v5" / "1.0.0"
    if destination.exists():
        parser.error("destination exists; migration will not overwrite a registered version")
    specifications = Path(args.specifications).resolve()
    if not (specifications / "README.md").is_file():
        parser.error("specifications must contain the reviewed README.md entry")
    source_assets = source / "assets"
    if not (source_assets / "examples/chat-flow-full.html").is_file():
        parser.error("source does not contain the required V5 example")
    records = []
    for original in sorted(source_assets.rglob("*")):
        if not original.is_file() or original.name == ".DS_Store" or "project-profile" in original.parts:
            continue
        relative = Path("assets") / original.relative_to(source_assets)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, target)
        changes = "copied unchanged; original sample business data is illustrative, not a product requirement"
        records.append({"path": relative.as_posix(), "sha256": digest(target),
                        "source_path": str(original), "source_sha256": digest(original), "changes": changes})
    platform_source = source / "scripts/check-platform.py"
    platform_target = destination / "checks/check-platform.py"
    platform_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(platform_source, platform_target)
    records.append({"path": "checks/check-platform.py", "sha256": digest(platform_target),
                    "source_path": str(platform_source), "source_sha256": digest(platform_source), "changes": "copied unchanged; optional explicit-file platform check only"})
    rail_source = source_assets / "components/history-rail.html"
    rail_document = rail_source.read_text(encoding="utf-8")
    rail_style = re.search(r"<style>(.*?)</style>", rail_document, re.S).group(1)
    rail_style = "\n".join(line for line in rail_style.splitlines() if line.lstrip().startswith(".v5-history-rail") or line.lstrip().startswith(".v5-main"))
    rail_markup = re.search(r"<aside\b.*?</aside>", rail_document, re.S).group(0)
    rail_script = re.search(r"<script>(.*?)</script>", rail_document, re.S).group(1)
    entry = destination / "assets/standalone/history-rail.html"
    entry.parent.mkdir(parents=True, exist_ok=True)
    entry.write_text('''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>V5 历史轨道标准件</title><link rel="stylesheet" href="../tokens.css">
<style>*{box-sizing:border-box}body{margin:0;font-family:var(--v5-font-family);color:#1d2129;background:#fff}.v5-main{position:relative;height:340px;padding:24px 56px 24px 24px}h1{font-size:18px;margin:0 0 16px}p{font-size:14px;line-height:1.7;max-width:440px}button{font:inherit;border:1px solid #e5e6eb;background:white;border-radius:8px;padding:8px 14px;cursor:pointer}dialog{border:1px solid #e5e6eb;border-radius:12px;padding:24px}dialog::backdrop{background:rgba(0,0,0,.45)}</style>
''' + "<style>" + rail_style + "</style>" + '''
</head><body><main class="v5-main"><h1>历史对话</h1><p>右侧刻度支持悬停、键盘聚焦、Escape 收起与当前会话定位。这里的 16 条会话仅为标准件独立样例，不计入宿主业务数据。</p><button id="open-modal">打开模态确认</button>
''' + rail_markup + '''
</main><dialog id="sample-modal" aria-modal="true" hidden><p>模态打开时历史轨道隐藏并退出键盘顺序。</p><button id="close-modal">关闭确认</button></dialog>
''' + "<script>" + rail_script + "</script>" + '''
<script>const modal=document.getElementById('sample-modal');document.getElementById('open-modal').onclick=()=>{modal.hidden=false;modal.showModal();};document.getElementById('close-modal').onclick=()=>modal.close();modal.addEventListener('close',()=>{modal.hidden=true;});</script></body></html>
''', encoding="utf-8")
    records.append({"path": "assets/standalone/history-rail.html", "sha256": digest(entry),
                    "source_path": str(rail_source), "source_sha256": digest(rail_source),
                    "changes": "copied exact .v5-history-rail CSS, aside markup and initializer into a standalone document; removed original global 1440px preview wrapper; added explanatory text and native modal controls using the original hidden-attribute observer contract"})
    specification_files = []
    for original in sorted(specifications.rglob("*")):
        if not original.is_file():
            continue
        if original.is_symlink():
            parser.error("specification symlinks are not accepted")
        relative = Path("references") / original.relative_to(specifications)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, target)
        specification_files.append(relative.as_posix())
        records.append({"path": relative.as_posix(), "sha256": digest(target),
                        "source_path": str(original), "source_sha256": digest(original),
                        "changes": "reviewed normalized specification copied unchanged from explicit input; not inferred from legacy text"})
    manifest = {
        "format_version": 1, "id": "v5", "version": "1.0.0", "title": "V5 对话与界面标准包",
        "platforms": ["desktop-1440", "mobile-375"],
        "scope": "Only user-selected pages or regions. Desktop chat, mobile chat and branded home are separate selections; use of one does not impose the others.",
        "locked": ["Selected component HTML structure, classes, CSS geometry and interaction semantics", "Real icons, illustrations and their identity mapping", "Desktop and mobile component families remain separate", "Versioned snapshot files remain immutable; customize in project-owned copies or explicit data slots"],
        "slots": [{"name": "business-content", "allowed": "Confirmed business names, labels, objects and records; any new data source or lifecycle requires specification update"}, {"name": "agent-identity", "allowed": "Reuse confirmed project mapping first. New identity selects a bundled media or avatar asset once."}, {"name": "host-scope", "allowed": "Embed selected region or deliberately integrate markup into host. Host layout outside scope is unconstrained."}],
        "states": ["desktop completed conversation", "desktop execution and plan edit", "desktop history hover/focus/current-query/Escape/modal-blocked", "mobile idle/input/task/thinking/selection/feedback/file/followup/history/sheet"],
        "examples": [{"path": "assets/examples/chat-flow-full.html", "kind": "desktop-visual-sample", "runtime_note": "history behavior present; other visible controls require project wiring"}, {"path": "assets/examples/chat-flow-execution.html", "kind": "desktop-execution-visual-sample"}, {"path": "assets/examples/chat-flow-plan-edit.html", "kind": "desktop-plan-edit-visual-sample"}, {"path": "assets/examples-mobile/mobile-chat.html", "kind": "mobile-visual-sample", "runtime_note": "sample renderer is not a complete interactive product"}, {"path": "assets/standalone/history-rail.html", "kind": "interactive-local-component"}],
        "source": {"type": "local-legacy-skill", "path": str(source), "skill_sha256": digest(source / "SKILL.md"), "upstream_design": [{"file": "4t35fBc4I64igQH6qZpIGL", "nodes": ["2117:1928", "2907:2110", "2907:3279", "6050:5423"], "status": "declared by legacy source; not freshly fetched"}, {"file": "ljg4eVP3elzzx5b2Q8FYdI", "nodes": ["56301:10134"], "status": "legacy mobile portal source only"}]},
        "license": {"status": "unknown", "note": "No asset redistribution license was found in the local legacy skill; do not invent an open-source license or claim ownership."},
        "visual_baselines": {"directory": "assets/figma-reference", "origin": "legacy component-render screenshots, not original Figma exports", "mobile_limit": "shell-mobile baselines reflect an older portal/mobile shell source; not proof of parity with current mobile B/C nodes"},
        "boundaries": {"not_included": ["legacy skill entrypoint", "legacy project onboarding", "legacy page navigation injection", "legacy project profile"], "sample_data": "All bundled legacy names, counts, dates and 16 history entries are fixture content, not verified project facts or database constants.", "legacy_shells": "Source snapshots retained for geometry and assets. Read current package specifications before reuse; explicitly corrected rules take precedence over stale source examples. Static controls require project wiring."},
        "specification": {"entry": "references/README.md", "files": specification_files,
                          "precedence": "Current normalized rules take precedence for explicitly documented corrections; visual source snapshots do not prove interactions are wired."},
        "files": records,
    }
    write_json(destination / "pack.json", manifest)
    report = check_package(destination)
    import json
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
