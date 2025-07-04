
import sys
import math
import random
from common import print_tour, read_input, calculate_total_distance

"""
多始点greedyに改善
annealingもしたがうまくいかなかった、、
dist:8256.5(challenge3)
10793.653196418569(ipnut4)
20932.86(ipnut 5)
total distance: 41894.18155019957(N=2048)
"""
# いただいたアドバイス
# TSPのサイズによって適切なアルゴリズムは変わる
# 小さいサイズのアルゴリズムと大きいサイズのアルゴリズムは仕様が違うはず
# いま解きたい問題の特徴をまず最初に把握することが大切
# 頂点を可視化してみたらわかることがあるはず
# 出力をvisualizeしてみてみるのも良い
# 特徴に合わせたアルゴリズムを考えることが大切
# challenge7くらいでも回るアルゴリズムの中で考えてみる
# gaとかacoには何回回すか、っていうパラメータがある、これも問題によって減らす必要が出てくる
# 中の計算時間を工夫する必要がある、2-optを逐一使うかどうか、みたいな話にも繋がってくる
# ga一回ずつ2-optを回して回数が減るか、gaをいっぱい回してから2-optをかけるのか


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def multi_greedy(start_node,N,dist):
    """
    始点は0に限らない
    """
    current_city = start_node
    unvisited_cities = set(range(N))
    unvisited_cities.remove(start_node)
    tour = [current_city]

    while unvisited_cities:
        # 未訪問の都市の中から、一番近いものを選択
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        # N^2かかっちゃっている
        # 近いやつから順に見ていく
        # dist[city] = [(距離、next_node),,,]みたいな感じで保存しておいて、その距離近い順に並べておくと良い

        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    return two_opt(tour,dist)


def reverse_segment(tour,swap_start,swap_end):
    left = swap_start
    right = swap_end
    while left < right:
        tour[left],tour[right] = tour[right],tour[left]
        left += 1
        right -= 1
    return 


def two_opt(original_tour,dist):
    improve_tour = original_tour[:]
    size = len(improve_tour)
    improved = True
    while improved: # 改善の余地がなくなるまでループし続ける
        improved = False
        for i in range(size-1):
            for j in range(i + 2,size):
                i_plus_1 = i + 1
                j_plus_1 = (j + 1) % size # jが最後の都市の場合、次は0番目の都市に戻る

                # 現在の2辺の合計距離
                current_dist = dist[improve_tour[i]][improve_tour[i_plus_1]] + dist[improve_tour[j]][improve_tour[j_plus_1]]
                # 繋ぎ変えた場合の2辺の合計距離
                new_dist = dist[improve_tour[i]][improve_tour[j]] + dist[improve_tour[i_plus_1]][improve_tour[j_plus_1]]

                if new_dist < current_dist:
                    # 改善が見られたら、i+1からjまでの区間を反転させる
                    reverse_segment(improve_tour, i + 1, j)
                    improved = True # 改善があったことを記録
    
    return improve_tour

# パラメータチューニングという試行錯誤
def simulated_annealing_improved(initial_tour, dist, final_temp, cooling_rate):
    """
    改善された焼きなまし法 (Simulated Annealing)
    - 動的な初期温度設定
    - 各温度での試行回数を設定
    - 近傍探索の多様化 (2-opt と Swap)
    """
    N = len(initial_tour)
    current_tour = initial_tour[:]
    current_distance = calculate_total_distance(current_tour, dist)
    
    best_tour = current_tour[:]
    best_distance = current_distance
    
    # --- 動的な初期温度の計算 ---
    # ランダムな改悪を複数回行い、その平均値から初期温度を決定する
    # これにより「序盤に改悪案をある程度の確率で受け入れる」状態を保証する
    deltas = []
    for _ in range(100):
        i, j = sorted(random.sample(range(N), 2))
        temp_tour = current_tour[:]
        reverse_segment(temp_tour, i, j)
        delta = calculate_total_distance(temp_tour, dist) - current_distance
        if delta > 0:
            deltas.append(delta)
    
    # 平均的な改悪が80%の確率で受理されるような温度を設定
    avg_delta = sum(deltas) / len(deltas) if deltas else 1.0
    initial_temp = -avg_delta / math.log(0.8) 
    print(f"Dynamic Initial Temperature set to: {initial_temp:.4f}")
    
    temp = initial_temp
    
    # 各温度での試行回数（都市数に比例させることが多い）
    iterations_per_temp = N 

    while temp > final_temp:
        for _ in range(iterations_per_temp):
            # 近傍解の生成方法をランダムに選択 (2-opt: 80%, Swap: 20%)
            if random.random() < 0.8:
                # 2-opt近傍
                i, j = sorted(random.sample(range(N), 2))
                new_tour = current_tour[:]
                reverse_segment(new_tour, i, j)
            else:
                # Swap近傍
                i, j = sorted(random.sample(range(N), 2))
                new_tour = current_tour[:]
                new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

            new_distance = calculate_total_distance(new_tour, dist)
            delta = new_distance - current_distance

            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_tour = new_tour[:]
                current_distance = new_distance
                
                if current_distance < best_distance:
                    best_tour = current_tour[:]
                    best_distance = current_distance
                    print(f"IMPROVE!! : {best_distance}")
        
        # 温度を更新（冷却）
        temp *= cooling_rate
        print(f"temp : {temp}")
        
    return best_tour, best_distance


def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    # 多始点greedy
    best_tour_greedy = None
    best_distance = 2 ** 31
    for city in range(N): # 全都市をスタート地点として試してみる
        curr_tour = multi_greedy(city,N,dist)
        curr_distance = calculate_total_distance(curr_tour,dist)
        print(f"now start from {city} and current distance : {curr_distance} best distance : {best_distance}")
        if curr_distance < best_distance: # より良い経路を見つけられた場合
            best_tour_greedy = curr_tour
            best_distance = curr_distance
    
    # --- ステップ2: 焼きなまし法でさらなる改善を目指す ---
    print("\n--- Running Simulated Annealing ---")
    # 焼きなまし法のパラメータ (これらの値は問題の規模や特性に応じて調整が必要)
    FINAL_TEMP = 0.01      # 最終温度
    COOLING_RATE = 0.999 # 冷却率

    final_tour, final_distance = simulated_annealing_improved(
        best_tour_greedy, 
        dist,
        FINAL_TEMP, 
        COOLING_RATE
    )
    
    return final_tour, final_distance


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour,total_dist = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print(f"total distance: {total_dist}")