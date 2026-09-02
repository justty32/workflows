# 可組合單元 — 本 repo 缺的是中插契約，不是檔案更小

[investigation](../README.md)

- **問題**：mattpocock 式「小而可組合」的 skill 模式，要怎麼納入本 repo（kernel + flavor + `AGENTS.md` 薄路由器）這套分層工作流體系？

- **方法**：讀團隊 B 附篇（`team-b-composable.md`，母報告 `team-b-mattpocock.md`）。比較本 repo 工作流與 mattpocock skill 在粒度／觸發／組合方式上的差異；盤點本 repo 現有、事實上已符合「可組合單元」形狀的檔案；對四個候選方案（派發表加欄、全面拆步驟檔、新增 `skills/` 目錄、改 `TEMPLATE.workflow.md`／`STRUCTURE.md`）逐一評估破壞性與收益；用 `feature-dev` 實際拆一次做可行性示範。

- **發現**：
  - 分水嶺不是檔案大小——本 repo 8 KB 上限已在逼小（實測 677–7566 bytes）；mattpocock 無上限（164–12036 bytes）。真正的差異是**組合方式**：本 repo 是「尾接」（工作流跑完，「交接」段連下一步），mattpocock 是「中插」（流程中途 `Call the Skill tool` 呼叫另一支，回來接著跑）。
  - 本 repo **其實已經在中插**，只是沒寫成慣例：`feature-dev` 第 3 步呼叫 `testing`、`refactor` 第 1、3 步也呼叫 `testing`、`study-site` README 明寫「流程 2–3 之間插入 `foundations-first`」。新作者不知道工作流可以寫成「可被中插」的形狀。
  - 本 repo 已存在兩類事實上的可組合單元：
    - 純參考型（任何工作流可中途取用）：`common/conventions`、`common/code-map`、`common/gotchas`、`common/user`、`common/data-files`、`common/writing`、`common/index-rules`、`STRUCTURE.md`。
    - 可中插的程序型（已有實際中插先例）：`testing.md`、`decisions.md`、`refactor/moving-things.md`、teaching 的 `quality-gates.md`／`publish.md`、`foundations-first.md`、multi-agent 的 `resources.md`／`inbox/wake-policy.md`、tidy 的 `manager-brief.md`。這些都缺「我可以被中途呼叫、需要什麼輸入、回傳什麼」的宣告。
  - 大塊頭工作流可拆性：`feature-dev` 高（且拆了有實利）；`study-site` 半成品（子檔已存在但外部進不去）；`tidy`／`dispatch`／`source-intake` 中；`analysis` 低（Level 間嚴格依賴）；`inbox` 低且**不該拆**（它是一份協議，拆開兩邊會不一致）。
  - 四選項評估：
    - (b) 派發表加「串接」欄 — **不做**：串接是多對多，一欄裝不下，且片段散在 7 個 `WORKFLOWS.<flavor>.md`，改一次動七檔。
    - (c) 大工作流一律拆成步驟檔 — **只在自然膨脹時順帶**：直接違反 `STRUCTURE.md` 「不預先過度設計」原則，且會牽動 `wf-lint --self` 的 16 種 flavor 組合測試面。
    - (d) 新增 `skills/` 與 `SKILL.md` — **要，但須限定定位**：風險是引入第二套路由（同一件事兩處寫）。定位：`workflows/` = 進使用者專案的 durable 知識、harness 中立；`skills/` = 不進專案、跨專案可攜的一次性程序，且薄殼指回工作流。使用者已放的 `markdown-html-slides`、`html-slides-shared-assets` 正好符合此定位。
    - (a) 改 `TEMPLATE.workflow.md`＋`STRUCTURE.md` — **推薦主軸**：純加段，不動分層樹、派發表、lint、任何既有工作流路徑；空間足夠（`STRUCTURE.md` 6194→+600 仍在 8192 內）。具體三處：① `STRUCTURE.md` 成長軌跡後加「可組合單元」一節，定四條規則——有自己的 Done when、不假設呼叫者是誰（需要的輸入列成「必要輸入」）、回哪裡由呼叫者決定（不寫死接續哪個工作流）、被中插時不佔 `SESSION-LOG.md` 一行；② `TEMPLATE.workflow.md` 「交接」段之上加可選「被呼叫」段（誰會中途呼叫我／需要什麼輸入／回傳什麼），用不到就刪；③ `WORKFLOWS.md` 說明句加一行，講明「可組合單元」也照樣列在派發表，只是入口檔多一個「被呼叫」段。
  - `feature-dev` 拆解示範：把 7 段流程收成「呼叫 code-map → 改 → 呼叫 testing → 呼叫 commit」四行，新增 `workflows/commit.md`（commit 前對齊清單）。價值不在「拆小」本身，而在 `commit.md` 這份清單原本被 `feature-dev`、`refactor`、`tidy`、`patch` 各自重寫一份、寫得還不一樣——抽成一支單元是**解掉既有重複**，不是製造新檔。
  - setup skill 對照：mattpocock 有互動式 `setup-matt-pocock-skills`＋ADR 0001 硬／軟相依分級；本 repo 用佔位符＋`wf-lint --strict` 機械檢查，答案直接寫死進使用點，整體更強（有機械檢查、不留 config 層腐化、不需 harness 支援）。可借兩點：① 硬／軟相依二分——目前導入判斷段落沒分級，可加上「必填」／「可略」標記；② 探查優先於發問——`IMPORT.md` 可補一張「測試指令看 package.json/Makefile、分支慣例看 git symbolic-ref、語言看副檔名統計」的查法表。**不可借**：把導入本身做成 `SKILL.md`，會讓導入依賴特定 harness，違背 `AGENTS.md` 中立入口這個賣點。

- **結論**：可組合單元應以方案 (a) 為主軸、(d) 為輔、(c) 順帶、(b) 不做——具體是：
  1. 在 `STRUCTURE.md` 成長軌跡後加「可組合單元」一節，定義四條契約（自帶 Done when／不假設呼叫者／回呼叫者決定／不佔 SESSION-LOG）；
  2. 在 `TEMPLATE.workflow.md` 加一段可選的「被呼叫」段（用不到就刪，比照現有段落慣例）；
  3. 在 `WORKFLOWS.md` 說明句補一行，講明可組合單元照樣列派發表，只是入口檔多一段；
  4. 新增 `skills/` 目錄，但限定只放「不進使用者專案、跨專案可攜的一次性程序」，且必須薄殼指回對應工作流，不得與 `workflows/` 重複擁有同一份 durable 知識；
  5. 先把 `testing.md`、`common/code-map.md` 等已被實際中插的檔案補上「被呼叫」段作示範，`feature-dev` 抽出 `commit.md` 驗證「拆了有實利」這個判準；
  6. 派發表結構、8 KB 上限、`wf-lint` 一律不動；大工作流是否拆，仍照「自然膨脹／職責雜亂」判準，不預先拆。
  **狀態：待做**（報告只給出方案與示範，未實際修改 `STRUCTURE.md`／`TEMPLATE.workflow.md`／`WORKFLOWS.md`，也未新建 `skills/` 或 `commit.md`）。

- **來源**：`team-b-composable.md`（母報告 `team-b-mattpocock.md`，同一 `reports/` 目錄，路徑內部參照，報告未載明外部 mattpocock skill repo 的 URL）。評估日期：2026-09-02。
