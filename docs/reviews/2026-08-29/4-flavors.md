# 角度 4：flavor 包（dev / knowledge）的內容品質與完整度

量測：dev 包工作流合計 4.8 KB（feature-dev 2018 B、testing 862 B、conventions 1945 B）；knowledge 包六個工作流合計 7.2 KB，另 writing.md 一檔就 5.2 KB。`Done when:` 出現在 knowledge 六檔全部、dev 兩檔零次；「何時不用」段只有 knowledge 四檔有（decide、organize 也沒有）。

### 1. dev 派發表列了 8 個「只有名字沒有檔」的工作流，補 3 個最小骨架、其餘明說「合併進誰」
**問題**：`WORKFLOWS.dev.md` 菜單列 refactor / investigation / spec / plan / idea / roadmap / tooling / dev-env，但 `workflows/` 裡一個都沒有。agent 看到「需要哪個才加哪列」時，得自己從零發明格式，結果每個專案長出不同樣子——正好違反 kernel 想統一形式的初衷。
**建議**：
- 補三個單檔骨架（各 ≤ 1 KB）：`refactor.md`（觸發＝DEV-GUIDE 門檻超標；流程＝先定 Done when「行為不變 + 驗證綠燈」→ 拆 → 跑驗證）、`investigation.md`（產出＝一份可歸檔的調查筆記，模板：問題／方法／發現／結論／來源）、`dev-env.md`（AGENTS.md「開發環境」段已經指名要它，卻沒給檔）。
- 把 idea / roadmap / spec / plan 四個明說為**一條規劃管線一個資料夾** `planning/`（單 README + `ideas.md`、`roadmap.md`、`specs/`、`plans/` 長出來才建），不要四個獨立工作流——它們是同一個想法的四個成熟階段，分四檔會讓 agent 在「這算 idea 還是 roadmap」上卡住。
- tooling 併入 dev-env（工具設定、env var、依賴本來就是環境的一部分）。
**優先級**：高。

### 2. 兩包入口檔格式不一致，kernel 應提供 `TEMPLATE.workflow.md`
**問題**：knowledge 六檔都有 `Done when:` + 流程 + 「何時不用」；dev 的 feature-dev 與 testing 兩者都沒有 `Done when:`、沒有「何時不用」，feature-dev 卻有「內容」表（knowledge 沒有）。WORKFLOWS.md「工作流的統一形式」只規範檔名與資料夾型/單檔型，**沒規範入口檔內部的段落**。
**建議**：在 kernel 加 `template/workflows/TEMPLATE.workflow.md`，固定六段：`做什麼（一句）` / `何時用 ↔ 何時不用` / `Done when:` / `流程` / `內容表（資料夾型才有）` / `與其他工作流的交接（→ 接誰）`。inbox 已有 `TEMPLATE.letter.md` 前例，命名一致。兩包現有檔照它對齊一次；WORKFLOWS.md 統一形式段加一句指向它。
**優先級**：高。

### 3. `Done when:` 佔位符多半填不出「可觀察」條件，需要給範例對照
**問題**：現在的佔位是 `{{成品交付、涵蓋指定重點、來源已標註、語氣符合對象}}`——這是**類別**不是條件，agent 填出來很容易還是「文章寫好了」這種不可驗證句。dev 包對應概念（「驗證綠燈」）反而是可觀察的，卻沒冠上 Done when 的名字。
**建議**：每檔的 Done when 佔位改成「一行壞例 + 一行好例」：`✗ 文章寫好了` / `✓ docs/x.md 存在、含 3 個指定小節、每個數據後有出處連結`。並在 TEMPLATE.workflow.md 規定 Done when 必須是「檔案存在 / 指令回傳 / 表格填滿」三類之一。
**優先級**：中。

### 4. digest ↔ learn、plan-a-thing ↔ decide 邊界靠讀者猜
**問題**：learn.md 自己說「像 digest，但目標是長期吸收」——差別在**目的**不在**動作**，agent 從使用者一句話很難判。plan-a-thing 說「要抉擇 → 用 decide」，但 decide 沒有反向說「決定完要執行 → 回 plan-a-thing」。派發表觸發詞「讀長文做摘要」vs「學一個主題」對「幫我讀懂 Kubernetes」這種請求兩邊都中。
**建議**：
- 派發表加一欄「**分辨**」：digest＝材料有限、讀完即止、產出是索引；learn＝主題開放、會回訪、產出是主題地圖 + open questions。
- 或直接把 learn 降為 digest 的「升級形態」（digest 資料夾型長出 `topics/`、`questions.md` 就是 learn），減一個工作流。
- decide 加「完成後 → 接 plan-a-thing 執行」；「何時不用」段補齊到 decide、organize（現在只有四檔有）。
**優先級**：中。

