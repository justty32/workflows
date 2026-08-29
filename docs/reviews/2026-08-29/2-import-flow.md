# 角度 2：導入流程實測（kernel + dev flavor，標準 / 非侵入式）

## 實測結果

在 scratchpad 照 README + `flavors/dev/README.md` 五步合成 `dryrun/`（標準）與照 `non-invasive-import.md` 合成 `dryrun-ni/`（`wf/` 佈局），再用 `linkcheck.sh` 掃所有 `.md` 相對連結。

**標準導入：2 個壞連結**
- `WORKFLOWS.md → ../README.md`（〔模板說明〕裡「合併步驟見 README」連的是本 repo 的 README，導入後上一層沒這檔）
- `AGENTS.md → workflows/dev-env.md`（〔模板說明〕範例寫成真連結，檔不存在）

**非侵入式導入：22 個壞連結。`non-invasive-import.md` 說「`wf/` 內部彼此的相對連結不受影響」——不成立。** 三類：
1. **所有向上連到 `AGENTS.md` 的導覽列全斷**（`wf/INDEX.md`、`wf/WORKFLOWS.md`、`wf/DEV-GUIDE.md`、`wf/SESSION-LOG.md`、`wf/WAIT_USER.md`、`wf/workflows/{routines,schedule}.md`、`wf/workflows/{common,inbox,feature-dev}/README.md`、`conventions.md`）——AGENTS.md 搬到 `wf/` 上一層，`AGENTS.md` / `../AGENTS.md` / `../../AGENTS.md` 全指錯。
2. **`.claude/commands/wf-tick.md` ↔ `wf/workflows/tick.md` 雙向斷**，`wf/INDEX.md`、`wf/WORKFLOWS.md` 指向 `.claude/commands/wf-tick.md` 也斷。`non-invasive-import.md` **完全沒提 `.claude/` 該放哪**（Claude Code 只讀專案根的 `.claude/commands/`，它必須留頂層，所以「頂層只留兩個檔」的承諾其實是「兩檔 + 一個隱藏目錄」）。
3. 同標準導入的 `../README.md`、`dev-env.md`。

**其他摩擦**
- **inbox 地址慣例被非侵入式佈局打破**：inbox 工作流的地址定義是「對方工作資料夾底下的 `inbox/`」，非侵入式後實際在 `wf/inbox/`，AGENTS.md 還寫「放信處是 repo 根的 `inbox/`」。別的 agent 照通訊錄寄信會找不到信箱。文件沒講。
- 貼派發表後，`WORKFLOWS.md` 那段〔模板說明〕與 HTML 註解仍留著，要另外手刪；`WORKFLOWS.dev.md` 自己也帶一段〔模板說明〕菜單，貼進去等於又多一段要清。
- 導入後殘留：`{{` 24 處 / 8 檔，〔模板說明〕15 檔（template + flavors 共 36 段，其中 9 段是「不用就整段/整檔刪」型指令）。沒有任何機械化的「導入完成檢查」。
- 本 repo 內 `flavors/` 直接掃有 31 個壞連結（README 已宣告為預期），但這也代表 repo 自身**無法用連結檢查守住品質**——kernel 的 2 個真壞連結就是這樣漏掉的。

---

### 1. 非侵入式導入文件要重寫：列出實際要改的連結，不能說「不受影響」
**問題**：實測 22 斷；文件只叫人改頂層兩檔的向下連結，`wf/` 內所有向上連 `AGENTS.md`、`.claude/` 相關連結全漏。
**建議**：(a) 文中明列三類要改的連結與一行 `sed`（`AGENTS.md` → 多一層 `../`；`.claude/commands/wf-tick.md` → `../.claude/...`；`wf-tick.md` 內 `../../workflows/tick.md` → `../../wf/workflows/tick.md`）；(b) 補「`.claude/` 必須留專案根」與「inbox 地址變成 `wf/inbox/`，通訊錄與 AGENTS.md 那句要同步改」；(c) 或反過來讓 kernel 內部**不再用相對路徑向上連 AGENTS.md**（導覽列只連同層或向下；AGENTS.md 是入口，沒人需要從下面點回去）。
**優先級：高**

### 2. 修 kernel 自身 2 個真壞連結
**問題**：`template/WORKFLOWS.md` 的 `../README.md`、`template/AGENTS.md` 的 `workflows/dev-env.md` 導入後必斷。
**建議**：前者改成純文字「見本模板 repo 的 README」（或連到 GitHub URL）；後者範例改成反引號路徑、不做連結。
**優先級：高**

### 3. 給 repo 加一個連結檢查腳本（並在 README 導入步驟末尾要求跑）
**問題**：沒有任何自動檢查，kernel 壞連結與非侵入式錯誤宣稱都是因此漏掉。
**建議**：把 `scratchpad/linkcheck.sh`（20 行 bash，只查相對 `.md`/目錄連結）收進 repo `tools/`，README 步驟加第 5 步「跑 `tools/linkcheck.sh .`，0 個 BROKEN 才算導入完成」。flavors/ 在本 repo 內掃會有預期壞連結，可讓腳本接受 `--merged` 模式或直接對合成後的 dryrun 掃。
**優先級：高**

