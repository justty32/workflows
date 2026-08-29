# 改進提案（2026-08-29）

← [repo README](../README.md)｜原始討論記錄：[reviews/2026-08-29/](reviews/2026-08-29/)

五個 agent 各從一個角度獨立審視本 repo（① 導入後每天在裡面工作的 agent、② 導入流程實測、③ kernel 架構、④ flavor 包內容、⑤ repo 工程品質與唱反調），各寫一份報告。本檔是**綜合與排序**：把五份報告裡互相印證的結論收斂成一張優先清單，並標明幾個 agent 獨立提到同一件事（「共識度」）。細節與證據看各角度原報告。

量化基準（bash 實測）：kernel `template/` 13 個 md 共約 35 KB；其中定期喚醒四檔（tick / routines / schedule / wf-tick）約 9.7 KB（28%）、inbox 三檔約 7.2 KB（20%）。AGENTS.md 3.8 KB。從 AGENTS 走到「動手做一個功能」最短路徑 4 檔、約 12.7 KB。`{{` 佔位約 43 處、〔模板說明〕約 36 段。

---

## 一、先修的 bug（現況就是錯的，不是取捨）

### 1. kernel 內有 2 個導入後必斷的連結 　共識度：②
- `template/WORKFLOWS.md` 的 `[README](../README.md)` 指向本 repo 的 README，導入到專案後上一層沒這檔。
- `template/AGENTS.md` 「開發環境」段的範例 `[workflows/dev-env.md](workflows/dev-env.md)` 是真連結，但檔不存在（dev flavor 也沒提供）。
- **做法**：前者改純文字或 GitHub URL；後者改反引號路徑。順手看 §4 的連結檢查腳本。

### 2. `non-invasive-import.md` 的「`wf/` 內部連結不受影響」不成立——實測 22 個壞連結 　共識度：②
- 所有向上連 `AGENTS.md` 的導覽列（`INDEX`、`WORKFLOWS`、`DEV-GUIDE`、`SESSION-LOG`、`WAIT_USER`、`routines`、`schedule`、`common/README`、`inbox/README`、`feature-dev/README`、`conventions`）全部指錯一層。
- `.claude/commands/wf-tick.md` ↔ `wf/workflows/tick.md` 雙向斷。文件完全沒提 `.claude/` 必須留專案根（Claude Code 只讀根的 `.claude/commands/`），「頂層只留兩個檔」其實是「兩檔 + 一個隱藏目錄」。
- inbox 的地址規則「對方工作資料夾底下的 `inbox/`」被 `wf/inbox/` 打破，AGENTS.md 那句「放信處是 repo 根的 `inbox/`」也跟著錯。
- **做法**（二選一）：(a) 文件明列三類要改的連結各附一行 `sed`，並補 `.claude/` 留根、inbox 例外留根（它本來就是對外介面）；(b) 更根本：kernel 內部**不再向上連 AGENTS.md**——AGENTS 是入口，沒人需要從下面點回去；導覽列只連同層或向下，非侵入式就自然成立。**建議選 (b)**。

### 3. 鐵律「未經確認不 push」與 routines / schedule 打架 　共識度：①③⑤
- `AGENTS.md` 鐵律 2「未經確認不 push」；`routines.md` EOD 範例「跑收尾——保存 / push」；`schedule.md`「使用者親自排的→視為已授權」。tick 半夜醒來讀到 EOD 分區，兩條規則衝突，agent 得自己裁決。
- **做法**：鐵律 2 改成定義「**授權來源**」：不可逆／對外動作（push、刪除、對外送出）需有授權來源＝使用者當場確認、或 routines / schedule 裡**由使用者登記**的項目。routines / schedule 各改成引用這條而非各自解釋；EOD 範例改成「列出待 push 的 commit 問使用者」。

### 4. `/wf-tick` 「沒給週期就 self-pace」與 tick「不判時間」矛盾 　共識度：①
- self-pace 必然要判時間，責任落誰沒寫。**做法**：`/wf-tick` 強制帶週期（沒給用預設 `30m` 並回一句），刪 self-pace 分支。

### 5. `CONTACTS.md` 範例洩漏作者私人路徑 　共識度：⑤
- `{{~/repo/moddings/rimworld/inbox/}}`。換成中性範例。

---

## 二、結構性改進（最高共識）

