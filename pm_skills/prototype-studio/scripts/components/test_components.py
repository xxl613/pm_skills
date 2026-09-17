#!/usr/bin/env python3
"""Behavioral tests of registration, reuse and failed integrity checks."""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from install_standard import install
from register_standard import register
from standard_lib import check_package

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/check"))
from check_standard import check_project


class StandardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        shutil.copytree(ROOT / "examples/component-reuse/source", self.source)
        self.definition = ROOT / "examples/component-reuse/definition.json"
        self.registry = self.root / "registry"

    def tearDown(self):
        self.temp.cleanup()

    def new_pack(self):
        result = register(self.source, self.definition, self.registry)
        self.assertTrue(result["ok"])
        return Path(result["package"])

    def test_register_and_reuse_on_two_pages(self):
        pack = self.new_pack()
        project = self.root / "project"
        project.mkdir()
        for page in ("first.html", "second.html"):
            (project / page).write_text('<h1>Host</h1><!-- STANDARD-MOUNT:note -->')
            install(pack, project, page=page, scope="note", entry="index.html")
        result = check_project(project)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["usages"], 2)
        self.assertEqual(len(list((project / "standards/resource-note").iterdir())), 1)

    def test_same_version_cannot_overwrite(self):
        self.new_pack()
        with self.assertRaisesRegex(ValueError, "already exists"):
            register(self.source, self.definition, self.registry)

    def test_missing_resource_rejected_before_copy(self):
        (self.source / "card.css").unlink()
        with self.assertRaisesRegex(ValueError, "missing reference"):
            register(self.source, self.definition, self.registry)
        self.assertFalse(self.registry.exists())

    def test_hash_drift_detected(self):
        pack = self.new_pack()
        (pack / "card.js").write_text("changed")
        self.assertFalse(check_package(pack)["ok"])
        with self.assertRaisesRegex(ValueError, "failed checks"):
            install(pack, self.root / "project")

    def test_mount_drift_detected(self):
        pack = self.new_pack()
        project = self.root / "project"
        project.mkdir()
        page = project / "first.html"
        page.write_text("<!-- STANDARD-MOUNT:note -->")
        install(pack, project, page="first.html", scope="note", entry="index.html")
        page.write_text(page.read_text().replace('id="note"', 'id="wrong"'))
        self.assertFalse(check_project(project)["ok"])

    def test_no_marker_never_mutates_page(self):
        pack = self.new_pack()
        project = self.root / "project"
        project.mkdir()
        page = project / "first.html"
        page.write_text("<h1>unchanged</h1>")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            install(pack, project, page="first.html", scope="note", entry="index.html")
        self.assertEqual(page.read_text(), "<h1>unchanged</h1>")
        self.assertFalse((project / "standards").exists())

    def test_missing_specification_rejected_before_copy(self):
        definition = json.loads(self.definition.read_text())
        definition["specification"] = {"entry": "references/rules.md", "files": ["references/rules.md"]}
        path = self.root / "definition.json"
        path.write_text(json.dumps(definition))
        with self.assertRaisesRegex(ValueError, "missing specification"):
            register(self.source, path, self.registry)
        self.assertFalse(self.registry.exists())

    def test_specification_travels_with_pinned_package(self):
        (self.source / "references").mkdir()
        rules = self.source / "references/rules.md"
        rules.write_text("# Rule\nExpand toggles one details region.\n")
        definition = json.loads(self.definition.read_text())
        definition["specification"] = {"entry": "references/rules.md", "files": ["references/rules.md"]}
        path = self.root / "definition.json"
        path.write_text(json.dumps(definition))
        pack = Path(register(self.source, path, self.registry)["package"])
        self.assertTrue(check_package(pack)["ok"])
        project = self.root / "project"
        install(pack, project)
        self.assertEqual((project / "standards/resource-note/1.0.0/references/rules.md").read_text(), rules.read_text())

    def test_symlink_rejected(self):
        (self.source / "outside.css").symlink_to(self.definition)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            register(self.source, self.definition, self.registry)


if __name__ == "__main__":
    unittest.main(verbosity=2)
