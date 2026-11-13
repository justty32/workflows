# wf → aos 對照底稿（事實底稿，不含推薦）

2026-11-13，wf-agent 的子 agent 唯讀調查。沒改任何 repo 檔、沒跑 aos-* 指令；只用 Read／ls／grep／cat／python 讀檔，與兩次唯讀 aos 工具（`peek_clock`、`index_view`）。

篇幅照使用者給的四個面向分配：**導航層（第 2 節）、儲存架構（第 3 節）、資料儲存（第 4 節）寫深**；lint 次要，壓成第 1 節一張短表。

## 0. 記號與路徑縮寫

- **【查】**＝讀過原檔或跑過唯讀指令確認；**【推】**＝從文件推出、沒實測；**【缺】**＝找過沒找到，或沒讀到。
- 路徑縮寫：
  - `K`＝`/home/<user>/aos-home/knowledge`（aos 共用知識庫；是 `~/repo/aos/proto8/knowledge` 的**複本**，要重抄才更新，`P/howto.json#/daemon/what_takes_effect`）
  - `W`＝`/mnt/c/code/mine/workflows`（本 repo）
  - `T`＝`/home/<user>/repo/aos/proto8/thinking/2026-11`
  - `A`＝`/home/<user>/repo/aos`（aos repo；自己也導入了 wf，版本戳 `v0.5 (2026-08-30)`，`A/AGENTS.md` 末行）
  - `P`＝`/home/<user>/aos-home/ws/public`（這台機器的共用實況，eca_main 保管）
  - `H`＝`/home/<user>/aos-home`（定義與範本）
  - `O`＝`/mnt/c/code/<user>/ops-notes`
- 「wf」＝`W/template/`（真相）＋`W/flavors/`；`W/wf/` 是落後的導入成品（`W/wf/AGENTS.md:22` 是 v0.5.1、`W/template/AGENTS.md:22` 是 v0.6）【查】。
- 檔案大小一律 `wc -c` bytes。

## 0.5 一頁背景

- aos＝AI agent 當 Linux 行程跑在資料夾裡；八個詞見 `K/aos/_description.json`【查】。
- 兩種身體：agent-fsm（aos 自己的迴圈）與 eca（Claude Code／Codex 跑每一輪）（`K/aos/body.json`）。這台機器上的 agent 全是 eca（`P/agents.json` 各節 `kind`）【查】。
- eca 範本只掛 7 包 26 支 aos 工具（gadgets、events、self、def、mailbox、json、index），**沒有** look／change／delete／shell／subagent／goal／todo（`K/aos/packs.json#/about`）；eca 的 aos hook 看不到 CLI 自己的工具（`K/aos/body.json#/brain_tools`）【查】。
- Claude Code 子 agent 只拿到 9 支唯讀 aos 工具：peek_clock、peek_now_time、math、json_get、json_ls、json_search、json_len、json_multi_get、index_view（`H/agents/ops-agent/tools_sub.json`）【查】。

---

## 1. 對照總表（逐機制；導航、儲存、資料三塊細節在第 2–4 節）

程度：**直接**＝可直接取代；**部分**；**無**。

### 1A. 入口與規則

| wf 機制 | 解決什麼 | aos 對應物 | 程度 | 落差 | 證據 |
|---|---|---|---|---|---|
| `AGENTS.md` 薄路由器 | 開場一頁知道往哪走 | 知識庫根 `_description.json`＋上層 `_index.json`；定義 `system.txt`（現在只兩句指向知識庫） | 部分 | `AGENTS.md` 是 CLI 依檔名自動載入（Codex 原生、Claude 經 `CLAUDE.md`）；agent-fsm 兩者都不讀（`T/13/main-session-in-aos.md`）。json 節點不會被任何 CLI 自動載入【推】 | `W/template/AGENTS.md`；`H/agents/ops-agent/system.txt`【查】 |
| `CLAUDE.md`／`--redirect` | 讓別的工具也進同一入口 | 無（aos 不管 CLI 讀哪個檔） | 無 | 不需取代，eca claude 照讀工作區 `CLAUDE.md` | `W/template/CLAUDE.md`【查】 |
| 鐵律 always-on | 每輪都在 | `system.txt`（agent-fsm 整份 system；eca claude 每輪附加；eca codex 只在新對話）、`self_system`、`K/aos/rules.json`（aos 自己的禁忌） | 部分 | 只換得了「放哪」；改一次 cache 失效一次；13 日結論是規矩**不抄進** system.txt（第 8 節） | `K/aos/me/self_system.json`、`K/aos/body.json#/system_history`【查】 |
| 鐵律硬閘（不可逆先問） | 授權來源 | agent-fsm 的 `before_tool`（exit 10 擋）；eca：工作區 `.claude/settings.json` 的 CLI hook 在 aos 起的 claude 也生效；定義可自帶 CLI 設定（11-13 施工） | 部分 | codex 身無對應接點；使用者 11-13「全面開放」 | `T/13/ops-agent-six-suggestions.md`、`T/13/ops-fixes-施工結果.md` B3【查】 |
| 開場 checklist（grep SESSION-LOG／WAIT_USER、`ls inbox`） | 開場看未完的事 | `mail_notify`（信）、`goal`、`self_state` | 部分 | 信有自動版，SESSION-LOG／WAIT_USER 沒有 | `K/aos/mailbox.json#/check`【查】 |
| WORKFLOWS／INDEX／README 導航 | 分層找入口 | `_index.json`、`_description.json`、`index_view` | 見第 2 節 | — | — |
| STRUCTURE 門檻、四級成長、archive、日誌寫法 | 自主整理 | `K/docs/02` 大小建議（推薦不訂死）、`$ref` 拆檔、`aos-grow`（只管可執行 slot）、`trash` | 部分／無 | 見第 3.1 節 | `W/template/STRUCTURE.md`【查】 |
| `TEMPLATE.workflow.md`／`Done when` | 工作流同一形狀 | 無內容範本（範本只有定義 `agent_def`、工具 `tools_def`）；`goal done` 只是宣告 | 無 | 長散文進 json 沒有建議形狀（第 4(d)） | `W/template/workflows/TEMPLATE.workflow.md`【查】 |

### 1B. 活狀態與記錄

| wf 機制 | aos 對應物 | 程度 | 落差 | 證據 |
|---|---|---|---|---|
| `SESSION-LOG.md` | `todo`（stack，≤50 條、≤300 字、別人看不到）、`goal`（一句） | 無（對 eca） | eca 不掛 todo／goal（使用者 11-11，見第 8 節 U7）；不進 git；13 日結論照舊記 md | `K/aos/tools/todo.json`、`K/aos/tools/goal.json`；`T/13/main-session-in-aos.md`【查】 |
| `WAIT_USER.md` | 人當一隻 agent：`~/.aos/stack/mailbox`（這台存在【查】），寄 `NEEDS-USER` | 部分 | 讀了≠回了；人不會被通知；沒有分類；不跨機（`T/12/wf-to-aos/02-寄信給人與主session.md`）；13 日照舊 | 同左【查】 |
| decisions、planning、gotchas、user、reply-style | 無；機器層級的坑有 `P/howto.json#/known_issues` | 無／部分 | 內容，見第 3 節 | 【查】 |

### 1C. lint 與工具（壓縮版）

| wf 檢查／工具 | aos 對應 | 程度 |
|---|---|---|
| BROKEN 連結、BROKEN-ANCHOR、OVERSIZE、BIGLIST(-LINKS)、QUERYCMD、RESIDUE、local hook（`W/tools/wf-lint.sh`、`wf-lint-checks.sh`） | 都沒有 aos 工具。index 層的檢查只有 aos repo 的腳本 `A/wf/tools/index_check.py`（EntryGone／EntryMissing／LinkBad／LinkMissing／IndexBad）與 `index_gen.py`（不帶參數＝查是否過期），不是 aos 工具；使用者 11-13 裁「索引檢查讓 ops-agent 自己寫」 | 無 |
| `inbox_pending` | `mailbox_peek`、`mail_notify` | 直接 |
| `fix_moved_links.py` | `aos-json ref --move`（搬節點留 `$ref`，`K/docs/02`）、`agent_def new` 改寫工具相對路徑；別處的引用沒人改寫（`T/12/wf-to-aos/02…` 邊緣狀況 7） | 部分 |
| `find_big_lists.py`、tidy 盤點指令 | `glob`／`grep`／`stat`／`view` 屬 look 包，eca 沒有 | 部分 |
| CI（`W/.github/workflows/wf-lint.yml` 跑 `--self`） | 無；Actions 上沒有 aos | 無 |

證據：`W/tools/wf-lint-checks.sh` 的 `lint_dir`；`T/13/index-build.md`；`T/13/ops-agent-six-suggestions.md` 第 2 題【查】。

### 1D. 導入、版本、適配層

| wf 機制 | aos 對應物 | 程度 | 落差 | 證據 |
|---|---|---|---|---|
| `wf-init.sh` 導入 | `agent_def new`（複製定義範本）；知識庫多庫＝複製一份資料夾 | 部分 | 複製的是定義，不是專案內容；沒有片段插入點 | `W/IMPORT.md`；`K/aos/agents.json#/agent_def`【查】 |
| 非侵入式佈局 `wf/` | 無（工作區就是那個資料夾） | 無 | — | `W/docs/non-invasive-import.md`【查】 |
| kernel／flavor | pack 疊合（`$override`）、定義範本 | 部分 | 只對工具與定義成立 | `K/aos/packs.json#/about`【查】 |
| 版本戳＋kernel-owned／project-owned 升級 | overlay（stack 只存對定義的差異、`reset`）；知識庫重抄 | 部分 | overlay 是「單隻 agent 對定義」，不是「專案對上游」；格式版本討論在 `T/09/format-versioning/` 沒讀【缺】 | `K/aos/definition.json#/overlay`【查】 |
| CHANGELOG、examples/ | 無 | 無 | — | 【查】 |
| `skills/`→`.claude/skills/<n>/SKILL.md` | eca claude 開了 `Skill` 工具；13 日結論 skill 放 repo `.claude/skills/`，codex 讀 `.agents/skills/` | 直接（沿用 CLI） | aos 本身不認 skill | `H/templates/eca-claude/cli.json`；`T/13/main-session-in-aos.md`【查】 |
| `.claude/commands/`（`/wf-lint`、`/wf-tick`） | CLI 照載入（ops-notes 實測；repo-aos 子 agent 以 skill 出現） | 直接（沿用） | 做成 aos 工具則逾時 10 秒／aos-mcp 60 秒 | `O/notes/aos-migration-plan.md` §8；`K/aos/tools_def.json#/tool_spec`【查】 |

