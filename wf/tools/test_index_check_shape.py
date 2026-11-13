"""index_check.py 的測試（續二）：IndexWanted 門檻，與「一段文字＝字串或字串陣列」的形狀規則——各有會紅與會綠。

  python3 -m unittest discover -s wf/tools -p 'test_*.py'
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_index_check import Base, Dir, Raw, idx  # noqa: E402


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


class TestTextShapes(Base):
    def test_description_array_ok(self):
        # 檔內 `_description` 與資料夾 `_description.json` 都可以是字串陣列（一行一個元素）
        self.green({"wf": Dir({"_index.json": idx("a.json", "_description.json"),
                               "_description.json": ["# wf", "", "正文第二段"],
                               "a.json": {"_description": ["第一行", "- 清單"], "k": ["x", "", "y"]}})})

    def test_description_bad_shape(self):
        self.red({"wf": Dir({"a.json": {"_description": {"x": 1}}})}, "IndexBad")
        self.red({"wf": Dir({"a.json": {"_description": ["行", 3]}})}, "IndexBad")

    def test_folder_description_bad_shape(self):
        t = self.red({"wf": Dir({"_index.json": idx("_description.json"), "_description.json": 3})}, "IndexBad")
        self.assertIn("_description.json: 資料夾的", t)

    def test_index_description_must_stay_string(self):
        t = self.red({"wf": Dir({"_index.json": {"a.json": {"description": ["一句", "兩句"]}}, "a.json": {}})},
                     "IndexBad")
        self.assertIn("index 的 description 目前要維持一句字串", t)
        self.red({"wf": Dir({"a.json": {"_index": {"k": {"description": ["一", "二"]}}, "k": "v"}})}, "IndexBad")

    def test_extra_entry_keys_ok(self):
        self.green({"wf": Dir({"_index.json": {"a.json": {"description": "d", "source": "kernel", "title": "A"}},
                               "a.json": {}})}, "--strict")

    def test_refs_inside_string_arrays(self):
        tree = lambda lines: {"wf": Dir({"a.json": {"k": lines}, "c.md": Raw("x")})}  # noqa: E731
        t = self.red(tree(["第一行", "", "見 `wf/nope.json`"]), "RefBad")
        self.assertIn("a.json#/k/2", t)
        self.green(tree(["見 `wf/c.md`", "", "- `wf/a.json#/k`"]))
        # 跨元素的圍籬裡不驗；只有一個 ``` 開頭的元素不算圍籬（照驗）
        self.green(tree(["前文", "```bash", "cat `wf/nope.json`", "```", "後文 `wf/c.md`"]))
        self.red(tree(["```markdown 圍籬內可能放壞連結", "見 `wf/nope.json`"]), "RefBad")


if __name__ == "__main__":
    unittest.main()
