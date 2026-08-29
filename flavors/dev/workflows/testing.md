# testing — 跑測試 / 驗證

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

改完怎麼確認沒壞：有哪些驗證、各自的指令、哪些 agent 自己跑得了、哪些得交給使用者。

**何時用**：改完程式要驗、使用者說「跑測試」、重構前要記基準。
**何時不用**：環境還沒裝好、不知道指令哪來 → [dev-env](dev-env.md)；驗證紅了要查成因 → [investigation](investigation.md)。

## Done when

- 下表標「改完必跑」的列指令回傳 0。
- 「誰跑」是使用者的列，已在 [WAIT_USER](../WAIT_USER.md) 各留一行（寫明跑什麼、什麼算過）。

## 驗證表

| 驗證 | 指令 | 誰跑 |
|------|------|------|
| 快速驗證（改完必跑）| `{{npm test}}` | agent |
| 完整驗證（commit 前）| `{{npm run test:all}}` | agent |
| lint / 型別 | `{{npm run lint}}` | agent |
| {{要實機 / 外部服務的那類}} | `{{指令或步驟}}` | 使用者 → [WAIT_USER](../WAIT_USER.md) |

「誰跑」只有兩種值：**agent**（本機跑得動）、**使用者 → WAIT_USER**（要實機、外部服務、帳號、付費、目視）。判不準就當後者。

## 測試分類

> 〔導入判斷〕部分測試需要特殊環境（本機資產、外部服務、實機）→ 在驗證表補列，並在下方寫明離線可跑的子集（例：以標籤 `RequiresXxx` 區分，離線跑 `Category!=RequiresXxx`）。同步：`workflows/dev-env.md` 的「跨機 / 離線差異」表、`workflows/feature-dev/README.md` 的驗證步驟。

- {{分類方式與各環境能跑的子集}}

## 交接

- 綠燈後回 [feature-dev](feature-dev/README.md) 接完剩下的步驟（code map → 文檔 → commit）。
- 同一個紅燈第二次撞到 → [common/gotchas](common/gotchas.md)。
