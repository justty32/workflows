# SESSION-LOG — 進度（只列 open）

[INDEX](INDEX.md)｜等使用者的另記 [WAIT_USER.md](WAIT_USER.md)

**寫入時機，固定三條**：
1. **開始**一件多步驟工作前先寫一行 open（不是做完才寫）——硬中斷時本檔至少反映「進行中」。
2. **每次 commit 後**更新或刪除該行。
3. 條目格式固定：`- [工作流] 一句 open 狀態 → 下一步 / 連結`。完成即整條刪除，歷史交給 git log；設計決策落到 [workflows/decisions.md](workflows/decisions.md)。

> 膨脹就拆：本檔過大就開 `session_logs/`，按工作流拆檔＋一個 index（照 [STRUCTURE](STRUCTURE.md)）。

## 最新進度

（目前無 open 項）

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|
