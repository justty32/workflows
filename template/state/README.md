# state — routines 常駐精靈的執行期狀態（非 durable，不入版控）

← [design](../workflows/routines/design.md)｜[INDEX](../INDEX.md)

routines 常駐精靈（daemon）跑起來後的**執行期暫存**。這裡的檔案是 runtime 狀態、不是 durable 文件，所以除了本 README 外**全被 [`.gitignore`](../.gitignore) 掉**——頻繁讀寫 / 清空不該污染 `git status` / commit。各檔的方向與協定設計見 [routines design 的通訊協定段](../workflows/routines/design.md)。

## 檔案協定

| 檔 | 方向 | 用途 | 狀態 |
|----|------|------|------|
| `inbox.md` | 我 → 主 agent | CLI 塞的指示 / 資訊，`/tick` 喚醒時讀 | **已啟用** |
| `carryover.md` | 主 agent → 明天的自己 | `/wrapup` 一鍵清場 dump 的手上沒完的活，下次啟動撿回 | **已啟用** |
| `notify.json` | 主 agent → notifier | 通知請求 `{id, message, options}`（`options` 每項 `{簡述: 實際指令}`）| **已啟用** |
| `reply.json` | notifier → 主 agent | append log，每則 `{id, tsLocal, chosen, ranCommands, freeText}`；notifier 只 append、主 agent 讀完清空 | **已啟用** |
| `pending.json` | notifier dump | notifier 關閉時未處理的消息，主 agent 下次啟動撿回 | **已啟用** |
| `last-seen.json` | 主 agent 自寫自讀 | `{tsLocal, date, firedToday:[...]}`——上次 tick 時間戳 + 當天已觸發的鬧鐘，供判間隔 / 跨天 / 鬧鐘 | **已啟用** |

`notify.json` / `reply.json` / `pending.json` 的協定細節見 [notifier/README](../notifier/README.md)；`last-seen.json` / `carryover.md` 的用法見 [routines 心跳迴圈 / 收尾清場](../workflows/routines/README.md)。**免打擾 / 離座延後**（[design](../workflows/routines/design.md) 已規劃、延後）接上時會擴充 `notify.json` 的 `{message, options}` 加欄位。
