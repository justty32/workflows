# stop-slop — 去 AI 味清單，補進 writing.md 的空白

[investigation](../README.md)

- **問題**：外部 skill `hardikpandya/stop-slop`（抓「AI 味」英文散文的禁詞表／句式表／評分表）能不能整合進本 repo，尤其跟 `flavors/knowledge/workflows/common/writing.md` 的關係？

- **方法**：讀評估報告（`reports/kami-caveman-stopslop.md`）第三節，比對 stop-slop 各檔體積、授權、與 `writing.md` 現有「別寫成這樣（AI 味）」表的重疊範圍，抓出報告點名「值得借」的規則。

- **發現**：
  - 授權 **MIT**（Copyright 2025 Hardik Pandya），README 明講「Use freely, share widely」。
  - 體積很小，全部檔案都在 8 KB 內：`SKILL.md` 2,697 bytes、`references/phrases.md` 3,043 bytes、`references/structures.md` 5,389 bytes、`references/examples.md` 1,745 bytes；零腳本、零網路行為。
  - `writing.md` 現有的 AI 味表只有 8 條、偏中文口語套話（值得一提的是／賦能／抓手）；stop-slop 的清單細得多，且涵蓋 `writing.md` 完全沒有的**修辭結構**層級（不只是詞，是句型與段落節奏）。兩者重疊集中在「開場套話」「總結套話」「商業黑話」三類，其餘是本 repo 空白。
  - 值得借的 7 條規則（中文語境重寫，跳過英語特定的 Wh- 開頭句、-ly 副詞、em dash 等）：
    1. **二元對比反轉句是套路**：「不是因為 A，是因為 B」「問題不是 A，是 B」——中文一樣常見，直接講 B，不用鋪那段否定。
    2. **一路否定到揭曉答案的排比**：「不是 A……不是 B……是 C」——讀者不需要這個跑道，直接講 C。
    3. **無生命主詞做人類動作**：「這個決策浮現」「數據告訴我們」——決策是人做的、數據是人解讀的，找出那個人當主詞。
    4. **旁觀者敘述腔**：「沒有人設計過這個」「人們通常會」這種懸浮視角，改成把讀者拉進場景，或指名是誰。
    5. **三項並列清單是 AI 節奏的識別特徵**，改成兩項或拆開講。
    6. **表演性金句收尾**：「就這樣。就是這麼簡單。」這類段落結尾的表演腔，改成完整句子，相信內容本身。
    7. **有門檻的量化自檢**：送出前五維打分（直接／節奏／信任讀者／像不像人話／有沒有廢字），各 1–10 分，低於 35/50 就回頭改——這個「分數化整體檢查」的形式本身，比清單內容更值得借；`writing.md` 目前的自檢只有一行 grep 抓固定詞，沒有分數化機制。

- **結論**：**不 vendor**（MIT 進 CC0 仍需重寫解決授權），把上述 7 條規則**用自己的話併進既有 `flavors/knowledge/workflows/common/writing.md`**「別寫成這樣（AI 味）」表：規則 1–6 補進現有表格擴充詞句／句式覆蓋範圍，規則 7（量化自檢）另立一個小節，不新開檔、不獨立成 flavor。理由：stop-slop 體積小、零相依、純 markdown 清單，機械上沒有整合障礙，唯一要解決的是授權——重寫成中文語境版本後即完全 CC0；量化自檢的形式價值高於逐條清單本身，值得跟現有的一行 grep 自檢並存，作為更完整的送出前檢查。

- **來源**：https://github.com/hardikpandya/stop-slop （MIT License, Copyright 2025 Hardik Pandya）；評估日期：2026-09-02。