### 1E. multi-agent 包

| wf 機制 | aos 對應物 | 程度 | 落差 | 證據 |
|---|---|---|---|---|
| inbox 檔案信 | `mailbox_send/peek/read`；人用 `aos-mailbox` | 直接（雙方都在樹上） | 樹外對象收不到（`--box wf/inbox` 會 `MailboxBad`）；讀完預設刪；11-13 施工 `keep: 檔名`／`--keep-to` 收寄留一行 jsonl 到工作區，但 `K/aos/mailbox.json#/tools` 仍只寫 `{"keep": true}`（複本未更新）【查】；aos-home 的工具有沒有新參數【缺】 | `T/13/ops-fixes-施工結果.md` A1 |
| PROTOCOL（六 STATUS、四段、reply-to、必回終局、卡 10 分鐘發 BLOCKED） | `K/aos/mailbox.json#/rules`：同一組六個字、`StatusBad`、同兩條硬規則；欄位 title／what／outputs／not_done／decide／reply_to／in_reply_to | 直接 | 11-12 調查原話「照 wf PROTOCOL 搬」 | `W/flavors/multi-agent/workflows/inbox/PROTOCOL.md:123-144`；`T/12/wf-to-aos/01…` (a)【查】 |
| 狀態靠位置（頂層／done） | peek／read（刪或 keep） | 部分 | 讀了≠辦了 | `T/12/wf-to-aos/02…` 邊緣 4【查】 |
| 輪詢義務＋UserPromptSubmit hook 範例 | `mail_notify`（每 60 秒、有新信才通知）；畫面開著改 a2a 署名投遞 | 直接 | — | `K/aos/mailbox.json#/check`；`T/13/a2a-施工結果.md`【查】 |
| 五通道（mail／teams／topics／orders／new、`--up`） | `mailbox_send` 只有 `to`、`box`、`daemon` | 無 | — | `K/aos/mailbox.json#/tools`【查】 |
| wake-policy | `mail_notify` 不看 STATUS；可換 handler | 部分 | 要自寫程式 | `K/aos/mailbox.json#/check_hook`【查】 |
| ROSTER | `P/agents.json`（eca_main 保管；寫入寄 public: 信） | 直接（本機） | 只在這台；無團隊／訂閱欄 | 【查】 |
| resources（mkdir 鎖、順序、nice） | `aos-lock`（`--lease-cycles` 租期）、subagent `limits`、`aos-sandbox` | 部分 | 順序與「使用者優先」是規矩；`aos-lock` 是 CLI 零件不是腦的工具 | `K/aos/cli/parts/lock.json`【查】 |
| dispatch、TEMPLATE.handoff | `subagent`／`agents_ctl`／`fork`（agent-fsm）；交接書＝REQUEST 信 | 部分 | eca 無 subagent，用 CLI Agent 工具；領地表無對應 | `K/aos/agents.json`【查】 |
| driving-cli-agents | `aos-agent ctl add/start/stop`、`say/listen/open/watch`、daemon 表 phase/reason | 部分 | 這台機器的啟停歸 eca_main | `P/howto.json#/daemon/who_operates`【查】 |
| team-model | `self_llm` 的 model、llm-team kernel | 部分 | 分級判斷本身是內容 | `K/aos/kernel.json#/templates`【查】 |

### 1F. heartbeat 包

| wf 機制 | aos 對應物 | 程度 | 落差 | 證據 |
|---|---|---|---|---|
| `tick`＋`/wf-tick`（`/loop`） | on_clock hook（stack 內、重啟還在、不進 history）；`clock_register`（每次一輪） | 部分 | 沒有「每天幾點」，handler 自己看牆鐘；錯過只補一次；eca 閒著也每 0.3 秒看時鐘 | `K/aos/clock.json#/choose`；`T/13/ops-agent-six-suggestions.md` 第 6 點【查】 |
| routines、schedule 清單 | 無（內容）；hook 可讀清單 | 無 | heartbeat 自述「本包不是排程器、引擎外借」，hook 可當另一種引擎【推】 | `W/flavors/heartbeat/README.md:5`【查】 |

---

## 2. 導航層（深）

### 2.1 wf 這邊三種導航檔各承擔什麼

| 檔 | 承擔什麼 | 寫法規則 | 證據 |
|---|---|---|---|
| `AGENTS.md`（頂層） | 開場 checklist＋**四條路**（做事→WORKFLOWS、看結構→INDEX、偏好→user.md、各包插入的 bullet）＋鐵律 | 「只指向下一層」；下層檔「不向上連 AGENTS.md」 | `W/template/AGENTS.md`；`W/template/STRUCTURE.md:11-16`【查】 |
| `WORKFLOWS.md`（派發器） | **使用者說法→工作流→入口檔**三欄表；各 flavor 片段貼在 `<!-- wf-insert:WORKFLOWS -->`；另含兩段**規則**：「可以跳流程」四條件、「活狀態記哪裡」判別表（等使用者／同 repo 另一 session／別資料夾 agent） | 觸發欄是使用者口語，可一工作流多列（dev 片段把 refactor 列兩次：「重構」與「搬檔」），可加「分辨」欄（knowledge、teaching、research 片段） | `W/template/WORKFLOWS.md`；`W/flavors/dev/WORKFLOWS.dev.md`；`W/flavors/knowledge/WORKFLOWS.knowledge.md`【查】 |
| `INDEX.md`（結構地圖） | **只描述頂層**：每列「路徑｜一句話＋連結」；目錄內部複雜就放它自己的 README／INDEX | 小資料夾 README 與 INDEX 合一，大了才分 | `W/template/INDEX.md:3`；`W/template/STRUCTURE.md:17`【查】 |
| 各夾 `README.md` | 進資料夾先讀的入口／導引；資料夾型工作流的入口 | 四級成長第 3 級時 README 退回「先讀我」、拆出 `INDEX.md` | `W/template/STRUCTURE.md:50-53`【查】 |
| `workflows/common/README.md` | common 夾的導航表（路徑｜內容｜來源 kernel／包） | 表前 `<!-- wf-nav -->` 讓 lint 豁免 BIGLIST | `W/template/workflows/common/README.md`；`W/template/workflows/common/data-files.md:123`【查】 |
| md 表的連結 | 給人點的捷徑；wf 明說「給人點的留 md」 | 連結表超過十條才考慮、看用途 | `W/template/workflows/common/data-files.md:88`【查】 |

### 2.2 aos 的導航規則（確切）

全部【查】自 `K/docs/01-樹長怎樣與多庫.md`、`K/docs/02-寫入與節點怎麼寫.md`、`K/README.md`、`K/aos/tools/index_view.json`：

1. **index 的天然位置**：資料夾 `DIR` → `DIR/_index.json`（整個檔是表）；JSON 檔 `FILE` → `FILE#/_index`；物件 `FILE#/P` → `FILE#/P/_index`。想了解某節點就看**它上一層**的 index；上一層沒有 index＝夠小，直接讀。
2. **門檻（只給太大的補）**：資料夾裡**超過 15 個東西**才放 `_index.json`（`_index.json` 自己不算，剛好 15 不放）；json 檔**超過 8000 bytes 或頂層內容鍵超過 10 個**才放 `_index`。使用者 11-13「index範圍按照11-12的門檻。」（`T/13/index-build.md`）。出廠樹只有 `aos/`、`aos/cli/`、`aos/tools/` 三份 `_index.json` 與 `aos/packs.json#/_index`。
3. **條目形狀＝物件**：`{"名字": {"description": "…"}}`；資料夾的 `_index.json` 要**列出夾裡每一個東西**（`_description.json`、`README.md`、`docs` 也列；子夾鍵不帶尾斜線）【查：`K/aos/cli/_index.json` 確實列了 `_description.json` 與 `parts`】。字串形條目：`index_view` 只印鍵、句子被丟（`T/13/ops-agent-six-suggestions.md` 第 3 點），`index_check.py` 報 `IndexBad`。
4. **description**：英文一句話（範圍：出廠 `knowledge/aos`）；可塞其他鍵，`index_view` 只讀 `description` 與 `index`（使用者 11-12 晚「想塞啥塞啥，出事了自己負責」）。
5. **`index` 連結**：條目可帶 `"index": "路徑"`，值必須是字串、必須指向另一份 `_index.json` 或檔內 `_index`；檔內 `_index` 本身也可以是這種路徑字串。相對路徑**從裝著那份 index 的容器算**：`_index.json` 從它的資料夾；檔內 `_index` 從裝著它的 JSON 物件（物件當資料夾：名字＝往下一鍵、`..`＝外層物件，根物件的 `..`＝檔所在資料夾）；`#/` 開頭從那個 json 檔的根算；絕對路徑照用。`index_view` **不跟**著往下讀，要再呼叫一次 `{"index": PATH}`。例：`K/aos/_index.json` 的 `cli` 條目＝`{"description": "Use these shell commands…", "index": "cli/_index.json"}`【查】。
6. **`_description`＝節點自己的正文**（不是 index）：資料夾＝同夾 `_description.json`（一個 JSON 字串），物件＝`_description` 鍵；只放外面，不寫進 `_metainfo`（N-69）。
7. **`_metainfo`**：index 也可寫在 `_metainfo.json#/index`（資料夾）或物件的 `_metainfo/index`；`index_view` 先讀 `_metainfo` 那份、再疊獨立 `_index`，同鍵獨立那份贏；壞掉的 `_metainfo` 跳過並在首行註記。出廠樹現有的都放外面、不搬。`K/aos/` 底下沒有任何 `_metainfo*` 檔【查：find】。
8. **主觀 index**：`index_view` 的 `index` 參數可疊一份自己的看法；天然位置那份＝「通用視角（公用視角）」；「agent 自己私有的看法放哪不規定」（`K/README.md`）。
9. **index 是看法不是事實**：可缺可過期；要客觀用 `ls`／`json_ls`。改 index 用 json 工具（`json_set {"path": "d/_index.json#/a.json", "value": {"description": "…"}}`；鍵含 `/` 寫 `~1`）。
10. 名字只用 `[a-z0-9_-]`（檔名加 `.json`）；`.`、`_` 開頭保留（`_index*`、`_description*` 例外）（`K/docs/02`）。

