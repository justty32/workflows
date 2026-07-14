# 通用分層工作流模板（AGENTS.md 為入口）

從實際專案淬鍊出來的一套**以 AGENTS.md 為最頂層路由器的分層工作流**，可套用到任何種類的專案（不限程式專案）。對 AI agent（Claude Code 等）友善：agent 沿著層層 index 往下走，只讀需要的那一層，不用一次吞下整個專案的知識。

## 核心思想（一分鐘版）

1. **分層樹**：整個專案文檔是一棵樹，每層**只指向下一層、不存下層細節**：
   ```
   AGENTS.md（最頂，薄路由器）→ WORKFLOWS.md（依意圖派發）/ INDEX.md（結構地圖）
     → 各工作流入口（README 或單檔）→ 工作流內容 → 子工作流…
   ```
2. **檔名語意**：**README**＝初入一個資料夾先讀的**入口／導引**；**INDEX**＝描述該資料夾**頂層結構**的索引。小資料夾兩者合一，大了才分出獨立 INDEX。
3. **durable 知識歸層**：每份長期知識歸到它所屬的那個工作流／那一層，**絕不往上堆**——所以 AGENTS.md 永遠很薄。
4. **活狀態只列 open**：進度記 `SESSION-LOG.md`、需要使用者親自做/驗證的記 `WAIT_USER.md`；**完成即刪除**，不留已完成清單（歷史交給 git log）。
5. **膨脹即拆、雜亂即分類**：結構整理原則＋工作流四級成長軌跡收在 `DEV-GUIDE.md`——它是**被動參考**，只在要整理結構時取用，不是 always-on 憲法。
6. **鐵律極少而 always-on**：只有 3–5 條任何時刻都適用的鐵律常駐 AGENTS.md（行為不變、未經確認不 push…），其餘一切按需取用。

## 如何套用到新專案

1. 把 **[`template/`](template/)** 底下所有檔案複製到你專案的根目錄（`template/workflows/` → 專案的 `workflows/`）。
2. 全域搜尋 `{{`，把佔位符填成你專案的實況；讀到的 **`〔模板說明〕`** 區塊照它說的做，做完刪除該區塊。
3. 打開 `WORKFLOWS.md` 派發表：**刪掉用不到的列、加上你需要的**。新工作流一律從**單檔**開始長（見 DEV-GUIDE 四級成長軌跡），不要預先建資料夾。
4. 也可以直接讓 Claude 代勞：把本 repo 路徑給 Claude Code，說「照這套模板幫我的專案建立工作流」。

## template/ 內容

| 檔案 | 角色 |
|------|------|
| [AGENTS.md](template/AGENTS.md) | 最頂層路由器：專案一句話 + 鐵律 + 指向 WORKFLOWS / INDEX / 活狀態 |
| [CLAUDE.md](template/CLAUDE.md) | 相容用轉址：一句話指回 AGENTS.md（Claude Code 會讀它） |
| [WORKFLOWS.md](template/WORKFLOWS.md) | 派發器：使用者意圖 → 工作流 → 入口檔；工作流統一形式規範 |
| [INDEX.md](template/INDEX.md) | repo 頂層結構地圖 |
| [DEV-GUIDE.md](template/DEV-GUIDE.md) | 被動結構整理參考：膨脹即拆／雜亂即分類 + 四級成長軌跡 |
| [SESSION-LOG.md](template/SESSION-LOG.md) | 進度 hub（open-only）|
| [WAIT_USER.md](template/WAIT_USER.md) | 待使用者親自做/驗證的事（open-only）|
| [workflows/common/](template/workflows/common/README.md) | 跨工作流共享：conventions（碰原始碼才需要）+ writing（產出散文才需要）+ gotchas（踩坑）|
| [workflows/feature-dev/](template/workflows/feature-dev/README.md) | **資料夾型**工作流範例（功能開發）|
| [workflows/testing.md](template/workflows/testing.md) | **單檔型**工作流範例（跑測試）|

## 這套為什麼有效（設計理由）

- **AI agent 的 context 有限**：薄入口 + 層層派發，agent 每次只載入當前任務需要的知識，而不是把整包文檔塞進 context。
- **文檔不腐化**：durable 知識有唯一歸屬層、活狀態 open-only 完成即刪、過時文檔進 `archive/`——三招讓每份現役文檔都保持可信。
- **結構跟著需求長**：四級成長軌跡（單檔 → 資料夾＋單 README → 多檔分職 → 巢狀子工作流）讓組織成本永遠與實際體量匹配，不預先過度設計，降級也成立。
