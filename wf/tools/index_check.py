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
  IndexBad       `_index.json` 不是物件；條目不是物件或 description 不是非空字串；
                 `index` 不是字串、指不到、或指到的不是物件。檔內 `_index` 同樣驗（也可以是一條指到別份 index 的路徑字串）。
  IndexMissing   index 列了不存在的名字（資料夾的鍵可寫 `檔.json#/指標`）。
  IndexUnlisted  夾裡有東西沒列進該夾的 `_index.json`（不算 `_index.json`、`_index.local.json`、`.` 開頭、`__pycache__`）。
  IndexWanted    （warning）夾內超過 15 個東西沒有 `_index.json`；json 檔超過 8000 bytes 或頂層內容鍵超過 10 個沒有 `_index`。
  RefBad         字串值裡反引號包著的 repo 路徑（`#` 前含 `/`、不以 ./ ../ 開頭、副檔名 json|md|py|sh|tsv|csv|yml，可帶 `#/指標`）指不到；
                 含 `< > * … {` 的不驗、``` 圍籬裡的不驗；第一段不是 repo 根底下實際存在的項目（外部 repo、
                 合併後的路徑、範例）也不驗。`{"$ref": …}` 指不到也是 RefBad。忽略表登記的不報。
  IgnoreUnused   （warning）忽略表的某行沒壓到任何 RefBad（只算 PATH 範圍內的檔）。
路徑算法見 wfnode.py（`..` 走出 json 根＝回到檔所在的夾、`#/` 開頭＝本檔的根）。
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wfnode  # noqa: E402

INDEX = "_index.json"
LOCAL = "_index.local.json"
SKIP_DIRS = {"__pycache__"}
DIR_LIMIT, FILE_BYTES, FILE_KEYS = 15, 8000, 10
REF_RE = re.compile(r"^[\w./-]+\.(json|md|py|sh|tsv|csv|yml)(#/[^`\s]*)?$")
TICK_RE = re.compile(r"`([^`\n]+)`")
FENCE_RE = re.compile(r"```.*?(```|\Z)", re.S)
NO_CHECK = set("<>*…{")