### 2.3 wf 導航元素 ↔ aos 規則逐項

| wf 元素 | aos 對應 | 差在哪（事實） |
|---|---|---|
| AGENTS.md「四條路」 | 頂層 `_index.json` 各條目＋`_description.json` | AGENTS.md 由 CLI 依檔名載入；`_index.json` 要 agent 自己去 `index_view`（system.txt 或 AGENTS.md 得先告訴它）【查】 |
| WORKFLOWS 一列＝一種說法 | 一條目＝一個真實存在的名字 | 同一工作流不能列兩行；觸發說法只能塞進 description（ops-notes 做法）【查】；「分辨」欄無位置 |
| WORKFLOWS 的「可以跳流程」「活狀態記哪裡」 | 無 | index 是描述節點，不放規則；只能放到某個節點的 `_description`【推】 |
| INDEX.md 一列一句 | `_index.json` 一條目一句 | 幾乎同構；但 INDEX.md 寫頂層「每一個目錄」，aos 只在 >15 項才有 index【查】 |
| 小夾 README＝入口＋結構 | `_description.json`＝正文；<=15 項的夾沒有 index，直接 `ls` | aos 沒有「README 先讀我」這個角色名；`_description` 對應 README 的正文部分【推】 |
| `<!-- wf-nav -->`（導航表豁免 BIGLIST） | 無需要（index 本來就是表） | — |
| md 連結可點 | 條目的鍵＋`index` 路徑；`index_view` 印成 `KEY<TAB>description<TAB>index: PATH` | 人點不了；GitHub 上看到的是原始 json【推】 |
| 子層不向上連 | index 只在上一層，天然單向 | 同構【查】 |

### 2.4 實例一：ops-notes（手寫、門檻沒照 15）

【查】`find O -name _index.json`：12 份——頂層、`notes/`、`session_logs/`、`wf/`、`wf/wait_todo/`、`wf/workflows/`、`wf/workflows/common/`、`wf/workflows/model-entry-deploy/`、`wf/workflows/model-entry-replay/`、其下 `cleanhost/`、`fast/`、`nightctl/`。

| 份 | 夾內東西數 | 條目數 | 帶 `index` 連結 | 字串形 |
|---|---|---|---|---|
| `O/_index.json` | 17（含 `.git`） | 16 | 3 | 0 |
| `O/wf/_index.json` | 9 | 9 | 2 | 0 |
| `O/wf/workflows/_index.json` | 17 | 17 | 3 | 0 |
| `O/wf/workflows/common/_index.json` | 12 | 12 | 0 | 0 |
| `O/wf/wait_todo/_index.json` | 6 | 6 | 0 | 0 |
| `O/notes/_index.json` | 7 | 7 | 0 | 0 |
| `O/session_logs/_index.json` | 6 | 6 | 0 | 0 |
| `O/wf/workflows/model-entry-deploy/_index.json` | 29 | 27 | 0 | 0 |
| `O/wf/workflows/model-entry-replay/_index.json` | 19 | 18 | 3 | 0 |

- 各層長相：頂層 `_index.json` 條目如 `"wf": {"description": "工作流機制：派發表、專案地圖…使用者要你動手做事時從這裡找對應工作流。", "index": "wf/_index.json"}`；`.claude`、`secrets`、`ops-artifacts` 條目寫「不建索引」與何時進去。`wf/workflows/_index.json`（`index_view` 實跑，17 項）每條 description 都是「是什麼＋何時讀」，等於把 WORKFLOWS 的觸發說法搬進 description，例「`tick.md` 定期心跳的單次執行…跑 /wf-tick 時讀」【查】。
- 與 aos 規則的差：**不照 15 門檻**（7、6 項的夾也建）；description 用**繁中**、兩句（不是英文一句）；md 導航表（`WORKFLOWS.md`、`INDEX.md`）**並存不刪**，給人看【查】。
- 計畫：`O/notes/aos-migration-plan.md` §5「索引的整體設計」：路由線全建、領域夾建第一層、更深超過 15 項才建；按日期的紀錄不逐檔列；不用 `_metainfo`；子 agent 用 Write 改 index（等使用者拍板）【查】。
- 由 2 個 commit 建（`717f361`、`d8db786`）【查】。

### 2.5 實例二：aos repo（生成、照 15 門檻）

【查】`git ls-files A | grep _index.json`：25 份，例 `proto8/_index.json`、`proto8/docs/NORMS/_index.json`、`proto8/knowledge/aos/{,cli/,tools/}_index.json`、多份 `proto8/thinking/…/_index.json`、`wf/workflows/_index.json`、`wf/tools/_index.json`、`wf/session_logs/2026-10-parts/_index.json`。**repo 根與 `wf/` 沒有**（`ls A/wf` 14 項，未達門檻）。

- **生成而非手寫**：`A/wf/tools/index_gen.py` 依 `index_gen.json`（`more_than: 15`、`scopes`、`skip_dir_names`、`skip_dirs: ["wf/inbox"]`、`usual_dirs`/`usual_files` 通用句）生成；description 取**檔頭第一句**，取不到用 `index_gen_desc.json` 手寫句（約 790 句）；不帶參數＝檢查（不一致印 `IndexStale` 退 1）；`--apply` 寫入（`T/13/index-build.md`）【查】。
- 各層長相：`A/wf/workflows/_index.json` 25 條，description 例「`decisions.md` | decisions — 決策記錄（本專案的落點：proto8/thinking 的決定）」（＝md 標題）；資料夾條目寫「何時走這」，例 `common`「…使用者說『記／查踩坑』…時走這」【查】。`A/proto8/_index.json` 例 `docs`「使用者親口定下的三份條文…做設計前先通讀」【查】。
- md 導航並存：`A/wf/WORKFLOWS.md`、`A/wf/INDEX.md` 仍在，INDEX 已拆成 `A/wf/INDEX/`（`01-repo-layout.md`）、派發表拆出 `A/wf/WORKFLOWS-parts/`【查】。
- 檢查：`index_check.py` 28 份 655 項 `0 problems`（`T/13/index-build.md`）；「掛進規矩」甲（改鐵律 3）／乙（wf-lint 加 INDEX 關）**待使用者裁**【查】。
- `_metainfo`：生成器只用獨立 `_index.json`、不用 `_metainfo.json` 的 index（同上）【查】。

### 2.6 兩實例對照

| 項 | ops-notes | aos repo | aos 規範 |
|---|---|---|---|
| 門檻 | 不照（路由線全建） | 照 >15 | >15 |
| 產生 | 手寫（子 agent） | 生成器＋手寫句 | 不規定 |
| description 語言 | 繁中 | 繁中（檔頭句） | 英文（限出廠樹） |
| description 內容 | 是什麼＋何時讀 | 多為檔頭標題，資料夾寫何時走 | 一句說是什麼 |
| md 導航表 | 保留給人 | 保留並拆分 | — |
| 檢查 | 計畫自寫 | `index_check.py`、`index_gen.py` | 無工具 |

---

## 3. 儲存架構（深）：做事的流程 vs 純知識

### 3.1 分類準則

- **W 流程**：有「何時用」＋`Done when`＋步驟（流程／階段／A 登記 B 執行）——agent 要做事時拿來照做。
- **K 知識**：規則、慣例、契約、參考表、踩坑、偏好；沒有步驟或步驟只是附帶。
- **M 混合**：一檔同時是流程殼＋大塊知識／記錄（標出來）。
- **N 導航／片段**：路由、派發片段、包說明（給人或導入用）。
- **R 範本**：複製改寫用的骨架。
- **S 活狀態／記錄**：live 清單或登記表。
- **P 程式／設定**。

判定依據：逐檔 grep `## Done when`、`**何時用**`、`## 流程`／`### A. 登記`／`## 階段`，再讀開頭【查】；類別本身是本底稿的分類【推】。

### 3.2 template/（kernel）

| 檔案 | 類別 | 理由 | 大小 |
|---|---|---|---|
| `AGENTS.md` | **M**（N＋K） | 路由 bullet＋鐵律四條 | 1665 |
| `CLAUDE.md` | N | 一行轉址 | 275 |
| `WORKFLOWS.md` | **M**（N＋K） | 派發表＋「可以跳流程」規則＋活狀態判別表 | 2191 |
| `INDEX.md` | N | 結構地圖 | 1404 |
| `STRUCTURE.md` | K | 分層、門檻、四級、統一形式、archive、日誌、資料檔慣例；自稱「被動參考」 | 7433 |
| `SESSION-LOG.md` | **M**（S＋K） | open 清單＋寫入時機規則 | 907 |
| `WAIT_USER.md` | **M**（S＋K） | open 清單＋收什麼的規則 | 782 |
| `.claude/commands/wf-lint.md` | **M**（W 薄殼＋K） | 跑法一段＋各 finding 意義 | 1364 |
| `workflows/TEMPLATE.workflow.md` | R | 工作流骨架 | 1159 |
| `workflows/common/README.md` | N | common 導航表 | 982 |
| `workflows/common/data-files.md` | K | `wf-table/1` 契約與工具契約 | 6698 |
| `workflows/common/data-files-fmt.md` | K | `$fmt` 契約 | 6685 |
| `workflows/common/gotchas.md` | **M**（W 殼＋S） | 有何時用／Done when，主體是坑清單 | 983 |
| `workflows/common/reply-style.md` | K | 回覆規則表（always-on） | 3354 |
| `workflows/common/user.md` | **M**（W 殼＋K 鍵值） | Done when＋偏好表 | 1401 |
| `workflows/decisions.md` | **M**（W 殼＋S） | Done when＋決策記錄表 | 1085 |
| `workflows/planning.md` | **M**（W＋S） | 四階段管線＋想法表／roadmap 表 | 1710 |
| `workflows/tidy/README.md` | **M**（W 為主） | 流程五步＋五條原則判準＋盤點指令 | 6914 |
| `workflows/tidy/content-trim.md` | **M**（K 為主） | 留／刪判準、原文認法＋「怎麼做」六步 | 4138 |
| `workflows/tidy/gotchas.md` | K | 整理踩坑 | 4201 |
| `workflows/tidy/manager-brief.md` | R | 管理線簡報範本 | 1824 |

