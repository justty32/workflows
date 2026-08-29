# conventions — 程式碼慣例（碰原始碼的工作流共用）

[common/README](README.md)｜[INDEX](../../INDEX.md)

碰原始碼的工作流（feature-dev / refactor）共用這套規矩：**寫碼時要遵守什麼**。哪個檔負責什麼領域、測試在哪 → [code-map](code-map.md)；結構整理原則 → [STRUCTURE](../../STRUCTURE.md)。

## 慣例

| 項目 | 規矩 |
|------|------|
| 檔案拆分 | 按領域拆：`src/cli` 只解析與輸出、`src/store` 只讀寫、`src/commands` 一個子指令一檔；單檔超過 300 行就照 [STRUCTURE](../../STRUCTURE.md) 檢視 |
| 命名 | 檔名 kebab-case（`add-task.ts`）、型別 PascalCase、函式 camelCase；子指令的檔名＝使用者打的子指令名 |
| 註解語言 | 程式碼註解與 commit message 用英文，文件與對話用繁中 |
| 型別單一出處 | `Todo` 與存檔 schema 只定義在 `src/store/types.ts`，其他檔一律 import；不用 `any`（eslint 會擋） |
| 相依 | runtime 維持零外部相依（只用 Node 內建模組）；要加套件先問，版本鎖進 `package-lock.json` |
