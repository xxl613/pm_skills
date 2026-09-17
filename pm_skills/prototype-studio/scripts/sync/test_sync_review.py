"""Regression coverage for offline sources, stale outputs and guarded injection."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from sync_review import PACKAGE, START, read_sources, synchronize


class SyncReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = (Path(self.temp.name) / "prototype").resolve()
        shutil.copytree(PACKAGE / "examples/coherent-project/prototype", self.root)
        shutil.rmtree(self.root / "_review", ignore_errors=True)

    def tearDown(self):
        self.temp.cleanup()

    def pages(self):
        return json.loads((self.root / "pages.json").read_text())

    def write_pages(self, pages):
        (self.root / "pages.json").write_text(json.dumps(pages))

    def test_full_offline_content_and_idempotent_injection(self):
        prd = self.root / "prd/active.md"
        prd.write_text(prd.read_text() + "\nLast full-source marker </script>\n")
        synchronize(self.root, inject=True)
        generated = (self.root / "_review/review-data.js").read_text()
        self.assertIn("Last full-source marker \\u003c/script>", generated)
        self.assertIn("summary.html?view=active#records", generated)
        page_before = (self.root / "index.html").read_bytes()
        result = synchronize(self.root, inject=True)
        self.assertEqual(result["changed"], [])
        self.assertEqual(page_before, (self.root / "index.html").read_bytes())
        self.assertEqual((self.root / "index.html").read_text().count(START), 1)
        synchronize(self.root, check=True, inject=True)

    def test_check_is_readonly_and_detects_prd_change(self):
        synchronize(self.root, inject=True)
        (self.root / "prd/records.md").write_text("# Updated requirement\n")
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with self.assertRaisesRegex(ValueError, "Stale"):
            synchronize(self.root, check=True, inject=True)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_missing_and_empty_prd_rejected(self):
        pages = self.pages()
        pages["pages"][0].pop("prd")
        self.write_pages(pages)
        with self.assertRaisesRegex(ValueError, "no prd"):
            read_sources(self.root)
        pages["pages"][0]["prd"] = "prd/records.md"
        self.write_pages(pages)
        (self.root / "prd/records.md").write_text(" \n")
        with self.assertRaisesRegex(ValueError, "Empty page PRD"):
            read_sources(self.root)

    def test_duplicate_normalized_route_rejected(self):
        for alternative in ("./index.html", "folder/../index.html"):
            pages = self.pages()
            duplicate = copy.deepcopy(pages["pages"][0])
            duplicate.update(id="duplicate", path=alternative)
            pages["pages"].append(duplicate)
            self.write_pages(pages)
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                read_sources(self.root)
            pages["pages"].pop()
            self.write_pages(pages)

    def test_query_order_duplicate_and_distinct_hash(self):
        pages = self.pages()
        pages["pages"][0]["path"] = "index.html?a=1&b=2#x"
        duplicate = copy.deepcopy(pages["pages"][0])
        duplicate.update(id="duplicate", path="index.html?b=2&a=1#x")
        pages["pages"].append(duplicate)
        self.write_pages(pages)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            read_sources(self.root)
        pages["pages"][-1]["path"] = "index.html?b=2&a=1#y"
        self.write_pages(pages)
        self.assertEqual(len(read_sources(self.root)[0]["pages"]), 4)

    def test_outside_file_and_false_user_review_rejected(self):
        pages = self.pages()
        pages["pages"][0]["prd"] = "../private.md"
        (self.root.parent / "private.md").write_text("Should not embed")
        self.write_pages(pages)
        with self.assertRaisesRegex(ValueError, "out-of-project"):
            read_sources(self.root)
        pages["pages"][0]["prd"] = "prd/records.md"
        pages["pages"][0]["status"]["userReviewed"] = True
        self.write_pages(pages)
        with self.assertRaisesRegex(ValueError, "actual user evidence"):
            read_sources(self.root)

    def test_default_generation_does_not_inject(self):
        page = self.root / "index.html"
        from sync_review import BLOCK
        page.write_text(BLOCK.sub("", page.read_text()))
        before = page.read_bytes()
        synchronize(self.root)
        self.assertEqual(before, page.read_bytes())
        synchronize(self.root, check=True)
        with self.assertRaisesRegex(ValueError, "Stale"):
            synchronize(self.root, check=True, inject=True)

    def test_visible_performance_table_preserves_evidence(self):
        decisions = {"schemaVersion": 1, "decisions": [{"id": "PERF-TEST", "kind": "performance", "status": "pending", "question": "Test only", "affectedPages": ["summary"], "performance": {"trigger": "每次提交", "frequency": "每次一次", "impact": "影响响应", "alternative": "缓存", "measurement": "estimated", "evidence": "fixture test assumption; not a measurement", "highCost": True}}]}
        (self.root / "decisions.json").write_text(json.dumps(decisions))
        synchronize(self.root)
        table = (self.root / "_review/performance-review.md").read_text()
        self.assertIn("fixture test assumption; not a measurement", table)
        self.assertIn("pending: 待用户确认", table)
        self.assertIn("尚无用户确认", table)

    def test_invalid_injection_leaves_sources_and_outputs_unchanged(self):
        from sync_review import END
        page = self.root / "index.html"
        page.write_text(page.read_text().replace(END, ""))
        before = page.read_bytes()
        with self.assertRaisesRegex(ValueError, "Unbalanced"):
            synchronize(self.root, inject=True)
        self.assertFalse((self.root / "_review").exists())
        self.assertEqual(before, page.read_bytes())


if __name__ == "__main__":
    unittest.main()
