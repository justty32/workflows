# 第 5 位：repo 工程品質 + 唱反調（什麼該砍）

量化基準（bash 實測，2026-08-29）：kernel `template/` 全部 md 共 **35,256 bytes**；其中定期喚醒四檔（tick / routines / schedule / wf-tick）**9,749 bytes（28%）**、inbox 三檔 **7,166 bytes（20%）**——兩個「可選」機制合計佔 kernel **48%**。repo 根沒有 LICENSE、CHANGELOG、`.github/`、`docs/`、`examples/`、`.gitignore`。

## A. repo meta

### A1. 沒有 examples/：看不到「長好的樣子」
- 問題：模板通篇是 `{{}}` 與〔模板說明〕，讀者永遠在看骨架，沒有一個「填好、刪乾淨」的成品可對照。這是導入時最大的認知成本（「填完到底長怎樣？」）。
- 建議：加 `examples/dev-minimal/` 與 `examples/knowledge-minimal/`，各是一個真實合併完成、佔位符填成一個假專案（如「todo-cli」「日文學習筆記」）的成品，30 行以內的 AGENTS.md 就夠。README 導入步驟加一句「先看 examples/ 再動手」。
- 優先級：**高**。

### A2. 沒有 LICENSE
- 問題：GitHub 公開 repo 沒授權條款 = 法律上他人不能複製使用，與「模板給人套用」的目的直接矛盾。
- 建議：加 MIT 或 CC0（純文檔模板 CC0 更省事）。一分鐘的事。
- 優先級：**高**（成本極低）。

### A3. 沒有版本號，導入的專案無從得知自己用哪版
- 問題：kernel 已經歷 kernel/flavor 拆分、inbox、tick 三次結構性改版，既有導入專案無法知道落後多少、也無法 diff 升級。
- 建議：`template/AGENTS.md` 尾端加一行 HTML 註解 `<!-- wf-kernel v0.3 (2026-08-29) -->`（agent 不會讀進 context，人可 grep），配合根目錄 `CHANGELOG.md`（每次 kernel 改版一行：改了哪個檔、既有專案要不要跟）。git tag 同步打。
- 優先級：**中**。

### A4. CI：一個 link check + 殘留檢查就夠，別多
- 問題：flavor 內的連結「照合併後佈局寫」，在本 repo 是預期壞掉的（README 明說）——這意味著一般 markdown link checker 會全紅、無法直接用。目前完全沒有自動檢查。
- 建議：一支 `scripts/check.sh`（不一定要 GitHub Actions）：① `template/` 內部連結必須全部解析；② `flavors/` 連結以「合併後」路徑模擬（把 `flavors/X/workflows` 映射到 `template/workflows` 後檢查）；③ 統計 `{{` 與〔模板說明〕數量作為「導入時要處理幾處」的提示。GitHub Actions 只跑這支腳本。別做更多（spell check、lint 都是過度工程）。
- 優先級：**中**。

### A5. README 沒英文版
- 問題：目標讀者顯然是作者自己＋中文 Claude Code 使用者；模板內容（writing.md 的繁簡條款、參考作者）本來就強綁繁中。英文版只有 README 而 kernel 全中文，會讓英文讀者導入後全是中文，反而誤導。
- 建議：**不做** README.en.md。改在 README 第一段加一句英文 one-liner 說明「this template is written in Traditional Chinese; the structure is language-agnostic」即可。
- 優先級：**低**。

### A6. repo 自己沒吃狗糧：根目錄雜亂、無 AGENTS.md
- 問題：根目錄有 `README.md`、`non-invasive-import.md` 平鋪，沒有 `AGENTS.md`、`INDEX`、`docs/`。模板自己宣揚「雜亂即分類」「durable 知識歸層」，卻把「非侵入式導入」這種導入細節攤在頂層；未來加更多導入變體（升級、多 flavor 合併、examples 說明）會繼續平鋪。
- 建議：開 `docs/`（`docs/non-invasive-import.md`、本次改進提案也放這），README 只留連結。另加一份極薄的根 `AGENTS.md`（5 行：這是模板 repo、改 kernel 要同步 README 表、flavor 連結按合併後寫、跑 `scripts/check.sh`）——這正是模板主張的「薄路由器」，既示範又實用。不必套完整 kernel（SESSION-LOG 等對模板 repo 沒意義）。
- 優先級：**中**。

