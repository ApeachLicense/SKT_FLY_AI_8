"""Regression checks for staged leaks and credentials deleted from later commits."""
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import unittest

SCANNER = Path(__file__).resolve().parents[1] / "scripts/check_secrets.py"


class SecretProtectionTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.repo = Path(self.workspace.name)
        self.git("init", "--quiet")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "core.hooksPath", str(self.repo / "unused-hooks"))

    def tearDown(self):
        self.workspace.cleanup()

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    def scan(self, mode):
        return subprocess.run([sys.executable, str(SCANNER), mode, "--repo", str(self.repo)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_staged_key_is_blocked_without_printing_value(self):
        value = "sk-" + "proj-" + secrets.token_hex(32)
        (self.repo / "example.py").write_text("key = '" + value + "'\n", encoding="utf-8")
        self.git("add", ".")
        result = self.scan("--staged")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(value.encode(), result.stdout + result.stderr)
        self.assertIn(b"example.py:1", result.stderr)

    def test_deleted_key_is_still_detected_in_history(self):
        value = "pplx-" + secrets.token_hex(24)
        path = self.repo / "example.py"
        path.write_text("key = '" + value + "'\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Initial")
        path.write_text("# Credential removed\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Remove credential")
        self.assertEqual(self.scan("--staged").returncode, 0)
        result = self.scan("--history")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(value.encode(), result.stdout + result.stderr)

    def test_failed_git_inspection_blocks_instead_of_passing(self):
        self.git("config", "--unset", "user.name")
        result = subprocess.run([sys.executable, str(SCANNER), "--staged", "--repo", str(self.repo / "missing")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
