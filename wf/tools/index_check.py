#!/usr/bin/env python3
"""index_check — 查 json 節點樹的 index 與引用對不對得上（只讀、不改檔、不依賴 aos）。

  index_check.py [--strict] [--no-refs] [--root DIR] [--ignore FILE] [--json] [PATH…]  （PATH 預設 wf）
    --strict   檔內 `_index` 沒列到的內容鍵也報 IndexUnlisted；IndexWanted 改算 problem。
    --no-refs  不查 RefBad（反引號路徑與 `$ref`）。
    --root     反引號路徑從哪裡算。沒給＝第一個 PATH 所在的 git toplevel，找不到 git＝目前目錄。
    --ignore   RefBad 忽略表，預設 `<root>/wf/tools/index_check.ignore`（沒有就不用）。一行 `位置<TAB>字串`：
               位置＝repo 根算的 `檔.json#/指標`（只寫 `檔.json`＝整檔）；`#` 開頭與空行是註解。
    --json     輸出 {"problems": [...], "warnings": [...]}，代替逐行輸出。
  每個問題一行 `CODE 路徑: 說明`，warning 行尾加 `(warning)`；最後一行 `TOTAL problems=N warnings=M`。
  N>0 退 1，否則 0；參數錯退 2。
代號
  JsonBad        .json 解析失敗。
  IndexBad       `_index.json` 不是物件；條目不是物件或 description 不是非空字串（是陣列也報：index 的
                 description 目前要維持一句字串）；`index` 不是字串、指不到、或指到的不是物件。檔內 `_index` 同樣驗
                 （也可以是一條指到別份 index 的路徑字串）。`_description`（檔內鍵、資料夾的 `_description.json`）
                 不是字串或字串陣列（資料夾那份也可以是物件）。條目多出來的鍵（例 `source`）不管。
  IndexMissing   index 列了不存在的名字（資料夾的鍵可寫 `檔.json#/指標`）。
  IndexUnlisted  夾裡有東西沒列進該夾的 `_index.json`（不算 `_index.json`、`_index.local.json`、`.` 開頭、`__pycache__`）。
  IndexWanted    （warning）夾內超過 15 個東西沒有 `_index.json`；json 檔超過 8000 bytes 或頂層內容鍵超過 10 個沒有 `_index`。
  RefBad         字串值裡反引號包著的 repo 路徑（`#` 前含 `/`、不以 ./ ../ 開頭、副檔名 json|md|py|sh|tsv|csv|yml，可帶 `#/指標`）指不到；
                 含 `< > * … {` 的不驗、``` 圍籬裡的不驗（字串陣列跨元素的圍籬也算）；第一段不是 repo 根底下實際存在的項目（外部 repo、
                 合併後的路徑、範例）也不驗。反引號裡單獨的 `#/指標` 驗同一個檔裡走不走得到（跟 `$ref`；樣式字元同上不驗）。
                `{"$ref": …}` 指不到也是 RefBad。忽略表登記的不報。
  IgnoreUnused   （warning）忽略表的某行沒壓到任何 RefBad（只算 PATH 範圍內的檔）。
程式分三支：本檔（CLI）、index_check_tree.py（走樹與 index）、index_check_refs.py（引用與忽略表）。
路徑算法見 wfnode.py（`..` 走出 json 根＝回到檔所在的夾、`#/` 開頭＝本檔的根）。
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wfnode  # noqa: E402,F401  （測試從這裡拿 wfnode）
from index_check_refs import load_ignore  # noqa: E402
from index_check_tree import Checker  # noqa: E402


def git_root(start):
    d = start if os.path.isdir(start) else os.path.dirname(os.path.abspath(start))
    try:
        out = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                             universal_newlines=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 and out.stdout.strip() else None


def main(argv):
    opts, roots = {"strict": False, "refs": True, "root": None, "json": False, "ignore": None}, []
    it = iter(argv)
    for a in it:
        if a == "--strict":
            opts["strict"] = True
        elif a == "--no-refs":
            opts["refs"] = False
        elif a == "--json":
            opts["json"] = True
        elif a.split("=", 1)[0] in ("--root", "--ignore"):
            name = a.split("=", 1)[0][2:]
            opts[name] = a.split("=", 1)[1] if "=" in a else next(it, None)
            if not opts[name]:
                print("index_check: error: --%s 要給路徑" % name, file=sys.stderr)
                return 2
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        elif a.startswith("-"):
            print("index_check: error: 不認得的參數 %s" % a, file=sys.stderr)
            return 2
        else:
            roots.append(a)
    roots = roots or ["wf"]
    repo = opts["root"] or git_root(roots[0]) or os.getcwd()
    ign = opts["ignore"] or os.path.join(repo, "wf", "tools", "index_check.ignore")
    try:
        ignore = load_ignore(ign) if opts["ignore"] or os.path.isfile(ign) else {}
    except (OSError, ValueError) as e:
        print("index_check: error: 忽略表 %s" % e, file=sys.stderr)
        return 2
    c = Checker(opts["strict"], opts["refs"], repo, ignore)
    c.run(roots)
    if c.refs:
        c.report_unused(roots)
    if opts["json"]:
        print(json.dumps({"problems": c.problems, "warnings": c.warnings}, ensure_ascii=False, indent=1))
    else:
        for p in c.problems:
            print("%s %s: %s" % (p["code"], p["path"], p["msg"]))
        for w in c.warnings:
            print("%s %s: %s (warning)" % (w["code"], w["path"], w["msg"]))
        print("TOTAL problems=%d warnings=%d" % (len(c.problems), len(c.warnings)))
    return 1 if c.problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
