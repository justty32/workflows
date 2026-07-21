# 非侵入式導入：只在頂層留兩個入口，其餘收進 `wf/`

把這套模板引進**既有專案**時，若直接把 kernel 的佈局攤在專案根目錄，頂層會一下子冒出一堆 `.md`（`SESSION-LOG.md`、`DEV-GUIDE.md`、`WORKFLOWS.md`、`INDEX.md`…），讓原專案的目錄結構瞬間變得很雜亂。

**非侵入式佈局**解決這個問題：頂層只留 agent 的兩個入口檔，其餘全部收進單一子資料夾。

## 目標佈局

```
你的專案/
  AGENTS.md          ← 唯一留在頂層的入口（薄路由器）
  CLAUDE.md          ← 相容轉址，指回 AGENTS.md
  wf/                ← 模板其餘全部收進來（名稱自取：wf、.workflow、ops…）
    WORKFLOWS.md
    INDEX.md
    DEV-GUIDE.md
    SESSION-LOG.md
    WAIT_USER.md
    inbox/
    workflows/
  ...（你專案原本的檔案，維持不動）
```

## 相對於標準導入的差異

標準導入流程見 [README](README.md)。非侵入式佈局只差兩點：

1. 複製 kernel 時**把 `AGENTS.md`、`CLAUDE.md` 留在專案根目錄**，其餘（`WORKFLOWS.md`、`INDEX.md`、`DEV-GUIDE.md`、`SESSION-LOG.md`、`WAIT_USER.md`、`inbox/`、`workflows/`）放進 `wf/`。
2. **修正頂層兩檔的向下連結**：`AGENTS.md` / `CLAUDE.md` 原本指向同層的 `WORKFLOWS.md`、`INDEX.md` 等，現在要改成 `wf/WORKFLOWS.md`、`wf/INDEX.md`。`wf/` 內部彼此的相對連結不受影響（整包一起搬，相對關係不變）。

## 是否 git ignore

依需求決定：若不想把這套工作流納入專案版控，就把 `AGENTS.md`、`CLAUDE.md`、`wf/` 全部加進 `.gitignore`；想納入就不 ignore。

```gitignore
/AGENTS.md
/CLAUDE.md
/wf/
```