### 3.3 flavors/

**dev**

| 檔案 | 類別 | 理由 | 大小 |
|---|---|---|---|
| `README.md` | N | 包說明、合併步驟 | 5042 |
| `AGENTS.dev.md`／`COMMON.dev.md`／`WORKFLOWS.dev.md` | N | 貼入片段（WORKFLOWS 片段另含 analysis／investigation／patch 分辨規則一段＝K） | 247／224／1848 |
| `workflows/feature-dev/README.md` | W | 何時用、Done when、流程 | 2813 |
| `workflows/testing.md` | **M**（W 殼＋K 驗證表） | 有何時用／Done when，主體是「驗證｜指令｜誰跑」表，沒有流程段 | 3060 |
| `workflows/refactor/README.md` | W | | 1213 |
| `workflows/refactor/moving-things.md` | **M** | 六類斷裂（K）＋偵測程序；Done when 寫在 code block 裡 | 3759 |
| `workflows/investigation.md` | W | | 1587 |
| `workflows/analysis.md` | W | | 2733 |
| `workflows/patch.md` | W | | 3113 |
| `workflows/dev-env.md` | **M**（W 殼＋K 指令表／環境表） | | 2460 |
| `workflows/common/conventions.md` | K | 慣例表（範本形） | 1159 |
| `workflows/common/code-map.md` | K | 領域表＋維護鏈 | 1863 |

**knowledge**

| 檔案 | 類別 | 理由 | 大小 |
|---|---|---|---|
| `README.md`、`COMMON.knowledge.md`、`WORKFLOWS.knowledge.md` | N | | 5457／286／1614 |
| `workflows/write.md`、`digest.md`、`plan-a-thing.md`、`decide.md`、`learn.md`、`organize.md` | W | 都有何時用／Done when／流程 | 2110／1977／2008／2036／2171／2035 |
| `workflows/common/writing.md` | K | 自稱「被動參考：寫散文才取用」，有兩處「何時用」但無 Done when／流程 | 4901 |
| `workflows/common/writing/zh-tw.md` | K | 簡繁對照表 | 1145 |
| `workflows/common/info-map.md` | K | 材料導航表＋維護鏈 | 1849 |

**teaching**

| 檔案 | 類別 | 理由 | 大小 |
|---|---|---|---|
| `README.md`、`WORKFLOWS.teaching.md` | N | | 4318／1377 |
| `workflows/plain-explain.md` | **M**（W＋大量寫法規則） | 7302 B，表列 9 行【推：主體是寫法規範】 | 7302 |
| `workflows/study-site/README.md` | W | | 6417 |
| `…/build-with-agents.md`、`enrich-existing.md`、`publish.md` | W | | 6759／5423／3138 |
| `…/foundations-first.md` | **M** | 「剖面」：有何時套用、Done when，無流程段，主體是課程要求（K） | 6358 |
| `…/quality-gates.md` | K | 交付前品質關卡清單 | 5272 |
| `…/TEMPLATE.build-spec.md`、`TEMPLATE.project-brief.md` | R | | 2417／1821 |

**research**

| 檔案 | 類別 | 理由 | 大小 |
|---|---|---|---|
| `README.md` | **M**（N＋K） | 包說明＋真相層／衍生層、`logs/` 原則 | 5969 |
| `COMMON.research.md`、`INDEX.research.md`、`WORKFLOWS.research.md` | N | | 137／727／932 |
| `workflows/source-intake.md`、`survey.md`、`collide.md` | W | | 3600／2856／2758 |
| `workflows/backlog.md` | **M** | 何時用／Done when，無流程段，主體是候選池規則 | 2564 |
| `workflows/common/index-rules.md` | K | 索引真相層規則 | 1771 |
| `workflows/TEMPLATE.batch.md`、`TEMPLATE.summary.md` | R | | 1616／2017 |

**ops**

| 檔案 | 類別 | 大小 |
|---|---|---|
| `README.md`、`WORKFLOWS.ops.md` | N | 2148／440 |
| `workflows/inventory.md`、`incident.md`、`deploy.md` | W | 1768／2045／2067 |

**heartbeat**

| 檔案 | 類別 | 理由 | 大小 |
|---|---|---|---|
| `README.md` | **M**（N＋K） | 包說明＋引擎分工表＋Windows TZ 踩坑 | 4918 |
| `WORKFLOWS.heartbeat.md` | N | | 564 |
| `workflows/tick.md` | W | | 1901 |
| `workflows/routines.md` | **M**（W＋S） | A 登記／B 執行＋live 時機分區與間隔登記表 | 3702 |
| `workflows/schedule.md` | **M**（W＋S） | A／B＋一次性時刻表 | 2560 |
| `.claude/commands/wf-tick.md` | W 薄殼（適配層） | | 1122 |

**multi-agent**

| 檔案 | 類別 | 理由 | 大小 |
|---|---|---|---|
| `README.md` | **M**（N＋K） | 包說明＋並發假設＋與即時通道分工 | 6970 |
| `AGENTS/INDEX/WORKFLOWS.multi-agent.md` | N | | 233／391／867 |
| `workflows/inbox/README.md` | W | | 6751 |
| `workflows/inbox/PROTOCOL.md` | K | 格式契約 | 7441 |
| `workflows/inbox/wake-policy.md` | K | | 2080 |
| `workflows/inbox/ROSTER.md` | **M**（K 規則＋S 名冊） | | 3444 |
| `workflows/inbox/TEMPLATE.letter.md` | R | | 961 |
| `workflows/resources.md` | **M**（W＋S 資源表） | | 4197 |
| `workflows/dispatch/README.md` | **M**（W＋K 六條＋S 領地表） | | 6739 |
| `workflows/dispatch/driving-cli-agents.md` | **M**（步驟為主，無 Done when） | | 4663 |
| `workflows/dispatch/lessons.md` | K | 派線踩坑 | 2865 |
| `workflows/team-model.md` | **M**（W 殼＋K 分級表與判準） | 有 Done when，無流程段 | 6781 |
| `workflows/team-model/context.md`、`speed.md` | K | | 1201／1755 |
| `workflows/team-model/plans.md` | S | project-owned 活頁 | 825 |
| `workflows/TEMPLATE.handoff.md` | R | | 2553 |
| `tools/*.sh`（7 支）、`hook-settings-snippet.json` | P | | 1138–6893／496 |

### 3.4 統計（由上表數）【查：本底稿計數】

- 純 W（流程）24 檔（含 `wf-tick.md` 薄殼）；純 K 17 檔；**M 混合 27 檔**（template 11、dev 3、teaching 2、research 2、heartbeat 3、multi-agent 6）；N 21 檔；R 8 檔；S 1 檔（plans.md，其餘活狀態都混在 M 裡）；P 8 檔。
- 混合型常見三種：①「W 殼包住一張 S 或 K 表」（gotchas、decisions、user、testing、dev-env、team-model、routines、schedule、resources、ROSTER、dispatch）；②「N 包說明夾 K 原則」（各包 README、AGENTS.md、WORKFLOWS.md）；③「K 判準夾步驟」（content-trim、moving-things、tidy README）。

### 3.5 「新開一個 knowledge 庫」在 aos 裡事實上可行的放法

使用者的想法（協調者轉述）：「agent 想做事時有 workflow 可以參考；如果只是知識，或許可以弄個新的 knowledge（知識庫）」。

**docs/01 的多庫規則（原文）**：「多庫＝多棵資料夾樹。要另一棵就複製一份或另開一個資料夾，把路徑告訴 agent 即可；不登記、沒有掛載設定（使用者 11-05「隨意複製，隨意修改，隨意給agent指定、隨意拆卸增添」）。」（`K/docs/01` 末段）【查】

| 放法 | 誰能寫 | agent 怎麼得知路徑 | 進 git 嗎 | 發給非 aos 專案時 | 證據 |
|---|---|---|---|---|---|
| ① `K/<subject>/`（跟 `aos/` 並排） | 定義的 system.txt 寫「read it, do not write it」；`K/README.md`「人用 `aos-json` 或編輯器改」；且 `K` 是 `proto8/knowledge` 的複本，正本在 aos repo | system.txt 已指 `K`；`K` 根目前沒有 `_index.json`（不到 15 項），要靠 `_description.json` 或 system.txt 提到新 subject | `K` 本身不是 git repo【查：`git rev-parse` 失敗】；正本 `A/proto8/knowledge` 在 aos repo 的 git | 帶不走（在 aos-home） | `H/agents/ops-agent/system.txt`；`K/README.md` |
| ② `P/`（ws/public） | eca_main 保管，各 agent 寄「public:」信 | `P/_index.json`；agents.json | `H/ws` 不是 git repo【查】 | 帶不走；且規則只收「這台機器的實況」，不收專案筆記 | `P/howto.json#/sharing` |
| ③ 放在 workflows repo 裡（例 `W/knowledge/` 或 `W/template/knowledge/`，隨 wf-init 複製） | 有權改 repo 的人／agent | 由 `AGENTS.md`（CLI 自動載入）連過去；或在上層 `_index.json` 加條目／`index` 路徑（相對或絕對都可） | 是 | 跟著檔案走；非 aos 工具也讀得到 json 檔（只是沒有 index_view）【推】 | `K/docs/01`「絕對路徑照用」 |
| ④ 每個下游專案自己的 `wf/knowledge/`（或 `notes/`） | 該專案 agent | 該專案 AGENTS.md／`_index.json` | 跟該專案 | 是各專案自己的 | 實例：`/mnt/c/code/<user>/model_entry/wf/notes/_description.json`、`_index.json`（md 筆記＋aos index）【查】 |
| ⑤ 獨立 repo（另一棵樹），路徑告訴 agent | repo 擁有者 | system.txt（eca_main 改定義）、AGENTS.md、`P/agents.json` 的條目 | 是 | 要另外 clone | 多庫規則 |

