# launchers — 一鍵啟動 Claude Code 跑某工作流

雙擊即開 Claude Code 並自動下一個 slash command 的 `.bat`。搭配 [`.claude/commands/`](../.claude/commands/) 裡的自訂指令用。

> 〔模板說明〕三支 `.bat` 裡的 `{{repo 絕對路徑}}`（例 `C:\code\your-project`）填成你 repo 的實際路徑；`daemon.bat` 尾行的 `claude "..."` 旗標依需要調整。用不到常駐精靈就整個 `launchers/` 刪掉。

| 檔 | 做什麼 | 對應指令 |
|----|--------|----------|
| [daemon.bat](daemon.bat) | 起一個常駐 session，每 30 分喚醒跑一次心跳（routines 常駐精靈）。**啟動時順手偵測 [notifier](../notifier/README.md) 沒開就一起帶起網頁版並開瀏覽器** | `/loop 30m /tick` → [.claude/commands/tick.md](../.claude/commands/tick.md)（設計見 [routines design](../workflows/routines/design.md)）|
| [notifier-web.bat](notifier-web.bat) | 單獨起 / 重開 [notifier](../notifier/README.md) **網頁版** server（`http://127.0.0.1:8787/`）並開瀏覽器（通常由 daemon.bat 自動帶起）| `powershell -File notifier\notifier-web.ps1` |
| [notifier.bat](notifier.bat) | 單獨起 / 重開 [notifier](../notifier/README.md) **terminal 版**（純 terminal 選單、不開瀏覽器的替代）| `powershell -File notifier\notifier.ps1` |

## 桌面怎麼用

不要把 `.bat` 複製去桌面（會變舊版）。在桌面**建捷徑指向 repo 內這個 `.bat`**：
- 桌面右鍵 → 新增 → 捷徑 → 位置填 `{{repo 絕對路徑}}\launchers\daemon.bat`。
- 之後雙擊捷徑：cmd 會切到 repo 目錄、啟動 `claude "/loop 30m /tick"`，Claude Code 就起一個常駐 session 定時跑心跳。

## 前提

- `claude` CLI 已安裝且在 PATH（開 cmd 打 `claude --version` 有回應）。
- 機制：`claude "<初始訊息>"` 會用該訊息當第一句啟動互動階段；把訊息設成 `/loop 30m /tick`（或任一 `/<指令>`）就會觸發對應的自訂 slash command。

## 加新的

1. 在 `.claude/commands/<名>.md` 寫指令（frontmatter `description:` + 指令本文）。
2. 在 `launchers/<名>.bat` 複製 daemon.bat、把 `/loop 30m /tick` 換成 `/<名>`。
3. 在上表加一列。
