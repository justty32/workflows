# 角度 1：導入後每天在裡面工作的 agent 怎麼看

量化基準（`wc -c`）：kernel 13 個 .md 共 **32.9 KB**。從 AGENTS.md 出發到「動手做一個功能」的最短路徑：AGENTS（3.8K）→ WORKFLOWS（4.4K）→ feature-dev README（~2.5K）→ conventions（~2K）＝ **4 檔、約 12.7 KB**，且 AGENTS 還要求「碰結構時再讀 DEV-GUIDE」。宣稱「薄路由器」的 AGENTS.md 有 3.8 KB，其中真正做路由的只有「先讀哪裡」兩行 + 活狀態三行；其餘是分層思想說明與鐵律。

### 1. 同一段「哲學」在 5 個檔各講一遍，agent 每次都重讀

**問題**：「只指向下一層、不存下層細節」（README.md:8、AGENTS:16-17）、「README＝入口／INDEX＝結構」（README.md:13、AGENTS:20、WORKFLOWS:38-40）、「DEV-GUIDE 是被動參考」（README.md:16、AGENTS:27、INDEX:23、DEV-GUIDE:5）、「三軸活狀態只列 open」（AGENTS:33-41、INDEX:29-37、WORKFLOWS:50-56、WAIT_USER:7、inbox/README:8）。這些是**給導入者讀的設計理由**，不是給工作中的 agent 的指令。agent 走路徑時每一站都吞一次，等於把「薄」的 byte 預算花在解釋為什麼薄。
**建議**：哲學集中到 repo 根 README（導入者讀）與 DEV-GUIDE（整理結構時讀）；AGENTS / WORKFLOWS / INDEX 各只留一行反向連結「組織原則見 DEV-GUIDE」。目標 AGENTS.md ≤ 1.5 KB。
**優先級**：高

### 2. 〔模板說明〕與 `{{}}` 有 43 個佔位、26 處說明，靠「全域搜尋後刪掉」不會乾淨

**問題**：導入步驟只說「全域搜尋 `{{`、讀到〔模板說明〕照做後刪除」（README.md:45）。沒刪乾淨時，agent 會把〔模板說明〕當成現役指令執行（例 routines.md:40「本檔就是 routines 的清單…用不到就整檔刪」——agent 可能真的把它刪了），或在 `{{測試指令}}` 上直接跑 shell。目前 repo 沒有任何「導入完成檢查」。
**建議**：加一個 **`Done when:` 導入驗收清單**到 README：`grep -r '{{\|〔模板說明〕' . 回傳 0 筆`、`WORKFLOWS.md 派發表已貼且佔位行已刪`、`未用的可選工作流（inbox / tick）已整包刪`。順手把它做成 `/wf-doctor` slash 指令，讓 agent 自己跑。
**優先級**：高

### 3. 鐵律「未經確認不 push」與 routines 範例「EOD 收尾 push」打架

**問題**：AGENTS:24 鐵律 2「未經確認不 push」；routines.md:49 範例分區寫「沒事就跑收尾——保存 / push」，且 routines.md:47 說唯讀事務「當場做」。tick 半夜醒來讀到 EOD 分區，兩條規則衝突，agent 得自己裁決。
**建議**：routines 範例改成「跑收尾——保存、**列出待 push 的 commit 問使用者**」，並在 routines 執行段明寫「登記表裡的項目不豁免鐵律」。
**優先級**：高

### 4. `/wf-tick` 無週期時「self-pace」，但 tick 宣稱「不判時間」

**問題**：wf-tick.md:11 說「沒給 → 模型自行決定節奏」；tick.md:5 說 tick「自己不判時間」。自行決定節奏就必須判時間，責任落在誰身上沒寫。實務上 `/loop` 動態模式會由 tick 那次 session 決定下次幾分鐘，等於 tick 偷偷承擔了 routines 的職責。
**建議**：`/wf-tick` 強制帶週期（沒給就用預設 `30m` 並回一句），刪掉 self-pace 分支；或把「下次醒來間隔」明訂為 routines 執行段的輸出。
**優先級**：中

### 5. 「何時寫 SESSION-LOG」只有一句模糊觸發，agent 會漏寫或亂寫

**問題**：唯一觸發在 AGENTS:35「事情告一段落、因應需求結束、或臨時中止時」——這三個時點 agent 都很難自我偵測（context 被壓縮、使用者 Ctrl+C）。flavor 裡各自再補一句「跨 session 記…」（write.md:27、feature-dev:21），措辭不一。
**建議**：改成可執行的固定動作：「**每次 commit 前**檢查 SESSION-LOG：有 open 的就更新、沒 open 的確認為空」。commit 是 agent 一定會經過的關卡，比「告一段落」可靠。
**優先級**：高

### 6. `archive/` 出現 5 處但零命名／格式規則

**問題**：DEV-GUIDE:21、WORKFLOWS:45、common/README:16、feature-dev:31 都說「過時的丟 archive/」，沒說檔名要不要帶日期、要不要在檔頭寫「被誰取代」。兩個 session 各丟一份就分不出先後、也不知道現役版在哪。
**建議**：DEV-GUIDE 加三行：檔名保留原名；檔頭第一行 `> 封存 YYYY-MM-DD，由 <路徑> 取代`；archive 內不放 README。
**優先級**：中

### 7. gotchas 只有「記／查」派發，沒有「什麼算一個坑」的門檻

**問題**：gotchas.md:13 條目格式有例，但無記錄門檻。agent 會不記（怕多餘）或把每個小錯都記成坑，檔案很快超過 8192 bytes 觸發拆分。
**建議**：加一句門檻：「**第二次**撞到、或使用者說『上次也是這樣』才記；一次性錯誤不記」。
**優先級**：低

### 8. 「commit 到主分支是慣例」寫在鐵律裡，對多人／有 PR 流程的專案是錯的

**問題**：AGENTS:24 括號內「commit 到主分支是慣例」是原專案的習慣，不是通用鐵律。導入到有 branch protection 的 repo，agent 會照做並被拒。
**建議**：括號改成佔位 `{{分支慣例：直接 commit main / 開 branch 走 PR}}`，讓導入時必填。
**優先級**：中

### 9. 名稱 `DEV-GUIDE` 在知識 flavor 專案裡是誤導

**問題**：知識包 organize.md:5 說自己是「DEV-GUIDE 的非開發版」，但整份 DEV-GUIDE 內容其實已經領域中立（結構整理原則）。名稱含 DEV，非開發專案的 agent 會判斷「這是開發文件、跳過」。
**建議**：改名 `STRUCTURE-GUIDE.md`（或 `ORGANIZING.md`），README/INDEX/AGENTS 同步。
**優先級**：低

### 10. 三軸活狀態每次都要開 3 個檔才能確認「有沒有事」

**問題**：session 開始要判斷「有沒有未完的事」得讀 SESSION-LOG、WAIT_USER、掃 `inbox/` 三處；AGENTS 沒有「開場 checklist」。
**建議**：AGENTS「先讀哪裡」之前加一段 3 行的 **開場動作**：`ls inbox/*.md`、`grep -c '^- ' SESSION-LOG.md WAIT_USER.md`，有東西才進去讀。
**優先級**：中
