import os
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, "wf-lint.sh")


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    return p


def run(root, *args):
    return subprocess.run(
        ["bash", LINT, *args, root],
        capture_output=True, text=True,
    )


class QueryCmdTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name

    def tearDown(self):
        self.d.cleanup()

    def test_command_line_form_is_reported(self):
        write(self.root, "notes/a.md",
              "# a\n\n已抽到 x.json（3 列）。怎麼查：\n\n```\n"
              "python3 ../wf/tools/tabledb.py x.json\n```\n")
        r = run(self.root)
        self.assertIn("QUERYCMD notes/a.md:6", r.stdout)
        self.assertIn("querycmd=1", r.stdout)

    def test_bare_tool_path_without_python3_is_reported(self):
        write(self.root, "notes/b.md", "# b\n\n- `wf/tools/tabledb.py logs/x.json get 0`\n")
        r = run(self.root)
        self.assertIn("QUERYCMD notes/b.md:3", r.stdout)
        self.assertIn("querycmd=1", r.stdout)

    def test_bare_tool_name_is_not_reported(self):
        write(self.root, "notes/c.md", "# c\n\n讀寫走 `tabledb.py`，不整份讀進 context。\n")
        r = run(self.root)
        self.assertNotIn("QUERYCMD", r.stdout)
        self.assertIn("querycmd=0", r.stdout)

    def test_exempt_paths_and_files(self):
        cmd = "python3 tools/tabledb.py x.json get 0\n"
        write(self.root, "wf/workflows/common/x.md", cmd)
        write(self.root, "archive/old.md", cmd)
        write(self.root, "AGENTS.md", cmd)
        write(self.root, "notes/AGENTS.md", cmd)
        write(self.root, "workflows/common/data-files.md", cmd)
        write(self.root, "workflows/common/data-files-fmt.md", cmd)
        write(self.root, "workflows/tidy.md", cmd)
        r = run(self.root)
        self.assertNotIn("QUERYCMD", r.stdout)
        self.assertIn("querycmd=0", r.stdout)

    def test_strict_fails_plain_warns(self):
        write(self.root, "notes/a.md", "# a\n\npython3 wf/tools/tabledb.py x.json\n")
        self.assertEqual(run(self.root).returncode, 0)
        r = run(self.root, "--strict")
        self.assertEqual(r.returncode, 1)
        self.assertIn("querycmd=1", r.stdout.splitlines()[-1])

    def test_multiple_hits_counted_per_line(self):
        write(self.root, "notes/a.md",
              "# a\n\n```\npython3 tools/tabledb.py x.json\n"
              "python3 tools/tabledb.py x.json get 0\n"
              "python3 tools/tabledb.py x.json find id=1\n```\n")
        r = run(self.root)
        self.assertIn("querycmd=3", r.stdout)


if __name__ == "__main__":
    unittest.main()
