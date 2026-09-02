# Kami — 排版產品太重，vendor 不了就用 submodule 掛外部

[investigation](../README.md)

- **問題**：外部 skill `tw93/Kami`（markdown 排版成履歷／白皮書／投影片／landing page 的完整生成管線）能不能整合進本 repo？

- **方法**：讀評估報告（`reports/kami-caveman-stopslop.md`）第一節，檢查整包體積、8 KB 上限是否超標、授權、相依與連外行為，並跟本 repo 既有的 `skills/markdown-html-slides`／`html-slides-shared-assets` 比對定位。

- **發現**：
  - 整包 147 MB／314 檔（不含 `.git`）；光兩支中文字體就佔 37 MB，另有多國 `index-*.html`、展示 PNG、PDF。
  - 排除 `assets/`、`dist/`、`.git` 後，`references/`＋`scripts/` 底下仍有 **52 個文字檔超過 8192 bytes**：`SKILL.md` 本身 44,679 bytes（近 5.5 倍上限）、`references/design.md` 83 KB、`scripts/checks.py` 67 KB、`references/production.md` 47 KB——超標的是產品核心邏輯本身，不是可以拆一兩檔就過關的量級。
  - 授權 **MIT**（Copyright 2026 Tw93），本 repo 是 **CC0 1.0**；逐檔複製會在 CC0 repo 裡插入帶條件的 MIT 區塊。
  - 執行需要 Node（MathJax 轉譯）與 Python 3；`scripts/check-update.sh` 明文「任務開始時執行」，每 session 至少打一次 `https://github.com/tw93/Kami/releases/latest` 查新版（不上傳使用者內容，失敗靜默），跟先前否決的 archify／dashi-ppt-skill 是同一套「每 session 至少一次連外」設計。
  - 跟本 repo 兩個現有 CC0 skill 在「markdown 轉簡報／HTML」上功能重疊，但 Kami 是完整品牌化排版產品（專屬字體＋四層品牌設定檔），量級跟本 repo 的輕量骨架差一個數量級。
  - 報告原本的建議是 (e) 只放 README 外部連結，理由是「vendor 就得為 `skills/` 開 8 KB 豁免，等於拆掉 `wf-lint --self` 的機械保證」——這個顧慮在 submodule 方案下不成立，因為 submodule 內容本來就不是本 repo 的檔案。

- **結論**：**不 vendor**，改以 **git submodule 掛在 `skills/external/kami/`**：上游檔案原樣保留、授權留在上游（不混入 CC0 主 repo，解決 MIT/CC0 衝突）、不受本 repo 8192 bytes 契約約束（`wf-lint --self` 不掃 submodule 內容，52 個超標檔與 44 KB 的 SKILL.md 因此不是問題）、`wf-init.sh` 導入新專案時不複製（147 MB 體積與每 session 連外行為不會預設帶進每個使用者的專案，要用才自己拉 submodule）。比純 README 連結多一層「repo 裡有位置可指」的可見度，又不需要為它破壞現有的體積與授權保證。

- **來源**：https://github.com/tw93/Kami （MIT License, Copyright 2026 Tw93）；評估日期：2026-09-02。
