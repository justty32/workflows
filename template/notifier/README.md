# notifier — routines 常駐精靈的「通知 daemon」

← [design](../workflows/routines/design.md)｜[INDEX](../INDEX.md)｜協定的另一半在 [state/README](../state/README.md)

一支**普通程式、非 agent**（PowerShell）。routines 主 daemon（agent session，`/loop /tick`）有**提醒 / 要外包重活**時 → 寫一則消息給 notifier → 它把提示**推到我眼前**、讓我當場選要不要處理。**它本身沒判斷力**，一切靈活性都在主 agent 傳來的消息裡。整體設計見 [routines design「通知 daemon」段](../workflows/routines/design.md)。

**三個可互換的前端、同一套 [`state/`](../state/README.md) 檔案協定**（下面「檔案協定」對三者都成立，同時只跑一支）：

| 前端 | 檔 | 平台 | 呈現 | 何時用 |
|------|----|------|------|--------|
| **網頁版（Windows 預設）** | [notifier-web.ps1](notifier-web.ps1) | Windows | 內建 TcpListener 綁 `127.0.0.1:8787`、手擼極簡 HTTP，提醒呈現在**網頁**（一頁醜 HTML，每 2s 輪詢）| daemon.bat 預設帶起這支。手滑關掉分頁也不丟（資訊存 server 端，重開網頁又在）|
| terminal 版（PowerShell）| [notifier.ps1](notifier.ps1) | Windows | 跳 **terminal 選單**、打編號 | 想要純 terminal、不開瀏覽器時的替代 |
| terminal 版（Python）| [notifier.py](notifier.py) | **跨平台**（Linux / macOS / Windows）| 跳 **terminal 選單**、打編號 | **Linux 用這支**（daemon.sh 帶起，需 `python3`）；Windows 想用 Python 也行 |

## 怎麼跑

- **Windows**：通常不用手動——[`launchers/daemon.bat`](../launchers/README.md) 起主 daemon 時**偵測 notifier 沒開就一起帶起網頁版**（並開瀏覽器到 `http://127.0.0.1:8787/`），一次到位。單獨起 / 重開：網頁版雙擊 [`launchers/notifier-web.bat`](../launchers/README.md)、terminal 版雙擊 [`launchers/notifier.bat`](../launchers/README.md)（兩支視窗標題都是 `routines-notifier`，daemon.bat 靠它偵測、不重複開）。
- **Linux / macOS**：[`launchers/daemon.sh`](../launchers/README.md) 起主 daemon 時**用 `pgrep` 偵測 `notifier.py` 沒開就試著在新 terminal 帶起**（headless 無 emulator 時改請你自己在另一個 terminal 跑 [`launchers/notifier.sh`](../launchers/README.md)）。Python 版沒有網頁前端（見上表）。
- **Ctrl-C 結束**會把佇列裡沒處理完的消息 dump 到 [`state/pending.json`](../state/README.md)；直接**關窗**（按 X）則來不及 dump——那是 OS 硬殺、屬「默認當作沒回」的容許損失。

## 它做什麼（三版本共通四動作）

1. **收信**：`state/notify.json` 存在 → 讀進**記憶體佇列**、刪檔（騰出槽位給下一則）。讀到一半（主 agent 還在寫）就略過、下次再讀。讀檔強制 UTF-8，免 Windows PowerShell 5.1 把無 BOM 中文當 ANSI（見 [gotchas](../workflows/common/gotchas.md)）。
2. **呈現待處理**：把佇列每則的 `message` + 選項（每項「簡述 → 實際指令」都列出，讓我一眼看清選下去會跑什麼）推到我眼前——terminal 版跳選單、網頁版渲染在頁面。
3. **跑選中指令**：我勾/打的 = 選項（`exit 0` / 空 = 啥都不做，略過），另可帶自由文字。選中的指令在**新視窗 / 新 terminal** 跑（Windows 用 `Start-Process`；Python 版試 terminal emulator，headless 無 emulator 就背景跑、輸出丟 `state/notifier-run.log`）——別卡住輪詢。
4. **回寫** `state/reply.json`：append 一則 `{id, tsLocal, chosen, ranCommands, freeText}`，讓主 agent 下次 `/tick` 讀到、知道我回應過；回完把該則移出佇列。

> 收信時機：terminal 版每 2s 主動輪詢 `notify.json`；網頁版在每次頁面輪詢 `/api/pending` 時順手讀（lazy）。兩者佇列都存 server 記憶體。

## 檔案協定（都在 [`state/`](../state/README.md)，單檔、不入版控）

| 檔 | 方向 | 內容 |
|----|------|------|
| `notify.json` | 主 agent → notifier | 一則通知請求 `{id, message, options}`；`options` 每項是單鍵物件 `{簡述: 實際指令}` |
| `reply.json` | notifier → 主 agent | **append log**（陣列），每則 `{id, tsLocal, chosen:[編號], ranCommands:[實跑的], freeText}`；**notifier 只 append，清空由主 agent 讀完負責** |
| `pending.json` | notifier dump | Ctrl-C 結束時佇列剩餘消息（append 既有的、不覆蓋）；主 agent 下次啟動撿回 |

消息格式範例（主 agent 產生 `notify.json` 時遵循）：

```json
{"id": "msg-001",
 "message": "該去跑某項巡檢了（距上次 >3 天）。",
 "options": [
   {"啥都不做": "exit 0"},
   {"開新 agent 跑巡檢": "claude \"/loop-once some-survey\""}
 ]}
```

- **key = 主 agent 寫的簡述**（這選項會幹嘛）、**value = 實際要跑的指令**。`exit 0` = 略過放掉；要開新 agent 就填 `claude …`、要跑腳本就填腳本指令。
- **一次可打多個編號** → 全部執行；**編號 + 自由文字並存** → 選項照跑、自由文字另外回傳主 agent 判斷（重生成一則消息 or 啥都不做，始終被動）。

## 已知限制（低量夠用）

- `reply.json` 的 append／主 agent 清空之間有**極小競態**（清空前 notifier 剛好又 append 會漏一則）。人大部分時候在電腦前、消息量低，可接受。
- 網頁版是**單執行緒**、一次處理一個請求（localhost 個人用夠）；terminal 版選單是**阻塞式**（等我回某則時新消息先排佇列）。
- 網頁 server 用 `Connection: close` 每請求一條連線、不處理 `Expect: 100-continue`（瀏覽器 fetch 不會用），故只認 localhost 簡單請求。
- **免打擾 / 離座延後**尚未做（[design](../workflows/routines/design.md) 已規劃、延後）：屆時擴充 `{message, options}` 協議加欄位。
