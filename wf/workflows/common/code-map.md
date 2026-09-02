# code-map — 程式碼導航 index（哪個檔負責什麼）

[common/README](README.md)｜[INDEX](../../INDEX.md)

碰原始碼前先查這張表，只讀相關領域列出的檔；動完再照維護鏈把表更新回去。寫碼慣例本身在 [conventions](conventions.md)。本 repo 的「原始碼」＝ `tools/` 的 bash 與 python；`template/`、`flavors/` 是內容不是碼，導航見 [docs/kernel-contents.md](../../../docs/kernel-contents.md)。

## 領域表

| 領域 | 檔案 | 職責 | 測試在哪 |
|------|------|------|---------|
| 導入 | `tools/wf-init.sh`、`tools/wf-init-relink.sh` | 把 kernel ＋ 選定 flavor 合成到一個專案：複製、貼片段、非侵入式改寫斷掉的相對連結（改寫那半段在 relink）| 無自動測試（手動跑 `--target` 到暫存目錄）|
| 檢查 | `tools/wf-lint.sh`、`tools/wf-lint-checks.sh` | 掃壞連結／超標檔／超標條列／資料檔連結／佔位符與導入判斷段落的殘留；`--self` 是合併後檢查模板端，檢查函式在 checks | `tools/test_wf_lint.py` |
| 錨點 | `tools/check_anchors.py` | 驗 md 連結的 `#錨點`（heading slug 與顯式 id）在目標檔存不存在 | `tools/test_check_anchors.py` |
| 資料檔 | `tabledb.py`、`tabledb_table.py`、`tabledb_links.py`（都在 `tools/`）| `wf-table/1` 契約的 CRUD 與連結查驗；`Table` 型別在 table、連結檢查在 links | `tools/test_tabledb.py` |
| 資料檔 `$fmt` | `tools/tabledb_fmt.py`、`tabledb_fmt_expand.py`、`tabledb_fmt_vars.py`、`tools/fmt-vars.json` | json 值裡的跨層路徑代號展開；變數表在 `fmt-vars.json`（專案自加的放 `fmt-vars.local.json`）| `tools/test_tabledb_fmt.py`、`test_tabledb_fmt_vars.py` |
| 超標偵測 | `tools/find_big_lists.py` | 列出超標的表／清單，附連結數判斷是不是連結表 | `tools/test_find_big_lists.py` |
| 搬檔改連結 | `tools/fix_moved_links.py`、`fix_moved_links_scan.py`、`fix_moved_links_fmt.py` | 照 `moves.tsv` 重寫連結；掃描與搬移表在 scan、`$fmt` 那半段在 fmt | `tools/test_fix_moved_links.py` |
| CI | `.github/workflows/wf-lint.yml` | push／PR 時跑 `bash tools/wf-lint.sh --self`（合併後檢查）；**不跑 pytest** | — |

## 真相層優先序

各專案可以改自己的優先序，但必須明確。本 repo：

```text
code/tests > template/ 與 flavors/ 的內容 > code map > docs/ 與 README > generated
```

- 上層與下層衝突時，**以上層為準並修正下層**。
- `examples/` 是**合併產物**（generated），永遠不是唯一真相；真相在 `template/` ＋ `flavors/`。
- 原始來源與摘要衝突時，以**原始來源**為準（例：`docs/kernel-contents.md` 與實際檔案清單不合，以實際檔案為準）。
- code map 是**導航不是規格**；行為以 code/tests 為準。

## 維護鏈：程式碼 > code map > 文檔

**優先級**（衝突或時間不夠時，依序保持一致）：程式碼 > code map > 文檔。
**code map 與程式碼衝突時以程式碼為準，立刻改 code map。**

1. **修改前**：先讀本表找到相關領域，只讀清單裡的檔——不讀無關領域的檔。
2. **修改後**：新增／刪除了 `tools/` 的檔，或某檔職責顯著改變，必須同步更新本表**與** [docs/kernel-contents.md](../../../docs/kernel-contents.md)（見 [conventions](conventions.md) 的同步義務）。
3. 原始碼裡**不加**「對應 code map」的註釋（維護成本過高）；反向查找直接 grep 本檔。
4. 迭代期間本表可暫時落後，**commit 前必須對齊**（見 [feature-dev](../feature-dev/README.md)）。
