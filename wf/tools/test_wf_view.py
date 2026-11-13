"""wf-view.py 的測試（unittest；pytest 也跑得動）。檔名有連字號，用 importlib 載入。

  python3 -m unittest discover -s wf/tools -p 'test_*.py'
"""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("wf_view", os.path.join(HERE, "wf-view.py"))
wv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(wv)


def put(path, val):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(val, str) and not path.endswith(".json"):
            f.write(val)
        else:
            json.dump(val, f, ensure_ascii=False, indent=1)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        wv.wfnode.clear_cache()

    def tearDown(self):
        self.tmp.cleanup()

    def p(self, *parts):
        return os.path.join(self.d, *parts)

    def view(self, *args):
        wv.wfnode.clear_cache()
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = wv.main(list(args))
        return rc, out.getvalue(), err.getvalue()

    def ok(self, *args):
        rc, out, err = self.view(*args)
        self.assertEqual(rc, 0, err)
        return out


class TestFolder(Base):
    def setUp(self):
        Base.setUp(self)
        put(self.p("wf", "_description.json"), "# wf\n\n這是 wf 的正文。")
        put(self.p("wf", "_index.json"), {
            "_description.json": {"description": "正文"},
            "a.json": {"description": "A 檔｜含直線"},
            "sub": {"description": "子夾", "index": "sub/_index.json"}})
        put(self.p("wf", "a.json"), {"_description": "A"})
        put(self.p("wf", "sub", "_index.json"), {"x.json": {"description": "X 檔"}})
        put(self.p("wf", "sub", "x.json"), {})
        put(self.p("wf", "sub", "deep", "y.md"), "y")

    def test_index_table(self):
        out = self.ok(self.p("wf"))
        lines = out.splitlines()
        self.assertTrue(lines[0].startswith("# ") and lines[0].endswith("wf/"), out)
        self.assertLess(out.index("這是 wf 的正文"), out.index("| 名字 | 說明 | index |"))
        self.assertIn("| sub | 子夾 | sub/_index.json |", out)
        self.assertIn("| a.json | A 檔｜含直線 |  |", out)
        self.assertNotIn("X 檔", out)  # 沒 --tree 不往下

    def test_tree(self):
        out = self.ok("--tree", self.p("wf"))
        self.assertIn("## " + self.p("wf", "sub") + "/", out)
        self.assertIn("| x.json | X 檔 |  |", out)
        self.assertIn("### " + self.p("wf", "sub", "deep") + "/", out)
        self.assertIn("- y.md", out)  # 沒 index 的夾列目錄內容

    def test_no_index_lists_dir(self):
        out = self.ok(self.p("wf", "sub", "deep"))
        self.assertIn("- y.md", out)
        self.assertNotIn("| 名字", out)

    def test_overlay(self):
        put(self.p("wf", "_index.local.json"), {"a.json": {"description": "我自己的看法"},
                                                "new.json": {"description": "只在私有"}})
        out = self.ok("--overlay", self.p("wf", "_index.local.json"), self.p("wf"))
        self.assertIn("| a.json (私有) | 我自己的看法 |  |", out)
        self.assertNotIn("A 檔", out)
        self.assertIn("| new.json (私有) | 只在私有 |  |", out)
        self.assertIn("| sub | 子夾 | sub/_index.json |", out)
        self.assertLess(out.index("sub | 子夾"), out.index("new.json"))  # 私有獨有的接在後面

    def test_overlay_missing(self):
        rc, out, err = self.view("--overlay", self.p("nope.json"), self.p("wf"))
        self.assertEqual(rc, 1)
        self.assertIn("wf-view: error: PathMissing", err)


