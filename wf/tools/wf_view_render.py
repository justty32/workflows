"""wf-view 的排版那半：View 把資料夾與 json 值排成 markdown 行（CLI 與參數在 wf-view.py）。

字串陣列有兩種用法：一條一個元素的清單（印成編號清單），或一段多行文字拆成一行一個元素（照順序用換行
接起來就是原文，原樣當 markdown 印）。判斷用 looks_like_lines。
"""
import json
import os
import re

import wfnode

HIDDEN = {"__pycache__"}
META = {"_description", "_index", "_metainfo"}


LINE_START = re.compile(r"(- |\* |#|\||>|\d+\. )")


def h(level, text):
    return "%s %s" % ("#" * min(max(level, 1), 6), text)


def str_list(v):
    return isinstance(v, list) and bool(v) and all(isinstance(x, str) for x in v)


def looks_like_lines(v):
    """字串陣列像「一段多行文字拆成行」：有空字串元素、有元素以 markdown 行首（- * # | > 1.）開頭，
    或含成對的 ``` 圍籬行（只有一個 ``` 開頭的元素不算：清單裡一條剛好以 ``` 起頭的字很常見）。"""
    if not str_list(v):
        return False
    fences = sum(1 for x in v if x.lstrip().startswith("```"))
    return fences >= 2 or any(x == "" or LINE_START.match(x.lstrip()) for x in v)


def text_of(v):
    """一段文字（字串或字串陣列）→ 字串；不是就回 None。"""
    if isinstance(v, str):
        return v
    return "\n".join(v) if str_list(v) else None


def cell(v):
    if v is None:
        return ""
    s = v if isinstance(v, str) else "\n".join(v) if looks_like_lines(v) else json.dumps(v, ensure_ascii=False)
    return s.replace("|", "\\|").replace("\r", "").replace("\n", "<br>")


def table(rows, cols):
    out = ["| " + " | ".join(cell(c) for c in cols) + " |",
           "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        out.append("| " + " | ".join(cell(r.get(c, "")) for c in cols) + " |")
    return out


class View:
    def __init__(self, follow=False):
        self.follow, self.out = follow, []

    def emit(self, *lines):
        self.out.extend(lines)

    def blank(self):
        if self.out and self.out[-1] != "":
            self.out.append("")

    # ---- 資料夾 ----
    def folder(self, d, level, tree, overlay=None):
        self.emit(h(level, d.rstrip("/") + "/"))
        self.blank()
        dpath = os.path.join(d, "_description.json")
        if os.path.isfile(dpath):
            desc = wfnode.load_json(dpath)
            if isinstance(desc, dict):
                self.node(desc, (dpath, []), level + 1, top=True)
            else:
                text = text_of(desc)
                self.emit(text.rstrip("\n") if text is not None else json.dumps(desc, ensure_ascii=False))
            self.blank()
        ipath = os.path.join(d, "_index.json")
        names = sorted(x for x in os.listdir(d) if not x.startswith(".") and x not in HIDDEN)
        if os.path.isfile(ipath) or overlay:
            idx = wfnode.load_json(ipath) if os.path.isfile(ipath) else {}
            if not isinstance(idx, dict):
                raise wfnode.NodeError("IndexBad", "%s 不是物件" % ipath)
            rows = self.merge(idx, overlay)
            self.emit(*table(rows, ["名字", "說明", "index"]))
        else:
            for n in names:
                self.emit("- %s%s" % (n, "/" if os.path.isdir(os.path.join(d, n)) else ""))
        self.blank()
        if tree:
            for n in names:
                sub = os.path.join(d, n)
                if os.path.isdir(sub):
                    self.folder(sub, level + 1, tree)

    def merge(self, idx, overlay):
        priv = overlay or {}
        rows = []
        for k, e in list(idx.items()) + [(k, e) for k, e in priv.items() if k not in idx]:
            mine = k in priv
            e = priv[k] if mine else e
            e = e if isinstance(e, dict) else {"description": e}
            desc = e.get("description", "")
            desc = desc if isinstance(desc, str) else json.dumps(desc, ensure_ascii=False)
            rows.append({"名字": k + (" (私有)" if mine else ""), "說明": desc, "index": e.get("index", "")})
        return rows

    # ---- 檔案內容 ----
    def node(self, val, loc, level, top=False, title=None):
        if title is not None:
            self.emit(h(level - 1, title))
            self.blank()
        if isinstance(val, dict) and isinstance(val.get("$ref"), str):
            if not self.follow:
                self.emit("→ `%s`" % val["$ref"] + ("（$at: %s）" % val["$at"] if "$at" in val else ""))
                self.blank()
                return
            tloc, tval = wfnode.follow_ref(loc, val)
            self.emit("（展開自 `%s`）" % val["$ref"])
            self.blank()
            return self.node(tval, tloc, level)
        if isinstance(val, dict):
            if text_of(val.get("_description")) is not None:
                self.emit(text_of(val["_description"]).rstrip("\n"))
                self.blank()
            for k, v in val.items():
                if k in META:
                    continue
                self.node(v, (loc[0], loc[1] + [k]), level + 1, title=k)
        elif looks_like_lines(val):
            self.emit("\n".join(val).rstrip("\n"))
        elif isinstance(val, list):
            self.array(val, loc, level)
        elif isinstance(val, str):
            self.emit(val.rstrip("\n"))
        else:
            self.emit("`%s`" % json.dumps(val, ensure_ascii=False))
        self.blank()

    def array(self, val, loc, level):
        if not val:
            self.emit("（空）")
        elif all(isinstance(x, dict) and not isinstance(x.get("$ref"), str) for x in val):
            cols = []
            for r in val:
                cols.extend(k for k in r if k not in cols)
            self.emit(*table(val, cols))
        elif all(text_of(x) is not None for x in val):
            for i, s in enumerate(val, 1):
                lines = text_of(s).split("\n")  # 元素本身是拆成行的字串陣列時先接回去
                self.emit("%d. %s" % (i, lines[0]), *["   " + x if x else "" for x in lines[1:]])
        else:
            for i, x in enumerate(val):
                self.node(x, (loc[0], loc[1] + [str(i)]), level + 1, title="[%d]" % i)


