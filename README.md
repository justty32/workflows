# 通用分層工作流模板（AGENTS.md 為入口）

> Written in Traditional Chinese; the structure itself is language-agnostic.

一套從實際專案淬鍊出來的**分層工作流**，以 AGENTS.md 為最頂層路由器，可套用到任何種類的專案（不限程式）。對 AI agent 友善：沿層層 index 往下走，只讀要的那一層。

## 核心思想（一分鐘版）

1. **分層樹**：專案文檔是一棵樹，每層**只指向下一層、不存下層細節**：`AGENTS.md`（最頂，薄路由器）→ `WORKFLOWS.md`（依意圖派發）/ `INDEX.md`（結構地圖）→ 各工作流入口 → 工作流內容 → 子工作流…
2. **檔名語意**：**README**＝進資料夾先讀的入口；**INDEX**＝該資料夾頂層結構的索引。小資料夾兩者合一。
3. **durable 知識歸層**：長期知識歸到所屬工作流／那一層，**絕不往上堆**——AGENTS.md 因此永遠很薄。
4. **活狀態只列 open**：進度記 `SESSION-LOG.md`、等使用者的記 `WAIT_USER.md`，**完成即刪**；「改了什麼」交給 git log，「為什麼」記 `workflows/decisions.md`。
5. **膨脹即拆、雜亂即分類**：整理原則與四級成長收在 `STRUCTURE.md`——**被動參考**，整理結構時才取用；同質記錄表 >1 KB 進資料檔（`wf-table/1`），給人導航的連結表留 md。
6. **鐵律極少而 always-on**：3–5 條任何時刻都適用的鐵律常駐 AGENTS.md（不改原意、不可逆動作要有授權來源…）。

這六條只在這裡與 [`template/STRUCTURE.md`](template/STRUCTURE.md) 各寫一次。

## 佈局：一個 kernel + 多個 flavor 包

領域中立的骨架抽成**共用 kernel**（[`template/`](template/)）；各領域工作流拆成 **flavor 包**（[`flavors/`](flavors/)）。導入 = **kernel + 挑幾個 flavor 包合起來**。

```
template/   共用 kernel（整包拿走）
flavors/    七個領域包（見下表）
tools/      導入／檢查／資料檔與整理工具
examples/   合併成品（dev / knowledge）
docs/       本 repo 的文件
```

### 挑你的 flavor 包

| 包 | 適合的專案 | 工作流 |
|----|-----------|--------|
| [dev/](flavors/dev/README.md) | 程式開發 | feature-dev、testing、refactor/moving-things、investigation、analysis、patch、dev-env、conventions、code-map |
| [knowledge/](flavors/knowledge/README.md) | 寫作／研讀／規劃／決策／學習 | write、digest、plan-a-thing、decide、learn、organize、writing、info-map |
| [teaching/](flavors/teaching/README.md) | 做成給別人學的教材 | plain-explain、study-site |
| [research/](flavors/research/README.md) | 持續累積的文獻／資料庫（> 30 件）| source-intake、backlog、survey、collide |
| [ops/](flavors/ops/README.md) | 伺服器／服務維運 | inventory、incident、deploy |
| [heartbeat/](flavors/heartbeat/README.md) | 定期喚醒做例行事務 | tick、routines、schedule（引擎借 agent 工具或 OS 排程）|
| [multi-agent/](flavors/multi-agent/README.md) | 多 agent／session 協作 | team-model（角色三層／選模型）、inbox（五通道、上游路由、醒鐘）、resources（資源鎖）、dispatch（派線／驅動 CLI agent／收線）|

**混合型專案**兩包以上都合，派發表依序貼進同一個 `WORKFLOWS.md`；觸發詞重疊怎麼分流見各包 README。gotchas、planning、decisions、user 只有 kernel 一份。

> flavor 包的連結照**合併後**佈局寫，在本 repo 直接點會指不到 kernel（預期）；`wf-lint.sh --self` 合併後才檢查。

## 如何套用到新專案

**Done when**：`{{` 為 0、〔模板說明〕為 0、〔導入判斷〕為 0、`wf-lint` 0 BROKEN。

```bash
tools/wf-init.sh --target <你的專案根> --flavor dev,heartbeat   # 既有專案建議加 --non-invasive wf
```

1. **合併**：腳本複製 kernel、合入 flavor、貼入派發片段並改寫非侵入式連結；手動步驟見各包 README 與 [non-invasive-import](docs/non-invasive-import.md)。
2. **填 `{{}}`**：搜尋 `{{` 填成專案實況（唯一需要專案事實的步驟）。
3. **處理〔導入判斷〕**：每段是「條件 → 動作。同步：哪些檔」，決定後刪段並同步。**不要的工作流＝刪檔＋刪派發表那一列**（README／INDEX 提到它的列一併刪）。
4. **刪〔模板說明〕**：純解說，讀完刪整段。
5. **驗收**：`tools/wf-lint.sh --strict <專案根>`（Claude Code 可用 `/wf-lint`）。

