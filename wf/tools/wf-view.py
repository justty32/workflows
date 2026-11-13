#!/usr/bin/env python3
"""wf-view — 把 json 節點印成人讀的 markdown（stdout；只讀、不依賴 aos）。

  wf-view.py [--tree] [--overlay FILE] [--follow] PATH
    PATH        資料夾，或 `檔.json`、`檔.json#/JSON Pointer`。
    --tree      資料夾：遞迴往下印每一層（標題層級＝深度）。
    --overlay   資料夾：再疊一份私有 index（例 wf/_index.local.json），同名條目以它為準並標 (私有)。
    --follow    檔案：`{"$ref": …}` 展開成指到的內容（預設只印「→ 路徑」）。
資料夾：先印 `_description.json`，再把 `_index.json` 印成表（名字｜說明｜index）；沒有 index 就列目錄內容。
檔案：`_description` 印最前；字串照 markdown 原樣印；物件陣列印成表（欄＝各筆鍵的聯集、照首次出現）；
      字串陣列：像拆成行的一段文字（有空字串元素、元素以 `- ` `* ` `#` `|` `>` `1. ` 開頭、或含成對 ``` 圍籬）
      就用換行接回去原樣印，否則印成編號清單；`_description` 是陣列時一律接回去；巢狀物件遞迴成小節
      （鍵名當標題）；`_index`、`_metainfo` 不印。排版在 wf_view_render.py。
錯誤：stderr `wf-view: error: CODE 說明`，退 1（找不到＝PathMissing、壞 json＝JsonBad）；參數錯退 2。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wfnode  # noqa: E402
from wf_view_render import View, h  # noqa: E402


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
