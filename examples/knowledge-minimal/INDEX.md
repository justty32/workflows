# INDEX — jp-notes 專案地圖

jp-notes = **一個人的日文學習筆記庫，目標 JLPT N3**。本檔只描述**頂層**：每列一句話＋連結；某目錄內部複雜就在該目錄放它自己的 README / INDEX。

## Repo 佈局

| 路徑 | 內容 |
|------|------|
| `grammar/` | 文法筆記，一條文法一檔（檔名即文法本身，如 `〜ばかりに.md`）：接續、語氣、例句、來源 |
| `vocab/` | 單字表，按主題分檔（`travel.md`、`work.md`…），一列一個詞：`詞 \| 假名 \| 中譯 \| 例句` |
| `reading/` | 讀過的文章：一篇一檔，含原文出處、生詞、一段摘要 |
| `plans/` | 學習計畫，一份一檔（roadmap 排進來的事項在這裡展開成步驟）|
| `workflows/` | 工作流（派發見 [WORKFLOWS.md](WORKFLOWS.md)；共享區 [workflows/common/](workflows/common/README.md)）|
| `.claude/commands/` | slash 指令適配層（可選）：`/wf-lint` 等薄殼。Claude Code 為例，只讀專案根的這個目錄；沒有 slash 機制的工具忽略本目錄，直接跑 `tools/wf-lint.sh` |
| `tools/` | kernel 工具：`wf-lint.sh`（檢查）、`tabledb.py`（資料檔 CRUD／連結）、`find_big_lists.py`、`fix_moved_links.py`；資料檔契約見 [workflows/common/data-files.md](workflows/common/data-files.md) |
<!-- wf-insert:INDEX -->

哪份材料餵哪一條線，見 [workflows/common/info-map.md](workflows/common/info-map.md)。

## 頂層文件

| 檔案 | 角色 |
|------|------|
| [WORKFLOWS.md](WORKFLOWS.md) | 派發器：意圖 → 工作流入口 |
| [STRUCTURE.md](STRUCTURE.md) | 結構整理參考（被動）：分層原則、膨脹即拆、四級成長、archive 規則、工作流統一形式 |
| [SESSION-LOG.md](SESSION-LOG.md) | 我的 open 進度 |
| [WAIT_USER.md](WAIT_USER.md) | 等使用者親自做 / 驗證的事 |
| [workflows/TEMPLATE.workflow.md](workflows/TEMPLATE.workflow.md) | 新工作流入口檔的骨架 |
