# CHANGELOG — kernel 變動記錄

每次 kernel（`template/`）或導入契約變動記一節：改了哪檔、**既有專案要不要跟**。版本戳在 `template/AGENTS.md` 尾端 `<!-- wf-kernel vX.Y (日期) -->`，導入後 `grep wf-kernel AGENTS.md` 查自己是哪一版。kernel-owned / project-owned 分類見 [IMPORT.md](IMPORT.md)。

## v0.5 (2026-08-30)

來源專案一輪整理長出的通用做法回抽進 kernel：tidy 升成資料夾並附踩坑與管理線簡報、`WORKFLOWS.md` 加「可以跳流程」、`WAIT_USER` 拆法定死、`wf-lint` 加 `#錨點` 檢查；dev 包補 moving-things（搬檔六類斷裂）、「綠燈不等於有檢查」、真相層優先序，以及 analysis／patch 兩個可選工作流。

- `workflows/tidy/`（整夾）→ kernel-owned 覆蓋；既有專案要跟：刪舊 `workflows/tidy.md`、複製整夾，所有指向 `tidy.md` 的連結改成 `tidy/README.md`。
- `WORKFLOWS.md` → project-owned 手動套「可以跳流程」並改 tidy 入口；dev 有 refactor 時另改成資料夾入口並加 moving-things 派發列。
- `STRUCTURE.md` → kernel-owned 覆蓋：活狀態膨脹時拆 `session_logs/`／`wait-user/` 並只留導航，tidy 連結同步。
- `WAIT_USER.md` → project-owned 手動套：統一拆成 `wait-user/`，hub 留 `| 類別 | open | 清單 |` 導航表；既有專案要跟。
- `workflows/planning.md` → project-owned 手動套交接段；有 dev investigation 的專案補「只是要調查清楚」分流。
- `workflows/common/user.md` → project-owned 手動套：回答「要不要」時附可執行判準、門檻數字與後果。
- `workflows/common/data-files.md`／`data-files-fmt.md` → kernel-owned 覆蓋：改 tidy 路徑、補錨點檢查契約，並把 `git-top` 說明去專案化。
- `.claude/commands/wf-lint.md` → kernel-owned 覆蓋：新增 `BROKEN-ANCHOR` 說明。
- `tools/check_anchors.py`＋`tools/wf-lint.sh` → kernel-owned 覆蓋；**行為變更**：壞錨點計入 `broken`，原本綠燈的專案可能變紅，應修連結而不是關檢查。
- `tools/wf-lint.sh`＋`tools/check_anchors.py` → kernel-owned 覆蓋；修正 `broken` 透過 0–255 exit status 傳值造成的計數溢位（例如顯示 517 而非實際 `BROKEN` 行數），並讓 Markdown／資料檔掃描排除 `archive/`、reference/vendor 與 `.gitmodules` 宣告的 submodule；既有專案覆蓋後總數會回復精確且通常大幅下降。
- `tools/wf-init.sh` → kernel-owned 覆蓋：複製清單納入 `check_anchors.py`；本 repo 另加 `tools/test_check_anchors.py`。
- `AGENTS.md` 版本戳 → v0.5，project-owned 手動套；既有專案要跟。
- dev `workflows/refactor/`＋`moving-things.md` → flavor 檔直接覆蓋，既有專案刪 `refactor.md`、複製整夾並重寫連結。
- dev `testing.md`、`common/code-map.md`、`common/conventions.md`、`investigation.md` → project-owned 手動套四類測試、檢查器雙向驗證、真相層優先序與調查流程；既有專案要按實況填。
- dev 新增 `analysis.md`／`patch.md` → 可選工作流，需用才導入；`WORKFLOWS.dev.md`／`README.md` → flavor 內容表與派發表同步，既有專案依實際選用手動套。
- `examples/` → 同步 kernel v0.5 與已納入的 flavor；`README.md`、`IMPORT.md`、`docs/` 同步本 repo 說明。