### 4. 導入可以全自動化，做一支 `tools/wf-init.sh <flavor...> [--non-invasive DIR]`
**問題**：目前五步全手動；合併、貼表、改連結都是純機械操作，人與 Claude 各做各的容易走樣。
**建議**：腳本負責：複製 kernel → 複製 flavor `workflows/` → 用標記（現成的 `<!-- ↓↓↓ … ↑↑↑ -->`）把 `WORKFLOWS.<flavor>.md` 貼入並刪佔位行 → 非侵入式時搬 `wf/` 並 sed 改連結 → 最後跑 linkcheck。**無法自動化的只有兩件事**：填 `{{}}`（要專案事實）與判斷〔模板說明〕裡「用不到就刪」的分支；腳本結束時印出兩張清單（殘留 `{{` 位置、含〔模板說明〕的檔）交給人或 Claude 收尾。
**優先級：高**

### 5. 「讓 Claude 代勞」要有給 Claude 的指示檔
**問題**：README 步驟 4 只說「把 repo 路徑給 Claude」，沒有任何 agent 可執行的流程；Claude 只能讀 README 自行發揮，每次結果不同，也不會知道要改非侵入式的 22 個連結。
**建議**：加 `IMPORT.md`（或 `.claude/commands/wf-init.md` 放在**本 repo**）：明確步驟＝跑 `tools/wf-init.sh` → 逐檔處理 `{{` → 逐段處理〔模板說明〕（列出 9 段「條件刪除」型的判斷題）→ 跑 linkcheck → 回報殘留清單。README 步驟 4 改成「叫 Claude 讀 IMPORT.md」。
**優先級：高**

### 6. 完全沒有「升級」路徑：kernel 改版後既有專案怎麼跟
**問題**：導入＝複製後脫鉤；kernel 已改過 5 次（拆 flavor、加 inbox、加 tick），先前導入的專案無從得知、也無法安全合併（佔位符填過、模板說明刪過，diff 全是噪音）。
**建議**：(a) 在 `template/` 放 `KERNEL-VERSION`（或 AGENTS.md 底部一行 `<!-- wf-kernel: 2026-08-29 -->`），本 repo 加 `CHANGELOG.md` 每次 kernel 變動寫「對既有專案要做什麼」；(b) 把檔案分成**kernel-owned**（`DEV-GUIDE.md`、`workflows/tick.md`、`workflows/inbox/README.md`、`TEMPLATE.letter.md`、`/wf-tick`：無佔位符、可直接整檔覆蓋）與 **project-owned**（`AGENTS.md`、`INDEX.md`、`WORKFLOWS.md`、活狀態、`routines.md` 清單：只讀 CHANGELOG 手動套），在 INDEX 或 IMPORT.md 標明；(c) 長期可考慮 `wf-upgrade.sh` 只覆蓋 kernel-owned 檔。
**優先級：中**

### 7. 〔模板說明〕分兩種，該用不同標記
**問題**：36 段〔模板說明〕混著「純解說（讀完刪）」與「條件指令（不用 X 就刪整檔並改上層那列）」；後者一被機械刪除，上層 INDEX / common/README 的列就成孤兒，實測 `common/README` 那列 `conventions`/`writing` 就是這種。
**建議**：條件指令型改標 `〔導入判斷〕`，並各自列明「刪掉後要同步改哪幾個檔的哪一列」；IMPORT.md 把它們集中成一張 checklist。
**優先級：中**

### 8. `WORKFLOWS.<flavor>.md` 片段的〔模板說明〕菜單不該被貼進專案
**問題**：片段除派發表外還附一段菜單與規劃管線說明，貼進 `WORKFLOWS.md` 後多一段要清；且它的 `[DEV-GUIDE](DEV-GUIDE.md)`、`[gotchas](workflows/common/gotchas.md)` 假設貼在專案根，非侵入式下正好也對（都在 `wf/`），但在本 repo `flavors/` 裡是壞的。
**建議**：片段只留表；菜單搬回 flavor README。
**優先級：低**

### 9. inbox 在非侵入式佈局下的地址規則要明文
**問題**：見實測。「地址＝工作資料夾/inbox/」與「一切收進 wf/」互斥。
**建議**：二選一寫進 `non-invasive-import.md`：inbox 例外留根（推薦，因為它本來就是對外介面）、或通訊錄地址一律寫完整路徑含 `wf/`。
**優先級：中**

### 10. 導入完成的定義（`Done when:`）
**問題**：模板到處教人寫 `Done when:`，自己的導入流程卻沒有。
**建議**：README 結尾加一行：`Done when: grep -r '{{' 為 0、grep -r '〔模板說明〕' 為 0、linkcheck 0 BROKEN、AGENTS.md ≤ N 行`。
**優先級：低**
