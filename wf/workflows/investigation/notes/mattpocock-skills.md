# mattpocock/skills 評估 — 借哲學、不借檔

[investigation](../README.md)

- **問題**：Matt Pocock 的個人 agent skill 集（MIT，25 支 SKILL.md，~968 KB）能否整合進本 repo（CC0 的 workflows 模板 repo）？該整包 vendor、部分重寫，還是只放連結？

- **方法**：讀原 repo 結構（`skills/{engineering,productivity,misc,in-progress,deprecated}/`）與其寫法理論文件（`writing-for-agents/SKILL.md`、`SKILL-MECHANICS.md`、`.agents/writing-docs.md`、`.agents/invocation.md`）；逐支 skill 對照本 repo 現有工作流（dev flavor、kernel、既有 `skills/`）找重疊／互補／全新；量測每支 SKILL.md 的 bytes 數，比對本 repo `wf-lint.sh --self` 的 8192 bytes 全 repo鐵律；檢查授權相容性（MIT → CC0 專案）。

- **發現**：
  - 定位差異：對方的 skill 是「跨專案、按觸發詞喚起的一次性程序」，本 repo 的工作流是「沿目錄層讀、跟著 repo 走的 durable 專案知識」——不是同一種東西，多數該落在使用者的 `skills/`，不是 `template/`。
  - 內容重疊過半：18 支 engineering skill 裡約 10 支與 dev flavor／kernel 既有工作流撞（如 ask-matt≈`WORKFLOWS.md`、implement≈`feature-dev`、handoff≈`SESSION-LOG.md`）；真正全新的約 4–5 支（code-review、triage、resolving-merge-conflicts、prototype、wizard）。
  - CI 硬衝突：25 支中 5 支超過 8192 bytes 上限（wayfinder 12036、ask-matt 11507、writing-for-agents 10967、teach 9646、diagnosing-bugs 8667），整包收進來會讓 `wf-lint.sh --self` 立刻紅；本 repo 現有兩支 skill 最大 7844，卡在線下顯然是刻意設計。
  - 授權：MIT → CC0 單向可行但要保留版權聲明與 MIT 全文，需另開隔離目錄＋LICENSE 副本＋NOTICE，會讓「全 repo 都是 CC0」出現例外——這是整包 vendor 方案的隱形成本；純借「觀念」用自己的話重寫則不受 MIT 拘束。
  - 可借的寫法哲學（四件事，本 repo 目前沒講到或講得較淺）：
    1. **context pointer 措辭決定觸發率**——指標的用字、而非它指向什麼，決定 agent 何時去讀；建議剪枝規則：一分支一觸發詞、同義詞合併、不重述目標檔已有身份。
    2. **兩種 load 要分開命名**：context load（每回合都花的常駐字）vs cognitive load（人要記得有哪些檔）；本 repo「AGENTS.md 永遠薄」只講了前者，`WORKFLOWS.md` 派發表其實是在消後者，命名了才好判斷什麼該進 AGENTS.md。
    3. **completion criterion 除了 clarity 還要有 demand 維度**：不只「產出可觀察的結果」，還要「逼出的功夠不夠」（例：每個被改的 model 都交代過，而非只給變更清單）；同時「看得見後面步驟會誘發提前收工」，所以應先磨鋒界線、磨不動才按序列拆。
    4. **environment-as-cache 的判準與 no-op 測試**：文件重述環境等同一份 cache，只有查詢很貴才划算；判準是「這句話改變了預設行為嗎？改不了就整句刪」——比本 repo「不留查法」的原則更具體可操作。
    5. 兩個小點：leading word（用預訓練已有的短詞當錨，別自創術語）、negation 是失敗模式（禁止句反而把被禁行為拉進 context，應正面陳述目標；本 repo 現有不少「✗ 不要…」寫法值得檢視）。
  - 對方缺我方所有：其 doctrine 完全靠人／agent 手動遵守 `CLAUDE.md`，沒有任何 lint 或 CI 檢查——這正是本 repo `wf-lint` 補的那一半，不必反向學。

- **結論**：採「借哲學、不借檔」——不整包 vendor mattpocock/skills，避免撞 8192 bytes 全 repo 鐵律、避免把單一 CC0 授權變混合、避免長期跟上游同步的維護負擔。改為：(1) 把上述可借的寫法哲學，用自己的話重寫進 `template/STRUCTURE.md`（environment-as-cache 判準、negation 反模式）與 `template/workflows/TEMPLATE.workflow.md`（context pointer 剪枝規則、Done when 的 demand 維度）；(2) 對少數全新且小的一次性程序（如 grilling、wizard、prototype），視需要另行以本 repo 風格重寫成 `skills/` 底下的獨立檔，而非搬移原檔；(3) 內容已被既有工作流覆蓋的部分（ask-matt、implement、handoff、teach、research、improve-codebase-architecture 等）不重寫、不引入。

- **來源**：mattpocock/skills（外部 repo，報告未載明完整 URL，僅以 `mattpocock/skills` 稱之，MIT License，Copyright (c) 2026 Matt Pocock）；評估日期：2026-09-02。