### 6. 定期喚醒（tick / routines / schedule / wf-tick）移出 kernel 成 flavor 包 　共識度：③⑤（①④ 側面支持）
- `WORKFLOWS.md` 說它「不屬任一 flavor、kernel 一律有」，隨後又說「整套用不到就刪」——「一律有」與「可刪」自相矛盾。內容高度特定（Windows PowerShell 時區指令、「09:00 開工盤點 docker ps」「16:30 EOD push」是作者的 ops 日常）。與 Claude Code 原生 `/loop`、cloud routines（`/schedule`）、OS cron 完全重疊——`/wf-tick` 本身就是 `/loop` 的薄殼。佔 kernel 28%。
- **做法**：搬成 `flavors/heartbeat/`（或併入未來的 ops 包）。kernel `WORKFLOWS.md` 只留一行「要定期喚醒→合 heartbeat 包」。包內 README 明講定位：**清單放 repo、跟版控、agent 可讀**是它唯一價值，執行引擎一律借原生。時區指令縮成 `TZ=… date` 一行，平台差異丟 gotchas。

### 7. inbox 也移出 kernel 成 `flavors/multi-agent/` 　共識度：⑤（③ 側面支持）
- 對單人單 session（模板多數受眾）是純負擔：導入後要在 AGENTS / INDEX / WORKFLOWS / WAIT_USER 四檔刪六段才乾淨，忘了刪就永遠帶著空 `inbox/` 與 email 比喻。「可選但常駐 kernel」直接違反 README 自己的主張「只複製你要的那包，不必刪」。佔 kernel 20%。
- **做法**：kernel 活狀態回到兩軸（進度 / 待使用者）；multi-agent 包的合併步驟負責「貼一行進 AGENTS / WORKFLOWS」把第三軸加回來。同時補 ③ 指出的兩件事：README 明寫並發假設（單一收件 agent、單機同一檔案系統）與「和原生 SendMessage / ListAgents 的分工」（inbox 是跨機、跨時間、可版控的慢通道）；CONTACTS 地址改相對某個 root 或明講「機器本地，各機自維護」。
- 砍完 §6 §7 後 kernel 約 18 KB，「薄」的宣稱才成立。**不該砍的**（⑤ 反向確認）：`CLAUDE.md` 一行轉址、SESSION-LOG / WAIT_USER 兩軸、四級成長軌跡、`Done when:`。

### 8. 核心思想在 5 個檔重述，改成 single source 　共識度：①③⑤
- 「只指向下一層」「README＝入口 / INDEX＝結構」「DEV-GUIDE 是被動參考」「三軸活狀態只列 open」各在 README、AGENTS、INDEX、WORKFLOWS、DEV-GUIDE、SESSION-LOG、WAIT_USER、inbox/README 出現 1–3 次。措辭已漂移（「完成即刪除」「完成即移除」「完成即刪」）。這些是**給導入者看的設計理由**，不是給工作中 agent 的指令，agent 卻每站吞一次。
- **做法**：原則只活在兩處——repo README「一分鐘版」（對外）與 DEV-GUIDE（整理結構時讀）。AGENTS.md「分層思想」段縮成兩行（樹圖 + 「原則見 DEV-GUIDE」）+ 鐵律，目標 ≤ 1.5 KB；INDEX / WORKFLOWS / SESSION-LOG 的重述句刪掉只留連結。`WORKFLOWS.md`「統一形式」整節搬 DEV-GUIDE，派發器只剩：派發表 + 「都不符→INDEX」。

### 9. `DEV-GUIDE.md` 改名（`STRUCTURE.md`） 　共識度：①⑤
- kernel 標榜領域中立，整理原則的檔名卻叫 DEV-GUIDE；知識 flavor 的 organize.md 得解釋「這是 DEV-GUIDE 的非開發版」。與 §8 一起做才划算（約 25 處連結一次 sed）。

### 10. 工作流入口檔缺統一骨架 　共識度：③④
- knowledge 六檔都有 `Done when:` + 流程 + 「何時不用」；dev 的 feature-dev、testing 兩者皆無（`Done when` 在 dev 包 grep 為 0 筆）。`WORKFLOWS.md`「統一形式」只規範檔名與資料夾型/單檔型，不規範**內容段落**。
- **做法**：kernel 加 `template/workflows/TEMPLATE.workflow.md`（與 `TEMPLATE.letter.md` 命名一致），固定段落：一句做什麼 / 何時用 ↔ 何時不用 / `Done when:` / 流程 / 內容表（資料夾型才有）/ 交接（→ 接誰）。兩包現有檔照它對齊。`Done when:` 佔位改成「✗ 壞例 / ✓ 好例」並限定三類：檔案存在、指令回傳、表格填滿。

---

## 三、讓 agent 少出錯（可操作的觸發條件）

