# dev-env — 開發環境、指令、外部工具

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

這台機器上要能開發需要什麼、怎麼裝、跑什麼指令；外部工具設定與 env var 也收在這裡。

**何時用**：fresh clone、換機器、裝不起來、忘了指令、要加一個外部工具或環境變數。
**何時不用**：驗證 / 測試怎麼跑 → [testing](testing.md)；程式碼慣例 → [common/conventions](common/conventions.md)。

## Done when

- 照「流程（fresh clone 後）」走完，`npm run build` 回傳 0。
- 下面兩張表沒有空欄。

## 流程（fresh clone 後）

1. `npm ci` 裝依賴（lockfile 已進 repo；不要用 `npm install`，會動到版本）。
2. `npm run build`：tsc 編到 `dist/`。
3. `npm test` 跑一次確認綠燈（這就是冒煙測試）。
4. 想在本機直接用 `todo` 指令：`npm link`（可選；不做也能用 `node dist/cli/index.js`）。

沒有 `.env`：本專案不需要任何必填 env var，資料檔位置有預設值。

## 指令表

| 做什麼 | 指令 | 備註 |
|--------|------|------|
| 安裝依賴 | `npm ci` | `package-lock.json` 一變動就重跑 |
| build | `npm run build` | tsc → `dist/`；改完 `src/` 沒 build 就跑 `dist/` 會跑到舊碼 |
| 跑起來 | `node dist/cli/index.js <子指令>` | 進入點 `src/cli/index.ts`；`npm link` 後可直接 `todo <子指令>` |
| lint / format | `npm run lint` | eslint + prettier check，不會自動改檔 |

驗證與測試指令不列這裡——連同「誰跑」一起在 [testing](testing.md)。

## 外部工具與 env var

| 名稱 | 用途 | 怎麼取得 / 設定 |
|------|------|----------------|
| `node` | 執行與建置 | v20 以上（`node -v` 確認）；系統套件或 nvm 皆可 |
| `TODO_FILE` | 覆寫資料檔位置 | 未設定時預設 `~/.todo.json`；測試都靠它指到暫存檔，不要在日常 shell 裡固定設它 |

本專案沒有需要帳號、付費、授權的相依，也沒有外部服務。日後真的加了：守鐵律 2（授權來源），並在 [WAIT_USER](../WAIT_USER.md) 記一行。

## 交接

- 環境就緒要開工 → [feature-dev](feature-dev/README.md)；先確認驗證跑得動 → [testing](testing.md)。
- 同一個裝機坑第二次撞到 → [common/gotchas](common/gotchas.md)。
