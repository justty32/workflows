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


class LinkScopeAndCountTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name

    def tearDown(self):
        self.d.cleanup()

    def test_broken_count_does_not_overflow_exit_status(self):
        for index in range(300):
            write(self.root, f"docs/{index}.md", "[missing](nowhere.md)\n")
        r = run(self.root)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.count("BROKEN "), 300)
        self.assertIn("TOTAL broken=300", r.stdout)

    def test_markdown_scope_excludes_archive_reference_vendor_and_submodules(self):
        write(self.root, "README.md", "[missing](nowhere.md)\n")
        excluded_noise = (
            "[missing](missing.md)\n\n"
            "python3 tools/tabledb.py data.json\n\n"
            "{{placeholder}}\n\n"
            + "".join(f"- row {index}: {'x' * 40}\n" for index in range(30))
        )
        write(self.root, "archive/old.md", excluded_noise)
        write(self.root, "reference/target.md", "# present\n")
        write(self.root, "reference/source.md", excluded_noise + "[anchor](target.md#absent)\n")
        write(self.root, "vendor/package.md", "[vendor](missing.md)\n")
        write(self.root, "components/arbitrary-child/child.md", "[child](missing.md)\n")
        write(
            self.root,
            ".gitmodules",
            '[submodule "not-a-hard-coded-name"]\n'
            "\tpath = components/arbitrary-child\n"
            "\turl = https://example.invalid/child.git\n",
        )
        r = run(self.root)
        self.assertEqual(r.stdout.count("BROKEN "), 1)
        self.assertIn("BROKEN README.md -> nowhere.md", r.stdout)
        self.assertIn("TOTAL broken=1", r.stdout)
        self.assertNotIn("archive/old.md", r.stdout)
        self.assertNotIn("reference/source.md", r.stdout)
        self.assertNotIn("vendor/package.md", r.stdout)
        self.assertNotIn("arbitrary-child/child.md", r.stdout)
        self.assertIn("biglist=0", r.stdout)
        self.assertIn("querycmd=0", r.stdout)
        self.assertIn("residue={{=0", r.stdout)


if __name__ == "__main__":
    unittest.main()