### 11. SESSION-LOG 的寫入時機不可偵測 　共識度：①③
- 唯一觸發「事情告一段落、需求結束、臨時中止時」——三者 agent 都難自我偵測（context 被壓縮、使用者 Ctrl+C）。
- **做法**：改成固定動作三條寫在 `SESSION-LOG.md` 開頭：① **開始**多步驟工作前先寫一行 open（不是做完才寫）；② **每次 commit 後**更新／刪除該行；③ 條目格式固定 `[工作流] 一句 open 狀態 → 下一步 / 連結`。硬中斷時 log 至少反映「進行中」。

### 12. 開場 checklist 　共識度：①
- session 開始要判斷「有沒有未完的事」得開 3 個檔。AGENTS「先讀哪裡」之前加 3 行開場動作：`ls inbox/*.md`、`grep -c '^- ' SESSION-LOG.md WAIT_USER.md`，有東西才進去讀。

### 13. 「commit 到主分支是慣例」不該是鐵律 　共識度：①③
- 對有 branch protection / PR 流程的 repo 是錯的。改成佔位 `{{分支慣例：直接 commit main / 開 branch 走 PR}}`；或依 §17 搬到使用者偏好。

### 14. `archive/` 出現 5 處但零命名規則；gotchas 缺記錄門檻 　共識度：①
- DEV-GUIDE 加三行：檔名保留原名；檔頭第一行 `> 封存 YYYY-MM-DD，由 <路徑> 取代`；archive 內不放 README。gotchas 加門檻：「第二次撞到、或使用者說『上次也是這樣』才記」。

### 15. 三軸判別表 　共識度：③
- 「催另一個 agent」橫跨 WAIT_USER 與 inbox；同 repo 的 fork / 子 agent 交接三軸都沒接住。加 2×2 判別：等**人**→WAIT_USER；等**別資料夾的 agent**→inbox；等**同 repo 另一 session / fork**→SESSION-LOG 一行。

---

## 四、缺的 durable 類別

### 16. 決策記錄（為什麼選 A 不選 B） 　共識度：③
- 「完成即刪、歷史交給 git log」漏掉「為什麼」——git log 找得回改了什麼，找不回為什麼放棄方案 C。knowledge 的 `decide.md` 有模板，dev 與 kernel 沒有落點。
- **做法**：kernel 加 `workflows/decisions/`（從單檔 `DECISIONS.md` 第 1 級長起），格式借 decide 的「結論 / 未選原因 / 前提」。活狀態是「未完」，決策是「已定但要留理由」——三軸不動，只是多一類 durable。

### 17. 使用者偏好與領域詞彙 　共識度：③
- AGENTS.md 沒有「使用者是誰、語言、什麼事要先問、什麼可直接做」的位置；目前散落（push 規則硬編成鐵律、繁簡條款藏在 writing.md）。非開發專案術語量大，agent 每次重猜。
- **做法**：`workflows/common/user.md`（偏好：語言、確認邊界、風格）+ `common/glossary.md`（可選，長出來才建）。鐵律縮回真正「任何專案都成立」的那幾條。

---

## 五、導入體驗與工具

### 18. 連結檢查 + 導入驗收腳本 　共識度：②③⑤（最高）
- 沒有任何機械檢查，§1 §2 的壞連結就是這樣漏掉的；DEV-GUIDE 寫死門檻數字卻沒東西掃。
- **做法**：`tools/wf-lint.sh`（純 bash，附錄有雛形）：① 相對 `.md` / 目錄連結解析；② `find -size +8192c` 超標檔；③ `grep -rn '{{\|〔模板說明〕'` 殘留；④ `inbox/` 頂層堆積數。`flavors/` 在本 repo 內連結是預期壞的，腳本要能以「合併後路徑」模擬（把 `flavors/X/workflows` 映射到 `template/workflows`）。配一個 `.claude/commands/wf-lint.md` 薄殼；README 導入步驟末尾加「跑 wf-lint，0 BROKEN 才算完成」；順便給 routines 一個真實的間隔型用例。GitHub Actions 只跑這支，別做更多（⑤：spell check / lint 都是過度工程）。

### 19. 導入全自動化 `tools/wf-init.sh <flavor…> [--non-invasive DIR]` 　共識度：②
- 五步全手動，但合併、貼表、改連結都是純機械操作。**無法自動化的只有兩件事**：填 `{{}}`（要專案事實）與判斷〔模板說明〕裡「用不到就刪」的分支——腳本結束時印出這兩張殘留清單交給人或 Claude 收尾。現成的 `<!-- ↓↓↓ … ↑↑↑ -->` 標記已可當貼入錨點。