也可以讓 agent 代勞：把本 repo 路徑給它，說「照 [IMPORT.md](IMPORT.md) 用 dev flavor 幫我的專案建立工作流」。

## template/（kernel）內容

| 檔案 | 角色 |
|------|------|
| [AGENTS.md](template/AGENTS.md) | 最頂層路由器（≈1.5 KB）：開場 checklist＋入口＋鐵律 |
| [CLAUDE.md](template/CLAUDE.md) | 轉址 → AGENTS.md |
| [WORKFLOWS.md](template/WORKFLOWS.md) | 派發器：flavor 派發表貼入區＋kernel 內建表＋活狀態判別表 |
| [INDEX.md](template/INDEX.md) | 結構地圖 |
| [STRUCTURE.md](template/STRUCTURE.md) | 被動結構參考：分層、膨脹即拆、四級成長、archive |
| [SESSION-LOG.md](template/SESSION-LOG.md) | open 進度 |
| [WAIT_USER.md](template/WAIT_USER.md) | 等使用者做／驗證的事（open-only）|
| [workflows/TEMPLATE.workflow.md](template/workflows/TEMPLATE.workflow.md) | 新工作流入口檔骨架 |
| [workflows/planning.md](template/workflows/planning.md) | idea → roadmap → 詳規 → 執行 管線 |
| [workflows/decisions.md](template/workflows/decisions.md) | 為什麼選 A 不選 B |
| [workflows/tidy/](template/workflows/tidy/README.md) | 文件整理：封存／分類／合併小檔／抽資料檔／拆大檔；附 `gotchas.md` 踩坑與 `manager-brief.md` 管理線簡報 |
| [workflows/common/](template/workflows/common/README.md) | 共享：gotchas、user、glossary、data-files |
| [workflows/common/data-files.md](template/workflows/common/data-files.md) | 資料檔契約 `wf-table/1` |
| [data-files-fmt.md](template/workflows/common/data-files-fmt.md) | `$fmt` 代號 |
| [.claude/commands/wf-lint.md](template/.claude/commands/wf-lint.md) | `/wf-lint` 薄殼（Claude Code 適配層）|

## tools/

| 工具 | 做什麼 |
|------|--------|
| `wf-init.sh` | 導入：複製 kernel、合入 flavor 包、非侵入式改寫連結 |
| `wf-lint.sh` | 檢查：壞連結與錨點／超標檔／條列／資料檔連結／殘留 |
| `check_anchors.py` | 驗 md 連結的 `#錨點`（heading slug 與顯式 id）在目標檔存不存在 |
| `tabledb.py` | 資料檔 CRUD 與連結查驗 |
| `find_big_lists.py` | 列出超標的表／清單，附連結數判斷是不是連結表 |
| `fix_moved_links.py` | 搬檔後照 `moves.tsv` 重寫連結 |

## 不只 Claude

`AGENTS.md` 是**中立入口**；`CLAUDE.md` 與 `.claude/` 只是 **Claude Code 適配層**，可換可刪。

| 工具 | 入口怎麼讀 | slash 指令 / hook 對應 |
|------|-----------|----------------------|
| Codex CLI | 原生讀 `AGENTS.md` | 無 → 跑 `tools/` 腳本 |
| Claude Code | `CLAUDE.md` 轉址 → `AGENTS.md` | `.claude/commands/`：`/wf-lint`、`/wf-tick` |
| Gemini CLI | `--redirect GEMINI.md` 產轉址檔 | 無 → 跑 `tools/` 腳本 |
| 其他 agent 工具 | 讀 `AGENTS.md`；不支援就 `--redirect <指示檔名>` | 沒有就跑 `tools/` 腳本 |

## 升級既有專案

導入是複製後脫鉤。最新 **v0.5** 變動記在 [CHANGELOG.md](CHANGELOG.md)（改哪檔、要不要跟）；版本戳可查自己是哪版，升級分類見 [IMPORT.md](IMPORT.md)，repo 文件見 [docs/](docs/README.md)。

## 這套為什麼有效

**省 context**：薄入口＋層層派發，agent 只載入當前任務要的知識。**不腐化又跟著長**：知識有唯一歸屬層、活狀態完成即刪、過時進 `archive/`。**機械兜底**：`wf-lint` 抓壞連結與壞**錨點**、超標檔、>1 KB 條列與資料檔壞連結、佔位殘留，CI 對每包合併後再檢查。