相關事實：
- 13 日寫手結論「不把 wf 規矩寫進 system.txt 或共用知識庫」（`T/13/main-session-in-aos.md`）——限制了放法 ①②【查】（非使用者裁定）。
- 「內容語言英文」只管出廠 `knowledge/aos`；外部語料收進來的庫，節點名英文、內文照原文（`K/docs/02` 末段）【查】。
- 知識庫的組織原則本來借自 wf：`K/README.md`「照 wf/STRUCTURE 分層原則：上層只放簡介與目錄、不重講下層細節」【查】。
- 子 agent 只能讀不能用 aos 工具寫，寫要用 CLI Write（`P/howto.json#/daemon/claude_subagent_tools`）【查】。
- 拆成「流程 vs 知識」兩棵後，混合型（3.4 的 27 檔）要先切開【推】；wf 的 STRUCTURE 原則「durable 知識歸到它所屬的那一層」與「知識另開一庫」方向不同（前者按工作流歸屬、後者按性質歸屬）【查：`W/template/STRUCTURE.md:18`；比較是推論】。

---

## 4. 資料儲存（深）

### 4(a) aos 知識庫的 json 節點實際長什麼樣

規範（`K/docs/02`）【查】：一段文字＝一個 JSON 字串（Markdown 也是字串，`\n` 換行）；幾段相關的併成物件檔；大了開資料夾；建議一段約 1 KB、一個檔約 8 KB（推薦）；穩定名字用物件不用陣列；拆檔留 `{"$ref": "新檔.json"}`（`aos-json ref --move` 一步做完）；名字 `[a-z0-9_-]`。

**樣本 1：整個檔就是一段 markdown 字串**——`K/aos/rules.json`（2324 B，一個字串 2297 字元）：

```json
"# Boundaries\n\nWhat you must not do, and why. Read this before doing anything that changes the system.\n\nNever:\n\n1. Edit a definition by hand. …"
```

**樣本 2：物件檔，`_description`＋幾段字串＋`$ref` 拆出**——`K/aos/me.json`（6437 B）：

```json
{
 "_description": "# Who am I\n\nFinding your own name, what is in your stack, …",
 "stack": "# What is in your stack\n\nYour stack is `$AOS_STACK`, …",
 "self_tools": {"$ref": "me/self_tools.json"},
 "self_llm": {"$ref": "me/self_llm.json"},
 …
 "self_state": "# Looking at yourself: self_state\n\n…",
 "self_ctl": "# Stopping yourself: self_ctl\n\n…"
}
```
各鍵大小：`_description` 2677、`stack` 1156、`self_state` 1165、`self_ctl` 1067 字元【查】。被拆出的 `K/aos/me/self_tools.json` 本身又是物件（`_description`、`add`、`rules` 三鍵）。`K/aos/errors.json`（3764 B）同型：`_description`、`codes`、`exits` 字串＋`common: {"$ref": "errors/common.json"}`【查】。

**樣本 3：帶檔內 `_index` 的物件**——`K/aos/packs.json`（7968 B，頂層 18 鍵 > 10，所以有 `_index`）：

```json
{
 "_description": "Your tools come in packs. …",
 "_index": {"about": {"description": "How packs work and how to turn one off."},
            "look": {"description": "Pack look: read, ls, view, stat, grep, glob; …"}, …},
 "about": "# Tool packs\n\n…",
 "look": "Pack look: Read-only file tools: …",
 …
}
```

**樣本 4：資料夾 index**——`K/aos/cli/_index.json`：`{"flags.json": {"description": "…"}, …, "parts": {"description": "Low-level programs …"}, "_description.json": {"description": "Commands for humans …"}}`（23 條，含 `_description.json` 自己的條目）【查】。

觀察【查】：出廠節點的值幾乎都是 **markdown 字串**（標題、條列、code fence 都在字串裡），不是結構化欄位；表格也以 md 表格寫在字串裡（例 `K/aos/world.json`、`K/aos/definition.json#/overlay`）。

### 4(b) `wf-table/1` 與 aos json 節點的異同；tabledb 子指令對照

**形狀異同**【查：`W/template/workflows/common/data-files.md`、`data-files-fmt.md`；`K/docs/01`、`02`】

| 面向 | `wf-table/1` | aos json 節點 |
|---|---|---|
| 頂層 | `{"contract","source","extracted","columns","link_columns","rows":[…]}` | 任意物件或字串；`_description`、`_index` 保留鍵 |
| 記錄 | `rows` **陣列**，0-based index | 建議**物件**、穩定名字（「不用陣列」） |
| 欄位契約 | `columns` 定順序、缺欄＝空字串 | 無 |
| 連結 | `link_columns`、`_path`/`_link` 欄名、`[..](..)`；相對資料檔目錄 | 無「連結欄」概念；跨檔取值用 `$ref`（相對所在檔） |
| 路徑代號 | `{"$fmt": "${gitRoot}/x.md#錨"}` 只拼字串、讀時展開 | `$ref`（取回另一檔的值，可 `#/` 從根、`..` 跨出、`$at`）、`$env`；jsonx 跟／解析 |
| 指示詞外形 | 單鍵、`$` 開頭、值字串 | 同（`data-files-fmt.md` 一致性表） |
| 來源 md | md 留原路徑、只放目的／欄位說明／統計，不留表副本 | 無 md 對應物；`_description` 就是正文 |
| csv | 支援（扁平表） | 無 |
| 大小觸發 | 條列 >1 KB 才抽 | 一段 ~1 KB、一檔 ~8 KB 建議；`json_get` >8000 B 回 `[too big]` |

**tabledb.py 子指令 ↔ json_*/jsonx_***（tabledb 指令表出自 `data-files.md:125-139`；json 工具出自 `K/aos/tools/*.json`）

| tabledb | aos 工具 | 狀況 |
|---|---|---|
| `tabledb.py FILE`（meta、count、columns） | `json_ls FILE`、`json_len FILE#/rows`、`json_get FILE#/columns` | 拼得出，要多次呼叫（或 `json_multi_get`）【查】 |
| `get I` | `json_get FILE#/rows/I` | 直接 |
| `find k=v…` | `json_search {path, key, value}`（精確同型值；回 pointer 清單） | 部分：多條件 AND 要自己組【推】 |
| `grep RE` | `json_search` 加 `contains: true`（子字串，**不支援正規式**） | 部分 |
| `--slice A B` | `json_ls` 的 `offset`／`limit` | 部分：列的是鍵不是值【推】 |
| `columns` | `json_get FILE#/columns` | 直接 |
| `add k=v…` | `json_set FILE#/rows/-`（`/-` 附加）或 `json_add` | 直接 |
| `update I k=v` | `json_set FILE#/rows/I/k`、`json_multi_set` | 直接 |
| `delete I` | `json_del FILE#/rows/I` | 直接 |
| `links FILE`、`check FILE`、`open FILE I`、`resolve FILE I` | 無 | **無**（連結查驗） |
| `fmt FILE`（展開 `$fmt`） | 無（jsonx 只解析 `$ref`/`$env`，不認 `$fmt`） | 無 |
| Python API `load/Table` | 無（工具是 JSON 進 stdout 出） | 無 |
| csv 任何操作 | 無 | 無 |
| 列數對帳（md 端「N 列」 vs 檔） | `json_len` 給數字；沒有對帳 | 部分 |
| `find_big_lists`、`wf-lint` 掃資料檔 | 無 | 無 |

另：子 agent 只有 json_get／ls／search／len／multi_get，沒有寫入類【查】；`json_get` 讀到 `$ref` 不跟（`PointerMissing`），跟要 jsonx（範本不掛）【查】。

### 4(c) 依「轉成 json 的難易」分型，附樣本與會失去什麼

型別判定與樣本是本底稿的整理；樣本為示意，不是任何現存檔【推】。

**型 1：同質記錄表**——decisions 記錄表、planning 想法／roadmap 表、gotchas 條目、`W/wf/workflows/investigation/README.md` 的筆記索引、code-map 領域表、info-map、testing 驗證表、dev-env 指令表、routines 間隔登記表、schedule 時刻表、ROSTER、dispatch 領地表、resources 資源表。

```json
{"_description": "Decisions: what was decided and the premise. New first.",
 "2026-09-02-non-invasive": {"date": "2026-09-02",
   "decision": "本 repo 自己用非侵入式導入…",
   "source": "使用者原文…", "premise": "`wf/` 納入版控…"}}
```
（或保留 `wf-table/1` 的 `rows` 陣列形）。難度低：本來就是一列一筆【推】。

**型 2：鍵值設定**——`common/user.md` 偏好表、heartbeat 時區、team-model 分級表。

```json
{"_description": "This user's preferences; always-on rules stay in AGENTS.md.",
 "language": "回覆與文件繁體中文；shell／python 註解可中可英",
 "branch": "main 為主線；…commit 由使用者決定",
 "ask_first": "刪檔、改 template/flavors 的既有契約、安裝依賴",
 "timezone": "Asia/Taipei"}
```
難度低【推】。

**型 3：流程散文**——各工作流入口的何時用／何時不用／Done when／流程／交接。

```json
{"_description": "# tidy — 文件整理\n\n把文件層收乾淨：…",
 "when": "「幫我整理 X」；一個資料夾幾十個檔扁平混放；…",
 "when_not": "改程式碼結構 → refactor；…",
 "done_when": "- 目標資料夾根層只剩入口 README…\n- …",
 "steps": "1. **盤點（調度者）**：\n   ```bash\n   find . …\n   ```\n2. …",
 "handoff": "- 完成後 → …"}
```
難度中：段落切得開，但每段仍是 markdown 字串，內含 code fence、相對連結【推】。「長散文進 json 沒有建議形狀」（第 4(d)）。

**型 4：給人導航的頁**——INDEX.md、各 README 路由表、WORKFLOWS 派發表、common/README、各包 README。

