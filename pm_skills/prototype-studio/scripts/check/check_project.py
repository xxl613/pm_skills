#!/usr/bin/env python3
"""Check prototype contracts and derived review data without changing project sources."""
import argparse
import json
import posixpath
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

KINDS = {'user-input', 'external', 'derived', 'fixed', 'ai', 'synthetic', 'pending'}
MODES = {'interactive', 'external', 'derived', 'fixed', 'not-applicable'}
SUPPORT_DIRS = {'assets', 'standards', '_review', 'node_modules', '.git'}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            value = dict(attrs).get('href')
            if value:
                self.hrefs.append(value)


def check_project(project, allow_pending=False, check_generated=True):
    root = Path(project).resolve()
    errors, pending, warnings = [], [], []

    def error(message):
        errors.append(message)

    def read(name):
        try:
            result = json.loads((root / name).read_text(encoding='utf-8'))
            if not isinstance(result, dict) or result.get('schemaVersion') != 1:
                raise ValueError('expected object with schemaVersion: 1')
            return result
        except (OSError, ValueError) as exc:
            error(f'{name}: {exc}')
            return {}

    def indexed(doc, key):
        rows = doc.get(key, [])
        if not isinstance(rows, list):
            error(f'{key}: expected array')
            return {}
        result = {}
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id'].strip():
                error(f'{key}: every entry needs a nonempty string id')
                continue
            if row['id'] in result:
                error(f'{key}: duplicate id {row["id"]}')
            result[row['id']] = row
        return result

    def ids_valid(ids, label, known):
        if not isinstance(ids, list):
            error(f'{label}: expected array')
            return []
        for value in ids:
            if not isinstance(value, str) or value not in known:
                error(f'{label}: unknown reference {value}')
        return ids

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    def safe_file(value, label, suffix=None):
        if not nonempty(value):
            error(f'{label}: missing path')
            return None
        target = (root / value).resolve()
        if Path(value).is_absolute() or not target.is_relative_to(root):
            error(f'{label}: path must remain inside project')
            return None
        if suffix and target.suffix.lower() not in suffix:
            error(f'{label}: expected {suffix}')
        if not target.is_file():
            error(f'{label}: missing file {value}')
            return None
        return target

    page_doc, data_doc, decision_doc = read('pages.json'), read('data.json'), read('decisions.json')
    pages, objects, decisions = indexed(page_doc, 'pages'), indexed(data_doc, 'objects'), indexed(decision_doc, 'decisions')
    fixture = data_doc.get('fixtureOnly') is True
    if fixture:
        warnings.append('fixtureOnly: synthetic validation fixture; this report does not approve real product data')
    if not pages:
        error('pages.json: register at least one page')
    routes = {}
    page_files = {}
    for pid, page in pages.items():
        label = f'page {pid}'
        if not nonempty(page.get('title')):
            error(f'{label}: missing title')
        path = page.get('path')
        if isinstance(path, str):
            url = urlsplit(path)
            if url.scheme or url.netloc or '\\' in path:
                error(f'{label}: use a local relative route')
            decoded = unquote(url.path)
            html_file = safe_file(decoded, label, {'.html', '.htm'})
            if html_file:
                page_files[html_file] = pid
            route = (posixpath.normpath(decoded), tuple(sorted(parse_qsl(url.query, keep_blank_values=True))), unquote(url.fragment))
            if route in routes:
                error(f'{label}: route duplicates {routes[route]}')
            routes[route] = pid
        else:
            error(f'{label}: missing path')
        prd = safe_file(page.get('prd'), f'{label} PRD', {'.md'})
        if prd and not prd.read_text(encoding='utf-8').strip():
            error(f'{label}: empty PRD')
        ids_valid(page.get('dataObjects', []), f'{label} dataObjects', objects)
        status = page.get('status')
        if not isinstance(status, dict):
            error(f'{label}: missing status object')
        else:
            for key in ['implemented', 'verified', 'userReviewed']:
                if not isinstance(status.get(key), bool):
                    error(f'{label}: status.{key} must be boolean')
            if status.get('verified') and not status.get('implemented'):
                error(f'{label}: cannot be verified before implementation')
            if status.get('userReviewed') and not nonempty(page.get('userReviewEvidence')):
                error(f'{label}: userReviewed needs real userReviewEvidence')

    # Runtime/support directories contain component specimens, not product pages.
    # Every other physical HTML is a business page unless explicitly documented.
    supporting = page_doc.get('supportingHtml', [])
    supporting_paths = set()
    if not isinstance(supporting, list):
        error('supportingHtml: expected array of {path, reason}')
        supporting = []
    for entry in supporting:
        if not isinstance(entry, dict) or not nonempty(entry.get('reason')):
            error('supportingHtml: an explicit non-business purpose is required')
            continue
        target = safe_file(entry.get('path'), 'supportingHtml', {'.html', '.htm'})
        if target:
            supporting_paths.add(target)
    for html_file in root.rglob('*'):
        if html_file.suffix.lower() not in {'.html', '.htm'} or not html_file.is_file():
            continue
        if any(part in SUPPORT_DIRS for part in html_file.relative_to(root).parts):
            continue
        if html_file.resolve() not in page_files and html_file.resolve() not in supporting_paths:
            error(f'unregistered business HTML: {html_file.relative_to(root)}')
    for html_file, pid in page_files.items():
        parser = Links()
        parser.feed(html_file.read_text(encoding='utf-8'))
        for href in parser.hrefs:
            url = urlsplit(href)
            same_page_query = not url.path and href.lstrip().startswith('?')
            if url.scheme or url.netloc or (not same_page_query and not url.path.lower().endswith(('.html', '.htm'))):
                continue
            # Query-only links replace the current query; plain #anchors remain local navigation.
            target = html_file if same_page_query else (html_file.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(root):
                error(f'page {pid}: business link escapes project: {href}')
                continue
            if target in supporting_paths:
                continue
            relative = target.relative_to(root).as_posix()
            route = (relative, tuple(sorted(parse_qsl(url.query, keep_blank_values=True))), unquote(url.fragment))
            if route not in routes:
                error(f'page {pid}: link to unregistered business route: {href}')

    for did, decision in decisions.items():
        label = f'decision {did}'
        if decision.get('kind') not in {'data-source', 'mock-rule', 'performance', 'scope'}:
            error(f'{label}: unknown kind')
        if decision.get('status') not in {'pending', 'confirmed', 'rejected'}:
            error(f'{label}: unknown status')
        if not nonempty(decision.get('question')):
            error(f'{label}: missing question')
        ids_valid(decision.get('affectedPages', []), f'{label} affectedPages', pages)
        if decision.get('status') == 'confirmed':
            for key in ['answer', 'evidence']:
                if not nonempty(decision.get(key)):
                    error(f'{label}: confirmed requires {key}')
        if decision.get('kind') == 'performance':
            perf = decision.get('performance')
            if not isinstance(perf, dict):
                error(f'{label}: missing performance assessment')
                continue
            for key in ['trigger', 'frequency', 'impact', 'alternative']:
                if not nonempty(perf.get(key)):
                    error(f'{label}: missing performance.{key}')
            if perf.get('measurement') not in {'estimated', 'measured', 'unknown'}:
                error(f'{label}: measurement must distinguish estimates from measurements')
            if not isinstance(perf.get('highCost'), bool):
                error(f'{label}: highCost must be boolean')
            if not nonempty(perf.get('assessmentBasis')):
                error(f'{label}: performance cost judgment needs assessmentBasis')
            if perf.get('measurement') == 'measured' and not nonempty(perf.get('evidence')):
                error(f'{label}: measured performance needs evidence and environment')
            if perf.get('highCost') is True and decision.get('status') == 'pending':
                pending.append(f'{label}: high-cost operation awaits user decision')
            elif decision.get('status') == 'pending':
                warnings.append(f'{label}: low-cost assessment still has a pending decision; verify whether user input is needed')
        elif decision.get('status') == 'pending' and not (fixture and decision.get('kind') == 'mock-rule'):
            pending.append(f'{label}: {decision.get("question", "awaits user decision")}')

    fields = {}
    for oid, obj in objects.items():
        obj_fields = indexed({'fields': obj.get('fields', [])}, 'fields')
        if not obj_fields:
            error(f'object {oid}: no fields')
        for fid, field in obj_fields.items():
            fields[f'{oid}.{fid}'] = field
        crud = obj.get('crud')
        if not isinstance(crud, dict):
            error(f'object {oid}: missing object lifecycle (crud)')
            continue
        for action in ['create', 'read', 'update', 'delete']:
            operation = crud.get(action)
            if not isinstance(operation, dict):
                error(f'object {oid}: missing {action} rule')
                continue
            if operation.get('mode') not in MODES:
                error(f'object {oid} {action}: unknown mode')
            involved = ids_valid(operation.get('pages', []), f'object {oid} {action} pages', pages)
            if operation.get('mode') == 'interactive' and not involved:
                error(f'object {oid} {action}: interactive operation needs a page')
            for pid in involved:
                if pid in pages and oid not in pages[pid].get('dataObjects', []):
                    error(f'object {oid} {action}: page {pid} does not declare object')
            if not nonempty(operation.get('rule')):
                error(f'object {oid} {action}: rule must explain permissions, effects or readonly reason')

    dependencies = {}
    for fid, field in fields.items():
        oid = fid.split('.', 1)[0]
        consumed_on = [pid for pid, page in pages.items() if oid in page.get('dataObjects', [])]
        if 'pages' in field:
            consumed_on = ids_valid(field['pages'], f'field {fid} pages', pages)
            for pid in consumed_on:
                if pid in pages and oid not in pages[pid].get('dataObjects', []):
                    error(f'field {fid}: consumer page {pid} does not declare the object')
        if field.get('type') not in {'string', 'number', 'boolean', 'date', 'enum'}:
            error(f'field {fid}: unsupported or missing type')
        source = field.get('source')
        if not isinstance(source, dict):
            error(f'field {fid}: missing source')
            continue
        kind = source.get('kind')
        if kind not in KINDS:
            error(f'field {fid}: unknown source kind {kind}')
        if kind != 'pending' and not nonempty(source.get('reference')):
            error(f'field {fid}: missing source reference')
        source_pages = ids_valid(source.get('pages', []), f'field {fid} source.pages', pages)
        if kind == 'user-input' and not source_pages:
            error(f'field {fid}: user input must identify its source page')
        if kind not in {'pending', 'user-input'} and not source_pages and not nonempty(source.get('noPageReason')):
            error(f'field {fid}: source without a page needs noPageReason')
        if kind == 'derived':
            inputs = ids_valid(source.get('inputs', []), f'field {fid} inputs', fields)
            dependencies[fid] = [key for key in inputs if isinstance(key, str) and key in fields]
            if not inputs or not nonempty(source.get('rule')):
                error(f'field {fid}: derived field needs inputs and formula rule')
        if kind == 'fixed' and source.get('storage') not in {'database-seed', 'maintained-config', 'prototype-example'}:
            error(f'field {fid}: fixed source must identify its maintenance/storage choice')
        if kind in {'external', 'fixed', 'ai'} and not nonempty(source.get('rule')):
            error(f'field {fid}: source rule must explain creation, synchronization or maintenance')
        if kind in {'external', 'fixed'} and not nonempty(source.get('maintainer')):
            error(f'field {fid}: source needs an explicit maintainer')
        if kind == 'external' and not (nonempty(source.get('artifact')) or nonempty(source.get('externalSystem'))):
            error(f'field {fid}: external source needs a local artifact or externalSystem identifier')
        if 'artifact' in source:
            safe_file(source['artifact'], f'field {fid} source artifact')
        if kind in {'synthetic', 'pending'}:
            decision = decisions.get(source.get('decisionId'))
            required_kind = 'mock-rule' if kind == 'synthetic' else 'data-source'
            if not decision or decision.get('kind') != required_kind:
                error(f'field {fid}: needs {required_kind} decisionId')
            elif kind == 'synthetic' and decision.get('status') == 'rejected':
                error(f'field {fid}: cannot use a rejected synthetic rule')
            elif kind == 'synthetic' and not fixture and decision.get('status') != 'confirmed':
                pending.append(f'field {fid}: synthetic generation rule is not confirmed')
            elif kind == 'pending' and decision.get('status') != 'pending':
                error(f'field {fid}: decision resolved; update source instead of retaining pending')
            if kind == 'synthetic' and not nonempty(source.get('rule')):
                error(f'field {fid}: synthetic generation needs a consistent rule')
        if kind == 'ai':
            inputs = ids_valid(source.get('inputs', []), f'field {fid} AI inputs', fields)
            if not inputs:
                error(f'field {fid}: AI generation needs explicit input fields')
            decision = decisions.get(source.get('performanceDecisionId'))
            if not decision or decision.get('kind') != 'performance':
                error(f'field {fid}: AI data needs a performance assessment decision')
            elif decision.get('status') == 'rejected':
                error(f'field {fid}: still uses a rejected AI operation')
            elif any(pid not in decision.get('affectedPages', []) for pid in consumed_on):
                error(f'field {fid}: performance decision omits consumer pages')

    visited, visiting = set(), set()
    def visit(fid):
        if fid in visiting:
            error(f'field {fid}: derived source cycle')
            return
        if fid in visited:
            return
        visiting.add(fid)
        for dep in dependencies.get(fid, []):
            visit(dep)
        visiting.remove(fid)
        visited.add(fid)
    for fid in dependencies:
        visit(fid)

    if check_generated and not errors:
        sync = Path(__file__).resolve().parents[1] / 'sync' / 'sync_review.py'
        result = subprocess.run([sys.executable, str(sync), '--project', str(root), '--check', '--inject'], text=True, capture_output=True)
        if result.returncode:
            error('review data is invalid or stale: ' + (result.stdout + result.stderr).strip())
    pending = list(dict.fromkeys(pending))
    return {'project': str(root), 'fixtureOnly': fixture, 'ok': not errors and (allow_pending or not pending),
            'contractReady': not errors and not pending and not fixture, 'errors': errors,
            'pending': pending, 'warnings': warnings,
            'counts': {'pages': len(pages), 'objects': len(objects), 'fields': len(fields)},
            'performanceDecisions': [d for d in decisions.values() if d.get('kind') == 'performance'],
            'evidenceScope': 'contract, physical HTML and static business-link coverage, and generated-file checks only; dynamic routes, browser behavior, source/evidence authenticity and semantic/visual quality require separate evidence'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--allow-pending', action='store_true', help='Permit draft progress; pending decisions remain visible')
    parser.add_argument('--report', type=Path, help='Optional JSON report destination outside project sources')
    args = parser.parse_args()
    report = check_project(args.project, args.allow_pending)
    output = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding='utf-8')
    print(output, end='')
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
