# CHANGELOG — kernel 變動記錄

每次 kernel（`template/`）或導入契約變動記一節：改了哪檔、**既有專案要不要跟**。本檔只留**每版摘要與去向**，完整條列拆在 `docs/`——變動記錄只會長不會短，留在母檔一定會撞 8 KB 上限。版本戳在 `template/AGENTS.md` 尾端 `<!-- wf-kernel vX.Y (日期) -->`，導入後 `grep wf-kernel AGENTS.md` 查自己是哪一版。kernel-owned / project-owned 分類見 [IMPORT.md](IMPORT.md)。

## 未發布

wf-lint 改為**可選**：預設不跑（很花時間），大量搬檔後擔心連結壞掉或使用者要求才跑。改的是規矩文字——`tidy/` 的 Done when／manager-brief／gotchas、`refactor/moving-things`、各 flavor README 的「改完跑」、`IMPORT.md`／`README.md`／`docs/non-invasive-import.md` 的導入驗收；`tools/wf-lint.sh` 與其測試不動（模板自己的 CI 仍跑 `--self`）。兩個 `examples/` 同步。來源：aos。**既有專案要跟**：`workflows/tidy/` 整夾是 kernel-owned，直接覆蓋；其餘照上列自行改成可選。

tidy 加原則 5「**內容精簡**」：新增 `workflows/tidy/content-trim.md`——檔內只留現行結論、寫精簡；決策過程、改過幾版、為什麼這樣定、作廢方案、演變史都刪，靠 git 歷史找；使用者原文逐字留（被使用者後來的話推翻的舊原文可刪），附原文認法與 `LOST` 檢查指令；日誌每日檔、報告、`archive/`、`SESSION-LOG`／`WAIT_USER` 不適用，會議／評審的場次紀錄適用。`tidy/README.md` 改五條原則、Done when 加原文檢查、精簡另開一條線分開 commit；`tidy/gotchas.md` 照新規則精簡。對齊：`STRUCTURE.md` 分層原則 4 改成「決定記 decisions、檔內只留現行結論」，新增「**日誌寫法**」一節（每日檔每條一行＋連到結論所在處、總目錄每天一句「這天定下了什麼」、月結收成月摘要並封存每日檔），「工作流的統一形式」補兩句（入口檔下次動到再補齊、單檔型撐大照四級成長升級），並照 content-trim 刪掉說明句；`decisions.md` 欄位「未選方案與原因」改成「來源（使用者原文或誰定的）」，不再記比較過的方案與理由（knowledge 包 `decide.md` 的 Done when、`planning.md` 交接、`SESSION-LOG.md` 指向跟著改）；`WORKFLOWS.md` tidy 觸發加「只留結論」。兩個 `examples/` 同步。來源：aos 導入回饋。**既有專案要跟**：`workflows/tidy/` 整夾與 `STRUCTURE.md` 是 kernel-owned，直接覆蓋；`decisions.md` 是 project-owned，表頭自己改（舊列的理由欄可照 content-trim 精簡或留著）。

lint：加 **project-local hook**——掃描目錄下有 `<dir>/wf/tools/wf-lint-local.sh` 就以 `bash <它> <dir> <strict>` 執行，它自己印 finding 行，結束碼非 0 計入新計數器 `local=N`（SUMMARY／TOTAL 都列），比照 biglist **只在 `--strict` 算失敗**；`--self`（模板 repo 自檢）不跑。那支是 project-owned，專案自訂檢查從此不必改 kernel 檔、也不會被 `tools/` 整包覆蓋清掉（來源：moddings/skyrim 要把自家 `brief_lint.py` 接進 wf-lint）。測試拆出 `test_wf_lint_local.py`（`test_wf_lint.py` 已到 8 KB 上限）。**既有專案要跟**：`tools/` 整包覆蓋（本 repo 自用的 `wf/tools/` 已同步），hook 本體各專案自理。

multi-agent `workflows/team-model.md` 二、三節兩張預填表換成 2026/09/25 的模型清單：Opus 5.5 全面 A（不再分軟工／其他）、gpt-6-astra／gpt-6-sol 同放 A、gpt-6-luna D、gpt-terra 移除；消耗速度沿用「GPT 下移兩級」。表仍 project-owned，**既有專案不必跟**，自己的表自己改。

lint：git repo 內 `.gitignore` 命中的路徑不掃（`list_owned_files` 與 `check_anchors.py` 都過一次 `git check-ignore`；tracked 檔照掃；非 repo、或明指的掃描根本身被 ignore 時照舊）——對整個 repo 跑 `wf-lint.sh .` 之前會掃進 ignore 掉的外部 clone，報上百筆假 RESIDUE／BIGLIST。測試加在 `test_wf_lint_scope.py`。來自 moddings/skyrim 導入回饋。**既有專案要跟**：`tools/` 整包覆蓋（本 repo 自用的 `wf/tools/` 已同步）。

