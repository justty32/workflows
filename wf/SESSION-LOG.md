# SESSION-LOG — 進度（只列 open）

[_index](_index.json)｜等使用者的另記 [WAIT_USER](WAIT_USER.md)

**寫入時機**：
1. **開始**多步驟工作前先寫一行 open（不是做完才寫）；硬中斷時本檔才有「進行中」。
2. **每次 commit 後**更新或刪除該行。
3. 條目格式：`- [工作流] 一句 open 狀態 → 下一步 / 連結`；完成即刪，歷史交給 git log，決策落到 [knowledge/decisions.json](knowledge/decisions.json)。

> 膨脹就拆：過大就開 `session_logs/` 按工作流拆檔＋index（照 [structure](knowledge/structure.json)）。

## 最新進度

- [planning] `wf/` 轉入 aos：試點已完成第 1 階段（index 組織的 json 節點、流程與知識分家；要點見 [knowledge/notes/wf-to-aos.json](knowledge/notes/wf-to-aos.json)）→ 下一步：用一陣子收集踩坑；私有 index（`wf/_index.local.json`）實際用起來；之後回寫 `template/`（v0.7）與 aos flavor
- [refactor] 試點留下待決的小項：`wf-insert` 插入標記消失後 flavor 片段怎麼併；tidy 原則 5（content-trim）`wf/` 沒跟上；tidy 的坑還寫 md 時代的做法；「agent 不自行 commit」與 feature-dev 流程尾端「→ commit」寫法不一致；`analysis/<project>/` 沒說相對哪裡；`index_check` 不驗單獨的 `#/…` 局部指標 → 逐項裁或順手修
- [planning] 可組合單元方案（中插契約進 `STRUCTURE.md`／`TEMPLATE.workflow.md`、`skills/` 定位、抽 `commit.md`）已定案但**未實作** → 方案全文見 [knowledge/notes/composable-units.json](knowledge/notes/composable-units.json)
- [refactor] 精簡稽核已裁示待做：heartbeat README 的 Windows `TZ` 踩坑段下沉到 `workflows/`；`team-model.md` 升成正規 `team-model/README.md`（所有連結跟著改）；其餘 11 項「要人決定」仍待裁 → 稽核報告在 2026-09-02 的 session scratchpad，明天先重跑一次稽核再動
- [feature-dev] `wf-lint.sh` 加 `--exclude a,b`／`.wf-lint-ignore`，讓 `--strict .` 對本 repo 跑時跳過 `template`、`flavors`、`examples`、`skills`；做法見 v0.6 CHANGELOG 未完成項 → 之後 CI 加一步對 `wf/` 跑 lint
- [testing] `.gitattributes` 已把行尾釘成 LF（2026-11-13），WSL 上 lint 跑得動；但 `python -m pytest tools` 還沒重驗：WSL 這台沒裝 pytest、Windows 端沒重跑 → 裝 pytest 要先問使用者；裝好後兩邊各跑一次，綠了就刪這條

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|

> 某工作流長出自己的 `session-log.md` 後加一列；空表很正常。
