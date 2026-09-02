# dev-env — 開發環境、指令、外部工具

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

這台機器上要能開發需要什麼、怎麼裝、跑什麼指令；外部工具設定與 env var 也收在這裡。

**何時用**：fresh clone、換機器、裝不起來、忘了指令、要加一個外部工具或環境變數。
**何時不用**：驗證 / 測試怎麼跑 → [testing](testing.md)；程式碼慣例 → [common/conventions](common/conventions.md)。

## Done when

- 照「流程（fresh clone 後）」走完，`bash tools/wf-lint.sh --self` 回傳 0。
- 下面三張表沒有空欄；要使用者親自做的（帳號、授權、金鑰）在 [WAIT_USER](../WAIT_USER.md) 各佔一行。

## 流程（fresh clone 後）

1. `git clone` 後**不需要裝任何依賴**——本 repo 只用 bash ＋ python 標準庫（見 [conventions](common/conventions.md) 的相依規矩）。
2. 確認 `bash --version` 與 `python --version`（3.x）都跑得動；Windows 上 bash 走 **Git Bash 或 WSL**，不要用 cmd/PowerShell 直接跑 `.sh`。
3. 要跑測試才需要 `pytest`（`python -m pip install pytest`）；只改 md、只跑 lint 的話不用。
4. 冒煙：`bash tools/wf-lint.sh --self`，回傳 0 表示環境沒問題。

## 指令表

| 做什麼 | 指令 | 備註 |
|--------|------|------|
| 安裝依賴 | 無 | 只用 bash／coreutils／python 標準庫；要跑測試才另裝 `pytest` |
| build | 無 | 本 repo 沒有 build 步驟，md ＋ 腳本即成品 |
| 試導入（等同「跑起來」）| `bash tools/wf-init.sh --target <暫存目錄> --flavor dev` | **一定導到暫存目錄**，不要導到 repo 自己以外的地方；本 repo 自己那份已導在 `wf/` |
| lint / 檢查 | `bash tools/wf-lint.sh --self` | 模板端合併後檢查；本層自己的用 `bash wf/tools/wf-lint.sh --strict wf` |

驗證與測試指令不列這裡——連同「誰跑」一起在 [testing](testing.md)。

## 跨機 / 離線差異

| 環境 | 能跑 | 跑不了的 → 怎麼辦 |
|------|------|------------------|
| Windows ＋ Git Bash / WSL（主力機）| 全部 | — |
| GitHub Actions（ubuntu-latest）| 只跑 `bash tools/wf-lint.sh --self`（見 `.github/workflows/wf-lint.yml`）| **CI 目前不跑 pytest**——`tools/test_*.py` 只有本機跑得到，動 `tools/` 後要自己在本機跑過 |

全程離線可跑：沒有任何步驟需要連外。

## 外部工具與 env var

| 名稱 | 用途 | 怎麼取得 / 設定 |
|------|------|----------------|
| `bash` | 跑 `tools/*.sh` | Windows 裝 Git for Windows（Git Bash）或 WSL；Linux／macOS 內建 |
| `python` 3 | 跑 `tools/*.py` 與測試 | 系統 python3 即可，未鎖定最低版本（只用標準庫）|
| `pytest` | 跑 `tools/test_*.py` | `python -m pip install pytest`；只有要動 `tools/` 才需要 |
| env var | 無 | 本 repo 不讀任何環境變數，也沒有金鑰 |

需要帳號、付費、授權才能取得的：守鐵律 3（授權來源），並在 [WAIT_USER](../WAIT_USER.md) 記一行。

## 交接

- 環境就緒要開工 → [feature-dev](feature-dev/README.md)；先確認驗證跑得動 → [testing](testing.md)。
- 同一個裝機坑第二次撞到 → [common/gotchas](common/gotchas.md)。
