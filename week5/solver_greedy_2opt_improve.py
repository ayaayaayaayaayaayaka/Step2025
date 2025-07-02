import sys
import math

from common import print_tour, read_input, calculate_total_distance


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def greedy(unvisited_cities,dist):
    current_city = 0
    tour = [current_city]
     
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

def reverse_segment(improve_tour,swap_start,swap_end):
    left = swap_start
    right = swap_end
    while left < right:
        improve_tour[left],improve_tour[right] = improve_tour[right],improve_tour[left]
        left += 1
        right -= 1
    return 

def two_opt(original_tour,dist):
    improve_tour = original_tour[:]
    for i in range(len(import sys
import math

from common import print_tour, read_input, calculate_total_distance


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def greedy(unvisited_cities,dist):
    current_city = 0
    tour = [current_city]
     
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

def reverse_segment(improve_tour,swap_start,swap_end):
    left = swap_start
    right = swap_end
    while left < right:
        improve_tour[left],improve_tour[right] = improve_tour[right],improve_tour[left]
        left += 1
        right -= 1
    return 

def two_opt(original_tour,dist):
    improve_tour = original_tour[:]
    for i in range(len(improve_tour)-3):
        for j in range(i+2,len(improve_tour)-1):
            if dist[improve_tour[i]][improve_tour[i+1]] + dist[improve_tour[j]][improve_tour[j+1]] > dist[improve_tour[i]][improve_tour[j]] + dist[improve_tour[i+1]][improve_tour[j+1]]:
                reverse_segment(improve_tour,i+1,j)
    return improve_tour


def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    unvisited_cities = set(range(1, N))
    

    initial_tour = greedy(unvisited_cities,dist)
    improve_tour = two_opt(initial_tour,dist)
    total_dist = calculate_total_distance(improve_tour,dist)
    return improve_tour,total_dist


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour,total_dist = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print(f"total distance: {total_dist}")tour)-3):
        for j in range(i+2,len(tour)-1):
            if dist[improve_tour[i]][improve_tour[i+1]] + dist[improve_tour[j]][improve_tour[j+1]] > dist[improve_tour[i]][improve_tour[j]] + dist[improve_tour[i+1]][improve_tour[j+1]]:
                reverse_segment(improve_tour,i+1,j)
    return improve_tour


def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    unvisited_cities = set(range(1, N))
    

    initial_tour = greedy(unvisited_cities,dist)
    improve_tour = two_opt(initial_tour,dist)
    total_dist = calculate_total_distance(improve_tour,dist)
    return improve_tour,total_dist


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour,total_dist = solve(read_input(sys.argv[1]))
    print_tour(tour)
    print(f"total distance: {total_dist}")
