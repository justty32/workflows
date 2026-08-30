# planning — 想法的成熟管線（idea → roadmap → 詳規 → 執行）

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

一個想法從「要不要做」到「動工」的四個階段收在**同一條管線**，不拆成四個工作流——免得卡在「這算 idea 還是 roadmap」。

**何時用**：使用者說「記個想法」「這件事以後要做」「排進 roadmap」「幫我規劃」。
**何時不用**：三兩步的小事直接做；已有 spec / plan 且在動工 → 執行工作流（開發：feature-dev；非開發：plan-a-thing）。

## Done when

- idea / roadmap：下方對應表多一列，或既有列的狀態欄更新。
- 詳規：spec 有「方案 / 取捨」段、plan 有「步驟 / 驗證」段；動工完成後 plan 移 `archive/`。

## 階段

| 階段 | 回答的問題 | 落點 |
|------|-----------|------|
| **idea** | 要不要做？ | 下方「想法」表，一列一句 |
| **roadmap** | 會做，何時？ | 下方「roadmap」表 |
| **詳規** | 怎麼做？ | 開發：**spec**（討論後的方案）→ **plan**（動工前詳規），各一檔放 `planning/specs/`、`planning/plans/`——第一份出現時本檔升級成資料夾型。非開發：接 plan-a-thing 工作流（knowledge 包）|
| **執行** | — | 開發：feature-dev；非開發：plan-a-thing 的執行段 |

## 想法（要不要做）

| 想法 | 一句話 | 狀態（想想 / 會做→搬進 roadmap / 不做＋原因）|
|------|--------|--------------------------------------------|
| `todo due <id> <日期>` 到期日 | `Todo` 加一個可選 `due` 欄位，`list` 依到期日排序 | 想想——單人自用還沒真的需要，先看用一個月會不會想要 |

## roadmap（會做，何時）

| 事項 | 何時 / 順序 | 前提條件 |
|------|------------|---------|
| `todo list --json` 輸出 | 下一個小版本，接在 `done` 的結束碼修好之後 | `Todo` 型別欄位定案（動到就得同時改輸出格式與 `tests/cli` 的 fixture）|

## 交接

- 決定「為什麼選 A 不選 B」 → [decisions](decisions.md)。卡在使用者 → [WAIT_USER](../WAIT_USER.md) 一行；跨 session → [SESSION-LOG](../SESSION-LOG.md) 一行。
