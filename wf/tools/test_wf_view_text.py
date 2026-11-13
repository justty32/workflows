"""wf-view.py 的測試（續）：字串陣列的兩種用法（清單／拆成行的一段文字）與命令列。

  python3 -m unittest discover -s wf/tools -p 'test_*.py'
"""
import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wf_view_render  # noqa: E402
from test_wf_view import HERE, Base, put  # noqa: E402


class TestTextArrays(Base):
    def setUp(self):
        Base.setUp(self)
        put(self.p("k", "t.json"), {
            "_description": ["# 標題", "", "正文。"],
            "steps": ["第一步", "第二步"],
            "body": ["前言：", "", "- 規則一", "- 規則二"],
            "code": ["說明", "```bash", "echo hi", "```"],
            "starts_fence": ["```markdown 圍籬內放壞連結", "另一條"],
            "notes": ["一條", ["拆成行的：", "  1. 子項"]],
            "rows": [{"date": "d", "note": ["a", "", "b"], "tags": ["x", "y"]}]})
        put(self.p("wf", "_description.json"), ["# wf", "", "資料夾正文。"])

    def test_lines_print_as_markdown(self):
        out = self.ok(self.p("k", "t.json"))
        self.assertTrue(out.split("\n", 2)[2].startswith("# 標題\n\n正文。"), out)
        self.assertIn("前言：\n\n- 規則一\n- 規則二", out)
        self.assertIn("說明\n```bash\necho hi\n```", out)
        self.assertNotIn("1. 前言", out)

    def test_plain_lists_stay_numbered(self):
        out = self.ok(self.p("k", "t.json"))
        self.assertIn("1. 第一步\n2. 第二步", out)
        self.assertIn("1. ```markdown 圍籬內放壞連結\n2. 另一條", out)  # 只有一個 ``` 不算圍籬
        self.assertIn("1. 一條\n2. 拆成行的：\n     1. 子項", out)   # 元素本身是行陣列：接回去

    def test_table_cells_and_folder(self):
        out = self.ok(self.p("k", "t.json"))
        self.assertIn('| d | a<br><br>b | ["x", "y"] |', out)
        self.assertIn("# wf\n\n資料夾正文。", self.ok(self.p("wf")))

    def test_looks_like_lines(self):
        r = wf_view_render
        self.assertTrue(r.looks_like_lines(["a", ""]))
        self.assertTrue(r.looks_like_lines(["a", "3. b"]))
        self.assertFalse(r.looks_like_lines(["a", "b"]))
        self.assertFalse(r.looks_like_lines([]))
        self.assertFalse(r.looks_like_lines(["a", 1]))


class TestCli(Base):
    setUp = TestTextArrays.setUp

    def test_cli_subprocess(self):
        r = subprocess.run([sys.executable, os.path.join(HERE, "wf-view.py"), self.p("k", "t.json") + "#/steps"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("1. 第一步", r.stdout)
        r = subprocess.run([sys.executable, os.path.join(HERE, "wf-view.py")],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