- multi-agent 包 `workflows/dispatch.md` → 資料夾 `workflows/dispatch/`：`README.md`（原內容＋六條最容易錯的、兩層派線、多信任但收線對證據、休眠前自檢；含活狀態表，project-owned）、新增 `driving-cli-agents.md`（互動式 tmux／非互動 exec 啟動、監看三訊號、通訊、清理、收線七步）與 `lessons.md`（派線四條坑）→ 兩新檔 kernel-owned 直接加；既有專案把指向 `workflows/dispatch.md` 的連結改成 `workflows/dispatch/README.md`。
- 新增 multi-agent `tools/inbox_mail.sh`（`mail/<對象>/`、`topics/<主題>/` 投遞）、`inbox_poll.sh`（輪詢個人信箱＋訂閱主題＋自己的 `orders/<我>.md`，`--once`／`--watch`）、`notify_watch.sh`（長駐輪詢 `new/`，無事件靜默）→ kernel-owned，隨 `tools/` 複製；root 由 `WF_INBOX_ROOT`／`<script>/../inbox` 推導，STATUS 白名單同 `inbox_send.sh`。未升級的專案用不到。
- multi-agent `workflows/inbox/PROTOCOL.md` 通道升級路徑擴充（四通道「可否取代」欄、`orders/` append-only 與 `from:` 段標題、調度者指示優先於交接書、輪詢義務、`done/` 按日期合併成 `messages.md`＋`messages.json`）→ kernel-owned 整檔覆蓋；`inbox/README.md`、`ROSTER.md`（＋訂閱主題欄、已收線格封存）、`resources.md`（headful 瀏覽器也取桌面鎖、鎖目錄被刪檢查恆真）→ project-owned 手動套；`TEMPLATE.handoff.md`（暫存不 `rm`、整檔改寫用 Update、送出前對背景與工作矛盾）→ kernel-owned 覆蓋。
- 新增 multi-agent `workflows/team-model.md` ＋ `workflows/team-model/{context,speed,plans}.md`：角色三層（頂層／領導＝計畫制定者／工人）、聰明度分級表、token 消耗速度表、六項選人判準、context 管理五條、執行速度三因素、逐模型指揮心得表。入口、分頁 kernel-owned 直接加；上述三表與 `plans.md` project-owned，專案填模型、實測。既有專案複製四檔，WORKFLOWS.md／AGENTS.md／workflows/dispatch/README.md 補 team-model 指向。
- inbox 五通道（＋`teams/<團隊>/`）：`inbox_mail.sh` 加 `--up`（依 `teams/*/members` 自動投領導，工人不必知道上游名）、`--team`（僅成員、頂層可投）；`inbox_poll.sh` 自動發現團隊信箱，加 `--wait [--timeout N]` 醒鐘（有信 exit 0、逾時 exit 3 靜默）；dispatcher 多掃 new/。新增 `tools/inbox_team.sh`（create／add／close；收線搬至 `done/<日期>/teams/`）、`tools/test_inbox.sh`（14 條）。`workflows/inbox/PROTOCOL.md` 改五通道佈局，拆 `wake-policy.md`（各層醒鐘策略、`--wait`、領導轉發三規矩）→ kernel-owned 覆蓋。`inbox_send.sh` 路徑定址簽名不變，未升級專案不受影響。
- `workflows/inbox/ROSTER.md` 加「團隊」欄；上游改「有團隊就是 `members` 第一行」；註明團隊信箱自動發現、不列訂閱主題。`TEMPLATE.handoff.md` 回報並列「基本佈局 `inbox_send.sh <上游 inbox 路徑>`／升級後佈局 `inbox_mail.sh <我> --up`」，加「本線團隊」欄 → ROSTER project-owned 手動套、handoff 範本 kernel-owned 覆蓋。

- `tools/wf-lint.sh`＋新增 `tools/wf-lint-checks.sh` → kernel-owned 覆蓋。修 percent-encoding 誤判：連結目標含空白或括號要寫成 `%20`／`%28`，原本拿原樣字串判存在，存在的檔會被重複報 `BROKEN`；新增 `link_exists()`，原樣找不到且含 `%` 才解碼再判，只判存在、不改寫文件。母檔已抵 8 KB，檢查函式與 `lint_dir` 同時拆到 `wf-lint-checks.sh` 由 `source` 載入——**既有專案要一併複製這支新檔**，`wf-init.sh` 與下表 kernel-owned 清單已納入。`test_wf_lint.py` 加 4 條。
- `workflows/tidy/gotchas.md` → kernel-owned 覆蓋，加「執行環境」段：`command -v` 只判存在不判可執行，假 `python3` shim 會讓 BIGLIST／錨點／資料檔靜默跳過卻仍綠燈；CRLF 的 `.sh` 在 Linux／WSL 跑不動、`wc -c` 每行多 1 byte，8 KB 上限在 Windows 工作區會誤報。
- multi-agent `workflows/team-model.md` 二、三節兩張表 → 預填默認值並標「2026/09/02 由 justty32 給出的個人判斷」，`{{}}` 清空；表仍 project-owned，換自己的模型清單就整張改掉。

## v0.4.1 (2026-08-30) 與更早

見 [docs/CHANGELOG-history.md](docs/CHANGELOG-history.md)。
