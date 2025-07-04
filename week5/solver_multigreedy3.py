
import sys
import math
import random
from common import print_tour, read_input, calculate_total_distance

"""
多始点greedyに改善
annealingも加えたがうまくいかなかった
total distance: 11042.364950488864 (input4)
21550.19(input5)
"""

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def greedy(start_node,N,dist):
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
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


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
def simulated_annealing(initial_tour, dist, initial_temp, final_temp, cooling_rate):
    """
    焼きなまし法 (Simulated Annealing)
    """
    N = len(initial_tour)
    current_tour = initial_tour[:]
    current_distance = calculate_total_distance(current_tour, dist)
    
    best_tour = current_tour[:]
    best_distance = current_distance
    
    temp = initial_temp

    while temp > final_temp:
        # 2-optと同様に、ランダムな2点を選び、その間の経路を反転させる（近傍解を生成）
        i, j = sorted(random.sample(range(N), 2))
        
        new_tour = current_tour[:]
        reverse_segment(new_tour, i, j) # iからjまでを反転
        
        new_distance = calculate_total_distance(new_tour, dist)
        
        delta = new_distance - current_distance

        # 解が改善された場合、または確率的に許容される場合に解を更新
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_tour = new_tour[:]
            current_distance = new_distance
            
            # 全体での最良解も更新
            if current_distance < best_distance:
                best_tour = current_tour[:]
                best_distance = current_distance
        
        # 温度を更新（冷却）
        temp *= cooling_rate
        
    return best_tour, best_distance

def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    # 多始点greedy
    best_greedy_tour = None
    best_distance = 2 ** 31
    for city in range(N): # 全都市をスタート地点として試してみる
        curr_tour = greedy(city,N,dist)
        curr_distance = calculate_total_distance(curr_tour,dist)
        if curr_distance < best_distance: # より良い経路を見つけられた場合
            best_greedy_tour = curr_tour
            best_distance = curr_distance

    improve_2opt_tour = two_opt(best_greedy_tour,dist)
    total_dist = calculate_total_distance(improve_2opt_tour,dist)

    print(f"distace : {total_dist}")
    # --- ステップ2: 焼きなまし法でさらなる改善を目指す ---
    print("\n--- Running Simulated Annealing ---")
    # 焼きなまし法のパラメータ (これらの値は問題の規模や特性に応じて調整が必要)
    INITIAL_TEMP = 100.0   # 初期温度
    FINAL_TEMP = 0.01      # 最終温度
    COOLING_RATE = 0.99999  # 冷却率

    final_tour, final_distance = simulated_annealing(
        improve_2opt_tour, 
        dist, 
        INITIAL_TEMP, 
        FINAL_TEMP, 
        COOLING_RATE
    )
    
    return final_tour, final_distance



if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour,total_dist = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print(f"total distance: {total_dist}")