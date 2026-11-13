"""index_check.py 的測試：每個檢查碼都有「會變紅」與「會變綠」（unittest；pytest 也跑得動）。

  python3 -m unittest discover -s wf/tools -p 'test_*.py'
"""
import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("index_check", os.path.join(HERE, "index_check.py"))
ic = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ic)


def build(root, tree):
    """tree: {名: dict/list/str(json 值) 或 Dir({...}) 或 Raw('文字')}。"""
    for name, val in tree.items():
        p = os.path.join(root, name)
        if isinstance(val, Dir):
            os.makedirs(p, exist_ok=True)
            build(p, val)
        elif isinstance(val, Raw):
            with open(p, "w", encoding="utf-8") as f:
                f.write(val)
        else:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(val, f, ensure_ascii=False, indent=1)


class Dir(dict):
    pass


class Raw(str):
    pass


def idx(*names, **extra):
    d = {n: {"description": "說明 %s" % n} for n in names}
    d.update(extra)
    return d


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        ic.wfnode.clear_cache()

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self, tree, *args):
        build(self.root, tree)
        ic.wfnode.clear_cache()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = ic.main(list(args) + ["--root", self.root, os.path.join(self.root, "wf")])
        text = out.getvalue()
        codes = [ln.split(" ", 1)[0] for ln in text.splitlines() if not ln.startswith("TOTAL")]
        return rc, text, codes

    def red(self, tree, code, *args):
        rc, text, codes = self.run_check(tree, *args)
        self.assertIn(code, codes, text)
        self.assertEqual(rc, 1, text)
        return text

    def green(self, tree, *args):
        rc, text, codes = self.run_check(tree, *args)
        self.assertEqual(rc, 0, text)
        self.assertEqual([c for c in codes if c != "IndexWanted"], [], text)
        self.assertTrue(text.splitlines()[-1].startswith("TOTAL problems=0"), text)
        return text


OK_TREE = {"wf": Dir({"_index.json": idx("a.json", "_description.json"),
                      "_description.json": "wf 是什麼", "a.json": {"_description": "x", "k": "v"}})}


class TestJsonBad(Base):
    def test_red(self):
        t = self.red({"wf": Dir({"bad.json": Raw("{oops")})}, "JsonBad")
        self.assertIn("TOTAL problems=1", t)

    def test_green(self):
        self.green({"wf": Dir({"good.json": {"a": 1}})})


class TestIndexBad(Base):
    def test_green(self):
        self.green(OK_TREE)

    def test_not_object(self):
        self.red({"wf": Dir({"_index.json": ["a.json"], "a.json": {}})}, "IndexBad")

    def test_string_entry(self):
        self.red({"wf": Dir({"_index.json": {"a.json": "說明"}, "a.json": {}})}, "IndexBad")

    def test_missing_or_empty_description(self):
        self.red({"wf": Dir({"_index.json": {"a.json": {"index": "x"}}, "a.json": {}})}, "IndexBad")
        self.red({"wf": Dir({"_index.json": {"a.json": {"description": " "}}, "a.json": {}})}, "IndexBad")

    def test_index_not_string(self):
        self.red({"wf": Dir({"_index.json": {"s": {"description": "d", "index": 3}}, "s": Dir({})})}, "IndexBad")

    def test_index_target_missing(self):
        tree = {"wf": Dir({"_index.json": {"s": {"description": "d", "index": "s/_index.json"}}, "s": Dir({})})}
        self.red(tree, "IndexBad")

    def test_index_target_ok_folder_and_pointer(self):
        sub = Dir({"_index.json": idx("x.json"), "x.json": {}})
        big = {"_index": {"k": {"description": "d"}}, "k": "v"}
        self.green({"wf": Dir({"_index.json": {
            "s": {"description": "d", "index": "s/_index.json"},
            "b.json": {"description": "d", "index": "b.json#/_index"}}, "s": sub, "b.json": big})})

    def test_index_pointer_missing(self):
        tree = {"wf": Dir({"_index.json": {"b.json": {"description": "d", "index": "b.json#/_index"}},
                           "b.json": {"k": "v"}})}
        self.red(tree, "IndexBad")

    def test_index_points_to_non_object(self):
        tree = {"wf": Dir({"_index.json": {"b.json": {"description": "d", "index": "b.json#/k"}},
                           "b.json": {"k": "v"}})}
        self.red(tree, "IndexBad")

    def test_infile_index_bad_shape(self):
        self.red({"wf": Dir({"a.json": {"_index": {"k": "字串"}, "k": "v"}})}, "IndexBad")
        self.red({"wf": Dir({"a.json": {"_index": ["k"], "k": "v"}})}, "IndexBad")

    def test_infile_index_link_string(self):
        # 檔內 `_index` 的相對路徑從裝它的物件算：要先 `..` 走出 a.json 才到隔壁檔
        self.green({"wf": Dir({"a.json": {"_index": "../b.json#/_index", "k": "v"},
                               "b.json": {"_index": {"z": {"description": "d"}}, "z": 1}})})
        self.red({"wf": Dir({"a.json": {"_index": "../b.json#/_index", "k": "v"}, "b.json": {"z": 1}})}, "IndexBad")
        self.red({"wf": Dir({"a.json": {"_index": "b.json#/_index", "k": "v"},
                             "b.json": {"_index": {"z": {"description": "d"}}, "z": 1}})}, "IndexBad")