```json
// <dir>/_index.json
{"workflows": {"description": "各工作流本體…從派發表選定工作流後到這裡讀它的入口。", "index": "workflows/_index.json"},
 "STRUCTURE.md": {"description": "結構整理參考（被動）…"}}
```
對 agent 有現成對應（第 2 節）；對人是退化【推】。

**轉換會失去什麼（事實＋標記）**

| 失去的東西 | 影響哪型 | 事實依據 |
|---|---|---|
| md 連結可點 | 1、3、4 | wf 明定「給人點的留 md」（`data-files.md:88`）【查】；json 字串裡的 `[x](y.md)` 在編輯器／GitHub 不可點【推】 |
| git diff 逐行可讀 | 3 最嚴重 | json 字串值是一行，多行 md 塞進去後改一個字整段一行 diff【推】；wf 的 content-trim 原文檢查、`git log -S` 以行為單位（`content-trim.md`「怎麼做」3、5）【查】 |
| wf-lint 連結與錨點檢查 | 全部 | `wf-lint` 只掃 `*.md` 的連結、`check_anchors.py` 只看 md heading；json 只檢查帶 `"contract": "wf-table/` 的（`wf-lint-checks.sh` lint_dir）【查】；aos 無對應 |
| GitHub 直接渲染 | 3、4 | GitHub 會把 `README.md` 等 md 渲染、json 顯示原文【推：常識，未在本環境查證】 |
| CLI 依檔名自動載入 | 入口檔 | 見 4(e) |
| tabledb 連結查驗、`$fmt` | 1 | 4(b) 表【查】 |
| 人用編輯器讀 | 3 | 「人看不懂 json：散文的跳脫字元」（`T/12/wf-to-aos/02…` 邊緣 3）【查】 |
| 非 aos 工具的讀法 | 全部 | wf 的使用者包含任何 AI 工具（`W/README.md:79-88`）；它們讀 json 要整檔讀，沒有 index_view／json_get【推】 |

### 4(d) 既有研究停在哪；現有輔助人讀 json 的工具

**「長散文進 json 的形狀」**：`T/12/wf-to-aos/01…` (b)「長散文進 json：沒有建議形狀（例如一節一物件：標題、內文、原話、出處），沒約定就各寫各的。」之後 12、13 日的檔沒找到定案【查：grep `長散文` 只命中 12/wf-to-aos 三檔】。aos 自己的出廠樹做法是「一節＝一個 markdown 字串鍵」（4(a) 樣本 2）【查】。

**「人怎麼讀 json」**：使用者 11-12「有需要的話再做一些輔助工具和程式幫助人看json就好」（D1）；`T/12/wf-to-aos/01…` (b) 列「一支把 json／`_index` 樹攤成人讀頁（md 或 HTML）的轉印器」為「差一點補小東西」；`T/12/wf-to-aos/02…`「之後自然會長的：人讀 json：`index_view`、`json_ls --depth`、`json_get`、`view`、`aos-json get/ls/search`」。沒找到轉印器施工紀錄【缺】。

**現有工具與頁面（存在與位置）**

| 工具／頁 | 位置 | 做什麼 | 狀態 |
|---|---|---|---|
| `index_view` | aos 工具（`K/aos/tools/index_view.json`；`A/proto8/lib/base/index_view`） | 一層 `KEY<TAB>description<TAB>index` | 存在【查】 |
| `view` | aos 工具（look 包，eca 沒有） | JSON 一層一層、md 先給 outline | 存在【查】 |
| `json_get`／`json_ls`（`long`） | aos 工具 | 一個值／一層鍵 | 存在【查】 |
| `aos-json get --str` | CLI 零件 | `K/README.md` 範例 `aos-json get --str …`＝把字串印成純文字 | 文件有寫【查】；11-12 筆記說「長字串的 `\n` 不展開」，與 `--str` 是否矛盾沒驗【缺】（不能跑 aos 指令） |
| `decide_page` | `A/wf/tools/decide_page/`（`decide_page.py`、`render.py`、`reply.py`、`web/`） | 「把一批題目資料做成離線互動頁，點選、補充後複製一行回覆，再讀回原資料」 | 存在，屬 aos repo 的 wf 工具，不是 aos 出廠工具【查】 |
| `progress_board` | `A/wf/tools/progress_board/`（`dash.py`、`collect.py`、`answers.py`…） | 「把各線回報、交棒、commit 與機器負載放在同一頁，細節點開才看」 | 存在，同上【查】 |
| 待裁頁成品 | `T/13/aos-wu-1113-*-待你裁.html`、`T/13/aos-home-手冊.html`、`T/13/kernel-framework-架構圖.html` | 給人看的 HTML | 存在【查：ls】 |
| `memory_export`（把樹印成 md） | 11-10 圖紙曾列 `lib/agent/memory_export` | `ls A/proto8/lib/agent` 沒有 memory／export 相關項——已不在【查】 |

### 4(e) 「非 md 不可」的檔（被 CLI 或平台依檔名載入）

| 檔 | 誰依檔名載入 | 證據 |
|---|---|---|
| `AGENTS.md` | Codex CLI 原生讀；其他工具「讀 AGENTS.md；不支援就 --redirect」 | `W/README.md:83-88`；`T/12/ops-notes-to-aos.md`「Codex 會讀裡面的 AGENTS.md」【查】 |
| `CLAUDE.md` | Claude Code | `W/README.md:86`；`T/13/main-session-in-aos.md`【查】 |
| `GEMINI.md`、`.github/copilot-instructions.md` | Gemini CLI、Copilot（wf 用 `--redirect` 產） | `W/IMPORT.md:11`【查：wf 文件所述；工具行為本身未驗】 |
| `.claude/commands/*.md` | Claude Code slash 指令（只讀專案根） | `W/docs/non-invasive-import.md:13`；ops-notes 實測載入【查】 |
| `.claude/skills/<name>/SKILL.md` | Claude Code skill 自動發現（只認專案根那層） | `W/IMPORT.md:20`；`W/docs/non-invasive-import.md:31`【查】 |
| `.agents/skills/`（codex 身） | Codex | `T/13/main-session-in-aos.md` 轉引【查：轉引；原 `eca-task-subagent` 沒讀】 |
| `README.md` | GitHub 在資料夾頁渲染 | 【推：平台常識】 |
| `CHANGELOG.md`、`LICENSE` | 慣例，非載入 | 【推】 |
| （非 md 但同類）`.claude/settings.json` | Claude Code 設定與 hook；aos 起的 claude 也讀 | `T/13/ops-agent-six-suggestions.md`【查】 |

另：aos 自己依檔名讀的是 `_index.json`、`_description.json`、`_metainfo.json`、定義的 `interfaces.json` 等（`K/docs/01`、`K/aos/definition.json`）——都是 json【查】。

---

## 5. aos 有、wf 沒有，轉入後可以順便用上的能力

| 能力 | 給 wf 帶來什麼 | 出處 |
|---|---|---|
| 新信自動提醒（`mail_notify`；畫面開著走 a2a） | 免輪詢義務【查】 | `K/aos/mailbox.json#/check`；`T/13/a2a-施工結果.md` |
| STATUS 擋錯（`StatusBad`） | 手寫信也被驗【查】 | `K/aos/mailbox.json#/rules` |
| 穩定 agent 名＋全機通訊錄 | 取代 ROSTER 地址【查】 | `P/agents.json` |
| `index_view` 一層一句＋主觀 index 疊加 | agent 不讀整份路由表【查】 | `K/aos/tools/index_view.json` |
| 統一路徑＋`json_*`＋`[too big]` | 「不整份讀進 context」不需 tabledb【查】 | `K/aos/tools/json_get.json` |
| 不靠 session 的定時器（on_clock） | 補 heartbeat「session 關了就停」【查】 | `K/aos/clock.json#/quiet_timer`；`W/flavors/heartbeat/README.md:49` |
| 事件 hook（9 種） | before_queue 注入、before_tool 擋（限 aos 工具／agent-fsm）【查】 | `K/aos/me/self_hook.json#/events` |
| `goal`（人可對 eca 下） | 當天主目標【查】 | `K/aos/cli/goal.json` |
| `do_task`、`self_history summarize` | context 管理（agent-fsm）【查】 | `K/aos/me/do_task.json` |
| daemon 表 phase／reason | 監看訊號機器可讀【推】 | `K/aos/status.json` |
| `aos-lock` 租期 | 鎖會過期【查】 | `K/aos/cli/parts/lock.json` |
| `limits`、`aos-sandbox` | 資源限制【推】 | `K/aos/agents/subagent.json#/add` |
| `tools_def`＋`self_tools` | 腳本包成工具（逾時限制見第 7 節）【查】 | `K/aos/tools_def.json` |
| `aos-feedback` | 工具難用回饋【查】 | `K/aos/cli/feedback.json` |
| 信留底到工作區（11-13 新） | 往來紀錄可進 git（留底行不含絕對路徑）【查】 | `T/13/ops-fixes-施工結果.md` A1 |

---

## 6. 無對應、應留為內容的部分

- 所有 W 型工作流本體、K 型規則／契約／踩坑／偏好、S 型清單（第 3 節逐檔）——aos 沒有任何機制對應「流程知識本身」【查】。
- 載體選項：(a) 保持 md＋補 `_index.json`（ops-notes、model_entry 現況）；(b) aos 式 json 節點（第 4 節）；(c) `K` 下開 subject；(d) 專案工作區 json；(e) 定義 `system.txt`；(f) `self_system`；(g) skill；(h) aos 工具。各自的寫入權、git、可讀性見第 3.5 節表與第 4(c) 失去清單；system.txt／self_system 的限制：定義多隻共用、只有使用者／eca_main 能改、改一次 cache 失效一次、codex 要新對話、self_system 不進 git 且 agent 可整份換掉（`K/aos/me/self_system.json`；`T/12/wf-to-aos/02…` 邊緣 2）【查】；aos 工具的限制：逾時 10 秒／60 秒、擋不住改用 Bash（`O/notes/aos-migration-mapping.md` §6）【查】。

---

## 7. 硬限制與風險（事實）

