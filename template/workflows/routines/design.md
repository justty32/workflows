# routines 常駐精靈 — 架構與演化設計

← [routines README](README.md)｜[INDEX](../../INDEX.md)

routines 從「雙擊跑一次」演化成「**工作時間全程常駐**的一個 session」的架構設計。操作面（心跳步驟、時機分區）在 [README](README.md)；本檔記**為什麼這樣設計**、各通道的協定、以及仍未做的部分。

> 〔模板說明〕本檔是這套常駐精靈的設計理由書，通用、可照抄。只有 `{{時區}}` / `{{repo 絕對路徑}}` 是佔位符。用不到常駐精靈就連同整個 `routines/` 一起刪。

## 願景

- 開工時雙擊桌面 [`daemon.bat`](../../launchers/README.md) → 起一個 session，**一路跑到收工才關**（取代跑一次就結束的一鍵做法）。
- session 起來先用**當地時區**（`{{時區}}`）判當前時間點，決定該跑哪段（例：早上某時前 → 跑開工段）。
- 內建多個**鬧鐘**在特定時刻喚醒做對應 routine（時刻與內容都是 [README](README.md) 裡的 **live 清單**，隨時增改刪；`/tick` 每次讀當下的清單、不寫死）。
- 融入**個人作息**（如會議時段、短暫離座）：喚醒時把這些納入判斷。

## 兩支 daemon 分工

- **主 daemon** = agent session（`/loop 30m /tick`）：被喚醒 → 判當前時間 → 查表（`state/inbox.md`、`state/reply.json`、live 清單）→ 稍微判斷 → 發提醒 / 做短動作。核心迴圈刻意簡單。
- **通知 daemon**（[`notifier`](../../notifier/README.md)）= 一支**普通程式、非 agent**：主 agent 有提醒 / 要外包時 → 傳訊給 notifier → 它把提示推到我眼前、讓我當場決定要不要處理。它**沒判斷力**，一切靈活性都在主 agent 傳來的消息裡。

## 主 agent 該具備的能力

- **輕量 / 可拋棄（核心取捨）**：主 session 只做**提醒**與**短動作**，**重活一律不自己跑**。碰到吃資源的 routine（深度巡檢 / 調查）→ 不自己查，而是寫一則「該去跑 XX 了」進 `state/inbox.md` / `state/notify.json` 並提醒我，我再**另開一個 agent session** 去處理。因此這 session 可被**隨意關掉重開**。
- **快速清場收尾（可隨時中止）**：快收工 / 懶得處理時直接關 terminal、關 notifier、關主 session，順序隨意。兩邊各有托底、不丟東西：
  - **主 agent**：slash 指令 [`/wrapup`](../../.claude/commands/wrapup.md) 一鍵清場——待辦 / 進行中的東西一股腦存進 `state/carryover.md`，明天心跳第 3 步撿回。
  - **notifier**：靠「消息存記憶體 + 關窗默認當沒回」+ 關閉時 dump `state/pending.json` 托底。
- **時間感知**：持久化「上次活動 / 結束」時間戳（`state/last-seen.json`），啟動時讀得到。若跨天（例如請假隔了一整天），做相應處置（不把昨天的鬧鐘補跑一遍）。
- **Context 節流（只守宗旨）**：唯一宗旨——**別隨便開新 agent session**（每開一個都要載入一堆東西、很吃 context）。連「重活外包 → 另開 session」也要克制：值得才開、能合併就合併；能用 fork / subagent 解決就別起整個新 session。
- **Adaptive / 免打擾（保留，延後做）**：喚醒時我若不在電腦前，需抉擇的事往後延、別卡住；並能設免打擾時段。這塊等被煩到了再做；屆時會擴充 `{message, options}` 協議加欄位（例如「可否此刻打擾 / 可否延後」）。

## 怎麼啟動

- **跑 [`launchers/daemon`](../../launchers/README.md)（Windows `.bat` / Linux/macOS `.sh`）** → 起主 daemon，用默認間隔（半小時）。實質是 `claude "/loop 30m /tick"`。
- launcher 順手**偵測 notifier 開了沒**（Windows 靠視窗標題 `routines-notifier`、Linux 靠 `pgrep notifier.py`），沒開就幫忙帶起（Windows 網頁版 / Linux terminal 版）——一次到位。
- 喚醒間隔可調：默認半小時，要盯緊時在 session 裡改跑 `/loop 5m /tick`（或臨時改 `.bat`）。

## 通訊協定（全走 `state/`、檔案化，不需 socket）

每種流各佔一個檔、彼此天然分開（協定細節見 [state/README](../../state/README.md) 與 [notifier/README](../../notifier/README.md)）：

| 檔 | 方向 | 內容 |
|----|------|------|
| `state/inbox.md` | 我 → 主 agent | CLI 塞的指示 / 資訊 |
| `state/notify.json` | 主 agent → notifier | 通知請求 `{id, message, options}` |
| `state/reply.json` | notifier → 主 agent | 我打的編號選擇 / 自由文字（append log）|
| `state/pending.json` | notifier dump | 關閉時未處理的消息，主 agent 啟動時撿回 |
| `state/last-seen.json` | 主 agent 自寫自讀 | 上次 tick 時間戳 + 當天已觸發鬧鐘，供時間感知 |
| `state/carryover.md` | 主 agent → 明天的自己 | `/wrapup` dump 的手上沒完的活 |

## 通知 daemon 的消息協定

- **不碰通訊軟體 / 郵件**（太重）。假設我大部分時候人在電腦前、就算離開也只是一段時間，**不為長時間離線設計**。
- **消息格式**（主 agent 產生時遵循）：`message` 是要顯示的文字；`options` 每項是 `{簡述: 實際指令}`——**key = 簡述**（這選項會幹嘛）、**value = 實際要跑的指令**。notifier 列選單時兩者都顯示，讓我一眼看清選下去會跑什麼。

  ```json
  {"message": "顯示在畫面的提示文字",
   "options": [
     {"啥都不做": "exit 0"},
     {"開新 agent 執行 XX": "claude \"/some-command\""}
   ]}
  ```

  `exit 0` = 略過放掉；要開新 agent 就填 `claude …`、要跑腳本就填腳本指令。**message 與 options 全由主 agent 按情境生成**——這是全部靈活性的來源。
- **輸入方式：打編號**。可一次打多個編號 → 選中的全部執行；也可編號 + 自由文字並存 → 選項照跑、自由文字另外回傳主 agent。
- **輸入一律回傳主 agent**（走 `state/reply.json` 反向通道）。自由文字由 agent 自己判斷要重生成一則消息、還是啥都不做——但**始終被動、不主動找事**。
- **托底**：收到消息先存記憶體；成功收到輸入並執行 → 從記憶體刪掉；單純關掉沒回 → 默認當沒回（`exit 0`）。關閉時把剩下的 dump 到 `state/pending.json`，主 agent 下次啟動撿回。
- **呈現形式自由**：terminal 選單或網頁都行（兩版同協定、可互換，見 [notifier/README](../../notifier/README.md)），但上面 `{message, options}` 是 agent ↔ daemon 之間的**固定接口**。

## 仍未做（成熟一塊做一塊）

- **免打擾 / 離座延後**：規則、怎麼偵測我在不在、延後策略；實作時會擴充 `{message, options}` 協議加欄位。
- 指示檔 `state/inbox.md` 的更精確格式（一則指示怎麼寫、時間戳怎麼帶）。
- 跨天 / 請假的處置細則。
- context 節流目前只守宗旨，有需要再加自動機制。
