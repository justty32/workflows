# decisions — 決策記錄（為什麼選 A 不選 B）

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

留下「為什麼」：git log 找得回改了什麼，找不回**為什麼放棄方案 C**。

**何時用**：在兩個以上可行方案裡選一個，且日後可能被問「當初為什麼」。
**何時不用**：只有一條路，或隨時可回頭的小事。決策過程要結構化評估 → knowledge 包的 decide 工作流，結論再落到這裡。

## Done when

- 下表新增一列，且「未選方案與原因」「前提」兩欄非空。

## 記錄（新的在上）

| 日期 | 決定 | 未選方案與原因 | 前提（變了就重看）|
|------|------|---------------|-----------------|
| 2026-09-02 | **本 repo 自己用非侵入式導入**：dev flavor 裝進 `wf/`，頂層只留 `AGENTS.md`／`CLAUDE.md`／`.claude/` | 標準佈局＝kernel 攤在根目錄，會跟 `template/`／`flavors/`／`tools/` 撞名撞視線，模板 repo 尤其不能這樣 | `wf/` 納入版控（不 ignore）；`wf-init` 的非侵入式改寫可靠 |
| 2026-09-02 | **`skills/` 進契約**：vendor 進來的 skill 受 `wf-lint` 檢查，導入後落在 `wf/skills/` | 放在契約外＝多一塊沒人檢查的區域，違反「機械兜底」 | `wf-lint` 的掃描範圍涵蓋 `skills/` |
| 2026-09-02 | **8 KB 上限對 `skills/` 不豁免** | 為單一外部 skill 開豁免＝拆掉 `wf-lint --self` 對全 repo 的機械保證，之後每個 skill 都會來要豁免 | 收進來的 skill 是 md 為主、拆得動 |
| 2026-09-02 | **外部大型 skill 不 vendor，改以 git submodule 掛 `skills/external/<name>/`**：上游原樣、授權歸上游、**不受 8 KB 契約**、`wf-init` 導入時不複製。已定案走這條：dashi-ppt-skill、archify、Kami | vendor（授權／體積／超標檔過不了 CI）；只在 README 放外部連結（評估白做、拿不到內容）；在 `skills/` 開「教你 `npx skills add`」的薄指引（模糊 vendor 契約，且等於背書執行期下載未審查程式碼）| submodule 是本 repo 自己的參考資產，不發給下游；`wf-init` 確實不複製它 |
| 2026-09-02 | **effective-html 收進 `skills/`** | 不收（MIT 相容、17 檔 51 KB、零執行期相依，沒有不收的理由）| 授權聲明留在 `skills/LICENSES/`；超標檔（`design-artifact/SKILL.md`）已拆 |
| 2026-09-02 | **i-have-adhd 與 caveman 不 vendor，用自己的話重寫成 kernel 的 `reply-style.md`**（caveman 的 5 條併入同一份）| vendor 原檔（要吸收的是回覆風格規則，不是檔案；重寫可繁中化並與鐵律對齊）；不收（規則本身有用）| `reply-style.md` 屬 kernel；`common/user.md` 的「回覆風格」欄改指向它 |
| 2026-09-02 | **stop-slop 的 7 條併進 knowledge flavor 的 `writing.md`**，不 vendor | vendor 原檔；另開新工作流（`writing.md` 本來就是這個題目的歸屬層，另開會分裂）| knowledge 包保留 `writing.md` |
| 2026-09-02 | **mattpocock/skills 借哲學不借檔** | 整包 vendor（會撞 8192 bytes 契約、混入另一套授權）| 哲學要點已寫進 investigation 筆記，之後落到 `STRUCTURE.md` 與 `TEMPLATE.workflow.md` |

細節與證據在對應的調查筆記：[investigation/notes/](investigation/notes/)（索引在 [investigation/README.md](investigation/README.md)）。

> 條目多到表格難讀就升級成 `decisions/` 資料夾、一決策一檔（照 [STRUCTURE](../STRUCTURE.md)）。
