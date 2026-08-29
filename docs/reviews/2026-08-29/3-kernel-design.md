# 角度 3：kernel（template/）架構批判

### 1. 「完成即刪、歷史交給 git log」漏掉了「為什麼」——需要第四類 durable：決策記錄
- **問題**：三軸活狀態（SESSION-LOG / WAIT_USER / inbox）只管「還沒完的事」，完成就刪（`SESSION-LOG.md` 第 8、14 行；`WAIT_USER.md` 第 7 行）。但 git log 只能找回「改了什麼」，找不回「為什麼選 A 不選 B」「為什麼放棄方案 C」。knowledge 包的 `decide.md` 已有決策記錄模板，dev 包和 kernel 卻沒有落點；`feature-dev/README.md` 的 `landed/` 只記「功能在哪」不記取捨。
- **建議**：kernel 加 `workflows/decisions/`（或單檔 `DECISIONS.md` 從第 1 級長起）：一條一決策，格式借 `decide.md` 的模板（結論 / 未選原因 / 前提）。在 `WORKFLOWS.md`「跨工作流的活狀態」旁加一段「durable 記錄：決策」，並在 `AGENTS.md` 第 148 行「事情告一段落」的清單加一句「有取捨就補一條決策」。三軸不動，只是明講：活狀態是「未完」，決策是「已定但要保留理由」。
- **優先級**：高

### 2. 三軸不正交：WAIT_USER 與 inbox 邊界靠「對方是不是人」，實務上會混
- **問題**：`WAIT_USER.md` 第 5 行把「催/開/fork 另一個 agent」也收進來，`inbox/README.md` 第 28 行又說催件要記到 WAIT_USER——同一件「等別的 agent」的事橫跨兩軸。inbox 是「跨資料夾 agent」，但同 repo 內 fork/子 agent 的交接（最常見）三軸都沒接住。
- **建議**：在 `WORKFLOWS.md`「跨工作流的活狀態」加一張 2×2 判別表：等的是**人**→WAIT_USER；等的是**別的資料夾的 agent**→inbox；等的是**同 repo 的另一個 session/fork**→SESSION-LOG 一行（含對方 session 或分支）。一句話收斂「催件」只寫 WAIT_USER，inbox 不再重述。
- **優先級**：中

### 3. 定期喚醒不該是 kernel「一律有」——降為可選包，並明講與原生機制的關係
- **問題**：`WORKFLOWS.md` 第 19–31 行說 tick/routines/schedule「不屬任一 flavor、kernel 一律有」，但它是實驗性（「提醒先不做」出現 3 次）且與 Claude Code 原生 `/loop`、cloud routines（`/schedule`）、OS cron 完全重疊：`/wf-tick` 本身就是 `/loop` 的薄殼。`routines.md` 第 19–26 行還內嵌 Windows PowerShell 時區指令——這是「取當地時間的平台細節」，屬 gotchas/dev-env，不屬 kernel 通用骨架。kernel 41 行的 AGENTS 之外，這三檔佔 kernel 近 1/4 體量。
- **建議**：搬成 `flavors/periodic/`（tick、routines、schedule、`.claude/commands/wf-tick.md`），kernel 的 `WORKFLOWS.md` 只留一行「需要定期喚醒→合 periodic 包」。包內 README 加一段「什麼時候該用這個而不是 `/loop` / cloud routines / cron」：本包的價值只在「清單放 repo、跟著版控、agent 可讀」，執行引擎一律借原生。時區指令縮成一行「用 `TZ=… date`；平台差異見 gotchas」。
- **優先級**：高

### 4. inbox：沒有鎖但也沒說清楚它假設的並發模型；CONTACTS 絕對路徑不可攜
- **問題**：`inbox/README.md` 第 22 行只靠「寄前掃同名」防撞，多個 agent 同時寄同 slug 仍會互蓋；`mv` 進 `done/` 與對方正在讀也無保護。設計上刻意 email 化是對的，但「一個 inbox 只一個 agent 收」（第 43 行）是隱含前提，沒寫進「地址」那節。`CONTACTS.md` 範例用 `~/repo/...` 絕對路徑，換機器、非侵入式導入（inbox 在 `wf/inbox/`）或多人 clone 就失效。另外完全沒提 Claude Code 原生 SendMessage/ListAgents——同機多 session 時原生機制更即時，inbox 該定位為「跨機、跨時間、可版控」的慢通道。
- **建議**：README「地址」節加「假設：單一收件 agent、單機同一檔案系統」；並加「與原生 SendMessage 的分工」一段。CONTACTS 改為「相對於某個 root 的路徑 + 該 root 怎麼定（例：`$REPOS/`）」，或明講「地址是機器本地的，每台機器各自維護通訊錄」。slug 建議加「寄件方前綴」（`from-xxx-<slug>`）降低撞名。
- **優先級**：中

