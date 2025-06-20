import sys
import collections
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {} # IDとtitleを紐付け

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {} # IDとリンクを紐付け

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ") #　空白が二つ以上あったらやばくないか？ -> なさそう
                id = int(id)
                assert not id in self.titles, id # assert <条件式>,<条件が満たされなかった場合に表示するメッセージ>
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        self.inverted_titles = {}
        for id in self.titles:
            title = self.titles[id] 
            self.inverted_titles[title] = id

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

        # self.linksでリンクがないページが追加されているかどうかチェックすべき


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    # find_shortest_path() 関数を書いて、あるページから別のページへの最短経路を出力してください😀
    # 「渋谷」から「小野妹子」にどうたどり着く？
    # ヒント：
    # BFS に工夫を入れて最短経路を出せるようにする
    # collections.deque を使うとスタックやキューが作れます
    # 30 行程度で書けます😀

    def find_shortest_path(self, start, goal):
        # たとえば、pathが一直線だったら
        # 時間も空間も伸びて、n^2になる
        # "pathを復元する"
        # 距離を計算してそれを保存する -> O(N + E)
        # 終点から逆を辿る
        # 変の向きを逆にしたグラフを考え、最短距離-1をまたかんがえ、これを繰り返すと元に戻れる
        # 行きも帰りもO(N+E)で実行できる
        queue = deque() # 探索中のノード集合
        seen = set() # 訪問済みid集合
        start_id = self.inverted_titles[start] # start titleをidに
        goal_id = self.inverted_titles[goal] # goal titleをidに
        queue.append([start_id]) # 始点をqueueに追加
        seen.add(start_id) # 始点には訪問済み
        while len(queue):
            curr = queue.popleft() # 探索ノードを取り出す
            if curr[-1] == goal_id: # goal判定
                path = [self.titles[id] for id in reversed(curr)] # 始点から終点へと並び替え
                print(f"shortest path : {path}")
                return
            for des in self.links[curr[-1]]: # ノードの行き先を調べる
                if not des in seen:
                    new_path = curr.copy() # queueに格納する新たなlist
                    # listの長さぶん時間がかかる
                    new_path.append(des) # listの末尾に行き先を追加
                    queue.append(new_path) # list格納
                    seen.add(des) # 訪問済みidに追加
        print("not found")
        return
    


    # Homework #2: Calculate the page ranks and print the most popular pages.
    # 正しさの確認方法
    # ページランクの分配と更新を何回繰り返しても「全部のノードのページランクの合計値」が一定に保たれることを確認してください
    # 一定にならない場合何かが間違ってます！

    # Large のデータセットで動かすためには O(N + E) のアルゴリズムが必要です
    # ページ数：N = 2215900
    # リンク数：E = 119006494

    # ページランクの更新が「完全に」収束するのは時間がかかりすぎるので、更新が十分少なくなったら止める

    # 収束条件の作り方の例：
    # ∑(new_pagerank[i] - old_pagerank[i])^2 < 0.01

    def find_most_popular_pages(self):
        pagerank = {} # {id:pagerank}
        new_pagerank = {} # 初期化
        for id in self.links: # O(N)
            pagerank[id] = 1.0 # 初期化
        memo = {}
        N = len(self.links) # Node数
        loop = 0 # loopカウント
        diff = 10000
        result = [] 
        sum_pageranks = 0

        while diff > 0.01: # 常にTrueならTrueって書けば良い
            res = 0 # 全ノード共通の足し算項、初期化
            diff = 0 # pagerankがループ一回でどれくらい更新されたか、初期化
            sum_pageranks = 0 # pagerankの総和、初期化
            # for id in self.links: # O(N)
            #     memo[id] = 0 # 初期化
            for id in self.links: # O(N)
                new_pagerank[id] = 0  # 初期化
            result = [] # 結果メモ用リスト
            for id in self.links: # O(N+E)　<- 今のコードであれば正しい　新し区それぞれ足し始めたらN^2 + E
                if len(self.links[id]) == 0: # 行き止まりノード
                    res += pagerank[id] / N # あとで全員一斉に更新するようメモ
                else:
                    res += pagerank[id] * 0.15 / N # 0.15 -> あとで全員一斉に更新するようメモ
                    add = pagerank[id] * 0.85 / len(self.links[id]) # 0.85 -> 近所に分ける
                    for neighbor in self.links[id]:
                        new_pagerank[neighbor] += add # 該当ノードのpagerankのみ更新
            for id in self.links: # O(N)
                diff += (new_pagerank[id] - pagerank[id] + res ) ** 2 # 誤差項
                pagerank[id] = new_pagerank[id] + res   # 共通項を一斉に更新
                sum_pageranks += pagerank[id] # 総和計算
                result.append((pagerank[id],id)) 
            loop += 1
            print(f"{loop}loop, diff : {diff}") # 途中経過(ループ数,誤差)表示

        
        print("-----------------CONVERGED!-----------------")
        print(f"sum ( == {N} であれば良い): {sum_pageranks}") # sum == Nになるはず、妥当性チェック
        result.sort(reverse = True) # pagerank大きい順に並びかえ
        top_ids = [tupl[1] for tupl in result[:10]] 
        top_titles = [(self.titles[id],pagerank[id]) for id in top_ids]
        print(f"top pagerank titles :{top_titles}")
        return
           



    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    # Wikipedia のグラフについて「渋谷」から「池袋」まで、同じページを重複して通らない、できるだけ長い経路を発見してください！！
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    # wikipedia.find_longest_titles()
    # # Example
    # wikipedia.find_most_linked_pages()
    # # Homework #1
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")

## python wikipedia.py wikipedia_dataset/pages_small.txt wikipedia_dataset/links_small.txt
## python wikipedia.py wikipedia_dataset/pages_medium.txt wikipedia_dataset/links_medium.txt
## python wikipedia.py wikipedia_dataset/pages_large.txt wikipedia_dataset/links_large.txt