### 20. 「讓 Claude 代勞」要有給 Claude 的指示檔 　共識度：②
- README 步驟 4 只說「把 repo 路徑給 Claude」，沒有 agent 可執行的流程，每次結果不同。加 `IMPORT.md`：跑 wf-init → 逐檔處理 `{{` → 逐段處理〔模板說明〕（集中列出 9 段「條件刪除」型判斷題）→ 跑 wf-lint → 回報殘留。README 加一行 `Done when:`（`{{` 為 0、〔模板說明〕為 0、0 BROKEN）。

### 21. 〔模板說明〕分兩種標記 　共識度：②⑤
- 36 段混著「純解說（讀完刪）」與「條件指令（不用 X 就刪整檔並改上層那列）」；後者被機械刪除後上層 INDEX / common/README 的列成孤兒。條件型改標 `〔導入判斷〕` 並列明「刪掉後要同步改哪幾個檔」；「用不到就刪」類全拔，規則只在 README 寫一次。`WORKFLOWS.<flavor>.md` 片段只留表、菜單搬回 flavor README。

### 22. 升級路徑完全缺席 　共識度：②⑤
- 導入＝複製後脫鉤；kernel 已結構性改版三次（拆 flavor、加 inbox、加 tick），既有專案無從得知、也無法安全 diff（佔位填過、說明刪過，diff 全是噪音）。
- **做法**：`template/AGENTS.md` 尾端 `<!-- wf-kernel v0.x (YYYY-MM-DD) -->`（agent 不讀、人可 grep）+ 根 `CHANGELOG.md`（每次 kernel 變動一行：改哪檔、既有專案要不要跟）+ git tag。把檔案分成 **kernel-owned**（DEV-GUIDE、tick、inbox/README、TEMPLATE.*、wf-tick：無佔位、可整檔覆蓋）與 **project-owned**（AGENTS、INDEX、WORKFLOWS、活狀態、routines 清單：只讀 CHANGELOG 手動套），在 IMPORT.md 標明。

### 23. `examples/`：看得到「長好的樣子」 　共識度：⑤
- 通篇 `{{}}` 與〔模板說明〕，沒有一個填好、刪乾淨的成品可對照——這是導入最大的認知成本。加 `examples/dev-minimal/`、`examples/knowledge-minimal/`，各是假專案（「todo-cli」「日文學習筆記」）的合併成品，AGENTS.md 30 行以內。它同時是 wf-lint 的迴歸測試對象。

---

## 六、flavor 包內容

### 24. dev 包：8 個「只有名字沒有檔」的菜單工作流 　共識度：④
- 補三個 ≤ 1 KB 單檔骨架：`refactor.md`（觸發＝門檻超標；Done when＝行為不變 + 驗證綠燈）、`investigation.md`（模板：問題 / 方法 / 發現 / 結論 / 來源）、`dev-env.md`（AGENTS 已指名要它）。idea / roadmap / spec / plan 是同一個想法的四個階段，合成**一個** `planning/` 管線資料夾，別分四檔讓 agent 卡在「這算 idea 還是 roadmap」。tooling 併入 dev-env。idea / roadmap 兩包都引用、與領域無關 → 上移 kernel。

### 25. knowledge 包：邊界與 writing.md 　共識度：④
- digest ↔ learn 差在目的不在動作（「幫我讀懂 Kubernetes」兩邊都中）：派發表加「分辨」欄，或把 learn 降為 digest 的升級形態（長出 `topics/`、`questions.md` 就是 learn）。decide 補「完成後 → 接 plan-a-thing 執行」；「何時不用」補齊到 decide、organize。
- `writing.md` 5.2 KB 是知識包最大的檔，但參考作者（張大春、阮一峰、Huli…）是作者個人閱讀史，90% 使用者會整段改掉卻沒用 `{{}}` 標出。改成 `{{參考作者（範例：…）}}`；AI 味清單改成 `詞 / 為什麼壞 / 替換` 表格 + 一行 `grep -nE '值得一提|眾所周知|總而言之|賦能|抓手|閉環'` 供產文後自檢；繁簡表抽 `writing/zh-tw.md` 子檔。

### 26. 混合型專案雙表衝突 　共識度：④
- dev 的 plan vs knowledge 的 plan-a-thing 觸發詞都是「規劃」（以「產出是否為程式碼」分流）；gotchas 列兩表都有（只留一份）；conventions 與 writing 都自稱共用，碰原始碼又要寫 README 時誰優先沒說。README「混合型」一句擴成小節。