class TestIndexMissing(Base):
    def test_red(self):
        self.red({"wf": Dir({"_index.json": idx("a.json", "gone.json"), "a.json": {}})}, "IndexMissing")

    def test_green_with_pointer_key(self):
        self.green({"wf": Dir({"_index.json": idx("a.json", "a.json#/k"), "a.json": {"k": "v"}})})

    def test_red_pointer_key(self):
        self.red({"wf": Dir({"_index.json": idx("a.json", "a.json#/nope"), "a.json": {"k": "v"}})}, "IndexMissing")

    def test_infile(self):
        self.red({"wf": Dir({"a.json": {"_index": idx("k", "gone"), "k": "v"}})}, "IndexMissing")
        self.green({"wf": Dir({"a.json": {"_index": idx("k"), "k": "v"}})})


class TestIndexUnlisted(Base):
    def test_red(self):
        t = self.red({"wf": Dir({"_index.json": idx("a.json"), "a.json": {}, "b.md": Raw("x"),
                                 "sub": Dir({})})}, "IndexUnlisted")
        self.assertIn("b.md", t)
        self.assertIn("sub", t)

    def test_green_ignores(self):
        self.green({"wf": Dir({"_index.json": idx("a.json"), "a.json": {}, ".hidden": Raw("x"),
                               "__pycache__": Dir({}), "_index.local.json": {"a.json": {"description": "私"}}})})

    def test_no_index_no_check(self):
        self.green({"wf": Dir({"a.json": {}, "b.md": Raw("x")})})

    def test_infile_only_strict(self):
        tree = {"wf": Dir({"a.json": {"_index": idx("k"), "k": "v", "extra": "w", "_description": "d"}})}
        self.green(tree)
        t = self.red(tree, "IndexUnlisted", "--strict")
        self.assertIn("extra", t)
        self.assertNotIn("_description 沒列", t)


class TestIndexWanted(Base):
    def many(self, n):
        return {"wf": Dir({"f%02d.md" % i: Raw("x") for i in range(n)})}

    def test_folder_warning_not_counted(self):
        rc, text, codes = self.run_check(self.many(16))
        self.assertEqual(rc, 0, text)
        self.assertIn("IndexWanted", codes)
        self.assertIn("(warning)", text)
        self.assertIn("TOTAL problems=0 warnings=1", text)

    def test_folder_strict_red(self):
        self.red(self.many(16), "IndexWanted", "--strict")

    def test_folder_green(self):
        self.green(self.many(15), "--strict")

    def test_file_big_or_many_keys(self):
        self.red({"wf": Dir({"a.json": {"k": "x" * 8100}})}, "IndexWanted", "--strict")
        self.red({"wf": Dir({"a.json": {"k%d" % i: 1 for i in range(11)}})}, "IndexWanted", "--strict")

    def test_file_green(self):
        self.green({"wf": Dir({"a.json": dict({"k%d" % i: 1 for i in range(10)}, _description="d")})}, "--strict")
        keys = {"k%d" % i: 1 for i in range(11)}
        self.green({"wf": Dir({"a.json": dict(keys, _index=idx(*keys))})}, "--strict")


class TestRefBad(Base):
    def tree(self, text, **more):
        d = {"a.json": {"k": text}, "b.json": {"sec": {"x/y": 1, "t~": 2}}, "c.md": Raw("x")}
        d.update((k if isinstance(v, Dir) else k + ".json", v) for k, v in more.items())
        return {"wf": Dir(d)}

    def test_red_missing_file(self):
        t = self.red(self.tree("見 `wf/nope.json`"), "RefBad")
        self.assertIn("wf/nope.json", t)

    def test_red_bad_pointer(self):
        self.red(self.tree("見 `wf/b.json#/sec/zzz`"), "RefBad")

    def test_green_paths_and_pointers(self):
        self.green(self.tree("見 `wf/b.json#/sec/x~1y`、`wf/b.json#/sec/t~0`、`wf/c.md` 與 `wf/b.json`"))

    def test_skips_examples_and_fences(self):
        self.green(self.tree("例 `wf/<name>.json`、`wf/*.md`、`wf/{x}.json`、`wf/a….json`、`../x.json`、`nope.json`\n"
                             "```\n`wf/nope.json`\n```"))

    def test_no_refs(self):
        self.green(self.tree("見 `wf/nope.json`", d={"$ref": "gone.json"}), "--no-refs")

    def test_ref_object(self):
        self.red(self.tree("x", d={"sec": {"$ref": "gone.json"}}), "RefBad")
        self.red(self.tree("x", d={"sec": {"$ref": "b.json#/nope"}}), "RefBad")
        self.green(self.tree("x", d={"s1": {"$ref": "b.json#/sec"}, "s2": {"$ref": "#/s1"},
                                     "s3": {"$ref": "sub/e.json"}, "s4": {"$ref": "#/../b.json#/sec"}},
                             sub=Dir({"e.json": {"z": {"$ref": "../b.json"}}})))

    def test_ref_in_list_and_index_desc(self):
        t = self.red(self.tree("x", d=[{"$ref": "gone.json"}]), "RefBad")
        self.assertIn("d.json", t)


class TestCli(Base):
    def test_json_output(self):
        build(self.root, {"wf": Dir({"bad.json": Raw("{")})})
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = ic.main(["--json", os.path.join(self.root, "wf")])
        self.assertEqual(rc, 1)
        self.assertEqual(json.loads(out.getvalue())["problems"][0]["code"], "JsonBad")

    def test_bad_arg(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(ic.main(["--nope"]), 2)


if __name__ == "__main__":
    unittest.main()
