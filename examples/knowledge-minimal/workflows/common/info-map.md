# info-map — 材料導航 index（哪份材料在哪、負責什麼）

[common/README](README.md)｜[INDEX](../../INDEX.md)

碰材料前先查這張表，只讀相關那幾份；動完再照維護鏈把表更新回去。與開發 flavor 的 code map **刻意對稱**：code map 描述程式碼結構，info-map 描述材料結構。碰材料的工作流（[digest](../digest.md) / [learn](../learn.md) / [organize](../organize.md) / [write](../write.md)）共用。

## 材料表

| 材料 | 位置 | 負責什麼 | 衍生產物 |
|------|------|---------|---------|
| 《みんなの日本語 中級 I・II》（課本，實體書）| 書本；進度對照 `plans/` 那份計畫的課次表 | 一條文法「怎麼接、什麼語氣、跟哪條容易混」的標準說明與例句 | `grammar/<文法>.md` |
| JLPT N3 出題基準單字表（PDF）| `vocab/_sources/n3-goi.pdf` | 該背哪些詞、詞性與標準讀音——單字有疑義以它為準 | `vocab/<主題>.md` |
| NHK News Web Easy（每日短新聞）| https://www3.nhk.or.jp/news/easy/ | 難度貼近 N3 的閱讀素材，附假名與語音 | `reading/<日期>-<標題>.md` |

## 維護鏈：材料 > info-map > 衍生產物

**優先級**（衝突或時間不夠時，依序保持一致）：材料 > info-map > 衍生產物（摘要、筆記、文章）。
**info-map 與材料衝突時以材料為準，立刻改 info-map。**

1. **動手前**：先讀本表找到相關材料，只讀清單裡的那幾份——不要整個資料夾翻。
2. **動手後**：新增／刪除了材料，或某份材料的職責顯著改變，必須同步更新本表。
3. 材料檔裡**不加**「對應 info-map」的註記（維護成本過高）；反向查找直接 grep 本檔。
4. 一輪 digest / learn 期間本表可暫時落後，**收尾前必須對齊**。
