# homework 5
## modularized_calculator.py:

evaluateのなかで括弧、掛け算割り算、足し算引き算の順に該当関数を用い、順番に処理した。
```
def evaluate(tokens,left,right): # ある式を演算してくれる関数
    tokens,right = eval_paren(tokens,left,right) # カッコ内を先に計算する、カッコ無しの式が返ってくる。abs.int,roundもここでまとめて処理
    eval_mul_div(tokens,left,right) # 割り算掛け算を処理
    ans = eval_add_sub(tokens,left,right) # 最後、足し算引き算をして答えを出してくれる
    return ans
```

### eval_paren:
  - カッコを見つけ出し、カッコ中の計算を回して、tokensからカッコを消去しておいてくれる関数。
  - eval_paren後はtokensにカッコが存在しなくなる。
  - 左カッコをstackに収納することで右カッコを検知した際に対応する左カッコのindexをget。
  - 対応するペア内の演算を、evaluateにぶちこむ(再帰)。カッコの内側を処理したら、カッコ以内の演算をtokensから抜き取り、代わりにカッコ内の計算結果を代入した。
    ```tokens = カッコの左側tokens + [{"type”:"NUMBER”,"number":カッコ内の計算結果} ] + カッコの右側tokens```
  - この前後でtokensの長さが変わること、indexもずれることへのケアが難しかった。

  - また、abs.int,roundには必ずカッコが付随することに注目し、eval_parenの条件分岐のなかでabs.int,roundを処理。abs,int,roundに付随するカッコとただのカッコでは、tokensの再生成の際のindexのずれが異なることにも注意した。

### eval_mul_div:
  - *か/を検知したらその前後のnumberを取ってきて演算し、右側のnumberに演算結果をメモしておく。
  - 左側のnumberは"type"を"NUMBER”からNoneにすることで無効化した。

### eval_add_sub:
 - 直前の演算子のtypeをis_plusというflagでメモしておく。
 - "type":"NUMBER”があればansにその値をaddまたはsubしてくれる。addかsubかの判断はis_plusを参照すればよい。
 - 最終的なansを返す。



## modularized_calculator_messy_draft.py: 

括弧内の計算をしたあと、括弧とその中の数式をtokensから抜く操作をすると計算量がかさむのではないかと考え、なんとかtokensのlist再生成を阻止し、そのままのlistを利用しようと試行錯誤した。具体的には、括弧内の演算結果をRPARENとLPARENに格納、以降の演算でかっこが出てきたら右かっこまでskipすることでそのままのtokenを用いて演算することができるようになった。**条件分岐が複雑で見づらいコードになってしまった。また、modularizeにも失敗している。**

### evaluate => 最初に掛け算割り算を計算、その後足し引き
#### 割り算掛け算
  - *と/の前後一つずつのnumberを用いて演算
  - 基本的には演算の一番右の数字のみを更新
  - 左の数字はnumber自体はそのまま、しかしtypeをNoneに変更することで無効化
  - カッコ導入につき、条件分岐
  - 前にカッコ演算がくる、つまり(3+9)＊8みたいなときは、)の数字を0にする <- 後の足し引きでのダブルカウントを防ぐ
  - 8*()みたいな時は、"(“と")"の数字どちらも更新する

#### 足し算引き算
  - type == NUMBERかRPARENの場合に演算をする
  - 演算の際はis_plusというflagを用い、直前に+があればTrue、-ならばFalseで足し引きの区別
  - "(“がきたら")”までスキップ、")”のnumberを参照する
  - カッコ内の演算がis_plusに影響しないようにした

### test => main関数の役割
  - "(“が来たら、対応する")”を探して、その中の数式をevaluate関数に入れる
  - 計算結果は"(“と")”に格納
  - 足し算する際は"(“はスキップされるので二重カウントを免れる
  - 掛け算割り算の時に必要になる（例えば、9*(8+7)みたいな時）ので"(“にも格納しておいた

### abs,int,roundへの対応　<-うまく行っていない
  - read_**を導入
  - こいつらは必ず直後に"(“を伴うはずなので、LPARENを先に検出し、その一つ前にABS,INT,ROUNDがないかチェック
  - あったらset()に格納 <- メモ
  - 対応するRPARENを見つけた時、いつもならRPARENに数字を格納するところを、abs,int,round操作を加える

### 問題点、課題
  - うまくmoduleできていない
  - evaluateの冒頭部分がぐちゃぐちゃ
  - LPARENが来たときにRPARENまで飛ばす動作がいちいち冗長
  - カッコ内の演算をどこに格納するのが良いのか結局曖昧

### 以下、メモ
- test()のなかに再帰とか入れちゃっている\
  ->evaluateのなかに入っているべき\
  ->なかに入ったら動くかどうか検討\

今のevalutateをinternal_evlにして、今のtestをevaluateにした方がいい
evaluateの**中で**absとかカッコの処理、条件分岐までしてあげる、丸っと全部処理するべき

