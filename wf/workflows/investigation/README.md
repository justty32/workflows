# investigation — 調查 / 解讀外部系統 / 可行性

[WORKFLOWS](../../WORKFLOWS.md)｜[INDEX](../../INDEX.md)

只讀不改，查清楚「這怎麼運作／可不可行」，產出可歸檔的筆記。

**何時用**：看懂外部系統或別人的碼、評估可行性、查 bug 成因、評估某個外部 repo 值不值得吸收。
**何時不用**：已知道怎麼改 → [feature-dev](../feature-dev/README.md)；只搬結構 → [refactor](../refactor/README.md)。

## Done when

- `notes/<主題>.md` 存在，且下列五段非空；單篇 < 8192 bytes（超了照 [STRUCTURE](../../STRUCTURE.md) 拆）。
- 下方「筆記索引」有對應列（主題、日期、一句結論、連結）。
- 結論是「要動手」→ [planning](../planning.md) 有接手列。

## 流程

1. **收集事實**：只讀不改，一條一則，附出處。
2. **對照現有能力**：這件事現在能不能做、靠什麼做。
3. **分類**：可直接做／有缺口／不值得做／需使用者驗證。
4. **產出 finding**：照下方筆記模板寫成 `notes/<主題>.md`；缺口進 [planning](../planning.md)，踩到的坑進 [common/gotchas](../common/gotchas.md)，需使用者驗證的進 [WAIT_USER](../../WAIT_USER.md)。
5. **登記**：在下方索引表加一列。

**不把未驗證的猜測寫成結論**——不確定就寫「缺什麼證據」，不要補完。

## 筆記模板

- **問題**：要回答什麼，一句話。
- **方法**：讀了哪些檔、跑了什麼指令。
- **發現**：一條一則事實，附出處。
- **結論**：直接回答問題；不確定就寫缺什麼。
- **來源**：檔案路徑＋行號、指令輸出、連結（外部 repo 標 URL 與評估日期）。

## 內容

| 檔案 | 內容 |
|------|------|
| [notes/](notes/) | 一主題一篇的調查筆記；索引見下表 |
| `archive/`（長出來才建）| 過時筆記封存（見 [STRUCTURE](../../STRUCTURE.md)）|

## 筆記索引

| 主題 | 日期 | 一句結論 | 筆記 |
|------|------|---------|------|
| dashi-ppt-skill | 2026-09-02 | **不 vendor，掛 submodule** `skills/external/`：AGPL 撞 CC0、素材禁散布、60 MB／426 檔大量超標 | [dashi-ppt-skill.md](notes/dashi-ppt-skill.md) |
| effective-html | 2026-09-02 | **收進 `skills/`**：MIT 相容、零執行期相依、17 檔 51 KB、分層路由與本 repo 同向 | [effective-html.md](notes/effective-html.md) |
| i-have-adhd | 2026-09-02 | **不 vendor，重寫**：把回覆風格規則用自己的話寫成 kernel 的 `reply-style.md` | [i-have-adhd.md](notes/i-have-adhd.md) |
| mattpocock/skills | 2026-09-02 | **借哲學不借檔**：吸收 context pointer／completion criterion 等寫法原則，不 vendor 檔案 | [mattpocock-skills.md](notes/mattpocock-skills.md) |
| 可組合單元 | 2026-09-02 | **補「中插契約」**進 STRUCTURE／TEMPLATE.workflow，把既有中插實踐寫明；狀態：待做 | [composable-units.md](notes/composable-units.md) |
| archify | 2026-09-02 | **不 vendor，掛 submodule** `skills/external/`：MIT 但是 Node 程式庫，最小子集 55 檔就 29 檔超標 | [archify.md](notes/archify.md) |
| Kami | 2026-09-02 | **不 vendor，掛 submodule** `skills/external/`：排版產品太重，vendor 不了 | [kami.md](notes/kami.md) |
| caveman | 2026-09-02 | **不 vendor**：5 條電報體規則併進 kernel `reply-style.md` | [caveman.md](notes/caveman.md) |
| stop-slop | 2026-09-02 | **不 vendor**：7 條去 AI 味規則併進 knowledge flavor 的 `writing.md` | [stop-slop.md](notes/stop-slop.md) |

## 交接

- 要動手 → [feature-dev](../feature-dev/README.md)；同一坑第二次 → [common/gotchas](../common/gotchas.md)；為什麼這樣選 → [decisions](../decisions.md)。
