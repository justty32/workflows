# testing — 跑測試 / 驗證

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

改完怎麼確認沒壞：有哪些驗證、各自的指令、哪些 agent 自己跑得了、哪些得交給使用者。

**何時用**：改完程式要驗、使用者說「跑測試」、重構前要記基準。
**何時不用**：環境還沒裝好、不知道指令哪來 → [dev-env](dev-env.md)；紅燈要往回查成因 → 讀 [common/code-map](common/code-map.md) 找到領域再回 [feature-dev](feature-dev/README.md)。

## Done when

- 下表標「改完必跑」的列指令回傳 0。
- 「誰跑」是使用者的列，已在 [WAIT_USER](../WAIT_USER.md) 各留一行（寫明跑什麼、什麼算過）。

## 驗證表

| 驗證 | 指令 | 誰跑 |
|------|------|------|
| 快速驗證（改完必跑）| `npm test` | agent |
| 完整驗證（commit 前）| `npm test && npm run build` | agent |
| lint / 型別 | `npm run lint` | agent |

「誰跑」只有兩種值：**agent**（本機跑得動）、**使用者 → WAIT_USER**（要實機、外部服務、帳號、付費、目視）。判不準就當後者。本專案目前每一列都是 agent 跑得動的——沒有實機、沒有外部服務。

## 測試分類

- 全部是 vitest 單元測試，放在 `tests/`，子目錄對應 `src/` 的三個領域（`tests/cli`、`tests/store`、`tests/commands`）。沒有環境差異，任何機器都跑得動全集。
- store 的測試不碰真實的 `~/.todo.json`：每個測試用 `mkdtemp` 開自己的暫存檔並以 `TODO_FILE` 指過去（見 [dev-env](dev-env.md) 的 env var 表）。
- 只想跑一個領域：`npx vitest run tests/store`。

## 交接

- 綠燈後回 [feature-dev](feature-dev/README.md) 接完剩下的步驟（code map → 文檔 → commit）。
- 同一個紅燈第二次撞到 → [common/gotchas](common/gotchas.md)。