1. **wf 的使用者不只 aos 內的 agent**：「可套用到任何種類的專案」，適配 Codex／Claude Code／Gemini／其他（`W/README.md:5,79-88`）；aos 依賴 `AOS_HOME`、daemon、llm kernel（`K/aos/world.json`）【查】。
2. **子 agent 只有 9 支唯讀 aos 工具**；寫 json 要 CLI Write（`P/howto.json#/daemon/claude_subagent_tools`）【查】。wf 的 tidy 大量派子 agent（`W/template/workflows/tidy/README.md:148`）【查】。
3. **eca 沒有 look／change／delete／shell／subagent／goal／todo**；也沒有 subagent／agents_ctl／fork（`K/aos/packs.json#/about`、`K/aos/agents.json`）【查】。
4. **eca 的 aos hook 看不到 CLI 工具**；CLI 自己的 hook 可用（claude 身），codex 無對應（`T/13/ops-agent-six-suggestions.md`）【查】。
5. **codex 沙箱**：workspace-write，寫不到工作區外、看不到外面行程；`.git` 預設唯讀要加 `writable_roots`（`P/howto.json#/codex`）；codex 讀 `AGENTS.md`、`.agents/skills/`，system.txt 只在新對話生效【查】。
6. **AOS_CLOCK**：`P/howto.json#/daemon/clock` 說沒有；本子 agent 環境有 `AOS_CLOCK=/home/<user>/aos-home/.stack//clock`，`peek_clock` 回 `{"cycle": 15340, "interval_ms": 1000}`【查】；13 日查證「樹有，是人開的畫面沒拿到」並已修（B1）。人開畫面修好後是否生效【缺】。
7. **可讀性**：見 4(c)。使用者 11-12「.json比markdown好…」與 ops-notes 10-27「條列維持 markdown」（轉述，原決定檔沒讀）適用範圍不同（第 9 節 C13）。
8. **git diff**：json 字串整段一行【推】；wf 的原文檢查以行為單位【查】。
9. **CI**：Actions 只跑 `bash tools/wf-lint.sh --self`，runner 上沒有 aos【查】。
10. **知識庫與 public 不在 git**（`H`、`H/ws` 都不是 git repo）；`K` 是複本要重抄，13 日的修正不一定到了（`K/aos/mailbox.json` 仍舊說法）【查】。
11. **定義與 daemon 操作歸 eca_main**；改定義影響所有共用者（repo-aos 與 me-agent 共用 `ws/defs/agent`）（`P/howto.json#/daemon/who_operates`；`T/13/main-session-in-aos.md`）【查】。
12. **工具形限制**：逾時 10 秒／aos-mcp 60 秒（`K/aos/tools_def.json#/tool_spec`、`K/aos/cli/mcp.json#/calls`）【查】。
13. **index 會說謊**：多一格不存在的也照印；字串形條目句子被丟（`T/12/wf-to-aos/02…` 邊緣 5；`T/13/ops-agent-six-suggestions.md`）【查】。
14. **活樹誤操作**：Bash 帶活樹 `AOS_*`；不要按名字 pkill（`P/howto.json#/daemon/aos_env_in_bash`、`#/known_issues/pkill_rule`）【查】。
15. **本 repo 契約要先問**：`user.md`「一定先問：改 template/flavors 的既有契約（版本戳、資料檔格式）」（`W/wf/workflows/common/user.md`）【查】。
16. **已導入的下游**：ops-notes（`v0.6+unreleased 368468a`）、model_entry（`v0.6 + 未發布 368468a`）、gpt-soap（`v0.6+unreleased 368468a`，knowledge＋heartbeat，codex）、aos repo（`v0.5`，大量客製：`decide_page`、`progress_board`、`index_gen`、`codemap_gen`、`compact_reload.sh`）（各 `AGENTS.md` 末行；`A/wf/tools/_index.json`）【查】。ops-notes 有等拍板的轉向規劃（`O/notes/aos-migration-plan.md`）【查】。

---

## 8. 使用者已裁決的事（附原檔出處與原話）

| # | 日期 | 裁了什麼 | 原話（逐字） | 出處 |
|---|---|---|---|---|
| U1 | 11-12 下午 | 方向：不是替代，是改成更適合 agent；先玩 | 「然後...我接下來想做的事情，是開始用aos體系替代掉wf/。或者說不是替代，而是將其變成更適合agent的情況，途中會發現wf/的一些東西已經不再有用，就可以拿掉。當然，我要先玩一玩啦。」 | `T/12/wf-to-aos.md` |
| U2 | 11-12 晚 | D1 內容走 json；D2 檢查工具先放；D3 always-on 之後玩；D4 等使用者＝寄信給人；D5 主 session 經 aos MCP／skill | 「.json比markdown好，有需要的話再做一些輔助工具和程式幫助人看json就好。2.先放着，這是後面一邊玩一邊自然會要做的。3.後續玩一玩，自然會想到怎麽做，反正有hook。4.把人類這個linux user作爲agent，寄信過去就是了。5.對，這個明天開始。」 | `T/12/wf-to-aos.md`「決定」 |
| U3 | 11-12 晚 | 沒有硬性缺的 | 「就是說，沒有硬性缺的了，現在wf/的東西，我們拼拼湊湊就能有了。」「以後一定會比wf/好用，放心。寄信這個以後自然就能夠搞定，反正必須的都有了。」 | `T/12/wf-to-aos.md` |
| U4 | 11-12 | index 與 description 合一、天然位置、只給太大的補 | 「description和index是可以合起來的，或者說，本來就該合起來，統一叫_index.json/_index…」「如果有些東西太大，那就補index.json/_index。如果夠小，那其實也不用做看法了，直接讀就是了。」 | `K/README.md`、`K/docs/01` |
| U5 | 11-12 晚 | 條目可放 `index` 路徑；物件內可塞別的鍵 | 「除了description之外，還可以放index，值必須是字串，必須是路徑，指向另一個_index或_index.json。」「_index的obj內要不要再多塞東西...可以，想塞啥塞啥，出事了自己負責。」 | `K/docs/01` |
| U6 | 11-11 | 知識庫大小只是推薦 | 「這個"不超過2kb"我沒說過，拿掉。不過也可以用，我的建議是改成一個檔案不超過8kb，一段不超過1kb。」「那個知識庫上限，只是推薦，不要訂死。」 | `K/docs/02` |
| U7 | 11-11 | eca 不給 goal／todo | 「eca基本都有goal，所以goal不用給eca。todo也不用。」 | 引自 `T/13/main-session-in-aos.md`（原 P-43 沒讀【缺】） |
| U8 | 11-13 | tcf-C42：推薦 JSON，不強制 | 「推薦都用json，我們做的東西也盡量以json為主。這是推薦，不遵守也沒差」；第二輪 `rd-C42:B`＝推薦 JSON、別的格式不禁止 | `T/13/裁定落地-1113.md` |
| U9 | 11-13 | eca_main 派的普通工作算授權、不可逆仍要本人；家機主 session 也進樹 | 「1.算。2.可以。」「2.對。」 | `T/13/裁定落地-1113.md`（ms-1、ms-2） |
| U10 | 11-13 | index 範圍照 11-12 門檻 | 「index範圍按照11-12的門檻。」 | `T/13/index-build.md` |
| U11 | 11-13 | 六點三題全照建議：定義可自帶 CLI 設定；索引檢查讓 ops-agent 自己寫；信收寄都能留一行到工作區 | 「都按照建議」 | `T/13/ops-agent-six-suggestions.md`、`T/13/ops-fixes-施工結果.md` |
| U12 | 11-13 | eca 的 Bash 交給 eca 機制，現在全面開放 | 「我覺得沒差，eca的bash工具，就是讓eca自己的機制擋。頂多加個hook，在eca跳yes/no的時候幫忙接住，寄信給特定目標處理。這個之後再做，這有點麻煩。我覺得現在就是勇敢一點，就全面開放。後面再來做這塊。」 | 同上（經 ops-agent 轉述） |
| U13 | 11-13 | a2a 照建議 | 「1.a2a這個按照建議。馬上送，eca他會自己處理。say/chat被當成不是使用者打的，我覺得可以，真的有要的話，就自己open進去說。」 | `T/13/a2a-施工結果.md` |
| U14 | 09-30（aos repo 的 wf） | Claude Code 自動記憶不用，wf/ 是結構化記憶 | 轉述句：「2026-09-30 他說 Claude Code 的自動記憶機制是垃圾，`wf/` 才是結構化的記憶與 skills。」 | `A/wf/workflows/common/user/01-說話授權與記憶.md:17` |
| U15 | 本 repo | wf-lint 可選、預設不跑 | commit `368468a` 訊息（非逐字原話） | `git log` |
| U16 | 本 repo | 改 template/flavors 既有契約要先問 | `user.md`「一定先問」欄 | `W/wf/workflows/common/user.md` |
| U17 | 本輪（協調者轉述） | 四個面向：lint 次要；導航層、儲存架構（workflow vs knowledge，知識或可另開 knowledge 庫）、資料儲存（「甚至全都可以用 .json，只留一些 .md 給使用者看」）寫深 | 轉述，非原檔 | 協調者訊息 |

**寫手依原則定案、非使用者裁（可翻案）**——`T/13/main-session-in-aos.md`：規矩只一份留 `CLAUDE.md→AGENTS.md→wf/`，「不把 wf 規矩寫進 system.txt 或共用知識庫」；compact 後重讀沿用 `.claude/settings.json`；skill 放 repo `.claude/skills/`；SESSION-LOG／WAIT_USER 照舊；兩套信（樹內 mailbox、樹外 `wf/inbox`）都留「直到『wf 往 aos 走』那條線動到 inbox 為止」。`T/13/ops-agent-six-suggestions.md` 代定：index 條目物件形、字串形不當條目。

**尚未裁**：`T/13/index-build.md` 掛進規矩甲／乙；`O/notes/aos-migration-plan.md` 七題（ops-notes 範圍）。

---

## 9. 既有研究之間互相矛盾或過時的地方

