# CHANGELOG — kernel 變動記錄

每次 kernel（`template/`）或導入契約變動記一節：改了哪檔、**既有專案要不要跟**。本檔只留**每版摘要與去向**，完整條列拆在 `docs/`——變動記錄只會長不會短，留在母檔一定會撞 8 KB 上限。版本戳在 `template/AGENTS.md` 尾端 `<!-- wf-kernel vX.Y (日期) -->`，導入後 `grep wf-kernel AGENTS.md` 查自己是哪一版。kernel-owned / project-owned 分類見 [IMPORT.md](IMPORT.md)。

## v0.5.1 (2026-09-02)

檢查器的修正版，**工作流內容沒動**。四個 bug：`broken` 計數溢位、掃描沒排除 submodule／`vendor/`／`reference(s)/`、`OVERSIZE` 範圍、連結目標 percent-encoding 誤判（存在的檔被重複報 `BROKEN`）。`tools/` 因為 8 KB 上限拆成多檔（新增 `wf-lint-checks.sh`、`tabledb_table.py`、`tabledb_fmt_expand.py`、`fix_moved_links_scan.py`，公開用法不變）——**拆完彼此相依，要跟就整包覆蓋 `tools/`**。另加 `workflows/tidy/gotchas.md` 的「執行環境」段。

**完整條列與升級判準（含怎麼查自己是哪一版）**：[docs/CHANGELOG-v0.5.1.md](docs/CHANGELOG-v0.5.1.md)。

## v0.5 (2026-08-30)

來源專案一輪整理長出的通用做法回抽進 kernel：tidy 升成資料夾並附踩坑與管理線簡報、`WORKFLOWS.md` 加「可以跳流程」、`WAIT_USER` 拆法定死、`wf-lint` 加 `#錨點` 檢查；dev 包補 moving-things（搬檔六類斷裂）、「綠燈不等於有檢查」、真相層優先序，以及 analysis／patch 兩個可選工作流。

**完整條列**：[docs/CHANGELOG-v0.5.md](docs/CHANGELOG-v0.5.md)。

## v0.4.1 (2026-08-30) 與更早

見 [docs/CHANGELOG-history.md](docs/CHANGELOG-history.md)。
