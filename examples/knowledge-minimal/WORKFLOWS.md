# WORKFLOWS — 工作流派發器

專案地圖 [INDEX.md](INDEX.md)｜結構整理 [STRUCTURE.md](STRUCTURE.md)

使用者說要做某件事 → **從派發表選工作流 → 讀它的入口檔**。細節都在入口檔，不在這裡。

## 派發表

### 知識工作 flavor

| 觸發（你說…）| 工作流 | 入口檔（先讀這個）| 分辨 |
|--------------|--------|-------------------|------|
| 「寫一篇東西：文章 / 筆記 / 文件 / 翻譯 / 貼文」 | **write** | [workflows/write.md](workflows/write.md) | 產物是**給人讀的成品** |
| 「幫我讀懂這份材料」「做個摘要」 | **digest** | [workflows/digest.md](workflows/digest.md) | 材料有限、讀完即止；產物是**摘要 + 出處索引** |
| 「在幾個選項間做決定」 | **decide** | [workflows/decide.md](workflows/decide.md) | 問的是「**選哪個**」；問「要不要做」走 planning |
| 「學一個主題，建立可延續的筆記」 | **learn** | [workflows/learn.md](workflows/learn.md) | 主題開放、會回訪；產物是**可回訪的筆記樹**（digest 的升級形態）|
| 「整理一堆資訊 / 檔案 / 筆記的結構」 | **organize** | [workflows/organize.md](workflows/organize.md) | 動的是**位置與分類**，不是內容 |

例：「幫我讀懂〜ばかりに 這條文法」——只要這次弄懂 → digest；要把它接進整套 N3 文法一路學下去 → learn。學習計畫要不要做、何時做（idea / roadmap）走 kernel 的 [planning](workflows/planning.md)，展開成步驟後落到 `plans/`。產出文字的工作流共用 [common/writing](workflows/common/writing.md)（文風）、材料導航共用 [common/info-map](workflows/common/info-map.md)。
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
