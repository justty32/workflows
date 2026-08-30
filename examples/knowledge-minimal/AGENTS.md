# jp-notes — AI agent 專案備忘

jp-notes = **一個人的日文學習筆記庫：文法、單字、閱讀三條線的 Markdown 筆記，目標 JLPT N3**。本檔是最頂層路由器：只指向下一層，細節一律不寫這裡（分層原則見 [STRUCTURE.md](STRUCTURE.md)）。

## 開場與入口

- 每個 session 先跑 `grep -c '^- \[' SESSION-LOG.md WAIT_USER.md`：非 0 才打開 [SESSION-LOG.md](SESSION-LOG.md)（我的 open 進度）/ [WAIT_USER.md](WAIT_USER.md)（等使用者的事）。
- **碰筆記與材料前**：先查 [workflows/common/info-map.md](workflows/common/info-map.md) 找到相關那幾份，不要整個資料夾翻。
<!-- wf-insert:AGENTS -->
- **使用者要你動手做事** → [WORKFLOWS.md](WORKFLOWS.md)：依意圖派發到工作流入口，再讀該入口檔。
- **想看專案長怎樣** → [INDEX.md](INDEX.md)。
- 使用者偏好、確認邊界、分支慣例 → [workflows/common/user.md](workflows/common/user.md)。

## 鐵律（always-on，任何工作流任何時候都遵守）

1. 重構 / 整理**不改原意**：本專案無自動驗證；對照該工作流的 `Done when:` 逐條驗收，再跑 `tools/wf-lint.sh` 檢查連結與檔案大小（Claude Code 可用 `/wf-lint`）。
2. **不可逆或對外的動作**（push、刪除、對外送出、動 DB）必須有**授權來源**：使用者當場確認，或使用者**親自登記**在清單裡的項目。兩者都沒有就先問。
3. **條列走資料檔、導航留 md**：給 AI 消化的表／清單 >1 KB 存 `.json`／`.csv`（契約 `wf-table/1`，見 [data-files](workflows/common/data-files.md)），用 `tools/tabledb.py` 讀寫、不整份讀進 context；給人點的導航連結留 md。
4. 各工作流的**具體流程在它自己的入口檔**，不在頂層。
5. 日文原文**照抄不改**：例句、單字、假名、漢字一律照來源，不自造也不「順一下」；沒把握的讀音或用法標 `?` 並留成待答問題，不要猜了就寫死。

<!-- wf-kernel v0.4.1 (2026-08-30) -->
