# launchers — 一鍵啟動 Claude Code 跑某工作流

雙擊即開 Claude Code 並自動下一個 slash command 的 `.bat`。搭配 [`.claude/commands/`](../.claude/commands/) 裡的自訂指令用。

> 〔模板說明〕`.bat`（Windows）與 `.sh`（Linux / macOS）並存、擇你平台用。裡面的 `{{repo 絕對路徑}}`（Windows 例 `C:\code\your-project`、POSIX 例 `/home/you/your-project`）填成 repo 實際路徑；`daemon` 尾行的 `claude "..."` 旗標依需要調整。用不到常駐精靈就整個 `launchers/` 刪掉。

### Windows（`.bat`）

| 檔 | 做什麼 | 對應指令 |
|----|--------|----------|
| [daemon.bat](daemon.bat) | 起一個常駐 session，每 30 分喚醒跑一次心跳（routines 常駐精靈）。**啟動時順手偵測 [notifier](../notifier/README.md) 沒開就一起帶起網頁版並開瀏覽器** | `/loop 30m /tick` → [.claude/commands/tick.md](../.claude/commands/tick.md)（設計見 [routines design](../workflows/routines/design.md)）|
| [notifier-web.bat](notifier-web.bat) | 單獨起 / 重開 [notifier](../notifier/README.md) **網頁版** server（`http://127.0.0.1:8787/`）並開瀏覽器（通常由 daemon.bat 自動帶起）| `powershell -File notifier\notifier-web.ps1` |
| [notifier.bat](notifier.bat) | 單獨起 / 重開 [notifier](../notifier/README.md) **terminal 版**（純 terminal 選單、不開瀏覽器的替代）| `powershell -File notifier\notifier.ps1` |

### Linux / macOS（`.sh`）

| 檔 | 做什麼 | 對應指令 |
|----|--------|----------|
| [daemon.sh](daemon.sh) | 起一個常駐 session，每 30 分喚醒跑一次心跳。**啟動時用 `pgrep` 偵測 [notifier](../notifier/README.md) 沒開就試著在新 terminal 帶起 Python 版**（headless 無 emulator 就提示你自己跑 notifier.sh）| `/loop 30m /tick` → [.claude/commands/tick.md](../.claude/commands/tick.md) |
| [notifier.sh](notifier.sh) | 單獨起 / 重開 [notifier](../notifier/README.md) **terminal 版（Python，跨平台）**——在自己的 terminal / tmux pane 裡跑 | `python3 notifier/notifier.py` |

> Linux 版**只有 terminal 前端**（Python），沒有網頁版；`.sh` 需可執行位（`chmod +x launchers/*.sh`，本 repo 已設）。notifier 需 `python3`（3.9+）。

## 桌面 / 快捷怎麼用

- **Windows**：不要把 `.bat` 複製去桌面（會變舊版）。桌面右鍵 → 新增 → 捷徑 → 位置填 `{{repo 絕對路徑}}\launchers\daemon.bat`；雙擊即 `cd` 到 repo 並啟動 `claude "/loop 30m /tick"`。
- **Linux / macOS**：`bash {{repo 絕對路徑}}/launchers/daemon.sh`（或建 `.desktop` 捷徑 / alias 指向它）。桌面環境的自動啟動也可掛這支。

## 前提

- `claude` CLI 已安裝且在 PATH（打 `claude --version` 有回應）。
- 機制：`claude "<初始訊息>"` 會用該訊息當第一句啟動互動階段；把訊息設成 `/loop 30m /tick`（或任一 `/<指令>`）就會觸發對應的自訂 slash command。

## 加新的

1. 在 `.claude/commands/<名>.md` 寫指令（frontmatter `description:` + 指令本文）。
2. 複製 daemon.bat / daemon.sh、把 `/loop 30m /tick` 換成 `/<名>`。
3. 在上表加一列。
