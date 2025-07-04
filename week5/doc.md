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
- greedy, 2opt, ACO(ant colony optimization), GA(genetic algorithm)の4手法を試した。
- これらをうまく組み合わせて、最も良いアルゴリズムを考えた

#### ACOについて
フェロモンを介したアリの群行動にヒントを得たアルゴリズム。

#### GAについて
生物の進化にヒントを得たアルゴリズム。

### greedy + 2opt + 