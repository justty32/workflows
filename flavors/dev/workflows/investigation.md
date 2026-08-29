# investigation — 調查 / 解讀外部系統 / 可行性

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

只讀不改，查清楚「這怎麼運作／可不可行」，產出可歸檔的筆記。

**何時用**：看懂外部系統或別人的碼、評估可行性、查 bug 成因。
**何時不用**：已知道怎麼改 → [feature-dev](feature-dev/README.md)；只搬結構 → [refactor](refactor.md)。

## Done when

- `{{筆記位置，如 docs/investigations/}}<主題>.md` 存在，且下列五段非空。
- 結論是「要動手」→ [planning](planning.md) 有接手列。

## 筆記模板

- **問題**：要回答什麼，一句話。
- **方法**：讀了哪些檔、跑了什麼指令。
- **發現**：一條一則事實，附出處。
- **結論**：直接回答問題；不確定就寫缺什麼。
- **來源**：檔案路徑＋行號、指令輸出、連結。

## 交接

- 要動手 → [feature-dev](feature-dev/README.md)；同一坑第二次 → [common/gotchas](common/gotchas.md)。
