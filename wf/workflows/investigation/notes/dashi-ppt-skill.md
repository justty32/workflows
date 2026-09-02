# dashi-ppt-skill — AGPL 加商業授權素材，不 vendor 改掛 submodule

[investigation](../README.md)

- **問題**：dashi-ppt-skill（離線 HTML／PPTX 簡報生成 skill）能不能 vendor 進本 repo 的 `skills/`？
- **方法**：讀原始 repo 的 LICENSE、`SKILL.md`、`project/assets/` 素材授權註解，比對本 repo 的 LICENSE（CC0）與 CI `wf-lint.sh --self` 的 8192 bytes 全域上限；把內容拆塊，逐塊判定該落哪個整合方案（vendor／README 外部連結／不收）。
- **發現**：
  - 授權為 AGPL-3.0（雙授權，另售商業授權），LICENSE 檔 35 KB；本 repo 是 CC0（公眾領域奉獻，承諾使用者無條件拿走），兩者不相容，不可 vendor。
  - 工作樹 60 MB、426 個 tracked 檔案（含 `.git` 達 86 MB）；相依 Node 20+、npm、playwright-core（需要 Chromium）；PPTX 匯出要起本機 HTTP 服務。
  - `project/assets/unicorn/*.json` 的 WebGL 素材附註明受 **Unicorn Studio 商業授權**，明文禁止未經授權的複製／再散布／用於競品——這批素材根本不受 AGPL 涵蓋，vendor 進來會直接違反第三方授權，且無合規路徑（比授權不相容更硬的否決點）。186 個字型檔的授權來源也未在原 repo 內交代。
  - 大量檔案超過本 repo CI 的 8192 bytes 上限：`SKILL.md` 27,382 bytes（3.3 倍）、`references/options.md` 8,993 bytes，另加數百個超標的 js/json/png/字型檔（`generated-metadata.js` 4.76 MB、`layout-manifest.json` 3.71 MB、186 個字型檔共 4.85 MB、theme03 3D 貼圖 16 MB）。`wf-lint.sh --self` 對全 repo（含 `skills/`）無差別掃描超過 8192 bytes 的檔案，vendor 會直接讓 CI 失敗。
  - `scripts/check_latest_version.mjs` 會在**每次任務結束前**對外部 registry（npmmirror、npmjs、raw.githubusercontent）發 HTTPS 請求，並要求把輸出貼進給使用者的最終回覆；與本 repo 鄰居 `flavors/teaching/workflows/study-site/` 明訂的「外部查詢預設 0、課程需可離線開啟」原則直接牴觸。
  - SKILL.md 的「先寫 goal.json 規格再生成」方法論本身可取，但本 repo `study-site/BUILD-SPEC.md` 已有更嚴格的同類版本；AGPL 授權下連散文摘要照抄都有風險，不值得單獨抽出。
- **結論**：**不 vendor，改以 git submodule 掛在 `skills/external/dashi-ppt-skill/`**。三個各自獨立即可否決 vendor 的理由——(1) AGPL-3.0 對上本 repo CC0，授權不相容；(2) `project/assets/unicorn/` 素材帶 Unicorn Studio 商業授權、明文禁止再散布，無合規路徑；(3) 60 MB／426 檔、數百個超過 8 KB 的檔案，機械上過不了 `wf-lint.sh --self`。submodule 同時解掉這三點：內容留在上游、**本 repo 不散布也不重新授權**（授權歸上游）、**不受 8 KB 契約約束**、`wf-init` 導入時**不複製**（是本 repo 自己的參考資產，不發給下游專案）。引用時仍要附授權、體積、連外行為的警語，讓使用者自行決定是否另外安裝。
- **來源**：https://github.com/chuspeeism/dashi-ppt-skill ，評估日期：2026-09-02。
