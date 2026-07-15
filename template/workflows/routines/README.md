# routines — 例行事務 / 定期待辦（常駐精靈工作流）

← [INDEX](../../INDEX.md)｜[AGENTS.md](../../AGENTS.md)｜架構與演化設計見 [design](design.md)

**做什麼**：記錄「在某個**時機 / 週期**下該做的事」——上班時、下班前、會議前後、改完程式、每週、每隔幾天……。目的有二：① 怕忘記；② 能交給 **agent 代勞**的就標出來、之後自動化。本檔是工作流**入口**（先讀本檔）；daemon 的架構與演化在 [design](design.md)。

> 〔模板說明〕「有常駐精靈的例行事務」通用骨架，配套 [`.claude/commands/`](../../.claude/commands/tick.md)（`/tick`、`/wrapup`）、[`notifier/`](../../notifier/README.md)、[`state/`](../../state/README.md)、[`launchers/`](../../launchers/README.md)。**跨平台**：Windows 走 `.bat` + PowerShell notifier、Linux/macOS 走 `.sh` + Python notifier（見 [launchers](../../launchers/README.md) / [notifier](../../notifier/README.md)）。機制與檔案協定兩邊通用；你只要填**自己的時機分區與間隔登記表**（下面兩段）＋全域 `{{repo 絕對路徑}}` 與時區佔位符（Windows 時區 ID + IANA 名，見各檔）。用不到就整組刪。

**怎麼組織**：依**觸發時機**分區（下面「時機分區」）。每個項目標三件事：**執行者**（我 / agent）、**內容**、**（間隔型才需要）上次執行日期**。間隔型靠登記表「上次執行」欄判到期，做完就更新那格。

**怎麼跑（常駐精靈）**：由 routines 常駐精靈 daemon 定時喚醒執行——桌面捷徑 → [`launchers/daemon.bat`](../../launchers/README.md) 起一個常駐 session，`/loop 30m /tick`（[.claude/commands/tick.md](../../.claude/commands/tick.md)）每 30 分喚醒一次，每次照下面「**心跳迴圈**」判當下該做哪段。**改本檔內容即改 daemon 行為，指令以本檔為準。** 整體演化設計見 [design](design.md)。

> always-on 鐵律照舊（見 [AGENTS.md](../../AGENTS.md)）：交給 agent 的項目也遵守——**唯讀盤點類可自己跑；會造成不可逆影響（動機器檔案 / DB / repo 工作樹）的，先問使用者**；未經確認不 push、不開新工作。

---

## 心跳迴圈（`/tick` 每次喚醒照這做）

daemon 的核心迴圈，**刻意簡單、輕量可拋棄**：只做「判斷 + 短動作 + 提醒」，重活一律外包（寫進 inbox / 提醒另開 session），好讓 session 能隨意關掉重開。`/tick` 是薄殼，實際步驟在這。執行期通道都在 [`state/`](../../state/README.md)（不入版控）；取當地時間（`{{時區}}`）Windows 用 PowerShell、Linux/macOS 用 `date`（見 [`/tick`](../../.claude/commands/tick.md)）。

1. **判當前時間（`{{時區}}`）**：取現在的當地時間。
2. **時間感知**：讀 `state/last-seen.json`（上次 tick 的時間戳 + 當天已觸發的鬧鐘）。算距上次多久——
   - 沒有這檔 → 新起的 session，當乾淨開始。
   - **跨天 / 請假**（上次是別天、或間隔很久）→ **不補跑昨天的鬧鐘**、`firedToday` 重置。
3. **撿回中斷遺留**：
   - 讀 `state/carryover.md`（上次 `/wrapup` 一鍵清場 dump 的手上沒完的活）→ 有就把昨天的接回來（該做的做、該排的排、該提醒的提醒）→ 處理完清空。
   - 讀 `state/pending.json`（notifier 被關時 dump 的未處理消息）→ 有就處理（多半重產一則 notify 提醒，或視情況放掉）→ 處理完刪掉該檔。
4. **收我對通知的回覆**：讀 `state/reply.json`（notifier append 的我的編號選擇 / 自由文字）→ 逐則看 `freeText`：要回應就**重生成一則 notify 消息**，不然放掉（選中的指令 notifier 已自己跑過，agent **不重跑**）→ **讀完清空 `reply.json`**（清空是主 agent 的責任）。
5. **判時段 + 鬧鐘**：對照下面「時機分區」——
   - **時段近似**：現在落在哪段就照該段做。
   - **鬧鐘（跨 tick 偵測）**：某鬧鐘時刻若落在 **(上次 last-seen tick, 現在]** 且**今天還沒觸發**（不在 `firedToday`）→ 跑它對應的段、記進 `firedToday`。這樣不重複跑、也不會因為 loop 每 30 分才醒而漏掉（頂多晚半小時）。
6. **查指示檔 `state/inbox.md`**：存在且有內容就逐則處理——
   - **短動作** → 當場做（守鐵律：會造成不可逆影響的先問）。
   - **重活**（深度巡檢、深度調查）→ **不自己跑**，寫一則 `state/notify.json` 提醒**另開 agent session**（見第 7 步）。
   - 純對話 / 想排到下次 → 視情況記下或保留。
   - 處理完**是否清空 `inbox` 自行決定**（多半清掉免下輪重跑；必要時保留）。檔案不存在 / 空 → 略過，不報錯。