### 27. 缺的 flavor：先補 ops 　共識度：④（⑤ 側面）
- routines 範例（docker ps、健康檢查、深度巡檢）全是維運場景，卻沒有 ops 包承接「異常 → 轉對應深查工作流」。`flavors/ops/`：`inventory.md`（routines 呼叫的就是它）、`incident.md`（現象原文照貼 → 定位 → 修 → 記 gotchas）、`deploy.md`（含 WAIT_USER 交接點）。research 與 knowledge 重疊高、personal 可用現有湊、modding 太特定——都不急。

### 28. 小項 　共識度：④
- `testing.md` 862 B 撐不起「離線機也能開發」：加 `驗證 | 指令 | 誰跑（Claude / 使用者→WAIT_USER）` 三欄表。
- code map / INFO_MAP 只有名字沒骨架：dev 加 `common/code-map.md`（領域 | 檔案 | 職責 | 測試在哪）、knowledge 加 `INFO_MAP.md`（材料 | 位置 | 負責什麼 | 衍生產物），結構故意對稱。
- 各 flavor README 末尾加「刪除某工作流要動的地方」表（有 wf-lint 後可降級為「跑腳本」）。

---

## 七、repo 自身

### 29. LICENSE 　共識度：⑤
- 公開 repo 沒授權條款＝法律上他人不能複製使用，與「模板給人套用」直接矛盾。純文檔建議 CC0（或 MIT）。一分鐘的事。

### 30. repo 沒吃自己的狗糧 　共識度：⑤
- 根目錄平鋪 `non-invasive-import.md`，沒有 AGENTS.md / INDEX / docs。本檔已開 `docs/`；建議 `non-invasive-import.md` 也搬進來，README 只留連結。另加一份 5 行的根 `AGENTS.md`（這是模板 repo、改 kernel 要同步 README 表、flavor 連結按合併後寫、跑 wf-lint）——正是模板主張的薄路由器，既示範又實用。不必套完整 kernel。

### 31. 不做英文版 README 　共識度：⑤
- kernel 全中文、writing.md 強綁繁中，英文 README 會誤導。只在 README 第一段加一句英文 one-liner：「Written in Traditional Chinese; the structure itself is language-agnostic.」

---

## 建議的執行順序

| 階段 | 內容 | 對應 |
|------|------|------|
| **0. 半小時內** | 修 2 個壞連結、CONTACTS 中性範例、LICENSE、`non-invasive-import.md` 搬 docs + README 連結 | §1 §5 §29 §30 |
| **1. 先讓檢查存在** | `tools/wf-lint.sh` + `examples/dev-minimal`（當迴歸對象）；用它重掃非侵入式佈局，據此重寫 `non-invasive-import.md`（建議走「kernel 不向上連 AGENTS」） | §18 §23 §2 |
| **2. 瘦 kernel** | 定期喚醒 → `flavors/heartbeat/`；inbox → `flavors/multi-agent/`；鐵律改「授權來源」；核心思想 single source；DEV-GUIDE 改名；AGENTS ≤ 1.5 KB | §6 §7 §3 §8 §9 |
| **3. 讓 agent 少出錯** | SESSION-LOG 三條寫入時機、開場 checklist、archive / gotchas 規則、三軸判別表、`TEMPLATE.workflow.md` + Done when 好壞例 | §11–15 §10 |
| **4. 導入與升級** | `wf-init.sh`、`IMPORT.md`、〔導入判斷〕標記、KERNEL-VERSION + CHANGELOG + kernel-owned / project-owned 分類 | §19–22 |
| **5. 補內容** | dev 三骨架 + `planning/`、decisions / user / glossary、ops flavor、writing.md 去個人化、knowledge 邊界 | §24 §16 §17 §27 §25 §26 §28 |

階段 1 放在瘦身之前是刻意的：先有 lint 和 example，階段 2 的大搬家才有迴歸保護。

---

## 附錄：連結檢查雛形（角度 ② 實測用，20 行）

```bash
#!/bin/bash
# usage: linkcheck.sh <root>  — 檢查所有 .md 相對連結（.md 與目錄）是否存在
root=$1
while IFS= read -r f; do
  d=$(dirname "$f")
  grep -oE '\]\(([^)#]+)(#[^)]*)?\)' "$f" | sed -E 's/^\]\(//; s/\)$//; s/#.*$//' | while read -r l; do
    [[ -z "$l" || "$l" =~ ^https?:// || "$l" =~ ^mailto: ]] && continue
    [[ -e "$d/$l" ]] || echo "BROKEN ${f#$root/} -> $l"
  done
done < <(find "$root" -name '*.md')
```

對 `template/` 直接跑會抓到 §1 的兩個；對照 README 導入步驟合成一個 dry-run 目錄再跑，就是 §2 的 22 個。