### 5. writing.md 的作者口味該退成「範例區塊」，AI 味清單改成可執行的 grep 表
**問題**：張大春、詹宏志、舒國治、阮一峰、Huli、黑大——這是作者個人閱讀史，5.2 KB 是知識包最大的檔，一個模板使用者 90% 會整段改掉，但它沒有用 `{{}}` 標出「哪些是你該換的」。AI 味清單是好內容，但形式是散文列舉，agent 產文後無法自動對照。
**建議**：
- 「參考聲音」兩區塊改成 `{{參考作者（範例：…）}}`，其餘「語氣」「好的樣子」保留為範例。
- AI 味清單改成表格：`詞 / 句型 | 為什麼壞 | 替換`，並附一行 `grep -nE '值得一提|眾所周知|總而言之|賦能|抓手|閉環' docs/` 供動筆後自檢——這樣「別寫成這樣」才有牙齒。
- 繁簡表也是同理，可抽到 `writing/zh-tw.md` 子檔，非繁中專案整檔刪，不用在 5 KB 裡挑段落。
**優先級**：中。

### 6. 缺的 flavor：先補 **ops**，因為 kernel 的 routines 範例其實已經是它
**問題**：routines.md 的範例（「開工唯讀盤點 docker ps / 服務健康檢查」「深度巡檢」）全是維運場景，卻沒有 ops 包承接「異常 → 轉對應深查工作流」那個「深查工作流」。research 與 knowledge 包重疊高（digest + learn + write 已覆蓋）；personal 可用 knowledge 的 plan-a-thing + routines 湊出來；modding 太特定，放回原專案即可。
**建議**：新增 `flavors/ops/`：`WORKFLOWS.ops.md` + `workflows/inventory.md`（唯讀盤點，routines 呼叫的就是它）+ `workflows/incident.md`（紅字/異常深查：現象原文照貼 → 定位 → 修 → 記 gotchas）+ `workflows/deploy.md`（打包/上線，含 WAIT_USER 交接點）。三檔各 ≤ 1 KB 即可。同時 routines 的範例改成指向 `{{inventory 工作流}}` 而不是寫死 docker ps。
**優先級**：中。

### 7. 混合型專案「兩張派發表都貼」有實際衝突，要給合併規則
**問題**：
- dev 菜單的 **plan** 與 knowledge 的 **plan-a-thing**，觸發詞都是「規劃」；dev 菜單的 **idea / roadmap** 在 `WORKFLOWS.knowledge.md` 末段也被提到（「idea → roadmap → plan-a-thing」），但 knowledge 包沒有這兩檔。
- 兩張表都有「記 / 查踩坑 → gotchas」一列（dev 在表內、knowledge 在表下一句），貼在一起會重複。
- 兩包都主張自己的 common 檔（conventions / writing）是「共用」，但沒說碰原始碼又要寫 README 時哪個優先。
**建議**：README「混合型專案」那句擴成一小節：(a) 派發表合併時 gotchas 列只留一份；(b) plan（開發計畫）與 plan-a-thing（非開發規劃）明確以「產出是否為程式碼」分流，寫進表格「分辨」欄；(c) idea / roadmap 從 dev 菜單移到 kernel（它們與領域無關，兩包都引用）。
**優先級**：中。

### 8. testing.md 太薄，撐不起「離線機也能開發」這個關鍵主張
**問題**：862 B，只有兩個 `{{指令}}` 佔位與一段模板說明。feature-dev 流程說「自動驗證綠燈 → 交使用者驗證」，但**哪些驗證 Claude 跑得了、哪些跑不了**的分類方式只在 testing 的〔模板說明〕裡帶一句，沒有表格骨架。
**建議**：加一張三欄表 `驗證 | 指令 | 誰跑（Claude / 使用者 → WAIT_USER）`，讓 feature-dev 那句「Claude 跑不了的一律由使用者做」有地方查。
**優先級**：低。

### 9. conventions.md 的「code map」沒有給最小骨架檔
**問題**：conventions 花一半篇幅講 code map 維護鏈（程式碼 > code map > 文檔），但沒有 `code-map.md` 範例，agent 第一次建時格式自由發揮。knowledge 包的 INFO_MAP 同樣只在 organize.md 提到名字。
**建議**：dev 包加 `workflows/common/code-map.md` 骨架（表格：`領域 | 檔案 | 職責 | 測試在哪`），knowledge 包加 `INFO_MAP.md` 骨架（`材料 | 位置 | 負責什麼 | 衍生產物`），兩者結構故意對稱，README 表格「導航中樞」欄直接連過去。
**優先級**：低。

### 10. 每個 flavor 缺「刪除清單」反向對照
**問題**：knowledge README 說「用不到的整列＋整檔刪掉」，但刪一個工作流要動的位置不只兩處：派發表列、檔案、其他工作流裡「→ 接 write」的交接句、writing.md 的引用。沒有清單，刪完必留斷連結。
**建議**：各 flavor README 末尾加「刪除某工作流時要動的地方」表（工作流 | 檔案 | 派發表列 | 被誰引用）。角度 2 的壞連結檢查腳本若成立，這條可降級為「跑腳本」。
**優先級**：低。
