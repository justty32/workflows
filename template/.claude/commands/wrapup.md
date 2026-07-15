---
description: routines 常駐精靈的一鍵清場——把手上進行中/待辦 dump 進 state，安心關窗、明天撿回
---

routines 常駐精靈的**一鍵清場收尾**（在常駐 session 的 CLI 手動下 `/wrapup`；快收工 / 懶得處理 / 要直接關 terminal 前用）。這指令刻意極薄，只交代：

從最頂層 [CLAUDE.md](../../CLAUDE.md) **一層層照分層樹走下去**（別繞開中間層），走到 **routines 工作流**（[workflows/routines/README.md](../../workflows/routines/README.md)），照它的「**收尾清場（`/wrapup`）**」段做——把手上進行中的活、待辦、還沒回的抉擇一股腦寫進 `state/carryover.md`，就能直接關窗，明天 daemon 起來自動撿回。

（這是「懶人快關」路徑，**只 dump 狀態、不做保存 / push**；要正式收尾保存 / push 走 routines 的 EOD 段。）
