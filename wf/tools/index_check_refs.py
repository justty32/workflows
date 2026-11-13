"""index_check 的引用那半：RefBad（反引號路徑、反引號裡 `#/` 開頭的同檔指標、`$ref`）與忽略表（IgnoreUnused）。

由 index_check_tree.Checker 混入；規則說明見 index_check.py 檔頭。
字串陣列（一段多行文字拆成一行一個元素）逐個元素掃；``` 圍籬跨元素時，圍籬內的元素不驗。
"""
import os
import re

import wfnode

REF_RE = re.compile(r"^[\w./-]+\.(json|md|py|sh|tsv|csv|yml)(#/[^`\s]*)?$")
LOCAL_RE = re.compile(r"^#/[^`\s]*$")
TICK_RE = re.compile(r"`([^`\n]+)`")
FENCE_RE = re.compile(r"```.*?(```|\Z)", re.S)
NO_CHECK = set("<>*…{")


def fence_flags(items):
    """字串陣列 → 每個元素是不是圍籬行或圍籬內（是就不驗）。非字串元素一律 False。
    只有一個元素以 ``` 開頭時不當圍籬（是清單裡剛好這樣起頭的一條，同 wf_view_render.looks_like_lines）。"""
    def fence(v):
        return isinstance(v, str) and v.lstrip().startswith("```")
    if sum(1 for v in items if fence(v)) < 2:
        return [False] * len(items)
    inside, out = False, []
    for v in items:
        if fence(v):
            inside = not inside
            out.append(True)
        else:
            out.append(inside and isinstance(v, str))
    return out


class RefChecks:
    def check_ref(self, path, keys, obj):
        ref = obj["$ref"]
        where = wfnode.fmt_loc((path, keys))
        if not isinstance(ref, str):
            self.add("RefBad", where, "$ref 要是字串")
            return
        try:
            wfnode.follow_ref((path, keys), obj)
        except wfnode.NodeError as e:
            self.add("RefBad", where, "$ref %s 指不到（%s）" % (ref, e.msg))

    def check_ticks(self, path, keys, text):
        if "`" not in text:
            return
        for m in TICK_RE.finditer(FENCE_RE.sub("", text)):
            cand = m.group(1).strip()
            if LOCAL_RE.match(cand):
                self.check_local(path, keys, cand)
                continue
            if (NO_CHECK & set(cand) or not REF_RE.match(cand) or cand.startswith(("./", "../"))
                    or "/" not in cand.split("#", 1)[0]):
                continue  # 範例／樣式／相對路徑，或只是檔名（不知道從哪算）
            if not os.path.exists(os.path.join(self.repo_root, cand.split("/", 1)[0])):
                continue  # 第一段不在 repo 根：外部 repo／合併後路徑／範例
            ok, res = wfnode.exists((self.repo_root, None), cand)
            if not ok and not self.ignored(path, keys, cand):
                self.add("RefBad", wfnode.fmt_loc((path, keys)), "`%s` 指不到（%s）" % (cand, res))

    def check_local(self, path, keys, cand):
        """`#/…` 單獨出現＝同一個檔裡的指標（跟 `$ref`）；含樣式字元的不驗。"""
        if NO_CHECK & set(cand):
            return
        ok, res = wfnode.exists((path, []), cand)
        if not ok and not self.ignored(path, keys, cand):
            self.add("RefBad", wfnode.fmt_loc((path, keys)), "`%s` 在本檔指不到（%s）" % (cand, res))

    def ignored(self, path, keys, cand):
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(self.repo_root)).replace(os.sep, "/")
        for where in (wfnode.fmt_loc((rel, keys)), rel):
            if (where, cand) in self.ignore:
                self.ignore[(where, cand)] = True
                return True
        return False

    def report_unused(self, roots):
        tops = [os.path.abspath(r) for r in roots]
        for (where, cand), used in sorted(self.ignore.items()):
            f = os.path.abspath(os.path.join(self.repo_root, where.split("#", 1)[0]))
            if not used and any(f == t or f.startswith(t + os.sep) for t in tops):
                self.warnings.append({"code": "IgnoreUnused", "path": where,
                                      "msg": "忽略表登記了 `%s`，沒壓到任何 RefBad" % cand})


def load_ignore(path):
    """忽略表 → {(位置, 字串): False}。格式錯丟 ValueError。"""
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            parts = line.rstrip("\n").split("\t")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if len(parts) != 2 or not all(parts):
                raise ValueError("%s:%d 要是 `節點位置<TAB>被引用的字串`" % (path, n))
            out[(parts[0], parts[1])] = False
    return out
