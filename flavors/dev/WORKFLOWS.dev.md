### 開發 flavor

| 觸發（你說…）| 工作流 | 入口檔（先讀這個）|
|--------------|--------|-------------------|
| 「我想開發 / 修改某個功能」「**修 bug**」 | **feature-dev** | [workflows/feature-dev/README.md](workflows/feature-dev/README.md) |
| 「跑測試 / 驗證」 | **testing** | [workflows/testing.md](workflows/testing.md) |
| 「**記 / 查踩坑**」 | **gotchas** | [workflows/common/gotchas.md](workflows/common/gotchas.md) |

碰原始碼的工作流共用 [common/conventions](workflows/common/conventions.md)（程式碼慣例 + code map）。

> 〔模板說明〕以下是常見**開發類**工作流菜單，**需要哪個才加哪列**（入口檔在第一次用到時才建，從單檔開始長——見 [DEV-GUIDE](DEV-GUIDE.md) 四級成長軌跡）：
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
