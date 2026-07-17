# 知識工作 flavor 包

← [repo README](../../README.md)（導航中樞）

非開發 / 知識工作專案用的工作流包（寫作、閱讀消化、規劃、決策、學習、整理）。搭配 [`template/`](../../template/) 這個**共用 kernel** 一起用：kernel 提供分層樹的骨架，本包只提供**知識類工作流**——把開發 flavor 的「code map / testing」換成「導航 index / `Done when:` 可觀察驗收」。

## 這個包有什麼

| 路徑 | 角色 |
|------|------|
| [WORKFLOWS.knowledge.md](WORKFLOWS.knowledge.md) | 知識 flavor 的**派發表片段**（貼進 kernel 的 WORKFLOWS.md）|
| [workflows/write.md](workflows/write.md) | 寫文章 / 筆記 / 文件 / 翻譯 / 貼文 |
| [workflows/digest.md](workflows/digest.md) | 讀長文 / 影片 / 一堆資料，做摘要與索引 |
| [workflows/plan-a-thing.md](workflows/plan-a-thing.md) | 規劃活動 / 旅行 / 流程 / 任意非開發專案 |
| [workflows/decide.md](workflows/decide.md) | 在幾個選項間做決定 |
| [workflows/learn.md](workflows/learn.md) | 學一個主題，建立可延續學習筆記 |
| [workflows/organize.md](workflows/organize.md) | 整理一堆資訊 / 檔案 / 筆記的結構 |
| [workflows/common/writing.md](workflows/common/writing.md) | 寫作風格；產出給人讀的文字時共用 |

六個工作流是**菜單**，用不到的整列＋整檔刪掉——不必全留。

## 怎麼合進 kernel（導入步驟）

1. 把 [`template/`](../../template/) 整包複製到你專案根目錄。
2. 把本包 **`workflows/` 底下你要的檔案**複製進專案的 `workflows/`（用不到的工作流別複製；`common/writing.md` 併入 `workflows/common/`）。
3. 打開專案的 `WORKFLOWS.md`，把 [WORKFLOWS.knowledge.md](WORKFLOWS.knowledge.md) 的內容**貼到那個 `〔佔位〕` 派發表區塊**（刪掉你沒複製的工作流那幾列），再刪掉佔位提示。
4. 全域搜尋 `{{` 填佔位符；讀到 `〔模板說明〕` 照做後刪除該區塊。
5. 混合型專案（同時要開發類工作流）→ 再合 [dev 包](../dev/README.md)，兩張派發表都貼。

也可以直接把本 repo 路徑給 Claude Code，說「用知識 flavor 幫我的專案建立工作流」。