### A7. 殘留字樣
- 問題：grep skyrim / modforge 無殘留（乾淨）；但 `template/workflows/inbox/CONTACTS.md:12` 範例寫 `~/repo/moddings/rimworld/`，是作者個人路徑洩漏，對他人無意義。
- 建議：換成中性範例（`~/repo/backend/inbox/`、`~/notes/ops/inbox/`）。
- 優先級：**低**。

## B. 唱反調：該砍 / 該縮

### B1. 定期喚醒（tick / routines / schedule / wf-tick）應移出 kernel
- 問題：佔 kernel 28%。內容高度特定：routines 內嵌 Windows PowerShell 時區指令、「每天上班 09:00 開工盤點 docker ps」「EOD 16:30 收尾 push」——這是作者的 ops 日常，不是領域中立骨架。且 `WORKFLOWS.md` 說它「不屬任一 flavor、kernel 一律有」，隨後又說「整套用不到就刪」——「一律有」與「可刪」自相矛盾。routines 的 EOD 範例「收尾 push」還直接與 AGENTS 鐵律 2「未經確認不 push」相撞。
- 建議：抽成 `flavors/heartbeat/`（或 `flavors/ops/` 的一部分），WORKFLOWS.md 的「定期喚醒」整節改為一行「要定期喚醒→合 heartbeat flavor」。kernel 少 10KB，且「kernel = 必要且中立」的宣稱才成立。
- 優先級：**高**。

### B2. inbox 對單人使用者是純負擔，也該出 kernel
- 問題：佔 kernel 20%，三處（AGENTS、INDEX、WORKFLOWS）都要解釋「三軸活狀態」並附「可選，用不到整包刪」。單人單 session 專案（模板的多數受眾）導入後要在 4 個檔刪 6 段文字才乾淨，忘了刪就永遠帶著一個空 `inbox/` 與一段 email 比喻。「可選但常駐 kernel」違反 README 自己說的「只複製你要的那包，不必刪」。
- 建議：同 B1，抽成 `flavors/multi-agent/`（inbox + CONTACTS + TEMPLATE.letter）。kernel 活狀態回到兩軸（進度 / 待使用者），第三軸由該 flavor 的合併步驟「貼一行進 AGENTS / WORKFLOWS」加回。
- 優先級：**高**。

### B3. 核心思想重述四處，改成 single source
- 問題：grep 實測「只指向下一層」「README＝入口 / INDEX＝結構」「open-only 完成即刪」「膨脹即拆」在 README、AGENTS、INDEX、WORKFLOWS、DEV-GUIDE、SESSION-LOG 各出現 1–3 次。AGENTS.md（3.8KB）有整段「分層思想」在講原則而非路由，與它自己「只做路由、durable 細節不寫這裡」互相打臉。重複的代價：改一處原則要同步五處，模板已出現措辭漂移（「完成即刪除」「完成即移除」「完成即刪」）。
- 建議：原則只活在一處——`DEV-GUIDE`（改名後，見 B4）的開頭「原則」節。AGENTS.md「分層思想」段縮成兩行（樹圖 + 「原則見 X」）+ 鐵律；INDEX / WORKFLOWS / SESSION-LOG 的重述句全刪只留連結。repo README 保留「一分鐘版」是唯一合理的重複（對外宣傳用）。
- 優先級：**中**。

### B4. DEV-GUIDE 改名 STRUCTURE.md
- 問題：kernel 標榜領域中立、有 knowledge flavor，但整理原則的檔名叫 DEV-GUIDE；knowledge 的 organize.md 還得解釋「這是 DEV-GUIDE 的非開發版」。名字誤導成本每天付。
- 建議：改 `STRUCTURE.md`（或 `GROWTH.md`），全域改連結（約 25 處，一次 sed）。順便承接 B3 的「原則 single source」角色。
- 優先級：**中**（與 B3 一起做才划算）。

### B5. `〔模板說明〕` 數量與位置該收斂
- 問題：kernel + flavor 共約 30 處〔模板說明〕散在各檔正文中，導入者要逐檔找。很多只是「用不到就刪」一句話，重複了 README 的總則。
- 建議：規則寫一次在 README（「凡 〔模板說明〕皆讀後刪；凡工作流用不到皆整檔刪＋刪派發列」），各檔只留真正檔案特有的說明；「用不到就刪」類全部拔掉。
- 優先級：**低**。

### B6. 不該砍的（反向確認）
- `CLAUDE.md` 一行轉址、`WAIT_USER` / `SESSION-LOG` 兩軸、四級成長軌跡、`Done when:`——這些短、中立、每個專案都用得到，是 kernel 的正當核心。砍完 B1/B2 後 kernel 約 18KB，才配得上「薄」。
