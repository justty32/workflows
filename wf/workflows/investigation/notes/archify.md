# archify — MIT 但是一支要跑的 Node 程式，走 submodule 不 vendor

[investigation](../README.md)

- **問題**：archify（JSON IR → 自包含互動 HTML/SVG 圖表的 CLI ＋ 渲染器）能不能整合進本 repo，該落在哪一層？
- **方法**：讀上游 LICENSE、`SKILL.md`、`bin/`／`renderers/`／`brand-marks/` 的檔案清單與大小，量出「skill 執行真正需要」的最小子集；比對本 repo 的 8192 bytes 契約、`wf-lint --self` 的掃描範圍、以及 effective-html 的 `html-diagram` 與 dev flavor `code-map` 的定位。
- **發現**：
  - 授權 MIT（fork 自 Cocoon-AI/architecture-diagram-generator），與本 repo CC0 相容——**否決 vendor 的不是授權，是體積與型態**。
  - 它不是 markdown 指引集合，而是**一套 Node.js 程式庫**：整個 repo 40 MB／471 檔；實際 skill 目錄 7.5 MB／192 檔；扣掉測試與範例的**最小執行子集仍有 2.3 MB／55 檔，其中 29 檔超過 8192 bytes**。
  - 超標的都是執行核心、不是可丟的文件：`SKILL.md` 16,396 bytes（2 倍上限）、`assets/template.html` 678 KB、`generated-validators.mjs` 430 KB、`workflow-compiler.mjs` 171 KB、`bin/archify.mjs` 71 KB。拆不動。
  - 相依：執行期**零 npm 套件**（只用 Node 內建模組，要求 Node ≥18）；`ajv`／`parse5`／`saxes`／`simple-icons` 只是建置期產碼用的 devDependencies，產物已 commit。可選的 `visual-check` 會找系統既有 Chrome 走 CDP 截圖，不自動下載瀏覽器。
  - 連外：`SKILL.md` 要求每個工作階段跑一次 `scripts/check-update.mjs`，對上游 GitHub Pages 查版本，有 schema 驗證、大小上限、timeout 與 `--ack`，且明講不自動下載安裝。比 dashi 的「每次任務結束都連外」克制，但仍與 teaching flavor `study-site` 的離線預設同向牴觸。
  - 第三方素材：107 個品牌商標圖示多數來自 Simple Icons 16.28.0（CC0，但上游自陳 CC0 只涵蓋收錄工作、不涵蓋底層商標），archify 已誠實揭露。**不是禁止再散布**，屬須註明的灰色地帶。
  - 與既有工作流不衝突：`html-diagram` 是「agent 自己手畫」的純方法論，archify 是「寫 JSON IR 交給渲染器編譯」；`code-map`／`info-map` 產出的是給 agent 讀的索引文字，層次不同。archify 多出品牌商標庫、Before/Delta/After 架構比對、WebM／PNG 匯出、視覺回歸檢查。
- **結論**：**不 vendor，改以 git submodule 掛在 `skills/external/archify/`**。理由：檔案上 vendor 機械上過不了 `wf-lint --self`（最小子集就有 29 檔超標），而 submodule 保留上游原樣、授權與商標揭露都歸上游、**不受本 repo 8 KB 契約約束**、`wf-init` 導入時**不複製**（它是本 repo 自己的參考資產，不是要發給下游專案的東西）。同時排除三個曾考慮的落點：進 kernel（太領域特定）、併入 `code-map`／`info-map`（產物層次不同，會讓零外部依賴的 flavor 包長出 Node 依賴）、在 `skills/` 開一支「教你去 `npx skills add`」的薄指引 skill（會讓 `skills/` 的 vendor 契約定義模糊，且等於把「執行期從網路裝未審查程式碼」包裝成本 repo 背書的標準流程）。README 引用它時要一併註明 Node ≥18、每階段連外查版本、商標圖示的授權界線。
- **來源**：https://github.com/tt-a1i/archify ，評估日期：2026-09-02。
