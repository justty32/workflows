"""index_check.py 的測試（續）：RefBad 的第一段規則、指標跟 `$ref`、忽略表——各有會紅與會綠。

  python3 -m unittest discover -s wf/tools -p 'test_*.py'
"""
import contextlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_index_check import Base, Dir, Raw, build  # noqa: E402


class TestRefScope(Base):
    def tree(self, text, **more):
        d = {"a.json": {"k": text}}
        d.update((k if isinstance(v, Dir) else k + ".json", v) for k, v in more.items())
        return {"wf": Dir(d)}

    def test_first_segment_must_exist(self):
        # 第一段不在 repo 根（外部 repo、合併後路徑、範例）→ 不驗
        self.green(self.tree("上游的 `references/x.md`、合併後的 `workflows/common/c.md`、例 `rel/path.md`"))
        # 第一段存在 → 照驗：會紅
        build(self.root, {"skills": Dir({"own.md": Raw("x")})})
        self.red(self.tree("見 `skills/caveman/SKILL.md`"), "RefBad")
        self.green(self.tree("見 `skills/own.md`"))

    def test_pointer_follows_ref(self):
        sub = Dir({"e.json": {"_description": "子", "sec": [{"k": 1}]}})
        main = {"top": {"$ref": "sub/e.json#/sec"}, "whole": {"$ref": "sub/e.json"}}
        self.green(self.tree("見 `wf/m.json#/top/0/k`、`wf/m.json#/whole/sec`、`wf/m.json#/top`",
                             m=main, sub=sub))
        self.red(self.tree("見 `wf/m.json#/top/5`", m=main, sub=sub), "RefBad")
        self.red(self.tree("見 `wf/m.json#/whole/nope`", m=main, sub=sub), "RefBad")

    def write_ignore(self, *lines):
        p = os.path.join(self.root, "ign.tsv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return "--ignore=" + p

    def test_ignore_file(self):
        build(self.root, {"skills": Dir({})})
        text = "上游的 `skills/caveman/SKILL.md`"
        self.red(self.tree(text), "RefBad", self.write_ignore("# 註解", "wf/a.json#/other\tskills/caveman/SKILL.md"))
        self.green(self.tree(text), self.write_ignore("# 上游", "", "wf/a.json#/k\tskills/caveman/SKILL.md"))
        self.green(self.tree(text), self.write_ignore("wf/a.json\tskills/caveman/SKILL.md"))  # 整檔
        # 忽略表只壓 RefBad 指名的字串，同位置別的壞引用照報
        self.red(self.tree(text + " `wf/nope.json`"), "RefBad",
                 self.write_ignore("wf/a.json#/k\tskills/caveman/SKILL.md"))

    def test_ignore_unused_and_bad_format(self):
        rc, t, _ = self.run_check(self.tree("x"), self.write_ignore("wf/a.json#/k\tskills/x.md"))
        self.assertEqual(rc, 0, t)
        self.assertIn("IgnoreUnused wf/a.json#/k", t)
        self.assertIn("warnings=1", t)
        self.assertNotIn("IgnoreUnused", self.green(self.tree("x"), self.write_ignore("other/z.json\tskills/x.md")))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc, _, _ = self.run_check(self.tree("x"), self.write_ignore("沒有 tab 的一行"))
        self.assertEqual(rc, 2)

    def test_default_ignore_location(self):
        build(self.root, {"skills": Dir({}), "wf": Dir({"tools": Dir({
            "index_check.ignore": Raw("wf/a.json#/k\tskills/caveman/SKILL.md\n")})})})
        self.green(self.tree("上游的 `skills/caveman/SKILL.md`"))



if __name__ == "__main__":
    unittest.main()
