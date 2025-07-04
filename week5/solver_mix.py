#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input, calculate_total_distance


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# --- 1. Greedy Algorithm ---
def greedy(cities, dist):
    num_cities = len(cities)
    current_city = 0
    unvisited_cities = set(range(1, num_cities))
    tour = [current_city]
    
    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

# --- 2. 2-opt Algorithm (Local Search) ---
def reverse_segment(tour, i, j):
    # i+1 から j までを反転させる
    left, right = i + 1, j
    while left < right:
        tour[left], tour[right] = tour[right], tour[left]
        left += 1
        right -= 1

def two_opt(original_tour, dist):
    tour = original_tour[:]
    size = len(tour)
    improved = True
    while improved:
        improved = False
        for i in range(size - 1):
            for j in range(i + 2, size):
                i_plus_1 = i + 1
                j_plus_1 = (j + 1) % size
                
                current_dist = dist[tour[i]][tour[i_plus_1]] + dist[tour[j]][tour[j_plus_1]]
                new_dist = dist[tour[i]][tour[j]] + dist[tour[i_plus_1]][tour[j_plus_1]]

                if new_dist < current_dist:
                    reverse_segment(tour, i, j)
                    improved = True
    return tour

# --- 3. Genetic Algorithm (GA) ---
def ga(cities, dist):
    # GA パラメータ
    population_size = 50
    n_generations = 150
    mutation_rate = 0.02
    tournament_size = 5
    elite_size = 2

    num_cities = len(cities)

    # 初期集団の生成
    population = []
    for _ in range(population_size):
        tour = list(range(num_cities))
        random.shuffle(tour)
        population.append(tour)

    best_tour_overall = min(population, key=lambda t: calculate_total_distance(t, dist))

    for _ in range(n_generations):
        # 適応度計算 (距離が短いほど良い)
        pop_with_fitness = [(t, 1 / calculate_total_distance(t, dist)) for t in population]
        
        new_population = []

        # エリート選択
        pop_with_fitness.sort(key=lambda item: item[1], reverse=True)
        for i in range(elite_size):
            new_population.append(pop_with_fitness[i][0])
        
        while len(new_population) < population_size:
            # 選択 (トーナメント)
            def tournament_selection():
                tournament = random.sample(pop_with_fitness, tournament_size)
                return max(tournament, key=lambda item: item[1])[0]
            
            parent1 = tournament_selection()
            parent2 = tournament_selection()

            # 交叉 (順序交叉 OX1)
            start, end = sorted(random.sample(range(num_cities), 2))
            child = [-1] * num_cities
            child[start:end+1] = parent1[start:end+1]
            
            p2_idx = (end + 1) % num_cities
            c_idx = (end + 1) % num_cities
            while -1 in child:
                if parent2[p2_idx] not in child:
                    child[c_idx] = parent2[p2_idx]
                    c_idx = (c_idx + 1) % num_cities
                p2_idx = (p2_idx + 1) % num_cities
            
            # 突然変異 (Swap)
            if random.random() < mutation_rate:
                i, j = random.sample(range(num_cities), 2)
                child[i], child[j] = child[j], child[i]
            
            new_population.append(child)
        
        population = new_population

        current_best = min(population, key=lambda t: calculate_total_distance(t, dist))
        if calculate_total_distance(current_best, dist) < calculate_total_distance(best_tour_overall, dist):
            best_tour_overall = current_best

    return best_tour_overall

# --- 4. Ant Colony Optimization (ACO) ---
def aco(cities, dist):
    # ACO パラメータ
    n_ants = 20
    n_iterations = 100
    alpha = 1.0  # フェロモンの影響度
    beta = 3.0   # ヒューリスティック情報(距離)の影響度
    evaporation_rate = 0.5
    q = 100.0    # フェロモン放出量

    num_cities = len(cities)
    pheromone = [[1.0] * num_cities for _ in range(num_cities)]
    best_tour_overall = []
    best_dist_overall = float('inf')

    for _ in range(n_iterations):
        all_tours = []
        for _ in range(n_ants):
            current_city = random.randint(0, num_cities - 1)
            tour = [current_city]
            unvisited = set(range(num_cities))
            unvisited.remove(current_city)
            
            while unvisited:
                probabilities = []
                total_prob = 0
                for next_c in unvisited:
                    if dist[current_city][next_c] == 0: continue
                    p = (pheromone[current_city][next_c] ** alpha) * \
                        ((1.0 / dist[current_city][next_c]) ** beta)
                    probabilities.append((next_c, p))
                    total_prob += p
                
                if total_prob == 0: break # 次の都市に行けない場合
                
                r = random.uniform(0, total_prob)
                upto = 0
                next_city = -1
                for city, p in probabilities:
                    if upto + p >= r:
                        next_city = city
                        break
                    upto += p
                if next_city == -1: next_city = probabilities[-1][0] # 浮動小数点誤差対策
                
                tour.append(next_city)
                unvisited.remove(next_city)
                current_city = next_city
            
            if len(tour) == num_cities:
                all_tours.append((tour, calculate_total_distance(tour, dist)))
        
        # フェロモン更新
        for i in range(num_cities):
            for j in range(num_cities):
                pheromone[i][j] *= (1 - evaporation_rate)

        for tour, tour_dist in all_tours:
            for i in range(num_cities):
                pheromone[tour[i]][tour[(i + 1) % num_cities]] += q / tour_dist
        
        current_best_tour, current_best_dist = min(all_tours, key=lambda x: x[1], default=(None, float('inf')))
        if current_best_dist < best_dist_overall:
            best_dist_overall = current_best_dist
            best_tour_overall = current_best_tour
                
    return best_tour_overall

# --- Main Solver ---
def solve(cities, method='ga+2opt'):
    N = len(cities)
    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    # 探索手法の選択
    if method.startswith('greedy'):
        initial_tour = greedy(cities, dist)
    elif method.startswith('ga'):
        initial_tour = ga(cities, dist)
    elif method.startswith('aco'):
        initial_tour = aco(cities, dist)
    else:
        print(f"Error: Unknown method '{method}'", file=sys.stderr)
        return []

    # 2-optによる改善
    if '+2opt' in method:
        final_tour = two_opt(initial_tour, dist)
    else:
        final_tour = initial_tour

    return final_tour

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 solver.py <city_file> [method]")
        print("Methods: greedy, greedy+2opt, ga, ga+2opt, aco, aco+2opt")
        sys.exit(1)
        
    selected_method = 'ga+2opt' # デフォルトの手法
    if len(sys.argv) > 2:
        selected_method = sys.argv[2]
    
    cities = read_input(sys.argv[1])
    final_tour = solve(cities, method=selected_method)
    
    if final_tour:
        total_dist = calculate_total_distance(final_tour, [[distance(cities[i], cities[j]) for j in range(len(cities))] for i in range(len(cities))])
        print_tour(final_tour)
        # print(f"\nMethod: {selected_method}")
        print(f"Total distance: {total_dist:.4f}")

   ##  python3 solver_mix.py input_3.csv ga+2opt
## python3 solver_mix.py input_3.csv aco+2opt
## python3 solver_mix.py input_6.csv aco+2opt