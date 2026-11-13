# workflows — AI agent 專案備忘

workflows = **通用分層工作流模板 repo**：`template/` 是共用 kernel、`flavors/` 是七個領域包、`tools/` 是導入／檢查／資料檔腳本、`examples/` 是合併成品、`docs/` 是本 repo 自己的文件。人的入口 [README.md](README.md)；幫別人導入照 [IMPORT.md](IMPORT.md)。**本 repo 自己也用這套**（非侵入式導入，全在 `wf/`）。本檔是最頂層路由器，只指向下一層。

## 開場與入口

- 每個 session 先跑 `grep -c '^- \[' wf/SESSION-LOG.md wf/WAIT_USER.md`：非 0 才開 [SESSION-LOG.md](wf/SESSION-LOG.md)（進度）/ [WAIT_USER.md](wf/WAIT_USER.md)（等使用者）。
- 從 `wf/_index.json` 讀起：在 aos 裡用 `index_view`（path 給 `wf`），其他工具直接讀那個檔。做事看 `wf/workflows/_index.json` 選工作流，查知識看 `wf/knowledge/_index.json`。
- **碰原始碼前**：`wf/knowledge/conventions.json`、`wf/knowledge/code-map.json`；環境與指令 `wf/knowledge/dev-env.json`。
- **改 `template/` 或 `flavors/` 前**：同步義務與連結寫法全在 `wf/knowledge/conventions.json`，讀完再動手。
- 想看專案結構與分層原則 → `wf/knowledge/structure.json`；使用者偏好與邊界 → `wf/knowledge/user.json`。

## 鐵律（always-on）

1. 重構 / 整理**不改原意**：開發＝行為不變且驗證綠燈（`bash tools/wf-lint.sh --self`、`python -m pytest tools -q`）；非開發＝原意不變，照 `done_when` 驗收。
2. **檢查過才算完成**：改 `wf/` 以外的任何 md 或 `tools/`（`template/`、`flavors/`、`examples/`、`skills/`、`docs/`、根層 md）跑 `bash tools/wf-lint.sh --self`（CI 也跑），有 BROKEN 就是沒做完；改 `wf/` 跑 `python3 wf/tools/index_check.py wf`，problems 不是 0 就是沒做完。
3. **不可逆或對外的動作**（push、刪除、對外送出、動 DB）要有**授權來源**：使用者當場確認，或他親自登記在清單裡。都沒有就先問。
4. **內容走 json、給人看的才留 md**：細節見 `wf/knowledge/structure.json`。
5. **具體流程**在各工作流節點，不在頂層。

<!-- wf-kernel v0.5.1 (2026-09-02) -->
