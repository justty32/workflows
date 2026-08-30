# workflows — 模板 repo 備忘（給 agent）

- 這是**模板 repo**，不是套用了模板的專案：`template/` 是 kernel、`flavors/` 是 flavor 包、`examples/` 是合併成品、`tools/` 是導入、檢查與資料檔腳本、`docs/` 是本 repo 自己的文件。人的入口 [README.md](README.md)；agent 幫人導入照 [IMPORT.md](IMPORT.md)。
- 改 kernel 或 flavor → 同步 README 的兩張內容表、[CHANGELOG.md](CHANGELOG.md)、`template/AGENTS.md` 尾端版本戳；`examples/` 受影響也要跟。
- flavor 包內的連結一律照**合併後**路徑寫（在本 repo 內點不到是預期的）；kernel 與 flavor 內部**不向上連 AGENTS.md**。
- 改完跑 `tools/wf-lint.sh --self`，0 BROKEN 才算完成。
