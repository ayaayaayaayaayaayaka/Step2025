#!/usr/bin/env python3

"""
コードの改善点：
calculate_total_distanceに渡しているのがimproved_tourじゃなくてtourになっている 
Two-optでもreverse segmentでもtourを上書きしてしまっているように、パッと見ると思われてしまうことがあるかもしれない。→ return tourがいらない。
greedy tourはtourとは違う別のものを返すと一般的には解釈するが、このコードではtourを更新して同じ変数をreturn tourしてる。新しい機能を追加するときやコードを見返す時に、これを忘れていると思わぬところでエラーがおきる。
"""


import sys
import math

from common import print_tour, read_input, calculate_total_distance


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def greedy(tour,unvisited_cities,dist,current_city):
    while unvisited_cities:
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
    return tour

def two_opt(tour,dist):
    """
    tourを破壊的に変更している
    """
    for i in range(len(tour)-3):
        for j in range(i+2,len(tour)-1):
            if dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]] > dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[j+1]]:
                tour = reverse_segment(tour,i+1,j)
    return tour

def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    # リストの変数問題について
    # 言語によってかなり仕様が違う
    # 今回はtourは一回しか使わないからコピーしてもしなくてもどっちでもいい
    # 元々のtourを維持したいならちゃんとcopyしてあげたほうがいい
    greedy_tour = greedy(tour,unvisited_cities,dist,current_city) # 同じものを指している変数が二つある、メモリの中の同じものを複数の変数が指している
    improve_tour = two_opt(greedy_tour,dist)
    """
    greedy(tour,unvisited_cities,dist,current_city)
    two_opt(tour,dist)
    でも良い
    """
    total_dist = calculate_total_distance(tour,dist)
    return improve_tour,total_dist


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour,total_dist = solve(read_input(sys.argv[1]))
    print_tour(tour)
    # print(f"total distance: {total_dist}")
