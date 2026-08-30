# INDEX — todo-cli 專案地圖

todo-cli = **命令列待辦工具（Node.js + TypeScript），待辦資料存在 `~/.todo.json`**。本檔只描述**頂層**：每列一句話＋連結；某目錄內部複雜就在該目錄放它自己的 README / INDEX。

## Repo 佈局

| 路徑 | 內容 |
|------|------|
| `src/` | 原始碼三塊：`cli/`（解析 argv 與輸出）、`store/`（讀寫 `~/.todo.json`）、`commands/`（各子指令）；哪個檔負責什麼見 [code-map](workflows/common/code-map.md) |
| `tests/` | vitest 測試，子目錄對應 `src/` 的三個領域；怎麼跑見 [testing](workflows/testing.md) |
| `workflows/` | 工作流（派發見 [WORKFLOWS.md](WORKFLOWS.md)；共享區 [workflows/common/](workflows/common/README.md)）|
| `.claude/commands/` | slash 指令適配層（可選）：`/wf-lint` 等薄殼。Claude Code 為例，只讀專案根的這個目錄；沒有 slash 機制的工具忽略本目錄，直接跑 `tools/wf-lint.sh` |
| `tools/` | kernel 工具：`wf-lint.sh`（檢查）、`tabledb.py`（資料檔 CRUD／連結）、`find_big_lists.py`、`fix_moved_links.py`；資料檔契約見 [workflows/common/data-files.md](workflows/common/data-files.md) |
<!-- wf-insert:INDEX -->

## 頂層文件

| 檔案 | 角色 |
|------|------|
| [WORKFLOWS.md](WORKFLOWS.md) | 派發器：意圖 → 工作流入口 |
| [STRUCTURE.md](STRUCTURE.md) | 結構整理參考（被動）：分層原則、膨脹即拆、四級成長、archive 規則、工作流統一形式 |
| [SESSION-LOG.md](SESSION-LOG.md) | 我的 open 進度 |
| [WAIT_USER.md](WAIT_USER.md) | 等使用者親自做 / 驗證的事 |
| [workflows/TEMPLATE.workflow.md](workflows/TEMPLATE.workflow.md) | 新工作流入口檔的骨架 |