class TestFile(Base):
    def setUp(self):
        Base.setUp(self)
        put(self.p("k", "dec.json"), {
            "_description": "決策記錄。",
            "_index": {"records": {"description": "不該印出來"}},
            "records": [{"date": "2026-09-02", "decision": "用 json"},
                        {"date": "2026-09-03", "premise": "多行\n第二行", "decision": "a|b"}],
            "steps": ["第一步", "第二步\n補充"],
            "rules": "- 規則一\n- 規則二",
            "nested": {"inner": {"leaf": "葉子"}, "n": 3},
            "a/b": {"c": "斜線鍵"},
            "far": {"$ref": "other.json#/sec"},
            "same": {"$ref": "#/rules"}})
        put(self.p("k", "other.json"), {"sec": {"_description": "別檔的段落", "body": "內文"}})

    def test_description_first_and_strings(self):
        out = self.ok(self.p("k", "dec.json"))
        body = out.split("\n", 2)[2]
        self.assertTrue(body.startswith("決策記錄。"), out)
        self.assertIn("- 規則一\n- 規則二", out)  # \n 展開、原樣印
        self.assertNotIn("不該印出來", out)

    def test_records_table(self):
        out = self.ok(self.p("k", "dec.json"))
        self.assertIn("## records", out)
        self.assertIn("| date | decision | premise |", out)  # 欄位聯集、照首次出現
        self.assertIn("| 2026-09-02 | 用 json |  |", out)
        self.assertIn("| 2026-09-03 | a\\|b | 多行<br>第二行 |", out)

    def test_string_list_and_nested(self):
        out = self.ok(self.p("k", "dec.json"))
        self.assertIn("1. 第一步\n2. 第二步\n   補充", out)
        self.assertIn("## nested", out)
        self.assertIn("### inner", out)
        self.assertIn("#### leaf", out)

    def test_pointer(self):
        out = self.ok(self.p("k", "dec.json") + "#/nested/inner")
        self.assertIn("## leaf", out)
        self.assertNotIn("records", out)
        out = self.ok(self.p("k", "dec.json") + "#/a~1b/c")
        self.assertIn("斜線鍵", out)
        out = self.ok(self.p("k", "dec.json") + "#/records/1")
        self.assertIn("a|b", out)

    def test_ref_not_followed(self):
        out = self.ok(self.p("k", "dec.json"))
        self.assertIn("→ `other.json#/sec`", out)
        self.assertIn("→ `#/rules`", out)
        self.assertNotIn("別檔的段落", out)

    def test_ref_followed(self):
        out = self.ok("--follow", self.p("k", "dec.json"))
        self.assertIn("別檔的段落", out)
        self.assertIn("### body", out)
        self.assertNotIn("→ `other.json", out)
        self.assertEqual(out.count("- 規則一"), 2)  # 同檔 $ref 也展開

    def test_ref_follow_broken(self):
        put(self.p("k", "bad.json"), {"x": {"$ref": "gone.json"}})
        self.assertIn("→ `gone.json`", self.ok(self.p("k", "bad.json")))
        rc, out, err = self.view("--follow", self.p("k", "bad.json"))
        self.assertEqual(rc, 1)
        self.assertIn("PathMissing", err)

    def test_path_missing(self):
        for arg in (self.p("k", "nope.json"), self.p("k", "dec.json") + "#/nope",
                    self.p("k", "dec.json") + "#/records/9"):
            rc, out, err = self.view(arg)
            self.assertEqual(rc, 1, arg)
            self.assertTrue(err.startswith("wf-view: error: PathMissing "), err)
            self.assertEqual(out, "")

    def test_json_bad(self):
        put(self.p("k", "broken.json"), "x")
        with open(self.p("k", "broken.json"), "w") as f:
            f.write("{")
        rc, out, err = self.view(self.p("k", "broken.json"))
        self.assertEqual(rc, 1)
        self.assertIn("JsonBad", err)

    def test_cli_subprocess(self):
        r = subprocess.run([sys.executable, os.path.join(HERE, "wf-view.py"), self.p("k", "dec.json") + "#/steps"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("1. 第一步", r.stdout)
        r = subprocess.run([sys.executable, os.path.join(HERE, "wf-view.py")],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
