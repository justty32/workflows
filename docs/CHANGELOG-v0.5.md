# CHANGELOG — v0.5 完整條列

[docs](README.md)｜[CHANGELOG](../CHANGELOG.md)

由 [CHANGELOG](../CHANGELOG.md) 拆出（母檔只留每版摘要與去向）：v0.5 改了哪些檔、**既有專案要不要跟**。更早的版本在 [CHANGELOG-history](CHANGELOG-history.md)。**本檔是 kernel repo 自用的變動記錄，不隨導入複製到專案。**

## v0.5 (2026-08-30)

來源專案一輪整理長出的通用做法回抽進 kernel：tidy 升成資料夾並附踩坑與管理線簡報、`WORKFLOWS.md` 加「可以跳流程」、`WAIT_USER` 拆法定死、`wf-lint` 加 `#錨點` 檢查；dev 包補 moving-things（搬檔六類斷裂）、「綠燈不等於有檢查」、真相層優先序，以及 analysis／patch 兩個可選工作流。

### kernel 與 dev 包

- `workflows/tidy/`（整夾）→ kernel-owned 覆蓋；既有專案要跟：刪舊 `workflows/tidy.md`、複製整夾，所有指向 `tidy.md` 的連結改成 `tidy/README.md`。
- `WORKFLOWS.md` → project-owned 手動套「可以跳流程」並改 tidy 入口；dev 有 refactor 時另改成資料夾入口並加 moving-things 派發列。
- `STRUCTURE.md` → kernel-owned 覆蓋：活狀態膨脹時拆 `session_logs/`／`wait-user/` 並只留導航，tidy 連結同步。
- `WAIT_USER.md` → project-owned 手動套：統一拆成 `wait-user/`，hub 留 `| 類別 | open | 清單 |` 導航表；既有專案要跟。
- `workflows/planning.md` → project-owned 手動套交接段；有 dev investigation 的專案補「只是要調查清楚」分流。
- `workflows/common/user.md` → project-owned 手動套：回答「要不要」時附可執行判準、門檻數字與後果。
- `workflows/common/data-files.md`／`data-files-fmt.md` → kernel-owned 覆蓋：改 tidy 路徑、補錨點檢查契約，並把 `git-top` 說明去專案化。
- `.claude/commands/wf-lint.md` → kernel-owned 覆蓋：新增 `BROKEN-ANCHOR` 說明。
- `tools/check_anchors.py`＋`tools/wf-lint.sh` → kernel-owned 覆蓋；**行為變更**：壞錨點計入 `broken`，原本綠燈的專案可能變紅，應修連結而不是關檢查。
- `tools/wf-lint.sh`＋`tools/check_anchors.py` → kernel-owned 覆蓋；修正 `broken` 透過 0–255 exit status 傳值造成的計數溢位（例如顯示 517 而非實際 `BROKEN` 行數），並讓 Markdown／資料檔掃描排除 `archive/`、reference/vendor 與 `.gitmodules` 宣告的 submodule；既有專案覆蓋後總數會回復精確且通常大幅下降。
- `tools/wf-init.sh` → kernel-owned 覆蓋：複製清單納入 `check_anchors.py`；本 repo 另加 `tools/test_check_anchors.py`。
- `AGENTS.md` 版本戳 → v0.5，project-owned 手動套；既有專案要跟。
- dev `workflows/refactor/`＋`moving-things.md` → flavor 檔直接覆蓋，既有專案刪 `refactor.md`、複製整夾並重寫連結。
- dev `testing.md`、`common/code-map.md`、`common/conventions.md`、`investigation.md` → project-owned 手動套四類測試、檢查器雙向驗證、真相層優先序與調查流程；既有專案要按實況填。
- dev 新增 `analysis.md`／`patch.md` → 可選工作流，需用才導入；`WORKFLOWS.dev.md`／`README.md` → flavor 內容表與派發表同步，既有專案依實際選用手動套。
- `examples/` → 同步 kernel v0.5 與已納入的 flavor；`README.md`、`IMPORT.md`、`docs/` 同步本 repo 說明。

### multi-agent 包

見 [CHANGELOG-v0.5-multi-agent.md](CHANGELOG-v0.5-multi-agent.md)（六條：dispatch 資料夾化、inbox 五通道與工具、team-model 四檔、ROSTER 團隊欄）。

### 2026-09-02 補

- `tools/wf-lint.sh`＋新增 `tools/wf-lint-checks.sh` → kernel-owned 覆蓋。修 percent-encoding 誤判：連結目標含空白或括號要寫成 `%20`／`%28`，原本拿原樣字串判存在，存在的檔會被重複報 `BROKEN`；新增 `link_exists()`，原樣找不到且含 `%` 才解碼再判，只判存在、不改寫文件。母檔已抵 8 KB，檢查函式與 `lint_dir` 同時拆到 `wf-lint-checks.sh` 由 `source` 載入——**既有專案要一併複製這支新檔**，`wf-init.sh` 與下表 kernel-owned 清單已納入。`test_wf_lint.py` 加 4 條。
- `workflows/tidy/gotchas.md` → kernel-owned 覆蓋，加「執行環境」段：`command -v` 只判存在不判可執行，假 `python3` shim 會讓 BIGLIST／錨點／資料檔靜默跳過卻仍綠燈；CRLF 的 `.sh` 在 Linux／WSL 跑不動、`wc -c` 每行多 1 byte，8 KB 上限在 Windows 工作區會誤報。
- multi-agent `workflows/team-model.md` 二、三節兩張表 → 預填默認值並標「2026/09/02 由 justty32 給出的個人判斷」，`{{}}` 清空；表仍 project-owned，換自己的模型清單就整張改掉。
- `README.md`（8058→6033）與 `tools/wf-init.sh`（7922→6365）拆檔，兩者都是本 repo 自用、不隨導入複製：README 的 `template/` 逐檔表與 `tools/` 工具表移到新增的 `docs/kernel-contents.md`，母檔留一行去向；`wf-init.sh` 的非侵入式連結改寫（`normalize`／`relpath`／改寫迴圈）移到新增的 `tools/wf-init-relink.sh`，由母檔 `source`，缺檔 FATAL 並 exit 2。順手把 `wf-lint --self` 的 repo 根連結掃描從寫死清單改成掃整個 `docs/*.md`。
- `tools/tabledb.py`（8133→5249）、`tabledb_fmt.py`（7979→6061）、`fix_moved_links.py`（7946→5373）→ kernel-owned 覆蓋。三支都貼著 8 KB 上限，各拆出一支同目錄模組：`Table` 資料模型 → 新增 `tabledb_table.py`；`$fmt` 的變數解析（`context`／`expand`／`names`／`canon`）→ 新增 `tabledb_fmt_expand.py`，`tabledb_fmt` 仍是對外門面；`fix_moved_links` 的掃描與搬移表（`git_root`／`files`／`load_moves`／`remap`／`old_dir_of`）→ 新增 `fix_moved_links_scan.py`，順手把 `scanned()`／`load_moves(specs)` 改成吃 `root` 參數、不再靠模組全域。**公開用法完全不變**（`from tabledb import load`、`tabledb.Table`、`tabledb_fmt.*`），三支新模組隨 `tools/*.py` 自動複製，既有專案覆蓋 `tools/` 時照舊整包拿。
