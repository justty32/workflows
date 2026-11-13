"""index_check 的 index 那半：走樹、查 `_index.json`／檔內 `_index`／`_description`（JsonBad、IndexBad、
IndexMissing、IndexUnlisted、IndexWanted）。規則說明見 index_check.py 檔頭；引用檢查在 index_check_refs.py。
"""
import os

import wfnode
from index_check_refs import RefChecks, fence_flags

INDEX = "_index.json"
LOCAL = "_index.local.json"
DESC = "_description.json"
SKIP_DIRS = {"__pycache__"}
DIR_LIMIT, FILE_BYTES, FILE_KEYS = 15, 8000, 10


def hidden(name):
    return name.startswith(".") or name in SKIP_DIRS


def is_text(v):
    """一段文字：字串，或字串陣列（一行一個元素）。"""
    return isinstance(v, str) or (isinstance(v, list) and all(isinstance(x, str) for x in v))


class Checker(RefChecks):
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
        """一格 index 條目：物件形、description 非空字串、index 是指得到物件的路徑。多出來的鍵（source…）不管。"""
        if not isinstance(ent, dict):
            self.add("IndexBad", where, "條目 %s 要是物件 {\"description\": …}，不是 %s" % (key, type(ent).__name__))
            return
        desc = ent.get("description")
        if isinstance(desc, list):
            self.add("IndexBad", where, "條目 %s 的 description 是陣列：index 的 description 目前要維持一句字串" % key)
        elif not isinstance(desc, str) or not desc.strip():
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
        if name == DESC and not isinstance(data, dict) and not is_text(data):
            self.add("IndexBad", path, "資料夾的 _description.json 要是字串或字串陣列（一行一個元素）")
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
            if "_description" in val and not is_text(val["_description"]):
                self.add("IndexBad", wfnode.fmt_loc((path, keys + ["_description"])),
                         "_description 要是字串或字串陣列（一行一個元素）")
            if "$ref" in val and self.refs:
                self.check_ref(path, keys, val)
            for k, v in val.items():
                self.walk_value(path, keys + [k], v)
        elif isinstance(val, list):
            for i, (v, skip) in enumerate(zip(val, fence_flags(val))):
                if not skip:
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
