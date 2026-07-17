# WORKFLOWS — 工作流派發器

← [AGENTS.md](AGENTS.md)｜專案地圖 [INDEX.md](INDEX.md)

你（使用者）說要做某件事 → **從這張表選對應工作流 → 讀它的「入口檔」→ 就知道要做什麼**。每個工作流的細節都在它自己的入口檔，不在這裡。

## 你想做什麼 → 用哪個工作流

> 〔模板說明〕本模板附**兩套 flavor**（同一套核心思想，只換工作流）：**開發**與**非開發 / 知識工作**。**保留你專案用得到的那套、刪掉另一套的列與檔**（見 [README](../README.md) 的 flavor 說明）。兩套可並存，混合型專案兩張表都留。

### 開發 flavor

| 觸發（你說…）| 工作流 | 入口檔（先讀這個）|
|--------------|--------|-------------------|
| 「我想開發 / 修改某個功能」「**修 bug**」 | **feature-dev** | [workflows/feature-dev/README.md](workflows/feature-dev/README.md) |
| 「跑測試 / 驗證」 | **testing** | [workflows/testing.md](workflows/testing.md) |
| 「**記 / 查踩坑**」 | **gotchas** | [workflows/common/gotchas.md](workflows/common/gotchas.md) |

碰原始碼的工作流共用 [common/conventions](workflows/common/conventions.md)（程式碼慣例 + code map）。

### 非開發 / 知識工作 flavor

規劃、寫作、閱讀消化、學習、決策、整理——借同一套分層思想，把「code map / testing」換成「導航 index / `Done when:` 驗收」。產出文字的工作流共用 [common/writing](workflows/common/writing.md)（文風）。

| 觸發（你說…）| 工作流 | 入口檔（先讀這個）|
|--------------|--------|-------------------|
| 「寫一篇東西：文章 / 筆記 / 文件 / 翻譯 / 貼文」 | **write** | [workflows/write.md](workflows/write.md) |
| 「讀長文 / 影片 / 一堆資料，做摘要與索引」 | **digest** | [workflows/digest.md](workflows/digest.md) |
| 「規劃一件事：活動 / 旅行 / 流程 / 任意非開發專案」 | **plan-a-thing** | [workflows/plan-a-thing.md](workflows/plan-a-thing.md) |
| 「在幾個選項間做決定」 | **decide** | [workflows/decide.md](workflows/decide.md) |
| 「學一個主題，建立可延續學習筆記」 | **learn** | [workflows/learn.md](workflows/learn.md) |
| 「整理一堆資訊 / 檔案 / 筆記的結構」 | **organize** | [workflows/organize.md](workflows/organize.md) |

> 〔模板說明〕以下是常見工作流菜單，**需要哪個才加哪列**（入口檔在第一次用到時才建，從單檔開始長——見 [DEV-GUIDE](DEV-GUIDE.md) 四級成長軌跡）：
> - **refactor**（重構 / 拆檔 / 整理結構）
> - **investigation**（調查 / 解讀外部系統 / 可行性研究）
> - **spec**（把一個 idea 討論成設計方案）
> - **plan**（把設計方案展開成動工計畫）
> - **idea**（記一個奇思妙想，不確定要不要做）
> - **roadmap**（記一件確定會做、不確定何時的事）
> - **tooling**（外部工具設定 / env var / 依賴）
> - **dev-env**（開發環境、fresh clone 後要做什麼、打包出貨）
>
> 若採用規劃類工作流，建議保留這條**規劃管線**（一個想法的成熟過程）：
> idea（要不要做？）→ roadmap（會做，何時？）→ spec（討論後方案）→ plan（動工前詳規）→ build（feature-dev）。

**都不符 → 看 [INDEX.md](INDEX.md)**（repo 頂層結構地圖）。

## 工作流的統一形式（規範）

所有工作流照同一套形式（細則見 [DEV-GUIDE](DEV-GUIDE.md)）：

**檔名規範**：
- **README** = 初入一個資料夾**先讀的入口／導引**（這資料夾在幹嘛、怎麼用）。
- **INDEX** = **描述該資料夾頂層結構**的索引（有哪些子項、各放什麼）。
- 小資料夾兩者可合一（README 兼述結構）；大到結構複雜時才分出獨立 INDEX。

形式：
- **資料夾型工作流**：
  - 一個**入口 README**（或主檔）——先讀它就知道這工作流在幹嘛、有哪些檔。
  - **`archive/`**：過時 / 被取代的文檔封存於此（保留脈絡、不在維護鏈）。
  - 視需要的 `gotchas.md`（踩坑）、`session-log.md`（本工作流 open 進度）。
- **單檔工作流**（還沒長成資料夾的那些）：一個 `.md` 同時是入口與內容；撐大了就照「[結構整理原則](DEV-GUIDE.md)」升級成資料夾型。到底有哪些工作流、各自入口在哪，看上面的派發表即可，不在這裡逐一點名（正面清單每次升級都會過期）。
- 入口檔本身膨脹 → 一樣照結構整理原則拆。

## 跨工作流的活狀態（repo 根）

- **進度**（還沒完成的 in-flight / open）→ [SESSION-LOG.md](SESSION-LOG.md)
- **待使用者親自做 / 驗證的**（實機環境 / 外部工具 / env / 權限）→ [WAIT_USER.md](WAIT_USER.md)
