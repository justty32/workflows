# user — 使用者偏好與確認邊界

[common/README](README.md)

agent 每次不用重猜的事。always-on 鐵律在 AGENTS.md；這裡是**這位使用者**的偏好——改了就改這裡，不改鐵律。

| 項目 | 設定 |
|------|------|
| 語言 | 回覆與文件繁中；程式碼註解與 commit message 英文 |
| 分支慣例 | 單人開發，直接 commit main，不開 branch、不走 PR |
| 直接做、不用問 | 改文件、加／改測試、跑 `npm test` / `npm run lint` / `npm run build` 這類唯讀或本地指令 |
| 一定先問 | 刪檔、加新的 npm 相依、改 `package.json` 的 scripts、動使用者真實的 `~/.todo.json`（push 與對外動作依鐵律 2）|
| 回覆風格 | 短、先結論；不要每段都 bullet |
| 時區 | Asia/Taipei |

## 領域詞彙（長出來才建）

術語多到 agent 常猜錯時，開 `glossary.md`（`詞 | 意思 | 別名`）並在 [common/README](README.md) 加一列。
