# malloc_challenge
## やったこと
- best_fit
- worst_fit
- best_fit + right_merge

## 結果
||Challenge1 Time|Challenge1 Utilization|Challenge2	Time|Challenge2	Utilization|	Challenge3 Time|	Challenge3 Utilization|		Challenge4 Time|		Challenge4 Utilization|		Challenge5	Time|		Challenge5	Utilization|
|--|--|--|--|--|--|--|--|--|--|--|
|best_fit|933|70	|665	|40	|792	|51	|5732	|72	|3822	|75|
|worst_fit|961|70|695|40|42991|4|737769|7|448281|7|
|best_fit + right_merge|996|70	|739	|40	|804	|51	|2262	|77	|1642	|79|

## 考察
- worst_fitは時間的にもutilization的にも効率が悪かった。
- right_mergeをしたら、utilizationが上がった。

## メンターさんと話したこと
-  隣であることが分かりさえすればmergeはできる
-  アドレスごとにsortするのもあり、
-  sortせずに全部探索して一つ一つ見てもできる
-  いつsortするかによって変わる
-  常にsortした状態を維持するのか、入らない時だけにsortするのか、utlizetionが幾つになったときにsortするのかetc
-  特定のタイミングのみsortするという方法が考えられる
-  free binだったらリストがいくつかできてしまう、
-  mergeしたら違うbinの中身に入れなければならなくなるかも
-  mergeだけする、free list binだけやる、の後に両方実装した方がわかりやすい
-  いきなり両方は多分複雑
