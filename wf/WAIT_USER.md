# WAIT_USER — 等待使用者（只列 open）

[_index](_index.json)｜我的進度另記 [SESSION-LOG](SESSION-LOG.md)

需要**使用者親自**做 / 驗證 / 決定的事：實機測試、外部服務登入、環境變數、權限、付費、需帳號的下載、去開另一個 agent。agent 做到結構性驗證的極限，跨不過的那關記這裡。

條目格式：`- [工作流] 請使用者做什麼 → 做完我接著做什麼`，做完即刪。等別的 session / agent 不記這裡（判別表見 [workflows/_description](workflows/_description.json)）。

> 膨脹就拆：堆多了就開 `wait-user/` 按類別拆檔，本檔只留一張 `| 類別 | open | 清單 |` 導航表，每列連到 `wait-user/<類別>.md`（照 [structure](knowledge/structure.json)）。

## 待使用者項

- [planning] 請使用者確認：本 repo 之後幾乎不再更新，SESSION-LOG 裡凍結前的三條舊待辦（可組合單元未實作、精簡稽核待做、`wf-lint --exclude`）是不是都作廢 → 作廢我就刪掉那三條；要留的我標明留著的理由
- [testing] 請使用者決定要不要在 WSL 裝 pytest（`python3 -m pip install pytest`；這台沒有 `python` 指令）→ 裝好我跑 `python3 -m pytest tools -q`，綠了刪 SESSION-LOG 的 [testing] 條
