# CHANGELOG — kernel 變動記錄

每次 kernel（`template/`）或導入契約變動記一節：改了哪檔、**既有專案要不要跟**。版本戳在 `template/AGENTS.md` 尾端 `<!-- wf-kernel vX.Y (日期) -->`，導入後 `grep wf-kernel AGENTS.md` 查自己是哪一版。kernel-owned / project-owned 分類見 [IMPORT.md](IMPORT.md)。

## v0.4.1 (2026-08-30)

**md 不再教查法。** kernel 已規定資料檔一律走 `tabledb.py`，md 再貼一次 `python3 …/tools/tabledb.py x.json` 對 agent 是雜訊、對人是會過期的路徑；要查法的人看工作流的資料檔說明就好。既有專案要跟：套完跑一次 `wf-lint.sh --strict`，把 `QUERYCMD` 報出來的行清掉——刪指令與圍欄，留「已抽到 x.json（N 列）」與欄位說明。

- `workflows/common/data-files.md` → kernel-owned 覆蓋：「md 只留摘要與查法」→「只留摘要」；「md 端留什麼」拿掉**三行查法**、改成 `已抽到 [x.json](x.json)（N 列）` 加一段「**不寫查詢指令、不寫工具路徑**」；`index.json` 段拿掉 README 那句指令；工具段補 ③ QUERYCMD。
- `workflows/tidy.md`、`STRUCTURE.md` → kernel-owned 覆蓋：「留摘要與查法」→「留摘要」；資料檔慣例的 `tools/tabledb.py` 改成 `tabledb.py`（路徑本身就是壞示範）。
- `tools/wf-lint.sh` → kernel-owned 覆蓋：新增檢查項 ⑦ `QUERYCMD <檔>:<行>`——任一行含 `tabledb.py` 且含 `python3 ` 或 `tools/tabledb.py`；免掃 `archive/`、`wf/`、`AGENTS.md` 與契約檔（`data-files.md`／`data-files-fmt.md`／`tidy.md`）。**行為變更**：`--strict` 時 `querycmd > 0` 也算失敗，平時只印；`SUMMARY`／`TOTAL` 多一個 `querycmd=`。
- 新增 `tools/test_wf_lint.py`（6 條 QUERYCMD 測試）→ 本 repo 自用，不隨 `wf-init.sh` 複製。
- `.claude/commands/wf-lint.md` → kernel-owned 覆蓋，加 `QUERYCMD` 說明；`AGENTS.md` 戳記 → v0.4.1（project-owned）；`examples/` 同步。
- CHANGELOG 自身超過 8192 bytes，v0.2 與 v0.1 兩節照本 repo 慣例壓成一段摘要，完整條列留在 git 歷史。

## v0.4 (2026-08-30)

json 資料檔的路徑值可以寫成 `$fmt` 代號模板（讀取時展開），省去深層 `../../../`；md 連結與 `.csv` 不受影響，契約名仍 `wf-table/1`。既有專案要不要跟：既有 json 不必改，跨兩層以上（≥ 2 個 `../`）的路徑建議改成 `$fmt`。

- 新增 `workflows/common/data-files-fmt.md`（`$fmt` 代號寫法、`${fileDirname}`／`${gitRoot}`／`${gitParent}`／`${gitTop}`／`${env:NAME}` 變數，契約 `wf-table/1` 附錄）→ kernel-owned，直接加。
- `workflows/common/data-files.md` 連結段加一條指向它 → kernel-owned，整檔覆蓋。
- `tools/tabledb.py`（新指令 `fmt FILE`；`links`／`check`／`open`／`resolve` 展開 `$fmt`、`get`／`find`／`grep` 原樣回傳）、`tabledb_links.py`、`fix_moved_links.py`（搬檔時 `$fmt` 值以同一代號重寫）與新模組（如 `tabledb_fmt.py`、`fix_moved_links_fmt.py`）→ kernel-owned，複製到專案 `tools/`；`wf-init.sh` 自動複製。
- 新增 `tools/fmt-vars.json`（契約 `wf-fmt-vars/1`：變數名→算法、說明、aliases；**解析器不寫死變數名**，名字之後可換）→ kernel-owned，隨 `wf-init.sh` 複製；專案自加變數放 `tools/fmt-vars.local.json` → project-owned，升級不碰；`tabledb.py fmt --vars` 印合併後的表。**手動覆蓋 .py 升級的專案要記得一併複製 `fmt-vars.json`**，缺它一用 `$fmt` 就報 missing。
- `STRUCTURE.md` 資料檔慣例一句補充 `$fmt` 代號 → kernel-owned，整檔覆蓋。
- `AGENTS.md` 版本戳 → v0.4 → project-owned。
- `workflows/common/README.md` 加 data-files-fmt 列 → project-owned。
- `README.md`／`IMPORT.md`／`examples/` 同步（本 repo 自己的）。

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

## v0.2 (2026-08-29) 與更早

v0.2 依 2026-08-29 的 31 條改進提案全面重構：`DEV-GUIDE.md` 改名 `STRUCTURE.md`；tick／routines／schedule 與 `inbox/` 移出 kernel 成 `flavors/{heartbeat,multi-agent}`；鐵律 2 改成「不可逆或對外動作要有**授權來源**」；`AGENTS.md` 縮到 ≈1.5 KB 並加版本戳；新增 `wf-init.sh`／`wf-lint.sh`、`workflows/{TEMPLATE.workflow,planning,decisions}.md`、`common/user.md` 與 teaching／research／ops 三個 flavor；文件改為 agent 工具中立（`CLAUDE.md`／`.claude/` 降級成適配層）。v0.1（2026-08-28 以前）是 `template/` + `flavors/{dev,knowledge}`，kernel 還含 tick／routines／schedule 與 inbox，無版本戳。**完整條列**：`git show a2a4077:CHANGELOG.md`。