7. **要提醒 / 外包就寫 `state/notify.json`**：格式 `{id, message, options}`——`options` 每項 `{簡述: 實際指令}`（`exit 0` = 放掉、`claude …` = 開新 session）。notifier 跳選單、跑我選的、把回覆寫回 `reply.json`（下輪第 4 步讀）。協定見 [notifier/README](../../notifier/README.md)。
8. **寫 `state/last-seen.json`**：這次 tick 的當地時間戳 + 更新後的 `firedToday`（跨天已重置）。供下次 tick 判間隔 / 鬧鐘。
9. **回一句簡短心跳摘要**：現在幾點、屬哪段 / 觸發了哪個鬧鐘、inbox / reply / pending 有無東西、做了 / 提醒了什麼。沒事就一句「無事」。

> **仍未接上**（[design](design.md) 已規劃、延後）：**免打擾 / 離座延後**——喚醒時我不在，就把需抉擇的事往後延、並設免打擾時段；屆時會擴充 `notify.json` 的 `{message, options}` 協議加欄位。

## 收尾清場（`/wrapup` 一鍵，可隨時中止）

快下班 / 懶得處理 / 要直接關 terminal 前，在 CLI 下 [`/wrapup`](../../.claude/commands/wrapup.md)——把手上沒完的一股腦存進 `state/carryover.md`，就能安心關窗，明天 daemon 起來自動撿回。這是「懶人快關」路徑：**只 dump 狀態、不做保存 / push**（要正式保存 / push 走下面 EOD 段）。

`/wrapup` 做什麼：

1. **盤點手上沒完的**：這個 session 進行中的活、記下的待辦、還沒回我的抉擇（含還沒送出的 notify）、任何「明天要記得」的線索。
2. **寫進 `state/carryover.md`**：一則一則列清楚（在做什麼、卡在哪、下一步、相關檔案 / 連結），帶當地時間戳。**這是寫給明天的自己看的**，寫到看了就能接續。
3. 寫完就**可以直接關 terminal / 關 notifier**，順序隨意——兩邊各有托底（daemon 靠 `state/pending.json`、agent 靠 `state/carryover.md`），不丟東西。

> 對應撿回：下次 daemon 啟動 / 首次 `/tick` 在上面心跳迴圈**第 3 步**讀 `state/carryover.md` 接回昨天沒完的、處理完清空；跨天判斷照 `state/last-seen.json`。

## 時機分區（live 清單，隨時增 / 改 / 刪）

`/tick` 判當地時間後對照本區。各時刻標註是**鬧鐘、我隨時增改刪**；鬧鐘靠心跳迴圈第 5 步「跨 tick 偵測」觸發（時刻落在上次 tick 到現在之間、當天未觸發就跑），loop 每 30 分醒一次、最多晚半小時。

> 〔模板說明〕下面全是**範例分區**，示範一則項目該標哪三件事（執行者 / 內容 /（間隔型才要）上次執行）。刪掉用不到的、換成你自己的時機；撐大了就照 [DEV-GUIDE](../../DEV-GUIDE.md) 再拆。

### 每天上班（morning，約 09:00 前）
- （範例）**開工唯讀盤點**（執行者：**agent**，唯讀可代勞）：跑一輪唯讀盤點（例 `{{盤點指令，如 docker ps / 服務健康檢查}}`），發現異常 → 轉對應深查工作流。

### 準備會議（約 08:45，會議前）
- （待補：準備會議所需的資訊）

### 每天下班（EOD，約 16:30）
- （待補：問我還有沒有事；沒事就跑收尾——保存 / push）

### 每小時掃
- 掃下面「間隔型登記表」，看有沒有到期的（距上次超過週期）：到期就提醒我，可唯讀代跑的就代跑。

## 間隔型 / 太久沒做就提醒

登記表（到期看「上次執行」+「週期」；由上面「每小時掃」定時檢）：

| 項目 | 週期 | 執行者 | 上次執行 | 細節 |
|------|------|--------|----------|------|
| （範例）刷新某盤點紀錄 | 每 3 天（或距上次 >3 天）| **agent**（唯讀，可代勞）| — | ↓ 見下 |
| （範例）問使用者才知道的來歷 | 不定期（使用者有空時）| **使用者口述 → agent 記** | — | ↓ 見下 |

> 〔模板說明〕上表兩列是**範例格式**：一列到期靠比對「上次執行 + 週期」（agent 自動判、做完更新那格、可用 `/schedule` 或 `/loop` 自動化），一列沒硬性週期、純提醒（「上次執行」留 `—`，例如「某分支為何存在」這種只有問使用者才知道、agent 光看檔案 / git 看不出的來歷）。換成你自己的間隔型事務；唯讀代跑守鐵律：不新建紀錄檔（除非有新目標）、不碰工作樹、不做不可逆操作。

---

## 之後可能新增的時機（先佔位）

需要時才展開成上面那樣的分區：**會議結束後** / **每週週會後** / **改好程式碼後** / **每週固定**要做的。