### 5. DEV-GUIDE 門檻寫死成數字，卻沒有任何自動檢查——加 `wf-lint`
- **問題**：`DEV-GUIDE.md` 第 16–20 行要求「客觀數字才能讓 agent 自主觸發整理」，但整套沒有一個能跑的檢查。agent 不會每次動手前 `wc -c`。同理沒有東西掃殘留的 `{{`、`〔模板說明〕`、壞相對連結、`inbox/` 頂層堆積、SESSION-LOG 「已完成」字樣。
- **建議**：kernel 加 `scripts/wf-lint.sh`（純 bash：`find -size +8192c`、`grep -rn '{{\|〔模板說明〕'`、相對連結解析、inbox 頂層檔數）+ `.claude/commands/wf-lint.md` 薄殼。把「跑 wf-lint」寫進 `routines.md` 範例（間隔型、agent 唯讀可代勞）——順便給 routines 一個真實的用例。AGENTS 鐵律不加，維持薄。
- **優先級**：高

### 6. 缺「使用者偏好」與「領域詞彙」的歸層——AGENTS.md 沒給位置
- **問題**：`AGENTS.md` 有專案一句話、鐵律、開發環境、活狀態，但沒有「使用者是誰、語言、什麼事要先問、什麼可直接做」（目前散落：鐵律 2「push 先確認」是偏好硬編成鐵律；`writing.md` 的繁簡條款其實是使用者語言偏好）。也沒有 domain glossary 的層——非開發專案（法律、醫療、遊戲 mod）術語量大，agent 每次重猜。
- **建議**：kernel 加 `workflows/common/user.md`（偏好：語言、確認邊界、風格）與 `workflows/common/glossary.md`（可選，長出來才建），`common/README.md` 表各加一列；`AGENTS.md` 只加一句「使用者偏好→common/user」。鐵律 2 的 push 規則搬到 user.md，鐵律縮回真正「任何專案都成立」的那幾條。
- **優先級**：中

### 7. 工作流入口格式兩包不一致——kernel 該定一份「入口檔骨架」
- **問題**：knowledge 包每檔都有 `Done when:` + 流程 + 何時不用；dev 包 `feature-dev/README.md`、`testing.md` 沒有 `Done when`（grep 為 0 筆），也沒「何時不用」。kernel 的 `WORKFLOWS.md` 第 33–48 行「統一形式」只講檔名與資料夾型/單檔型，不講**內容段落**。agent 讀到不同骨架的入口，判斷「該怎麼開始」的方式就不一致。
- **建議**：`WORKFLOWS.md`「統一形式」加「入口檔固定段落」：一行做什麼 / 何時用、何時不用 / `Done when:` / 流程 / 內容表（資料夾型才有）/ 專屬 gotchas 與 session-log 指標。kernel 放一份 `workflows/TEMPLATE.workflow.md`（像 `TEMPLATE.letter.md` 那樣）；dev 包兩檔補齊 `Done when` 與「何時不用」。
- **優先級**：中

### 8. WORKFLOWS.md 承擔太多：派發表 + 定期喚醒 + 形式規範 + 活狀態，與 INDEX/AGENTS 重述
- **問題**：`WORKFLOWS.md` 4.4 KB，其中「統一形式」與「跨工作流的活狀態」兩節在 `AGENTS.md`、`INDEX.md`、`DEV-GUIDE.md` 各重述一遍（三軸說明出現 4 處）。派發器的職責應只是「意圖→入口」；規範屬 DEV-GUIDE，活狀態屬 AGENTS。
- **建議**：「統一形式」整節搬進 `DEV-GUIDE.md`（它本來就是「形式與結構」的被動參考）；「跨工作流的活狀態」縮成一行連回 AGENTS。WORKFLOWS 只剩：派發表佔位 + 定期喚醒（若依第 3 條搬走則更薄）+ 「都不符→INDEX」。
- **優先級**：中

### 9. 「未經確認不 push」與「不開新工作」兩條鐵律，和 routines/schedule 的自動執行互相打架
- **問題**：`AGENTS.md` 鐵律 2「未經確認不 push、不開新工作」；`routines.md` 第 48 行範例 EOD「跑收尾——保存 / push」、`schedule.md` 第 27 行「使用者親自排的→視為已授權」。鐵律說任何時刻適用，定期工作流又給了例外——agent 會在 tick 裡無所適從。
- **建議**：鐵律 2 改成「不可逆／對外的動作（push、刪除、對外送出）需有**授權來源**：使用者當場確認、或 schedule/routines 裡由使用者登記的項目」，一句話把授權來源定義好；routines/schedule 各改成引用這條而非各自解釋。
- **優先級**：高

### 10. SESSION-LOG 的「跨 session 交接」沒有可操作的觸發時機
- **問題**：`AGENTS.md` 第 148 行只說「告一段落、需求結束、臨時中止時」記進度，但 agent 常被硬中斷（context 用完、使用者關視窗），根本來不及寫。`feature-dev/README.md` 有一條好例子（「文檔/code map 待同步」補一行），kernel 卻沒通則。
- **建議**：`SESSION-LOG.md` 開頭加「寫入時機」三條：① 開始一件多步驟工作前先寫一行 open（不是做完才寫）；② 每次 commit 後更新／刪除該行；③ 條目格式固定 `[工作流] 一句 open 狀態 → 下一步 / 連結`。這樣硬中斷時 log 至少反映「進行中」而非空白。
- **優先級**：高
