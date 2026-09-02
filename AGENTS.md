# workflows — AI agent 專案備忘

workflows = **通用分層工作流模板 repo**：`template/` 是共用 kernel、`flavors/` 是七個領域包、`tools/` 是導入／檢查／資料檔腳本、`examples/` 是合併成品、`docs/` 是本 repo 自己的文件。人的入口 [README.md](README.md)；幫別人導入照 [IMPORT.md](IMPORT.md)。**本 repo 自己也用這套**（非侵入式導入，工作流全在 [wf/](wf/INDEX.md)）。本檔是最頂層路由器，只指向下一層；細節不寫這裡（分層原則見 [STRUCTURE.md](wf/STRUCTURE.md)）。

## 開場與入口

- 每個 session 先跑 `grep -c '^- \[' wf/SESSION-LOG.md wf/WAIT_USER.md`：非 0 才開 [SESSION-LOG.md](wf/SESSION-LOG.md)（進度）/ [WAIT_USER.md](wf/WAIT_USER.md)（等使用者）。
- **碰原始碼前**：慣例與 code map → [workflows/common/conventions.md](wf/workflows/common/conventions.md)、[workflows/common/code-map.md](wf/workflows/common/code-map.md)；環境與指令 → [workflows/dev-env.md](wf/workflows/dev-env.md)。
- **改 `template/`（kernel）或 `flavors/`（flavor 包）前**：同步義務與連結寫法有硬規矩，全在 [conventions.md](wf/workflows/common/conventions.md)，動手前讀完。
- **要你動手做事** → [WORKFLOWS.md](wf/WORKFLOWS.md) 依意圖派發，再讀該工作流入口檔。
- **想看專案結構** → [INDEX.md](wf/INDEX.md)。
- 使用者偏好與邊界 → [workflows/common/user.md](wf/workflows/common/user.md)。

## 鐵律（always-on，隨時適用）

1. 重構 / 整理**不改原意**：開發＝行為不變且驗證綠燈（`bash tools/wf-lint.sh --self`、`python -m pytest tools -q`）；非開發＝原意不變，照 `Done when:` 驗收。
2. **0 BROKEN 才算完成**：改完 md 一定跑 `bash tools/wf-lint.sh --self`（模板端）與 `bash wf/tools/wf-lint.sh --strict wf`（本 repo 自己的工作流），還有 BROKEN 就是沒做完。
3. **不可逆或對外的動作**（push、刪除、對外送出、動 DB）要有**授權來源**：使用者當場確認，或他親自登記在清單裡。都沒有就先問。
4. **條列走資料檔、導航留 md**：給 AI 消化的表／清單 >1 KB 存 `.json`／`.csv`（契約 `wf-table/1`，見 [data-files](wf/workflows/common/data-files.md)），用 `wf/tools/tabledb.py` 讀寫、不整份讀進 context；給人點的導航連結留 md。
5. **具體流程**在各工作流入口檔，不在頂層。

<!-- wf-kernel v0.5.1 (2026-09-02) -->
