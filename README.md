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

## 佈局：一個 kernel + 多個 flavor 包

核心思想（分層樹、durable 歸層、活狀態 open-only、膨脹即拆、`Done when:`）**領域中立**，抽成一份**共用 kernel**（[`template/`](template/)）；各領域的工作流拆成獨立的 **flavor 包**（[`flavors/`](flavors/)）。導入 = **kernel + 挑一個（或多個）flavor 包合起來**。

```
template/     共用 kernel（骨架，整包拿走）
flavors/
  dev/        開發 flavor 包：feature-dev、testing、conventions
  knowledge/  知識工作 flavor 包：write、digest、plan-a-thing、decide、learn、organize、writing
```

> **為什麼這樣拆**：原本所有工作流擠在一個 `template/workflows/`，導入時得「刪掉另一個領域用不到的列與檔」。改成 kernel + flavor 包後，**只複製你要的那包**，不必刪。kernel 只有一份，不會在多個 template 之間漂移。

### 挑你的 flavor 包

| flavor 包 | 適合的專案 | 典型工作流 | 導航中樞 |
|-----------|-----------|-----------|----------|
| **[dev/](flavors/dev/README.md)** | 程式開發 | feature-dev、testing、refactor、spec、plan… | code map（程式碼結構）|
| **[knowledge/](flavors/knowledge/README.md)** | 寫作 / 研讀 / 規劃 / 決策等非開發知識工作 | write、digest、plan-a-thing、decide、learn、organize | INFO_MAP（材料結構）|

混合型專案兩包都合、兩張派發表都貼。各包 README 有它自己的內容清單與**合併步驟**。

## 如何套用到新專案

1. 把 **[`template/`](template/)** 這個 kernel 整包複製到你專案根目錄。
2. 打開你要的 **flavor 包 README**（[dev](flavors/dev/README.md) / [knowledge](flavors/knowledge/README.md)），照它的**合併步驟**把該包的 `workflows/*` 合進 `workflows/`、把它的 `WORKFLOWS.<flavor>.md` 派發表貼進 kernel 的 `WORKFLOWS.md` 佔位區塊。
3. 全域搜尋 `{{` 把佔位符填成你專案的實況；讀到的 **`〔模板說明〕`** 區塊照它說的做，做完刪除該區塊。
4. 也可以直接讓 Claude 代勞：把本 repo 路徑給 Claude Code，說「照這套模板、用 dev（或 knowledge）flavor 幫我的專案建立工作流」。

> **關於連結**：flavor 包裡工作流的向上導覽連結（`← [WORKFLOWS](../WORKFLOWS.md)` 等）是**照「合併後」的佈局**寫的——合進 kernel、落位到專案的 `workflows/` 後才會全部解析。在本 repo 裡從 `flavors/` 直接點會指不到 kernel 檔，這是預期的，不是壞連結。

## template/（kernel）內容

| 檔案 | 角色 |
|------|------|
| [AGENTS.md](template/AGENTS.md) | 最頂層路由器：專案一句話 + 鐵律 + 指向 WORKFLOWS / INDEX / 活狀態 |
| [CLAUDE.md](template/CLAUDE.md) | 相容用轉址：一句話指回 AGENTS.md（Claude Code 會讀它） |
| [WORKFLOWS.md](template/WORKFLOWS.md) | 派發器骨架：中立的「工作流統一形式 + 活狀態」+ 一個**派發表佔位區**（由 flavor 包貼入）|
| [INDEX.md](template/INDEX.md) | repo 頂層結構地圖 |
| [DEV-GUIDE.md](template/DEV-GUIDE.md) | 被動結構整理參考：膨脹即拆／雜亂即分類 + 四級成長軌跡 |
| [SESSION-LOG.md](template/SESSION-LOG.md) | 進度 hub（open-only）|
| [WAIT_USER.md](template/WAIT_USER.md) | 待使用者親自做/驗證的事（open-only）|
| `inbox/` + [workflows/inbox/](template/workflows/inbox/README.md) | agent 之間的**信件**：`inbox/` 是放信處（保持乾淨）、`workflows/inbox/` 是使用方式＋通訊錄＋模板（可選；活狀態第三軸，像 email——狀態靠位置、寄失敗/不回都無妨）|
| [workflows/common/](template/workflows/common/README.md) | 跨工作流共享：gotchas（踩坑，kernel 內建）；conventions / writing 由 flavor 包合入 |

## 這套為什麼有效（設計理由）

- **AI agent 的 context 有限**：薄入口 + 層層派發，agent 每次只載入當前任務需要的知識，而不是把整包文檔塞進 context。
- **文檔不腐化**：durable 知識有唯一歸屬層、活狀態 open-only 完成即刪、過時文檔進 `archive/`——三招讓每份現役文檔都保持可信。
- **結構跟著需求長**：四級成長軌跡（單檔 → 資料夾＋單 README → 多檔分職 → 巢狀子工作流）讓組織成本永遠與實際體量匹配，不預先過度設計，降級也成立。