class Checker:
    def __init__(self, strict=False, refs=True, repo_root=".", ignore=None):
        self.strict, self.refs, self.repo_root = strict, refs, repo_root
        self.ignore = ignore or {}  # {(位置, 字串): 用過沒}
        self.problems, self.warnings = [], []

    def add(self, code, where, msg):
        self.problems.append({"code": code, "path": where, "msg": msg})

    def want(self, where, msg):
        item = {"code": "IndexWanted", "path": where, "msg": msg}
        (self.problems if self.strict else self.warnings).append(item)

    # ---- 走樹 ----
    def run(self, roots):
        for root in roots:
            if os.path.isfile(root):
                self.check_file(root)
                continue
            if not os.path.isdir(root):
                self.add("PathMissing", root, "不存在")
                continue
            for d, dirs, files in os.walk(root):
                dirs[:] = sorted(x for x in dirs if not hidden(x))
                self.check_dir(d)
                for f in sorted(files):
                    if f.endswith(".json") and not f.startswith("."):
                        self.check_file(os.path.join(d, f))

    def check_dir(self, d):
        names = set(x for x in os.listdir(d) if not hidden(x))
        listable = names - {INDEX, LOCAL}
        ipath = os.path.join(d, INDEX)
        if INDEX not in names:
            if len(listable) > DIR_LIMIT:
                self.want(d, "夾內有 %d 個東西（> %d）卻沒有 %s" % (len(listable), DIR_LIMIT, INDEX))
            return
        try:
            idx = wfnode.load_json(ipath)
        except wfnode.NodeError:
            return  # check_file 會報 JsonBad
        if not isinstance(idx, dict):
            self.add("IndexBad", ipath, "整份要是物件 {名字: {\"description\": …}}")
            return
        listed = set()
        for key, ent in idx.items():
            self.check_entry(ipath, key, ent, (d, None), (ipath, []))
            if "#" in key:
                ok, _ = wfnode.exists((d, None), key)
                listed.add(key.split("#", 1)[0])
            else:
                ok = key in names
                listed.add(key)
            if not ok:
                self.add("IndexMissing", ipath, "列了 %s，夾裡沒有" % key)
        for name in sorted(listable - listed):
            self.add("IndexUnlisted", ipath, "%s 沒列進 index" % name)

    def check_entry(self, where, key, ent, base, file_root):
        """一格 index 條目：物件形、description 非空字串、index 是指得到物件的路徑。"""
        if not isinstance(ent, dict):
            self.add("IndexBad", where, "條目 %s 要是物件 {\"description\": …}，不是 %s" % (key, type(ent).__name__))
            return
        desc = ent.get("description")
        if not isinstance(desc, str) or not desc.strip():
            self.add("IndexBad", where, "條目 %s 缺 description 或不是非空字串" % key)
        if "index" in ent:
            self.check_link(where, "條目 %s 的 index" % key, ent["index"], base, file_root)

    def check_link(self, where, what, val, base, file_root):
        if not isinstance(val, str) or not val:
            self.add("IndexBad", where, "%s 要是路徑字串" % what)
            return
        ok, res = wfnode.exists(file_root if val.startswith("#") else base, val)
        if not ok:
            self.add("IndexBad", where, "%s 指不到: %s（%s）" % (what, val, res))
            return
        target = res if res[1] is not None else (res[0], [])
        try:
            obj = wfnode.value_at(target) if res[0].endswith(".json") else None
        except wfnode.NodeError:
            obj = None
        if not isinstance(obj, dict):
            self.add("IndexBad", where, "%s 指到的不是 index 物件: %s" % (what, val))

    # ---- 單檔 ----
    def check_file(self, path):
        try:
            data = wfnode.load_json(path)
        except wfnode.NodeError as e:
            self.add("JsonBad", path, e.msg.split(": ", 1)[-1])
            return
        name = os.path.basename(path)
        if isinstance(data, dict) and name not in (INDEX, LOCAL):
            content = [k for k in data if not k.startswith("_")]
            size = os.path.getsize(path)
            if "_index" not in data and (size > FILE_BYTES or len(content) > FILE_KEYS):
                self.want(path, "%d bytes、%d 個內容鍵（門檻 %d bytes／%d 鍵）卻沒有 _index"
                          % (size, len(content), FILE_BYTES, FILE_KEYS))
        self.walk_value(path, [], data)

    def walk_value(self, path, keys, val):
        if isinstance(val, dict):
            if "_index" in val and os.path.basename(path) != INDEX:
                self.check_infile_index(path, keys, val)
            if "$ref" in val and self.refs:
                self.check_ref(path, keys, val)
            for k, v in val.items():
                self.walk_value(path, keys + [k], v)
        elif isinstance(val, list):
            for i, v in enumerate(val):
                self.walk_value(path, keys + [str(i)], v)
        elif isinstance(val, str) and self.refs:
            self.check_ticks(path, keys, val)

    def check_infile_index(self, path, keys, obj):
        where = wfnode.fmt_loc((path, keys + ["_index"]))
        idx = obj["_index"]
        here = (path, keys)
        if isinstance(idx, str):
            self.check_link(where, "_index 連結", idx, here, (path, []))
            return
        if not isinstance(idx, dict):
            self.add("IndexBad", where, "_index 要是物件或指到別份 index 的路徑字串")
            return
        for key, ent in idx.items():
            self.check_entry(where, key, ent, here, (path, []))
            if key not in obj:
                self.add("IndexMissing", where, "列了 %s，物件裡沒有這個鍵" % key)
        if self.strict:
            for k in obj:
                if not k.startswith("_") and k not in idx:
                    self.add("IndexUnlisted", where, "%s 沒列進 _index" % k)

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
            if (NO_CHECK & set(cand) or not REF_RE.match(cand) or cand.startswith(("./", "../"))
                    or "/" not in cand.split("#", 1)[0]):
                continue  # 範例／樣式／相對路徑，或只是檔名（不知道從哪算）
            if not os.path.exists(os.path.join(self.repo_root, cand.split("/", 1)[0])):
                continue  # 第一段不在 repo 根：外部 repo／合併後路徑／範例
            ok, res = wfnode.exists((self.repo_root, None), cand)
            if not ok and not self.ignored(path, keys, cand):
                self.add("RefBad", wfnode.fmt_loc((path, keys)), "`%s` 指不到（%s）" % (cand, res))

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


def hidden(name):
    return name.startswith(".") or name in SKIP_DIRS


def git_root(start):
    d = start if os.path.isdir(start) else os.path.dirname(os.path.abspath(start))
    try:
        out = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                             universal_newlines=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 and out.stdout.strip() else None


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
