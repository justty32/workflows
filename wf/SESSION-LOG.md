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

- [planning] **下次開工先讀這條。** workflows 併入 aos（使用者 2026-11-13 裁：做法與內容變成 aos 的東西、repo 不掛進去、本 repo 之後幾乎不再更新；見 [knowledge/decisions.json](knowledge/decisions.json) 最前面兩筆）。做法：一次一塊由 repo-aos 的線抄進 aos 當正本，我備料與判斷，併完的在本 repo 標「已搬走」、不兩邊同時改。**已搬**：第 1 塊（組織原則，aos 159414053）、第 2 塊（工作流範本＋tidy 一組，aos dbefe6fd2），清單在 [knowledge/structure.json](knowledge/structure.json) 的 `moved`。**待落檔**：備料 `aos-prep/kernel/`、`aos-prep/dev/`（獨立稽核與複核的發現都已修，最終 commit 見 `git log -1 -- aos-prep`；複核報告在留底夾的 `prep-audit2.md`，登記不修的 N8–N10 在各批報告的 `unsure`）——repo-aos 下次在公司機開工時落成第 3、4 塊（本 repo 未 push，家機看不到）。**等使用者裁**：題目由 repo-aos 彙整在 aos repo 的 `proto8/thinking/2026-11/13/aos-1113-收工待裁.html`（W11～W22）。**不做**：其餘五包不併（使用者 2026-11-13 裁，見 decisions 最前面那筆），備料到 kernel、dev 兩批為止。**留底**：研究、稽核報告與兩份契約在 repo 外的 `~/code/wf-agent-scratch-1113/`（本 repo 的 lint 對所有檔套 8 KB，放不進來）；經過在 aos repo 的 `proto8/thinking/2026-11/13/workflows-into-aos.md`。 → 下一步：收 repo-aos 的落檔 commit 後在 `aos-prep/_index.json` 的 `status` 標已搬走；push 要先問使用者（未 push 的歷史裡有帶帳號名的絕對路徑，見下面 [refactor] 那條）
- [refactor] `wf/tools/` 的檢查工具不帶進 aos（使用者裁），已知的假綠案例已交給 repo-aos，本 repo 這套維持現狀不再修；`structure/tidying.json#/split` 裡的 `#/split_method` 該是完整路徑（已搬走的段，已告知 repo-aos，本 repo 不改）；**push 前**：未 push 的 commit 裡 `d2d87e7`、`3f2e927`、`add7744`（對照底稿）與 `9352168`、`ea562a1`（json_text 檔頭）的內容含帶帳號名的絕對路徑，現行檔已清掉、歷史還在；這是公開 repo，push 前問使用者要不要先改寫這段未公開的歷史
- [planning] 可組合單元方案（中插契約進 `STRUCTURE.md`／`TEMPLATE.workflow.md`、`skills/` 定位、抽 `commit.md`）已定案但**未實作** → 方案全文見 [knowledge/notes/composable-units.json](knowledge/notes/composable-units.json)
- [refactor] 精簡稽核已裁示待做：heartbeat README 的 Windows `TZ` 踩坑段下沉到 `workflows/`；`team-model.md` 升成正規 `team-model/README.md`（所有連結跟著改）；其餘 11 項「要人決定」仍待裁 → 稽核報告在 2026-09-02 的 session scratchpad，明天先重跑一次稽核再動
- [feature-dev] `wf-lint.sh` 加 `--exclude a,b`／`.wf-lint-ignore`，讓 `--strict .` 對本 repo 跑時跳過 `template`、`flavors`、`examples`、`skills`；做法見 v0.6 CHANGELOG 未完成項（tidy 已改成對範圍跑，這條動機變弱，做不做待定）→ 之後 CI 加一步檢查 `wf/`（現在是 `python3 wf/tools/index_check.py wf`）
- [testing] `.gitattributes` 已把行尾釘成 LF（2026-11-13），WSL 上 lint 跑得動；但 `python -m pytest tools` 還沒重驗：WSL 這台沒裝 pytest、也沒有 `python` 指令（只有 `python3`），Windows 端沒重跑 → 裝 pytest 等使用者（已記 [WAIT_USER](WAIT_USER.md)）；裝好後兩邊各跑一次，綠了就刪這條
