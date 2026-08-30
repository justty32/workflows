# WORKFLOWS — 工作流派發器

[INDEX](INDEX.md)｜結構 [STRUCTURE](STRUCTURE.md)

使用者要做事 → **從派發表選工作流 → 讀它的入口檔**；細節都在入口檔。

## 派發表

〔導入判斷〕尚未貼入任何 flavor 派發表。用 `tools/wf-init.sh` 導入會自動貼入並刪除本行；手動導入則把 `flavors/<flavor>/WORKFLOWS.<flavor>.md` 的內容貼到本行位置。
<!-- wf-insert:WORKFLOWS -->

### kernel 內建

| 觸發（你說…）| 工作流 | 入口檔 |
|--------------|--------|--------|
| 「記 / 查踩坑」 | **gotchas** | [workflows/common/gotchas.md](workflows/common/gotchas.md) |
| 「整理 X」「封存過時的」「檔案太多／太雜」「太大要拆」 | **tidy** | [workflows/tidy.md](workflows/tidy.md) |
| 「記個想法」「以後要做」「排進 roadmap」「幫我規劃」 | **planning** | [workflows/planning.md](workflows/planning.md) |
| 「記個決定」「為什麼選 A 不選 B」 | **decisions** | [workflows/decisions.md](workflows/decisions.md) |
| 「我的偏好是…」「以後直接做 / 先問」 | **user** | [workflows/common/user.md](workflows/common/user.md) |

**都不符 → 看 [INDEX.md](INDEX.md)**。新開工作流 → 複製 [workflows/TEMPLATE.workflow.md](workflows/TEMPLATE.workflow.md) 並在上表加一列。要定期喚醒合 heartbeat 包、多 agent 協作合 multi-agent 包（都在模板 repo 的 `flavors/`）。

## 活狀態記哪裡（只列 open，完成即刪）

| 在等誰 | 記哪裡 |
|--------|--------|
| 等**使用者**做 / 驗證 / 決定 | [WAIT_USER.md](WAIT_USER.md) |
| 等**同 repo 另一個 session / fork** | [SESSION-LOG.md](SESSION-LOG.md) 一行 open |
| 等**別資料夾的 agent** | 信件軸：multi-agent 包提供（派發表有 inbox 才有）|
