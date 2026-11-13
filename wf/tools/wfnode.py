#!/usr/bin/env python3
"""wfnode — wf-view.py 與 index_check.py 共用的節點路徑解析（只用標準庫，不依賴 aos）。

統一路徑＝`資料夾/檔.json#/JSON Pointer`（RFC 6901：`~1`＝`/`、`~0`＝`~`）。
把檔案系統與 JSON 當成同一棵樹走（同 aos 規範 01 的 `$ref` 算法）：
  - 名字＝往下一層（資料夾→子項、.json 檔→進檔、物件→鍵、陣列→索引）；
  - `..`＝往外一層，走出 JSON 根物件就回到檔所在的資料夾；
  - `#/…` 開頭不算相對：從「起點所在的那個 json 檔」的根算；
  - 走到 `{"$ref": …}` 物件還要往下（鍵不在物件裡）＝先跟 `$ref` 到目標再往下（停在它上面不跟）。
位置 Loc＝(path, keys)：keys 為 None 表示 path 是檔案系統上的東西；為 list 表示在 path 這份 json 檔裡。
"""
import json
import os

_CACHE = {}


class NodeError(Exception):
    """路徑走不到；code 是 PathMissing／JsonBad 之類的代號。"""

    def __init__(self, code, msg):
        Exception.__init__(self, msg)
        self.code = code
        self.msg = msg


def load_json(path):
    """讀 json（有快取）。壞檔丟 NodeError('JsonBad')。"""
    key = os.path.abspath(path)
    if key not in _CACHE:
        try:
            with open(path, encoding="utf-8") as f:
                _CACHE[key] = (True, json.load(f))
        except (OSError, ValueError) as e:
            _CACHE[key] = (False, str(e))
    ok, val = _CACHE[key]
    if not ok:
        raise NodeError("JsonBad", "%s: %s" % (path, val))
    return val


def clear_cache():
    _CACHE.clear()


def unescape(tok):
    return tok.replace("~1", "/").replace("~0", "~")


def escape(tok):
    return tok.replace("~", "~0").replace("/", "~1")


def pointer_segs(ptr, ref):
    """'/x/y~1z' → ['x', 'y/z']；'' → []。"""
    if ptr == "":
        return []
    if not ptr.startswith("/"):
        raise NodeError("PointerBad", "JSON Pointer 要以 / 開頭: %s" % ref)
    return [unescape(t) for t in ptr.split("/")[1:]]


def value_at(loc):
    """Loc → 值（只對 json 內的位置）。走不到丟 NodeError('PathMissing')。"""
    path, keys = loc
    cur = load_json(path)
    for i, k in enumerate(keys):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and k.isdigit() and int(k) < len(cur):
            cur = cur[int(k)]
        else:
            where = "/".join(escape(x) for x in keys[:i + 1])
            raise NodeError("PathMissing", "%s#/%s 不存在" % (path, where))
    return cur


def _step(loc, seg):
    path, keys = loc
    if seg in ("", "."):
        return loc
    if seg == "..":
        if keys:
            return path, keys[:-1]
        return os.path.dirname(os.path.normpath(path)) or ".", None
    if keys is None:
        if os.path.isdir(path):
            return os.path.join(path, seg), None
        if path.endswith(".json") and os.path.isfile(path):
            keys = []
        elif not os.path.exists(path):
            raise NodeError("PathMissing", "%s 不存在" % path)
        else:
            raise NodeError("PathMissing", "%s 不是資料夾或 json 檔，走不進 %s" % (path, seg))
    cur = value_at((path, keys))
    if isinstance(cur, dict) and isinstance(cur.get("$ref"), str) and seg not in cur:
        return _step(follow_ref((path, keys), cur)[0], seg)  # 往 `$ref` 物件裡走＝走進它指到的地方
    nxt = keys + [seg]
    value_at((path, nxt))  # 確認走得到
    return path, nxt


def enter(loc):
    """'#'：從檔案系統進到 json 檔的根。"""
    path, keys = loc
    if keys is not None:
        return loc
    if not os.path.isfile(path):
        raise NodeError("PathMissing", "%s 不存在" % path)
    load_json(path)
    return path, []


def walk(start, ref):
    """從 start（Loc）照 ref（統一路徑字串）走；回傳終點 Loc。走不到丟 NodeError。

    ref 以 '/' 開頭＝絕對檔案路徑；以 '#' 開頭＝起點所在 json 檔的根。
    `#` 之後可以再出現 `#`（`#/../x.json#/k`：走出根物件回到夾、再進隔壁檔）。
    """
    parts = ref.split("#")
    fpart, ptrs = parts[0], parts[1:]
    if fpart == "" and ptrs:
        path, keys = start
        if keys is None:
            raise NodeError("PathMissing", "%s 不在 json 檔裡，不能用 #/ 開頭" % path)
        loc = (path, [])
    else:
        loc = ("/", None) if fpart.startswith("/") else start
        for seg in fpart.split("/"):
            loc = _step(loc, seg)
        if loc[1] is None and not ptrs and not os.path.exists(loc[0]):
            raise NodeError("PathMissing", "%s 不存在" % loc[0])
    for i, ptr in enumerate(ptrs):
        if i or fpart:
            loc = enter(loc)
        for seg in pointer_segs(ptr, ref):
            loc = _step(loc, seg)
    return loc


def exists(start, ref):
    """walk 得到就回 (True, Loc)，否則 (False, 說明)。"""
    try:
        return True, walk(start, ref)
    except NodeError as e:
        return False, e.msg


def fmt_loc(loc):
    path, keys = loc
    if keys is None:
        return path
    return path + "#/" + "/".join(escape(k) for k in keys)


def follow_ref(loc, obj, seen=None):
    """obj 是 {"$ref": …}（位於 loc 那份檔裡）→ (目標 Loc, 值)；支援 `$at`，會連續跟到底。"""
    seen = set() if seen is None else seen
    while isinstance(obj, dict) and isinstance(obj.get("$ref"), str):
        ref = obj["$ref"]
        here = (loc[0], []) if ref.startswith("#") else (os.path.dirname(loc[0]) or ".", None)
        tgt = walk(here, ref)
        for seg in str(obj.get("$at", "")).split("/"):
            tgt = _step(tgt, seg)
        if tgt[1] is None:
            if not (tgt[0].endswith(".json") and os.path.isfile(tgt[0])):
                raise NodeError("PathMissing", "$ref 指到的不是 json 檔: %s" % tgt[0])
            tgt = (tgt[0], [])
        key = fmt_loc(tgt)
        if key in seen:
            raise NodeError("RefLoop", "$ref 繞圈: %s" % key)
        seen.add(key)
        loc, obj = tgt, value_at(tgt)
    return loc, obj
