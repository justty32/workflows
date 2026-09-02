# effective-html — MIT、零相依，收進 skills/

[investigation](../README.md)

- **問題**：effective-html（六個 HTML artifact skill：`html`、`design-artifact`、`html-wireframe`、`html-prototype`、`html-plan`、`html-diagram`）能不能 vendor 進本 repo 的 `skills/`，該收哪些部分？
- **方法**：讀原始 repo 的 LICENSE、六個 `SKILL.md` 與 `references/*.md`，比對本 repo 的 CC0 LICENSE、CI `wf-lint.sh --self` 的 8192 bytes 上限、以及 `lint_dir` 連結檢查／QUERYCMD 是否涵蓋 `skills/`；再跟本 repo 既有的 `markdown-html-slides` 系列 skill 做重疊與互補比對。
- **發現**：
  - 授權為 MIT（(c) 2026 plannotator），與本 repo CC0 相容——只需保留著作權聲明，比 AGPL 溫和很多。
  - repo 整體含 `.git` 45 MB、工作樹 25 MB，但那大半是 `site/`（Next.js 文件站 23 MB）＋ `examples/` ＋ banner 圖；真正要 vendor 的 `skills/` 只有 82 KB、17 個檔，內容約 51 KB 純 markdown。
  - 零執行期相依：六個 skill 全是 markdown ＋ `agents/openai.yaml` 元資料，沒有 HTML 範本、CSS、JS、圖片；唯一選用的 shell 工具是 `design-artifact` 裡的 `tot` CLI，且明文要求使用者同意才裝。
  - 8 KB 檢查：17 個檔中只有 `design-artifact/SKILL.md`（11,031 bytes）超過 8192 上限，其餘 16 檔全部 ≤ 6,625 bytes；`skills/` 本身不在 `lint_dir` 的連結檢查／QUERYCMD／BIGLIST 範圍內，只受 8 KB 全域上限約束。
  - 內容分層設計：`html` 當隱式路由器，`design-artifact` 管創意方向，`html-wireframe`／`html-prototype`／`html-plan`／`html-diagram` 各管一種保真度——「薄入口＋層層派發」的思想跟本 repo 現有設計同向。
  - 與既有 `markdown-html-slides` 系列比較：重疊部分（排版原則、QA 心法）其實是同一件事的不同抽象層，不算真重複；互補部分是 effective-html 完全沒碰過「簡報產線」與「多檔集合去重」，而本 repo 系列也完全沒有 wireframe／prototype／plan／diagram 四個場景，兩邊互補遠大於重疊。
  - 發現一個需要處理的路由衝突：`html/SKILL.md` 原文把「presentations」也列入自己的路由範圍，若不修正，「幫我做份簡報」可能被 `html` 接走而非導去 `markdown-html-slides`，產出的 deck 會缺少 `deck-theme`／`slides-core`／`slides-runtime` 三個 marker，導致 `html-slides-shared-assets` 之後靜默抽不出共用資產、且不會報錯。
- **結論**：收。已 vendor 進本 repo 的 `skills/`（六個 skill 目錄＋著作權聲明見 `skills/LICENSES/effective-html.MIT`），並把過大的 `design-artifact/SKILL.md` 拆成 `SKILL.md` ＋ `references/` 使其低於 8 KB。收錄的原則：(1) MIT 授權相容、零執行期相依、體積小；(2) 「薄入口＋分層派發」的路由設計跟本 repo 既有結構同向；(3) 與既有簡報類 skill 互補大於重疊，補上 wireframe／prototype／plan／diagram 四個本 repo 原本沒有的場景。收錄時務必同步修正 `html/SKILL.md` 的路由段，把簡報／slide deck 導去 `markdown-html-slides`，避免路由衝突造成 silent failure。
- **來源**：https://github.com/plannotator/effective-html ，評估日期：2026-09-02。
