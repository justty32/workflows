# CHANGELOG — kernel 變動記錄

每次 kernel（`template/`）或導入契約變動記一節：改了哪檔、**既有專案要不要跟**。版本戳在 `template/AGENTS.md` 尾端 `<!-- wf-kernel vX.Y (日期) -->`，導入後 `grep wf-kernel AGENTS.md` 查自己是哪一版。kernel-owned / project-owned 分類見 [IMPORT.md](IMPORT.md)。

## v0.3 (2026-08-30)

文件整理工具進 kernel：同質記錄表 >1 KB 走資料檔、新增 `tidy` 工作流；**考慮使用者**——連結表另計，給人導航的留 md、給 AI 消化的才抽。既有專案要跟的話：

- 新增 `workflows/common/data-files.md`（契約 `wf-table/1`：同質記錄表 >1 KB 抽 `.json`／`.csv`；連結表不看 bytes，>10 條才考慮，給人導航的留 md 走一般 8 KB 上限，給 AI 消化的才抽）→ kernel-owned，直接加。
- 新增 `workflows/tidy.md`（盤點 → 交接書 → 派工 → 核驗的整理流程）→ kernel-owned，直接加；`WORKFLOWS.md` kernel 內建表加 tidy 列 → project-owned。
- 新增 `tools/tabledb.py`、`tabledb_links.py`、`find_big_lists.py`、`fix_moved_links.py` → kernel-owned，複製到專案 `tools/`（非侵入式 `wf/tools/`）；`wf-init.sh` 現在自動複製。
- `tools/wf-lint.sh` → kernel-owned 整檔覆蓋：新增 `BIGLIST`（呼叫 `find_big_lists.py --min 1024`；同質記錄表 `--strict` 才算失敗）與 `BIGLIST-LINKS`（純連結表超過十條，**只 warning，永不影響結束碼**）；資料檔 `tabledb.py check` 壞連結計入 `broken`。**行為變更**：`--strict` 時 `oversize` 與 `biglist`（同質記錄表）也算失敗（原本 oversize 只報）。
- `STRUCTURE.md` → kernel-owned 整檔覆蓋：整理原則加「同質記錄表 >1 KB」「連結表 >10 條另計（考慮使用者：給人導航留 md、給 AI 消化才抽）」「<1 KB 小檔合併」「同類可放鬆」「原路徑保留當入口」；archive 規則改「連結拿掉、當它不存在」「`archive/README.md` 索引是唯一可連進去的地方（原本寫不放 README）」；新增「資料檔慣例」三行。
- `AGENTS.md` → project-owned：加鐵律「條列走資料檔、導航留 md」、版本戳 v0.3。
- `INDEX.md` `tools/` 列、`workflows/common/README.md` data-files 列 → project-owned。
- `.claude/commands/wf-lint.md` → kernel-owned 覆蓋：說明 `BIGLIST` 與 `BIGLIST-LINKS`（後者只 warning）的差別。
- `README.md`／`IMPORT.md`／`docs/` 同步（本 repo 自己的）。

## v0.2 (2026-08-29)

依 2026-08-29 的 31 條改進提案全面重構（提案原文：`git show 025f8a2:docs/improvement-proposals-2026-08-29.md`）。既有專案（v0.1）要跟的話：

- **改名** `DEV-GUIDE.md` → `STRUCTURE.md`（kernel-owned，整檔覆蓋；連結 `sed 's/DEV-GUIDE/STRUCTURE/g'`）。分層原則、工作流統一形式、archive 規則、gotchas 門檻現在只在這檔。
- **移出 kernel**：`workflows/{tick,routines,schedule}.md` + `/wf-tick` → `flavors/heartbeat/`；`inbox/` + `workflows/inbox/` → `flavors/multi-agent/`（並吸收實際多 agent 專案的協議：時間戳檔名、STATUS、ROSTER、資源鎖、派線／交接書）。原本在用的專案不必動，只是之後的更新從那兩包拿。
- **鐵律 2** 改成「不可逆或對外動作要有**授權來源**（使用者當場確認、或使用者親自登記的清單項目）」，取代「未經確認不 push」與 routines / schedule 各自的解釋（project-owned：手動改 AGENTS.md 那一條）。「commit 到主分支是慣例」移進 `workflows/common/user.md` 分支慣例欄。
- **AGENTS.md** 縮到 ≈1.5 KB：加開場 checklist（`grep -c '^- \[' SESSION-LOG.md WAIT_USER.md`）、刪「分層思想」段（改連 STRUCTURE）、加 `<!-- wf-insert:AGENTS -->` 標記與版本戳（project-owned）。
- **SESSION-LOG.md** 寫入時機改固定三條（開工前寫、commit 後更新、格式 `- [工作流] 狀態 → 下一步`）；**WORKFLOWS.md** 加活狀態判別表（等人 / 等同 repo 另一 session / 等別資料夾 agent）與 kernel 內建表（project-owned，手動套）。
- **新增** `workflows/TEMPLATE.workflow.md`、`workflows/planning.md`（idea→roadmap→詳規→執行 一檔）、`workflows/decisions.md`、`workflows/common/user.md`、`.claude/commands/wf-lint.md`（kernel-owned，直接加進去）。
- **工具**：`tools/wf-init.sh`（合併導入，含非侵入式連結改寫）、`tools/wf-lint.sh`（連結 / 8192 bytes / 殘留 / inbox 堆積）；CI 跑 `--self`。
- **標記**：〔模板說明〕（純解說）與〔導入判斷〕（條件式，附同步清單）分開；「用不到就刪」規則只在 README / IMPORT 寫一次。
- **kernel 內部不再向上連 AGENTS.md**（非侵入式佈局因此不再需要手改 22 個連結）。
- 新 flavor：`teaching/`（plain-explain、study-site）、`research/`（source-intake、backlog、survey、collide）、`ops/`（inventory、incident、deploy）。dev 補 refactor / investigation / dev-env / code-map；knowledge 補 info-map、writing 去個人化、派發表加「分辨」欄。
- **文件改為 agent 工具中立**：`AGENTS.md` 是中立入口，`CLAUDE.md` / `.claude/commands/` 降級成「Claude Code 適配層」（可換可刪），措辭一律用「agent」；`wf-init.sh --redirect <檔名>` 產其他工具的轉址檔，README 有適配表（project-owned：措辭手動套）。
- repo：LICENSE（CC0）、根 AGENTS.md / CLAUDE.md、`examples/`；`non-invasive-import.md` 搬進 `docs/`。

## v0.1 (2026-08-28 以前)

`template/` + `flavors/{dev,knowledge}`，kernel 含 tick / routines / schedule 與 inbox；無版本戳。