lint：`list_owned_files`／`list_oversize_files` 的 prune 清單補 `.venv`／`venv`（Python 虛擬環境）不下鑽——`uv`／`venv` 專案根目錄下的 `.venv/lib/.../site-packages/**/*.md` 之前會被當成專案檔掃進去，報一堆假 BROKEN／OVERSIZE。來自 llmkit 導入回饋。**既有專案要跟**：`tools/` 整包覆蓋（本 repo 自用的 `wf/tools/` 已同步）。

lint：`done/`／`superseded/` 與放信的 `inbox/`（頂層＋`done/`；`workflows/inbox/` 照掃）比照 `archive/` 封存不下鑽——信件是寄件原文不該改，BIGLIST／壞連結／錨點都不掃，`inbox_pending` 照數；STRUCTURE archive 規則補一句；測試拆出 `test_wf_lint_scope.py`（掃描範圍）。來自 paper_readings、engineer_study 導入回饋。**既有專案要跟**：`tools/` 整包覆蓋（本 repo 自用的 `wf/tools/` 已同步），engineer_study 可拿掉自家 `lint.sh` 過濾 `^BIGLIST inbox/done/` 的包裝。

## v0.6 (2026-09-02)

`skills/` 進契約：新增頂層 agent skill 資料夾，與 `template/`／`flavors/` 平行，8 KB 上限一體適用。8 個技能——本 repo 自有兩個（CC0）＋ vendor 自 effective-html 六個（MIT），本 repo 因此變**混合授權**，授權全文在 `skills/LICENSES/`。不 vendor 的產品向外部技能（`dashi-ppt-skill`、`archify`）改以 git submodule 掛在 `skills/external/`，授權維持上游、豁免 8 KB 契約，`--skills`（含 `all`）不觸碰它，要用自己 `git submodule update --init`。`wf-init.sh` 加 `--skills a,b|all`：複製到 `<wfroot>/skills/`，並在專案根 `.claude/skills/<name>/` 產轉址 `SKILL.md` 供 Claude Code 自動發現；skills 可選、不進 `WORKFLOWS.md` 派發表。`wf-lint.sh --self` 加對 `skills/` 的連結／錨點檢查（BIGLIST／`$fmt` 檢查跳過該目錄）。kernel 新增 `workflows/common/reply-style.md`（對話回覆風格），`common/README.md` 導覽表與 `user.md` 回覆風格欄同步指向它。另**文檔精簡**（工作流語意沒動）：kernel 的 `tidy/README.md` 不再重述 STRUCTURE、`common/gotchas.md` 與 `common/user.md` 補齊 TEMPLATE 段落；七個 flavor README 的通用導入步驟改連 `IMPORT.md`。既有專案要跟的只有 kernel 那幾檔。

**完整條列與升級判準**：[docs/CHANGELOG-v0.6.md](docs/CHANGELOG-v0.6.md)。

## v0.5.1 (2026-09-02)

檢查器的修正版，**工作流內容沒動**。四個 bug：`broken` 計數溢位、掃描沒排除 submodule／`vendor/`／`reference(s)/`、`OVERSIZE` 範圍、連結目標 percent-encoding 誤判（存在的檔被重複報 `BROKEN`）。`tools/` 因為 8 KB 上限拆成多檔（新增 `wf-lint-checks.sh`、`tabledb_table.py`、`tabledb_fmt_expand.py`、`fix_moved_links_scan.py`，公開用法不變）——**拆完彼此相依，要跟就整包覆蓋 `tools/`**。另加 `workflows/tidy/gotchas.md` 的「執行環境」段。

**完整條列與升級判準（含怎麼查自己是哪一版）**：[docs/CHANGELOG-v0.5.1.md](docs/CHANGELOG-v0.5.1.md)。

## v0.5 (2026-08-30)

來源專案一輪整理長出的通用做法回抽進 kernel：tidy 升成資料夾並附踩坑與管理線簡報、`WORKFLOWS.md` 加「可以跳流程」、`WAIT_USER` 拆法定死、`wf-lint` 加 `#錨點` 檢查；dev 包補 moving-things（搬檔六類斷裂）、「綠燈不等於有檢查」、真相層優先序，以及 analysis／patch 兩個可選工作流。

**完整條列**：[docs/CHANGELOG-v0.5.md](docs/CHANGELOG-v0.5.md)。

## v0.4.1 (2026-08-30) 與更早

見 [docs/CHANGELOG-history.md](docs/CHANGELOG-history.md)。
