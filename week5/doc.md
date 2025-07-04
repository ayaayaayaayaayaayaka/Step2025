# week5

## TSP - greedy + 2opt
### 概要
- greedyに2optを足した。
- 叶ら(2014)の2-optを参考にした。
- <img width="590" alt="スクリーンショット 2025-06-27 11 08 13" src="https://github.com/user-attachments/assets/6ea8f500-2b8d-44fb-af39-38e8add10ba6" />

### 手法
交差している項を探す。
- `if distance(x,x_next) + distance(y,y_next) > distance(x,y) + distance(x_next,t_next)`として立式。

交差を解き、新たなtourを作成。
- [x_next : y_next]について、順番を前後入れ替える。

### 出典
- 叶 驍強, 浜松 芳夫, 星野 貴弘. "巡回セールスマン問題におけるn-opt法適用の検討". 平成26年度日本大学理工学部学術講演会論文集, 2014, L-56.
URL, https://www.cst.nihon-u.ac.jp/research/gakujutu/58/pdf/L-56.pdf , (参照 2025-06-27).


# week6
### 概要
- greedy, 2opt, annealingを試した。
- これらをうまく組み合わせて、最も良いアルゴリズムを考えた

### 参考
https://qiita.com/take314/items/7eae18045e989d7eaf52

### files
||solver_multigreedy.py|solver_multigreedy2.py|solver_multigreedy3.py|
|------|----------------------|----------------------|----------------------|
|手法|多始点greedyで最も良い経路に対し、2opt|多始点greedyで全経路に対し2opt、その中で最も良い経路を採用|多始点greedyで最も良い経路に対し、2opt|
|annealing|なし|あり|あり|
|input4|11244.5|**10793.6**|11042.3|

 ### 結果
 annealingを加えたファイルでは、annealingによる解の改善は見られなかった。

### 考察
multigreedy + 2optでlocal最適解を出した。
このlocal最適解をannealingしたが、うまく山を越えられず、global最適解に至らなかった。
