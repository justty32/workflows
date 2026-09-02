# SESSION-LOG — 進度（只列 open）

[INDEX](INDEX.md)｜等使用者的另記 [WAIT_USER](WAIT_USER.md)

**寫入時機**：
1. **開始**多步驟工作前先寫一行 open（不是做完才寫）；硬中斷時本檔才有「進行中」。
2. **每次 commit 後**更新或刪除該行。
3. 條目格式：`- [工作流] 一句 open 狀態 → 下一步 / 連結`；完成即刪，歷史交給 git log，決策落到 [workflows/decisions.md](workflows/decisions.md)。

> 膨脹就拆：過大就開 `session_logs/` 按工作流拆檔＋index（照 [STRUCTURE](STRUCTURE.md)）。

## 最新進度

- [planning] 可組合單元方案（中插契約進 `STRUCTURE.md`／`TEMPLATE.workflow.md`、`skills/` 定位、抽 `commit.md`）已定案但**未實作** → 方案全文見 [investigation/notes/composable-units.md](workflows/investigation/notes/composable-units.md)
- [refactor] 精簡稽核已裁示待做：heartbeat README 的 Windows `TZ` 踩坑段下沉到 `workflows/`；`team-model.md` 升成正規 `team-model/README.md`（所有連結跟著改）；其餘 11 項「要人決定」仍待裁 → 稽核報告在 2026-09-02 的 session scratchpad，明天先重跑一次稽核再動
- [feature-dev] `wf-lint.sh` 加 `--exclude a,b`／`.wf-lint-ignore`，讓 `--strict .` 對本 repo 跑時跳過 `template`、`flavors`、`examples`、`skills`；做法見 v0.6 CHANGELOG 未完成項 → 之後 CI 加一步對 `wf/` 跑 lint
- [testing] `python -m pytest tools` 在 Windows 直接跑紅 23 條：subprocess 的 `bash` 解析到 WSL bash 且 checkout 是 CRLF；在 LF 正規化副本＋WSL 下 53 全綠 → 修法：`.gitattributes` 把 `*.sh` 釘 LF，或測試改用 Git Bash 路徑
- [investigation] 9 篇筆記已寫；之後若有新 repo 一併走 investigation → 索引在 [investigation/README.md](workflows/investigation/README.md)

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|

> 某工作流長出自己的 `session-log.md` 後加一列；空表很正常。
