# conventions — 本 repo 的寫作與同步慣例

[common/README](README.md)｜[INDEX](../../INDEX.md)

碰原始碼（`tools/*.sh`、`tools/*.py`）與碰模板內容（`template/`、`flavors/`、`examples/`、`docs/`）的工作流共用這套規矩：**動手時要遵守什麼**。哪個檔負責什麼、測試在哪 → [code-map](code-map.md)；真相層優先序也在 [code-map](code-map.md)。結構整理原則 → [STRUCTURE](../../STRUCTURE.md)。

## 文件慣例（md）

| 項目 | 規矩 | 怎麼檢查 |
|------|------|---------|
| 語言 | 文件與回覆繁體中文；shell／python 註解可中可英，一檔之內一致 | 目視 |
| 檔案大小 | `workflows/` 下單檔 ≤ 8192 bytes；使用手冊類 ≤ 300 行。**對 `skills/` 不豁免** | `bash tools/wf-lint.sh --self` |
| 條列 | 條列式區塊 > 1024 bytes 抽資料檔；連結表看用途不看 bytes（見 [data-files](data-files.md)）| `python tools/find_big_lists.py` |
| 連結 | 一律相對路徑；改完不能有 BROKEN，錨點也要存在 | `bash tools/wf-lint.sh --self` |
| 搬檔 | 搬 md 後用 `python tools/fix_moved_links.py` 照 `moves.tsv` 重寫連結，不手改 | lint 0 BROKEN |
| 檔名 | kebab-case；`README` ＝資料夾入口、`INDEX` ＝結構索引（見 [STRUCTURE](../../STRUCTURE.md)）| 目視 |

## 程式碼慣例（tools/）

| 項目 | 規矩 | 怎麼檢查 |
|------|------|---------|
| 檔案拆分 | 單檔 > 300 行就照 [STRUCTURE](../../STRUCTURE.md) 拆；bash 拆成被 `source` 的函式庫（`wf-lint-checks.sh`、`wf-init-relink.sh`）| 目視行數 |
| 相依 | 只用標準庫與 POSIX 工具（bash／cp／sed／awk／grep／python3）；**不新增第三方套件** | `grep -rn '^import\|^from' tools/*.py` |
| `tools/` 是整包 | 拆檔後彼此相依，升級或複製時**整包一起**，只挑一支會 `FATAL`／ImportError | 見 [IMPORT.md](../../../IMPORT.md) 升級表 |
| breaking change | 改腳本的 CLI 介面或輸出格式前先全域 grep 受影響處（`docs/`、`README.md`、`.claude/commands/`），同一 commit 一起改 | `bash tools/wf-lint.sh --self` |
| 測試 | 動 `tools/` 一定補／跑對應的 `tools/test_*.py` | `python -m pytest tools -q` |

## 改 kernel 或 flavor 的同步義務

**改 `template/`（kernel）或 `flavors/`（flavor 包）＝ 一定要連帶改這幾處**，漏一處 lint 不一定抓得到：

1. [README.md](../../../README.md) 的兩張內容表（flavor 表、kernel／tools 說明段）。
2. [CHANGELOG.md](../../../CHANGELOG.md)：寫「改哪檔、既有專案要不要跟」。
3. `template/AGENTS.md` 尾端版本戳 `<!-- wf-kernel vX.Y -->`。
4. [docs/kernel-contents.md](../../../docs/kernel-contents.md) 的逐檔清單（新增／刪除檔案時）。
5. `examples/` 受影響就一起更新（它是合併成品，會被 CI 檢查）。
6. 分類是 kernel-owned 還是 project-owned → 見 [IMPORT.md](../../../IMPORT.md) 附表；分類改了要同步該表。

## flavor 包內的連結寫法

- flavor 包（`flavors/<名>/`）內的連結**一律照合併後的路徑寫**（例：`workflows/common/conventions.md`，而不是 `../../template/...`）。在本 repo 內直接點會指不到 kernel，**這是預期行為**，不要「修好」它。
- kernel 與 flavor 內部**不向上連 `AGENTS.md`**——這條讓非侵入式佈局自然成立（`AGENTS.md` 留在專案根、其餘進 `wf/`，內部連結一個都不用改）。
- `wf-lint.sh --self` 是把 kernel ＋ 每個 flavor **合併後**才檢查，所以 flavor 包單獨看的 BROKEN 不算數；判準只看 `--self`。
