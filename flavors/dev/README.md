# 開發 flavor 包

← [repo README](../../README.md)（導航中樞）

程式開發專案用的工作流包。搭配 [`template/`](../../template/) 這個**共用 kernel** 一起用：kernel 提供分層樹的骨架（AGENTS / WORKFLOWS 骨架 / INDEX / DEV-GUIDE / 活狀態 / common/gotchas），本包只提供**開發類工作流**。

## 這個包有什麼

| 路徑 | 角色 |
|------|------|
| [WORKFLOWS.dev.md](WORKFLOWS.dev.md) | 開發 flavor 的**派發表片段**（貼進 kernel 的 WORKFLOWS.md）|
| [workflows/feature-dev/](workflows/feature-dev/README.md) | **資料夾型**工作流範例：功能開發 / 修 bug |
| [workflows/testing.md](workflows/testing.md) | **單檔型**工作流範例：跑測試 / 驗證 |
| [workflows/common/conventions.md](workflows/common/conventions.md) | 程式碼慣例 + 導航 index（code map）維護鏈；碰原始碼的工作流共用 |

## 怎麼合進 kernel（導入步驟）

1. 把 [`template/`](../../template/) 整包複製到你專案根目錄。
2. 把本包 **`workflows/` 底下所有檔案**複製進專案的 `workflows/`（`feature-dev/`、`testing.md` 直接落位；`common/conventions.md` 併入 `workflows/common/`）。
3. 打開專案的 `WORKFLOWS.md`，把 [WORKFLOWS.dev.md](WORKFLOWS.dev.md) 的內容**貼到那個 `〔佔位〕` 派發表區塊**，刪掉佔位提示。
4. 全域搜尋 `{{` 填佔位符；讀到 `〔模板說明〕` 照做後刪除該區塊。
5. 混合型專案（同時要知識類工作流）→ 再合 [knowledge 包](../knowledge/README.md)，兩張派發表都貼。

也可以直接把本 repo 路徑給 Claude Code，說「用開發 flavor 幫我的專案建立工作流」。