| # | 較舊說法 | 較新說法 | 判斷 | 出處 |
|---|---|---|---|---|
| C1 | 「這棵樹的 agent 沒有 AOS_CLOCK」；ops-notes「環境變數實測一致」 | 「樹有，是人開的畫面沒拿到」，已修 B1；本調查 `peek_clock` 有值 | howto 與 ops-notes 過時 | `P/howto.json#/daemon/clock`、`O/notes/aos-migration-mapping.md` vs `T/13/ops-agent-six-suggestions.md` |
| C2 | 11-12：always-on 規矩放 system.txt「現在就能搬」 | 13：不把 wf 規矩寫進 system.txt | 12 日沒回註 | `T/12/wf-to-aos/01…` (a) vs `T/13/main-session-in-aos.md` |
| C3 | 11-12：主 session 不在 daemon 表上 | 13：主 session 就是 `repo-aos` | 前提沒了 | `T/12/wf-to-aos/02…` vs `T/13/main-session-in-aos.md` |
| C4 | 11-12：等使用者寄信給人「現在就能搬」 | 13：WAIT_USER 照舊 | 方向在、施工暫緩 | 同上 |
| C5 | 11-12：SESSION-LOG 改 repo 裡的 json | 13：照舊 md | 未採用 | 同上 |
| C6 | 11-12：「同質列表：json 工具增刪改查夠用」 | 連結查驗、csv、$fmt 沒有 aos 版（4(b)） | 12 日只講 CRUD | `T/12/wf-to-aos/01…` (a) |
| C7 | 11-12：before_tool 能擋 push；ops-notes：「aos 做不到」「待查 PreToolUse」 | 13：CLI hook 生效；使用者全面開放 | ops-notes 待查已有答案 | `O/notes/aos-migration-mapping.md` §11 vs `T/13/ops-agent-six-suggestions.md` |
| C8 | 知識庫／ops-notes：留底只進 stack | 13：可留到工作區檔 | `K` 複本未更新 | `K/aos/mailbox.json#/tools` vs `T/13/ops-fixes-施工結果.md` A1 |
| C9 | ops-notes：index_view「照樣顯示字串形條目」 | 13：只印鍵、句子丟掉 | ops-notes 不準 | `O/notes/aos-migration-plan.md` §8 |
| C10 | `K/aos/body.json`：eca on_clock 在 each turn 檢查 | 13：每 0.3 秒，與信無關 | 知識庫待改 | `T/13/ops-agent-six-suggestions.md` |
| C11 | ops-notes：自寫索引檢查；建議出廠工具 | aos repo 已有 `index_check.py`；U11 裁 ops-agent 自寫 | 重疊 | `T/13/index-build.md` |
| C12 | `K/docs/02`：description 英文一句、index 只在 >15 項 | ops-notes 繁中兩句、不照門檻；aos repo 繁中但照門檻 | 範圍不同（docs/02 管出廠樹），實例各自偏離 | 第 2.6 節 |
| C13 | ops-notes：10-27「條列維持 markdown」（轉述） | 11-12「.json比markdown好」、11-13「推薦都用json…不遵守也沒差」；本輪使用者「甚至全都可以用 .json，只留一些 .md 給使用者看」（轉述） | 範圍不同；對 workflows repo 本身的最新傾向是後者（轉述） | `O/notes/aos-migration-mapping.md` §8 vs U2、U8、U17 |
| C14 | `W/wf/AGENTS.md` 鐵律 2「改完 md 一定跑 wf-lint」 | `368468a`、`W/README.md:59,69`、`W/IMPORT.md:3`：可選 | wf/ 落後 template | — |
| C15 | `W/wf/workflows/common/code-map.md:11`「導入：無自動測試」 | `W/tools/test_wf_init.py` 存在 | code-map 過時 | `ls W/tools` |
| C16 | `data-files-fmt.md:54-74` 寫 aos＝`~/repo/simple_tools/aos/core/inst`（`$env/$ref/$opt`） | 這台是 `~/repo/aos/proto8`；`$ref` 有 `#/`、`..`、`$at` | 可能過時【推】 | `K/docs/01` |
| C17 | `T/12/wf-to-aos/02…`：搬檔路徑換算內容樹沒有 | `K/docs/02`：`aos-json ref --move` 一步做完 | 不一定矛盾（後者是搬節點留 `$ref`，不改別處引用）【推】；`cli/parts/json.json` 沒讀【缺】 | — |
| C18 | `P/agents.json#/ops-agent/own_notes` 指 CONTACTS.md | ops-notes 計畫要瘦身 CONTACTS | 待同步 | `O/notes/aos-migration-mapping.md` §5 |
| C19 | 11-12：「`aos-json get` 印 JSON 字面、長字串的 `\n` 不展開」 | `K/README.md` 範例用 `aos-json get --str` | 可能已補 `--str`【推】，沒跑驗證 | `T/12/wf-to-aos/01…` (b) vs `K/README.md` |
| C20 | 11-10 圖紙：`lib/agent/memory_export` 把樹印成 md | `ls A/proto8/lib/agent` 已無 memory 相關 | 已移除（11-12 knowledge-removal 的推測，原檔沒讀） | `T/10/json-memory/04-轉換與連帶.md` |

---

## 10. 需要使用者決定的問題（扣掉第 8 節已裁的）

已裁不再列：大方向（U1）；內容推薦走 json、不強制（U2-D1、U8、U17 傾向）；檢查工具先放、索引檢查 ops-agent 寫（U2-D2、U11）；always-on 之後玩（D3）；等使用者方向＝寄信給人（D4）；index 門檻與格式（U4、U5、U10）；eca 不掛 goal／todo（U7）；Bash 全面開放（U12）。

剩下的，只列選項：

1. **workflows repo 的身分**：(a) 維持不依賴 aos 的通用模板；(b) 改 aos 專用；(c) 兩條線（通用版＋aos 版）。U1 講的是「wf/」，沒明說模板 repo 本身【查】。
2. **aos 化的形態**：(a) 新增 `flavors/aos/`；(b) kernel 改寫成 json 節點；(c) `wf-init` 加選項產 `_index.json`／json；(d) 不動模板只動下游。
3. **「全都 json、只留一些 md 給人」的邊界**：哪些留 md——(a) 只留 4(e) 的「非 md 不可」清單；(b) 再加給人導航的頁（型 4）；(c) 再加流程散文（型 3）。轉成 json 的部分用 `wf-table/1` 的 `rows` 陣列形，還是 aos 式物件形（4(b)）。
4. **流程與知識分家**：(a) 照第 3 節分兩棵（workflow 樹＋knowledge 庫）；(b) 維持按工作流歸屬（STRUCTURE 現行原則）只換載體；混合型 27 檔怎麼切。
5. **新 knowledge 庫放哪**：第 3.5 節 ①–⑤；誰能寫、怎麼告訴 agent 路徑（AGENTS.md 連結／system.txt／上層 index 的 `index` 路徑）、要不要進 git、發給非 aos 專案時是否隨 `wf-init` 複製。
6. **導航層**：(a) md 導航表保留給人、index 給 agent（兩實例現況）；(b) 只留 index；index 照 15 門檻（aos 規範、aos repo）還是路由線全建（ops-notes）；手寫還是生成（`index_gen.py` 可借）；description 語言（英文 vs 繁中）；WORKFLOWS 的「可以跳流程」「活狀態判別表」規則放哪個節點。
7. **`wf-table/1`／tabledb／`$fmt` 去留**：並存、合併到 aos 式 json、或退役；連結查驗要不要找替代。
8. **wf-lint 範圍**（次要）：保留給 md、加 index 檢查（可接 `index_check.py`）、等 ops-agent 的 aos 工具；CI 怎麼辦。
9. **inbox（multi-agent）**：同樹用 mailbox／否則檔案信、拿掉檔案信、或原樣；五通道與 wake-policy、ROSTER 對 `P/agents.json`。
10. **heartbeat**：要不要把 on_clock hook 列為引擎之一；清單是否轉 json 讓 hook 讀。
11. **SESSION-LOG／WAIT_USER**：13 日「照舊」是寫手定案；D4 何時施工、兩個洞（讀了≠回了、人不會被通知）怎麼補。
12. **規矩放哪的通則**：「規矩一份留 repo、不抄 system.txt」要不要升成模板規定。
13. **既有導入怎麼遷移**：ops-notes、model_entry、gpt-soap（codex）、aos repo 自己的 wf——各自節奏／模板出一次升級／先選一個試點；誰動手。
14. **`W/wf/` 本身**：先跟上 v0.6（C14、C15），還是直接當試點。

---

## 11. 沒讀到或讀不了的

- `K/aos/` 的 `brain.json`、`errors.json` 正文、`errors/`、`cli/` 的 daemon／sweeper／talk_settings／sandbox／clock／eca／mcp_import／tools／tool_env／tool_flags／flags／errors／history；`cli/parts/` 只讀了 `_description`、`lock`（`json.json` 沒讀：`aos-json ref --move`、`get --str` 確切行為不確定）。
- `T/12/index.md`、`index-link.md`、`metainfo-views.md`、`knowledge-removal.md`、`json-tools/` **原檔沒讀**，只經 `K/docs/01`、`T/13/index-build.md` 的引用得知。
- `T/13/ops-agent-six-suggestions/` 子檔、`a2a-施工結果.md` 與 `ops-fixes-施工結果.md` 後半、`裁定落地-1113.md` 大部分、`convention-vs-agent-fsm.md`（只看開頭）；P-43、C-88、N-69 條文原檔。
- `A/wf/` 只看了 `tools/_index.json`、`workflows/_index.json`、`index_gen.json`、`WORKFLOWS.md` 開頭、`user/01`／`user/03` 的 grep、`decide_page`／`progress_board` README 開頭；`dispatch/aos-teams/` 沒讀。
- ops-notes 10-27「條列維持 markdown」原決定檔沒讀；`O/notes/aos-migration-letters.md`、`aos.md`、`agents.md` 沒讀。
- 下游實例只讀入口檔與 `_index.json`。
- 沒實測：aos-home 的 mailbox 工具是否已有 `keep: 檔名`；人開畫面的 AOS_CLOCK 修正；on_clock 實際觸發；任何寫入類 aos 工具；GitHub 渲染行為。
- `W/CHANGELOG.md`、`docs/CHANGELOG-*.md`、`W/skills/README.md` 沒讀；teaching 的 `plain-explain.md` 只依大小與表列數判成混合（沒逐段讀）。
