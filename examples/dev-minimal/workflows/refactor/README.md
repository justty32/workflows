# refactor — 重構 / 拆檔 / 整理結構

[WORKFLOWS](../../WORKFLOWS.md)｜[INDEX](../../INDEX.md)

只改結構、不改行為。方法在 [STRUCTURE](../../STRUCTURE.md)，本檔只管流程。

**何時用**：STRUCTURE 門檻超標（單檔過大、資料夾雜亂），或使用者要求整理。
**何時不用**：順手改了行為 → [feature-dev](../feature-dev/README.md)；還沒搞懂現況 → 先讀 [common/code-map](../common/code-map.md) 把該領域的檔看過再動手。

## Done when

- [testing](../testing.md) 的驗證指令綠燈，且與動手前結果相同。
- [common/code-map](../common/code-map.md) 中受影響領域的列已更新。

## 流程

1. 先跑 `npm test`、`npm run lint` 記下基準；紅的先修掉，別和重構混在一起。
2. 照 [STRUCTURE](../../STRUCTURE.md) 按職責拆／分類，不等分硬切。
3. 一次搬一塊（例：把 `src/commands/index.ts` 裡的一個子指令拆成一檔），搬完就跑 `npm test`。
4. 更新 [common/code-map](../common/code-map.md) 與所有指向舊路徑的 import 與文檔連結（`npm run build` 會抓到漏掉的 import）。

## 內容

| 檔案 | 內容 |
|------|------|
| [moving-things.md](moving-things.md) | 搬檔／改目錄名／拆 repo：六類會斷的東西與驗證程序 |

## 交接

- 結構就位後要加功能 → [feature-dev](../feature-dev/README.md)；為什麼這樣拆 → [decisions](../decisions.md)。
