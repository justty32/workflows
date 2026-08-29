# todo-cli — AI agent 專案備忘

todo-cli = **一個用 Node.js（TypeScript）寫的命令列待辦工具，資料存在使用者家目錄的 `~/.todo.json`**。本檔是最頂層路由器：只指向下一層，細節一律不寫這裡（分層原則見 [STRUCTURE.md](STRUCTURE.md)）。

## 開場與入口

- 每個 session 先跑 `grep -c '^- \[' SESSION-LOG.md WAIT_USER.md`：非 0 才打開 [SESSION-LOG.md](SESSION-LOG.md)（我的 open 進度）/ [WAIT_USER.md](WAIT_USER.md)（等使用者的事）。
- **碰原始碼前**：慣例與 code map → [workflows/common/conventions.md](workflows/common/conventions.md)、[workflows/common/code-map.md](workflows/common/code-map.md)；環境與指令 → [workflows/dev-env.md](workflows/dev-env.md)。
<!-- wf-insert:AGENTS -->
- **使用者要你動手做事** → [WORKFLOWS.md](WORKFLOWS.md)：依意圖派發到工作流入口，再讀該入口檔。
- **想看專案長怎樣** → [INDEX.md](INDEX.md)。
- 使用者偏好、確認邊界、分支慣例 → [workflows/common/user.md](workflows/common/user.md)。

## 鐵律（always-on，任何工作流任何時候都遵守）

1. 重構 / 整理**不改原意**：開發＝行為不變且驗證綠燈（`npm test`、`npm run lint`、`npm run build`）；非開發＝內容原意不變，對照 `Done when:` 驗收。
2. **不可逆或對外的動作**（push、刪除、對外送出、動使用者真實的 `~/.todo.json`）必須有**授權來源**：使用者當場確認，或使用者**親自登記**在清單裡的項目（如 routines / schedule）。兩者都沒有就先問。
3. 各工作流的**具體流程在它自己的入口檔**，不在頂層。

<!-- wf-kernel v0.2 (2026-08-29) -->
