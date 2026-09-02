# testing — 跑測試 / 驗證

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

改完怎麼確認沒壞：有哪些驗證、各自的指令、哪些 agent 自己跑得了、哪些得交給使用者。

**何時用**：改完程式要驗、使用者說「跑測試」、重構前要記基準。
**何時不用**：環境還沒裝好、不知道指令哪來 → [dev-env](dev-env.md)；驗證紅了要查成因 → [investigation](investigation/README.md)。

## Done when

- 下表標「改完必跑」的列指令回傳 0。
- 「誰跑」是使用者的列，已在 [WAIT_USER](../WAIT_USER.md) 各留一行（寫明跑什麼、什麼算過）。

## 驗證表

| 驗證 | 指令 | 誰跑 |
|------|------|------|
| 模板端契約（改完必跑）| `bash tools/wf-lint.sh --self` | agent |
| `tools/` 單元測試（動到腳本就跑）| `python -m pytest tools -q` | agent |
| 本層工作流（改完 `wf/` 就跑）| `bash wf/tools/wf-lint.sh --strict wf` | agent |

「誰跑」只有兩種值：**agent**（本機跑得動）、**使用者 → WAIT_USER**（要實機、外部服務、帳號、付費、目視）。判不準就當後者。**本 repo 目前沒有 agent 跑不動的驗證**——全部離線、無外部服務；唯一得靠人的是「導入到真專案之後讀起來順不順」，那不是機械驗證，走使用者回饋。

## 測試分類

- `fast`：`python -m pytest tools -q`——`tools/test_*.py` 的單元測試，每次小改 `tools/` 都跑。
- `contract`：`bash tools/wf-lint.sh --self`——把 kernel 與**每一個 flavor 合併後**才檢查連結、錨點、8192 bytes、條列與殘留。改 `template/` 或 `flavors/` 一定跑這個；flavor 包單獨看的 BROKEN 不算數（見 [common/conventions](common/conventions.md)）。
- `full`：commit 前三個都跑（fast ＋ contract ＋ `bash wf/tools/wf-lint.sh --strict wf`）。
- `external`：無。

**注意 CI 只跑 `contract`**（`.github/workflows/wf-lint.yml` 只有 `wf-lint.sh --self`），`fast` 沒有 CI 兜底，動 `tools/` 後必須本機跑過——見 [dev-env](dev-env.md) 的跨機表。

## 綠燈不等於有檢查

**一道檢查通過，可能是因為它根本沒在檢查。** 這不是假設：曾在一天內抓到四個恆真檢查——結構稽核、「鎖已釋放」的檢查指向已刪目錄、連結檢查器走到子 repo 指標就停、自製字元偵測。

**規則：新增或修改一道檢查時，要證明它能變紅。** 先餵一個**應該被擋**的輸入，確認 exit ≠ 0；再餵正確的輸入，確認 exit = 0。**沒做過這個雙向驗證的綠燈不算證據。**

兩個推論：檢查器的**涵蓋範圍要跟著結構走**——拆出子 repo、搬走目錄之後，回頭確認檢查器還看得到那些地方（見 [refactor/moving-things.md](refactor/moving-things.md)）；**靜態全過不等於畫面上是對的**，方框、亂碼、截斷、手感只有人眼看得出來，這類記到 [WAIT_USER](../WAIT_USER.md)，不要自己宣稱通過。

## 交接

- 綠燈後回 [feature-dev](feature-dev/README.md) 接完剩下的步驟（code map → 文檔 → commit）。
- 同一個紅燈第二次撞到 → [common/gotchas](common/gotchas.md)。
