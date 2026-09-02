# 回覆風格規範 — 借 i-have-adhd 的規則，不借它的載體

[investigation](../README.md)

- **問題**：外部 skill `ayghri/i-have-adhd`（MIT，把 agent 回覆重塑成 ADHD 讀者能行動的形狀）能不能整合進本 repo？整包搬、局部搬，還是只借想法？

- **方法**：讀團隊 C 的評估報告（`reports/team-c-adhd.md`），逐條比對外部 10 條回覆風格規則與本 repo 既有規範（`user.md` 回覆風格欄、`writing.md` AI 味表、`SESSION-LOG.md`、`Done when` 驗收文化），並檢查授權（CC0 vs MIT）、8 KB 上限、wf-lint／BIGLIST 等機械限制是否相容。

- **發現**：
  - 外部 skill 566 KB，核心 SKILL.md 僅 6953 bytes（英文），其餘是九種 runtime adapter、六國翻譯、hook、evals harness——本 repo 只用得到規則本體。
  - 10 條規則中與本 repo 實質重疊只有 2 條（第一行講動作 ≈ `user.md` 先結論；不要客套 ≈ `writing.md` AI 味表），其餘 6 條是本 repo 目前的空白，值得吸收。
  - 值得吸收、供未來寫 `reply-style.md` 取材的具體風格要點：
    1. 第一行直接給可執行動作，不鋪陳開場白。
    2. 多步驟任務用編號、一步一動作，步數壓到最少。
    3. 回覆結尾給一個兩分鐘內能做的下一步。
    4. 使用者岔題時抑制順便回答，另起一問處理。
    5. 每輪簡短重述目前進度（例如「5 步的第 3 步」）。
    6. 給時間估計要帶具體單位，不用含糊詞。
    7. 完成的事要明講出來，不要埋在冗長 recap 裡。
    8. 錯誤訊息用平述句陳述事實，不用「糟糕」「似乎有問題」等情緒詞。
    9. 清單超過 5 條就分「現在做／之後做」兩段，不要一次全列。
    10. 不要開場白、不要總結段、不要客套語。
  - 比 10 條規則更重要的是規則之外的兩節：**六個破例情境**（要求「解釋」時就好好解釋、危險動作先確認、debug 卡住時停手問一個診斷問題、真有歧義先問、規則會砍掉答案本身時任務優先、harness 系統提示優先於 skill）與**送出前的五項自檢**——沒這兩節，「先講結論」會退化成答案被砍到不能用。
  - always-on hook 機制設計乾淨（SessionStart 注入、失敗必 exit 0 不擋 session），但不建議搬：本 repo 已有 `AGENTS.md` 鐵律段做同樣的事，且每 session 硬注入約 7 KB 全文，正好和 README「薄入口、按需載入」的主張相反；作用域也不合（原機制的 flag 檔在使用者家目錄，本 repo 是 per-project）。
  - evals harness（加權 rubric、盲評重貼、隔離 baseline）方法論有價值，但要花錢、非確定性，跟 `tools/` 目前「零成本本地確定性檢查」的定位不合；報告建議先記進 `workflows/planning.md` 當未來 idea，不在這輪做。
  - 授權障礙是實質的：本 repo 為 **CC0 1.0**（公眾領域拋棄），外部為 **MIT**（要求保留著作權聲明）。逐句複製會讓 CC0 repo 混入帶條件的 MIT 區塊，破壞單一授權。規則與想法不受著作權保護，SKILL.md 的具體措辭與例子才受保護。

- **結論**：**不 vendor 原檔**，改用自己的話把 10 條規則、六個破例情境、送出前自檢重寫成 kernel 層的 `template/workflows/common/reply-style.md`（繁中，目標 < 6 KB），`user.md` 回覆風格欄改成指向它；hook、evals harness、skill 整包都不搬進本 repo。理由：(1) 授權——MIT 逐句抄進 CC0 repo 會破壞單一授權，重寫是唯一乾淨路徑；(2) 8 KB 硬限——中文字重約為英文三倍，直譯必爆表，重寫本來就得壓縮到約四成篇幅；(3) 本 repo 既有機制（`AGENTS.md` 鐵律、`writing.md` 被動參考）已覆蓋兩條，只需補其餘六條空白，不是重複造輪子；(4) hook 的「每 session 全文注入」與 evals harness 的「花錢＋非確定性」都和本 repo「薄入口、零成本本地確定性檢查」的既定定位衝突，維持現狀即可。

- **來源**：https://github.com/ayghri/i-have-adhd （MIT License, Copyright (c) 2026 Ayoub Ghriss）；評估日期：2026-09-02。
