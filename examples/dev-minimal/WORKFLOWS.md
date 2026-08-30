# WORKFLOWS — 工作流派發器

專案地圖 [INDEX.md](INDEX.md)｜結構整理 [STRUCTURE.md](STRUCTURE.md)

使用者說要做某件事 → **從派發表選工作流 → 讀它的入口檔**。細節都在入口檔，不在這裡。

## 派發表

### 開發 flavor

碰原始碼的工作流共用 [common/conventions](workflows/common/conventions.md)（寫碼慣例）與 [common/code-map](workflows/common/code-map.md)（哪個檔負責什麼）。

| 觸發（你說…）| 工作流 | 入口檔（先讀這個）|
|--------------|--------|-------------------|
| 「開發 / 修改某個功能」「**修 bug**」 | **feature-dev** | [workflows/feature-dev/README.md](workflows/feature-dev/README.md) |
| 「跑測試 / 驗證」「這樣改有沒有壞」 | **testing** | [workflows/testing.md](workflows/testing.md) |
| 「重構 / 拆檔 / 整理結構」（行為不變）| **refactor** | [workflows/refactor.md](workflows/refactor.md) |
| 「環境怎麼裝」「fresh clone 後要做什麼」「指令是什麼」 | **dev-env** | [workflows/dev-env.md](workflows/dev-env.md) |
| 「討論方案」「寫動工計畫」（spec / plan）| **planning**（kernel 管線的後兩段）| [workflows/planning.md](workflows/planning.md) |
<!-- wf-insert:WORKFLOWS -->

### kernel 內建（不分 flavor）

| 觸發（你說…）| 工作流 | 入口檔（先讀這個）|
|--------------|--------|-------------------|
| 「記 / 查踩坑」 | **gotchas** | [workflows/common/gotchas.md](workflows/common/gotchas.md) |
| 「整理 X」「封存過時的」「檔案太多／太雜」「太大要拆」 | **tidy** | [workflows/tidy.md](workflows/tidy.md) |
| 「記一個想法」「這件事以後要做」「排進 roadmap」「幫我規劃」 | **planning** | [workflows/planning.md](workflows/planning.md) |
| 「記一個決定」「當初為什麼選 A 不選 B」 | **decisions** | [workflows/decisions.md](workflows/decisions.md) |
| 「我的偏好是…」「以後這種事直接做 / 先問」 | **user** | [workflows/common/user.md](workflows/common/user.md) |

**都不符 → 看 [INDEX.md](INDEX.md)**。要新開一個工作流 → 複製 [workflows/TEMPLATE.workflow.md](workflows/TEMPLATE.workflow.md)，在上表加一列。要定期喚醒 → 合 heartbeat 包；多個 agent 協作 → 合 multi-agent 包（各包在模板 repo 的 `flavors/`）。

## 活狀態：卡住的事記哪裡（只列 open，完成即刪）

| 在等誰 | 記哪裡 |
|--------|--------|
| 等**使用者**親自做 / 驗證 / 決定 | [WAIT_USER.md](WAIT_USER.md) |
| 等**同 repo 的另一個 session / fork** | [SESSION-LOG.md](SESSION-LOG.md) 一行 open |
| 等**別資料夾的 agent** | 信件軸——由 multi-agent 包提供（派發表有 inbox 才算存在這軸）|
