# SESSION-LOG — 進度（只列 open）

[_index](_index.json)｜等使用者的另記 [WAIT_USER](WAIT_USER.md)

**寫入時機**：
1. **開始**多步驟工作前先寫一行 open（不是做完才寫）；硬中斷時本檔才有「進行中」。
2. **每次 commit 後**更新或刪除該行。
3. 條目格式：`- [工作流] 一句 open 狀態 → 下一步 / 連結`；完成即刪，歷史交給 git log，決策落到 [knowledge/decisions.json](knowledge/decisions.json)。

> 膨脹就拆：過大就開 `session_logs/` 按工作流拆檔＋index（照 [structure](knowledge/structure.json)）；記成日誌時照 structure 的日誌寫法（`wf/knowledge/structure.json#/logs`）。
>
> 工作流不另開 session-log，open 進度都記本檔。

## 最新進度

- [planning] workflows 併入 aos（使用者 2026-11-13 裁：做法與內容變成 aos 的東西、repo 不掛進去、本 repo 之後幾乎不再更新；見 [knowledge/decisions.json](knowledge/decisions.json) 第一筆）：一次一塊由 repo-aos 的線抄進 aos 當正本，我備料與判斷，併完的在本 repo 標「已搬走」、不兩邊同時改。**第 1 塊（組織原則）已搬**，清單在 [knowledge/structure.json](knowledge/structure.json) 的 `moved`；下一塊 repo-aos 想併 `workflow-template.json`，再來 tidy 一組 → 下一步：把「哪些綁 aos」的表與我的搬法寄給 repo-aos；flavors/ 裡還是 md 的通用工作流要先備料
- [refactor] `wf/tools/` 的檢查工具不帶進 aos（使用者裁），已知的假綠案例已交給 repo-aos，本 repo 這套維持現狀不再修；`structure/tidying.json#/split` 裡的 `#/split_method` 該是完整路徑（已搬走的段，已告知 repo-aos，本 repo 不改）
- [planning] 可組合單元方案（中插契約進 `STRUCTURE.md`／`TEMPLATE.workflow.md`、`skills/` 定位、抽 `commit.md`）已定案但**未實作** → 方案全文見 [knowledge/notes/composable-units.json](knowledge/notes/composable-units.json)
- [refactor] 精簡稽核已裁示待做：heartbeat README 的 Windows `TZ` 踩坑段下沉到 `workflows/`；`team-model.md` 升成正規 `team-model/README.md`（所有連結跟著改）；其餘 11 項「要人決定」仍待裁 → 稽核報告在 2026-09-02 的 session scratchpad，明天先重跑一次稽核再動
- [feature-dev] `wf-lint.sh` 加 `--exclude a,b`／`.wf-lint-ignore`，讓 `--strict .` 對本 repo 跑時跳過 `template`、`flavors`、`examples`、`skills`；做法見 v0.6 CHANGELOG 未完成項（tidy 已改成對範圍跑，這條動機變弱，做不做待定）→ 之後 CI 加一步檢查 `wf/`（現在是 `python3 wf/tools/index_check.py wf`）
- [testing] `.gitattributes` 已把行尾釘成 LF（2026-11-13），WSL 上 lint 跑得動；但 `python -m pytest tools` 還沒重驗：WSL 這台沒裝 pytest、也沒有 `python` 指令（只有 `python3`），Windows 端沒重跑 → 裝 pytest 等使用者（已記 [WAIT_USER](WAIT_USER.md)）；裝好後兩邊各跑一次，綠了就刪這條
