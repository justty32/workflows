# user — 使用者偏好與確認邊界

[common/README](README.md)

agent 不用重猜的事。always-on 鐵律在 AGENTS.md，這裡是**這位使用者**的偏好——改了改這裡，不改鐵律。

| 項目 | 設定 |
|------|------|
| 語言 | 回覆與文件繁體中文；shell／python 註解可中可英，一檔之內一致 |
| 分支慣例 | `main` 為主線；成塊的改動開 feature 分支 `feat/…`、重構開 `refactor/…`，做完併回 main。**commit 由使用者決定**，agent 不自行 commit／push |
| 直接做、不用問 | 改文件、補測試、跑唯讀指令、跑 `wf-lint` 與 `pytest` |
| 一定先問 | 刪檔、改 `template/`／`flavors/` 的既有契約（版本戳、資料檔格式）、安裝依賴（push 與對外動作依鐵律 3）|
| 回覆風格 | 短、先結論；不要每段都 bullet。使用者問「要不要」時附**可執行判準**（門檻數字）與後果，讓他能改數字 |
| 時區 | Asia/Taipei |

領域詞彙常猜錯 → 開 `glossary.md`（見 [common/README](README.md)）。
