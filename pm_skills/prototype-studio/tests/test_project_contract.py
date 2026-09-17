import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('project_check', ROOT / 'scripts/check/check_project.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ProjectContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'index.html').write_text('<!doctype html><title>Test</title>', encoding='utf-8')
        (self.root / 'page.md').write_text('# Task page\nCreate and manage tasks.', encoding='utf-8')
        self.pages = {'schemaVersion': 1, 'projectId': 'test', 'title': 'Test', 'pages': [
            {'id': 'list', 'title': 'List', 'path': 'index.html?scene=list#tasks', 'prd': 'page.md', 'dataObjects': ['task'],
             'status': {'implemented': True, 'verified': False, 'userReviewed': False}}]}
        self.data = {'schemaVersion': 1, 'objects': [{'id': 'task', 'title': 'Task', 'fields': [
            {'id': 'title', 'type': 'string', 'source': {'kind': 'user-input', 'reference': 'Task creation form', 'pages': ['list']}}],
            'crud': {a: {'mode': 'interactive', 'pages': ['list'], 'rule': 'Owner can ' + a} for a in ['create', 'read', 'update', 'delete']}}]}
        self.decisions = {'schemaVersion': 1, 'decisions': []}

    def tearDown(self):
        self.temp.cleanup()

    def check(self, **kwargs):
        for name, value in [('pages', self.pages), ('data', self.data), ('decisions', self.decisions)]:
            (self.root / (name + '.json')).write_text(json.dumps(value), encoding='utf-8')
        return module.check_project(self.root, check_generated=False, **kwargs)

    def test_base_contract(self):
        result = self.check()
        self.assertTrue(result['ok'], result)
        self.assertTrue(result['contractReady'])

    def test_query_order_cannot_create_duplicate_route(self):
        self.pages['pages'][0]['path'] = 'index.html?scene=list&role=owner#tasks'
        row = copy.deepcopy(self.pages['pages'][0]); row.update(id='copy', path='index.html?role=owner&scene=list#tasks')
        self.pages['pages'].append(row)
        self.assertTrue(any('duplicates' in e for e in self.check()['errors']))

    def test_query_and_hash_states_are_distinct(self):
        row = copy.deepcopy(self.pages['pages'][0]); row.update(id='detail', path='index.html?scene=detail#record')
        self.pages['pages'].append(row)
        self.assertTrue(self.check()['ok'])

    def test_missing_input_page_and_unknown_origin(self):
        field = self.data['objects'][0]['fields'][0]
        field['source'] = {'kind': 'user-input', 'reference': 'form'}
        self.assertFalse(self.check()['ok'])
        field.pop('source')
        self.assertTrue(any('missing source' in e for e in self.check()['errors']))

    def test_pending_data_decision_is_preserved_in_draft(self):
        self.data['objects'][0]['fields'][0]['source'] = {'kind': 'pending', 'decisionId': 'Q-1'}
        self.decisions['decisions'] = [{'id': 'Q-1', 'kind': 'data-source', 'status': 'pending', 'question': 'What supplies the title?', 'affectedPages': ['list']}]
        self.assertFalse(self.check()['ok'])
        report = self.check(allow_pending=True)
        self.assertTrue(report['ok']); self.assertFalse(report['contractReady']); self.assertTrue(report['pending'])

    def test_confirmed_synthetic_rule_is_not_pending(self):
        self.data['objects'][0]['fields'][0]['source'] = {'kind': 'synthetic', 'reference': 'M-1', 'noPageReason': 'Isolated test fixture', 'decisionId': 'M-1', 'rule': 'Title equals task-{stable ID}'}
        self.decisions['decisions'] = [{'id': 'M-1', 'kind': 'mock-rule', 'status': 'confirmed', 'question': 'Use stable test names?', 'answer': 'Yes', 'evidence': 'Isolated unit-test fixture approval, not a product decision', 'affectedPages': ['list']}]
        self.assertFalse(self.check()['pending'])
        self.decisions['decisions'][0]['status'] = 'pending'
        self.assertFalse(self.check()['ok'])

    def test_fixture_is_not_product_delivery_ready(self):
        self.data['fixtureOnly'] = True
        report = self.check()
        self.assertTrue(report['ok']); self.assertFalse(report['contractReady'])

    def test_fixed_data_requires_maintenance_choice(self):
        self.data['objects'][0]['fields'][0]['source'] = {'kind': 'fixed', 'reference': 'Business configuration', 'maintainer': 'Operations', 'rule': 'Operations updates shared configuration', 'noPageReason': 'Maintained by operations outside this prototype'}
        self.assertFalse(self.check()['ok'])
        self.data['objects'][0]['fields'][0]['source']['storage'] = 'maintained-config'
        self.assertTrue(self.check()['ok'])

    def test_object_lifecycle_allows_readonly_reason(self):
        self.data['objects'][0]['crud']['delete'] = {'mode': 'not-applicable', 'pages': [], 'rule': 'Audit trail is retained; only system retention can expire it'}
        self.assertTrue(self.check()['ok'])
        self.data['objects'][0]['crud']['delete'].pop('rule')
        self.assertFalse(self.check()['ok'])

    def test_derived_references_and_cycles(self):
        fields = self.data['objects'][0]['fields']
        fields.append({'id': 'total', 'type': 'number', 'source': {'kind': 'derived', 'reference': 'Title records', 'noPageReason': 'Computed from source fields', 'inputs': ['task.missing'], 'rule': 'Count records'}})
        self.assertFalse(self.check()['ok'])
        fields[-1]['source']['inputs'] = ['task.title']
        self.assertTrue(self.check()['ok'])
        fields[0]['source'] = {'kind': 'derived', 'reference': 'Total', 'noPageReason': 'Computed from source fields', 'inputs': ['task.total'], 'rule': 'Format total'}
        self.assertTrue(any('cycle' in e for e in self.check()['errors']))

    def test_high_cost_ai_requires_decision_and_measured_evidence(self):
        self.data['objects'][0]['fields'][0]['source'] = {'kind': 'ai', 'reference': 'AI summary', 'inputs': ['task.title'], 'rule': 'Generate on demand and cache until input changes', 'noPageReason': 'Generated by system', 'performanceDecisionId': 'P-1'}
        self.decisions['decisions'] = [{'id': 'P-1', 'kind': 'performance', 'status': 'pending', 'question': 'Generate on every view?', 'affectedPages': ['list'],
            'performance': {'highCost': True, 'trigger': 'every view', 'frequency': 'every navigation', 'impact': 'network wait', 'alternative': 'cache until content changes', 'measurement': 'estimated', 'assessmentBasis': 'one network call per navigation; no timing claimed'}}]
        self.assertFalse(self.check()['ok'])
        self.decisions['decisions'][0].update(status='confirmed', answer='Generate on demand', evidence='Test-only approval')
        self.assertTrue(self.check()['ok'])
        self.decisions['decisions'][0]['performance']['measurement'] = 'measured'
        self.assertFalse(self.check()['ok'])

    def test_user_review_is_not_automatically_inferred(self):
        self.pages['pages'][0]['status'].update(verified=True, userReviewed=True)
        self.assertTrue(any('userReviewEvidence' in e for e in self.check()['errors']))

    def test_unregistered_page_and_link_are_rejected(self):
        (self.root / 'other.html').write_text('<title>Undocumented page</title>')
        (self.root / 'index.html').write_text('<a href="other.html">Other</a>')
        errors = self.check()['errors']
        self.assertTrue(any('unregistered business HTML' in e for e in errors))
        self.assertTrue(any('unregistered business route' in e for e in errors))
        self.pages['supportingHtml'] = [{'path': 'other.html', 'reason': 'Static source comparison artifact, not a business page'}]
        self.assertTrue(self.check()['ok'])

    def test_query_only_link_requires_registered_scene(self):
        (self.root / 'index.html').write_text('<a href="?scene=detail#record">Detail</a>')
        self.assertTrue(any('unregistered business route' in e for e in self.check()['errors']))
        row = copy.deepcopy(self.pages['pages'][0])
        row.update(id='detail', path='index.html?scene=detail#record')
        self.pages['pages'].append(row)
        self.assertTrue(self.check()['ok'])
        # The query replaces the list scene in the same file, rather than merging with it.
        self.pages['pages'][0]['path'] = 'index.html?scene=list&filter=open#tasks'
        self.assertTrue(self.check()['ok'])

    def test_empty_query_link_and_plain_anchor(self):
        (self.root / 'index.html').write_text('<a href="#help">Help</a>')
        self.assertTrue(self.check()['ok'])
        (self.root / 'index.html').write_text('<a href="?">Clear scene</a>')
        self.assertTrue(any('unregistered business route' in e for e in self.check()['errors']))
        row = copy.deepcopy(self.pages['pages'][0])
        row.update(id='default', path='index.html')
        self.pages['pages'].append(row)
        self.assertTrue(self.check()['ok'])

    def test_external_source_requires_maintenance_and_valid_local_artifact(self):
        source = {'kind': 'external', 'reference': 'input.csv', 'noPageReason': 'Scheduled import'}
        self.data['objects'][0]['fields'][0]['source'] = source
        self.assertFalse(self.check()['ok'])
        source.update(maintainer='Operations', rule='Import validated file daily', artifact='input.csv')
        self.assertFalse(self.check()['ok'])
        (self.root / 'input.csv').write_text('title\nTask\n')
        self.assertTrue(self.check()['ok'])

    def test_ai_decision_covers_consuming_pages(self):
        source = {'kind': 'ai', 'reference': 'Summary generation', 'noPageReason': 'System generation',
                  'inputs': ['task.title'], 'rule': 'Generate when requested; cache until edit', 'performanceDecisionId': 'P-1'}
        self.data['objects'][0]['fields'].append({'id': 'analysis', 'type': 'string', 'source': source})
        self.decisions['decisions'] = [{'id': 'P-1', 'kind': 'performance', 'status': 'confirmed',
            'question': 'Generate?', 'answer': 'On demand', 'evidence': 'Isolated test fixture', 'affectedPages': [],
            'performance': {'trigger': 'request', 'frequency': 'per user request', 'impact': 'network wait',
                'alternative': 'cached result', 'measurement': 'estimated', 'highCost': True, 'assessmentBasis': 'Network request needed'}}]
        self.assertTrue(any('omits consumer pages' in e for e in self.check()['errors']))
        self.decisions['decisions'][0]['affectedPages'] = ['list']
        self.assertTrue(self.check()['ok'])

    def test_path_escape_is_rejected(self):
        self.pages['pages'][0]['prd'] = '../private.md'
        self.assertTrue(any('inside project' in e for e in self.check()['errors']))


if __name__ == '__main__':
    unittest.main()
