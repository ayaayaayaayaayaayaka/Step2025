
import sys
import math

from common import print_tour, read_input, calculate_total_distance

"""
多始点greedyに改善
dist:8592.5
total distance : 42338.82(N=2048)
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


def aco(): # ant colony optimization
    return tour

def ga(): # genetic algorythm
    return tour

def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    # 多始点greedy
    best_tour = None
    best_distance = 2 ** 31
    for city in range(N): # 全都市をスタート地点として試してみる
        curr_tour = greedy(city,N,dist)
        curr_distance = calculate_total_distance(curr_tour,dist)
        if curr_distance < best_distance: # より良い経路を見つけられた場合
            best_tour = curr_tour
            best_distance = curr_distance

    improve_tour = two_opt(best_tour,dist)
    total_dist = calculate_total_distance(improve_tour,dist)
    return improve_tour,total_dist


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour,total_dist = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print(f"total distance: {total_dist}")