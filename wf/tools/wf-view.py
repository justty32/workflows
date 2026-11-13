#!/usr/bin/env python3
"""wf-view — 把 json 節點印成人讀的 markdown（stdout；只讀、不依賴 aos）。

  wf-view.py [--tree] [--overlay FILE] [--follow] PATH
    PATH        資料夾，或 `檔.json`、`檔.json#/JSON Pointer`。
    --tree      資料夾：遞迴往下印每一層（標題層級＝深度）。
    --overlay   資料夾：再疊一份私有 index（例 wf/_index.local.json），同名條目以它為準並標 (私有)。
    --follow    檔案：`{"$ref": …}` 展開成指到的內容（預設只印「→ 路徑」）。
資料夾：先印 `_description.json`，再把 `_index.json` 印成表（名字｜說明｜index）；沒有 index 就列目錄內容。
檔案：`_description` 印最前；字串照 markdown 原樣印；物件陣列印成表（欄＝各筆鍵的聯集、照首次出現）；
      字串陣列印成編號清單；巢狀物件遞迴成小節（鍵名當標題）；`_index`、`_metainfo` 不印。
錯誤：stderr `wf-view: error: CODE 說明`，退 1（找不到＝PathMissing、壞 json＝JsonBad）；參數錯退 2。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wfnode  # noqa: E402

HIDDEN = {"__pycache__"}
META = {"_description", "_index", "_metainfo"}


def h(level, text):
    return "%s %s" % ("#" * min(max(level, 1), 6), text)


def cell(v):
    if v is None:
        return ""
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
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
                self.emit(desc.rstrip("\n") if isinstance(desc, str) else json.dumps(desc, ensure_ascii=False))
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
            if isinstance(val.get("_description"), str):
                self.emit(val["_description"].rstrip("\n"))
                self.blank()
            for k, v in val.items():
                if k in META:
                    continue
                self.node(v, (loc[0], loc[1] + [k]), level + 1, title=k)
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
        elif all(isinstance(x, str) for x in val):
            for i, s in enumerate(val, 1):
                lines = s.split("\n")
                self.emit("%d. %s" % (i, lines[0]), *["   " + x if x else "" for x in lines[1:]])
        else:
            for i, x in enumerate(val):
                self.node(x, (loc[0], loc[1] + [str(i)]), level + 1, title="[%d]" % i)


def resolve(arg):
    """命令列 PATH → ('dir', 路徑) 或 ('json', Loc)。"""
    if "#" not in arg and os.path.isdir(arg):
        return "dir", arg
    fpart = arg.split("#", 1)[0]
    if not os.path.isfile(fpart):
        raise wfnode.NodeError("PathMissing", "%s 不存在" % fpart)
    start = (os.path.dirname(fpart) or ".", None)
    loc = wfnode.walk(start, os.path.basename(fpart) + ("#" + arg.split("#", 1)[1] if "#" in arg else "#"))
    return "json", loc


def main(argv):
    opts, args = {"tree": False, "follow": False, "overlay": None}, []
    it = iter(argv)
    for a in it:
        if a in ("--tree", "--follow"):
            opts[a[2:]] = True
        elif a == "--overlay":
            opts["overlay"] = next(it, None)
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        elif a.startswith("-") and a != "-":
            print("wf-view: error: ArgumentsBad 不認得的參數 %s" % a, file=sys.stderr)
            return 2
        else:
            args.append(a)
    if len(args) != 1 or ("--overlay" in argv and not opts["overlay"]):
        print("wf-view: error: ArgumentsBad 要剛好一個 PATH（--overlay 要給檔）", file=sys.stderr)
        return 2
    v = View(follow=opts["follow"])
    try:
        kind, target = resolve(args[0])
        if kind == "dir":
            overlay = None
            if opts["overlay"]:
                if not os.path.isfile(opts["overlay"]):
                    raise wfnode.NodeError("PathMissing", "overlay %s 不存在" % opts["overlay"])
                overlay = wfnode.load_json(opts["overlay"])
                if not isinstance(overlay, dict):
                    raise wfnode.NodeError("IndexBad", "overlay %s 不是物件" % opts["overlay"])
            v.folder(target, 1, opts["tree"], overlay)
        else:
            val = wfnode.value_at(target)
            v.emit(h(1, wfnode.fmt_loc(target) if target[1] else target[0]))
            v.blank()
            v.node(val, target, 2, top=True)
    except wfnode.NodeError as e:
        print("wf-view: error: %s %s" % (e.code, e.msg), file=sys.stderr)
        return 1
    while v.out and v.out[-1] == "":
        v.out.pop()
    sys.stdout.write("\n".join(v.out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
