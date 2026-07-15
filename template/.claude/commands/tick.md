---
description: routines 常駐精靈的一次心跳——判當地時段、讀 inbox、發短提醒
---

routines 常駐精靈（daemon）的**單次心跳**（由 [`launchers/daemon.bat`](../../launchers/README.md) 的 `/loop 30m /tick` 定時喚醒，也可在 CLI 手動下）。這指令刻意極薄，只交代兩件事：

1. **先確認現在的當地時間**（`{{時區，如 Asia/Taipei}}`：幾月幾號、星期幾、幾點幾分）——心跳要靠它判此刻該做哪段、有沒有到期的。取時間用 PowerShell（本機 Windows，Bash 的 `TZ=... date` 不一定生效、可能回 GMT）：
   ```powershell
   [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId((Get-Date), '{{時區 ID，如 Taipei Standard Time}}').ToString('yyyy-MM-dd dddd HH:mm')
   ```
2. 然後從最頂層 [CLAUDE.md](../../CLAUDE.md) **一層層照分層樹走下去**（別繞開中間層），走到 **routines 工作流**（[workflows/routines/README.md](../../workflows/routines/README.md)），照它的「心跳迴圈」段做。

**外包時挑對模型**（心跳只做短動作、重活一律外包，開 agent 時按複雜度選層級）：簡單雜務 → **haiku** agent；一般工作 → **sonnet** agent；複雜 / 需推理的 → **opus** agent。
