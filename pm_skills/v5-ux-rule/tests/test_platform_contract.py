import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(os.environ.get("V5_SKILL_ROOT", Path(__file__).resolve().parents[1]))


class PlatformContractTests(unittest.TestCase):
    def test_routing_contract_is_autonomous_and_evidence_based(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        skill = skill.split("## 平台判定", 1)[1].split("## 项目档案", 1)[0]
        required_in_order = [
            "用户明确指定",
            "页面规划文档",
            "v5-profile.md",
            "来源证据",
            "业务承载方式",
            "只有证据冲突",
        ]
        positions = [skill.find(item) for item in required_in_order]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions), positions)

    def test_platform_references_and_checker_exist(self):
        required = [
            "references/08-platform-routing.md",
            "references/09-mobile-ui.md",
            "scripts/check-platform.py",
            "assets/components-mobile/mobile-ui.css",
        ]
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_complete_mobile_examples_exist(self):
        required = [
            "mobile-portal.html",
            "mobile-chat.html",
            "mobile-composer.html",
            "mobile-task.html",
            "mobile-thinking.html",
            "mobile-agent-skill.html",
            "mobile-feedback.html",
            "mobile-file.html",
            "mobile-followup.html",
            "mobile-history.html",
        ]
        folder = ROOT / "assets/examples-mobile"
        for name in required:
            page = folder / name
            self.assertTrue(page.is_file(), name)
            html = page.read_text(encoding="utf-8")
            self.assertIn("v5m-screen", html, name)
            self.assertNotIn("v5-nav", html, name)
            self.assertNotIn("v5-drawer", html, name)
            self.assertNotIn("_viewport-fit.js", html, name)

    def test_desktop_examples_do_not_use_mobile_shell(self):
        folder = ROOT / "assets/examples"
        for page in folder.glob("*.html"):
            html = page.read_text(encoding="utf-8")
            self.assertNotIn("v5m-screen", html, page.name)

    def test_checker_accepts_valid_pages_and_rejects_cross_platform_mix(self):
        checker = ROOT / "scripts/check-platform.py"
        self.assertTrue(checker.is_file())
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            valid_mobile = tmp_path / "valid-mobile.html"
            valid_mobile.write_text(
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<main class="v5m-screen"></main>',
                encoding="utf-8",
            )
            invalid_mobile = tmp_path / "invalid-mobile.html"
            invalid_mobile.write_text(
                '<main class="v5m-screen v5-nav"></main>', encoding="utf-8"
            )
            valid_desktop = tmp_path / "valid-desktop.html"
            valid_desktop.write_text(
                '<main class="v5-app"></main><script src="_viewport-fit.js"></script>',
                encoding="utf-8",
            )
            invalid_desktop = tmp_path / "invalid-desktop.html"
            invalid_desktop.write_text(
                '<main class="v5-app v5m-safe"></main>', encoding="utf-8"
            )

            good = subprocess.run(
                [
                    sys.executable,
                    str(checker),
                    "--mobile",
                    str(valid_mobile),
                    "--desktop",
                    str(valid_desktop),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)

            bad_mobile = subprocess.run(
                [sys.executable, str(checker), "--mobile", str(invalid_mobile)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(bad_mobile.returncode, 0)
            self.assertIn("v5-nav", bad_mobile.stdout + bad_mobile.stderr)

            bad_desktop = subprocess.run(
                [sys.executable, str(checker), "--desktop", str(invalid_desktop)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(bad_desktop.returncode, 0)
            self.assertIn("v5m-safe", bad_desktop.stdout + bad_desktop.stderr)


if __name__ == "__main__":
    unittest.main()
