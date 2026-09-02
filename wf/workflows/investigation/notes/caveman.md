# caveman — 電報體壓縮術，挑幾條併進 reply-style.md

[investigation](../README.md)

- **問題**：外部 skill `JuliusBrussee/caveman`（把 agent 回覆壓成電報體的極簡溝通模式）能不能整合進本 repo，尤其跟正在建的 `reply-style.md` 是什麼關係？

- **方法**：讀評估報告（`reports/kami-caveman-stopslop.md`）第二節，檢查 `LICENSING.md` 的逐目錄授權切分、`skills/caveman/SKILL.md` 體積、與 `reply-style.md` 的手法差異，抓出報告點名「值得借」的規則。

- **發現**：
  - 授權是雙軌的：根 `LICENSE` 為 MIT，但 Engine 相關目錄（`engine/`、`proxy/`、`cacheengine/` 等）另走 BSL 1.1（2030-06-21 或首次發布滿四年才轉 Apache-2.0）；`LICENSING.md` 明講 **`skills/` 整個目錄固定 MIT**，不受 BSL 影響。
  - `skills/caveman/SKILL.md` 只有 **6518 bytes**，在 8 KB 內；本體不大，問題在授權（MIT）而非體積。
  - 它是 `reply-style.md` 同賽道的更激進版本：不只「先講結論、不客套」，而是逐詞計算 token 成本，砍冠詞、轉折詞、甚至因果連詞——手法（砍語法成分省 token）跟 `reply-style.md`（結構清楚、動作優先）是兩種不同優化目標，中文語境也不適合直接套「砍冠詞」這類英語特定規則。
  - 值得借的 5 條規則（原文用自己的話重寫）：
    1. **邊界要講清楚**：精簡風格只管當下對話回覆，不管寫進檔案的內容——commit 訊息、程式註解、文件、issue/PR 內文一律照常規寫；`reply-style.md` 該把「commit/PR/issue 內文不適用」點名寫出來。
    2. **工具呼叫別插旁白**：呼叫前只在需要澄清、警告危險動作、或消歧義時才講話，呼叫後直接給下一步或結論，不要「現在我要執行 X」這種播報。
    3. **連續卡關的處理**：caveman 沒有這條——這正是 `reply-style.md` 已有的「debug 卡在原地打轉就停手問診斷問題」例外，此點確認本 repo 已比它完整，不用借。
    4. **縮寫要真的省字數才用**：分詞器眼裡縮寫（cfg/impl/req）跟全字通常等長，硬縮反而讀者更難懂；轉譯成中文語境是「不要為了『看起來精簡』而拆短句到語意不清，精簡的前提是不折損可讀性」。
    5. **語言保真**：使用者用什麼語言就回什麼語言，壓縮的是風格不是語言本身；本 repo 定位繁中優先，這條實用性較低，可簡化成一句「不因求精簡而混用語言」。

- **結論**：**不 vendor**（MIT 進 CC0、且是產品化 skill 矩陣，跟本 repo 定位不合），把上述 5 條規則**用自己的話併進既有 `template/workflows/common/reply-style.md`**（重寫增補，不抄英文原文），不新開檔、不 vendor 周邊 skill／壓縮引擎。理由：核心精神（先講結論、不開場白、報錯直述）跟 `reply-style.md` 本來就重疊，值得吸收的是它划清的邊界（規則 1）與工具呼叫節奏（規則 2），至於逐詞砍語法成分那套手法本身不適合中文語境、也超出 `reply-style.md` 的優化目標，不整包搬。

- **來源**：https://github.com/JuliusBrussee/caveman （雙授權：根目錄 MIT／Engine 相關目錄 BSL 1.1，`skills/` 目錄固定 MIT）；評估日期：2026-09-02。
