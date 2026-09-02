# INDEX — workflows 專案地圖

workflows = **通用分層工作流模板 repo（kernel ＋ flavor 包 ＋ 導入／檢查腳本）**。本檔只描述**頂層**：每列一句話＋連結；目錄內部複雜就放它自己的 README / INDEX。

## Repo 佈局

| 路徑 | 內容 |
|------|------|
| `template/` | 共用 kernel：整包被複製到目標專案的骨架（逐檔清單見 [docs/kernel-contents.md](../docs/kernel-contents.md)）|
| `flavors/` | 七個領域包（dev / knowledge / teaching / research / ops / heartbeat / multi-agent），各含 `workflows/` 與貼入片段 |
| `tools/`（repo 根）| 導入與檢查腳本：`wf-init.sh`、`wf-lint.sh`、資料檔與搬檔工具；職責逐支列在 [workflows/common/code-map.md](workflows/common/code-map.md) |
| `examples/` | kernel ＋ flavor 的合併成品（generated，CI 會檢查）|
| `docs/` | 本 repo 自己的文件（[docs/README.md](../docs/README.md)）|
| `skills/` | vendor 進來的 agent skill（受 8 KB 契約）；`skills/external/` 是 git submodule 掛的上游原樣資產，不受 8 KB 契約、`wf-init` 不複製 |
| `wf/` | **本 repo 自己導入的工作流**（非侵入式佈局，就是你正在讀的這層）|
| `workflows/` | 工作流（派發見 [WORKFLOWS.md](WORKFLOWS.md)；共享區 [workflows/common/](workflows/common/README.md)）|
| `.claude/commands/` | slash 指令適配層（可選）。Claude Code 只讀專案根的這層，非侵入式佈局也留在根；沒有 slash 機制的工具忽略本目錄，直接跑 `wf/tools/wf-lint.sh` |
| `wf/tools/` | 本層自帶的 kernel 工具副本：`wf-lint.sh`（檢查）、`tabledb.py`（資料檔 CRUD／連結）、`find_big_lists.py`、`fix_moved_links.py`；資料檔契約見 [workflows/common/data-files.md](workflows/common/data-files.md) |

## 頂層文件

| 檔案 | 角色 |
|------|------|
| [WORKFLOWS.md](WORKFLOWS.md) | 派發器：意圖 → 工作流入口 |
| [STRUCTURE.md](STRUCTURE.md) | 結構整理參考（被動）：分層、膨脹即拆、四級成長、archive、工作流形式 |
| [SESSION-LOG.md](SESSION-LOG.md) | 我的 open 進度 |
| [WAIT_USER.md](WAIT_USER.md) | 等使用者親自做 / 驗證的事 |
