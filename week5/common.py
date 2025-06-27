def read_input(filename):
    with open(filename) as f:
        cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities


def format_tour(tour):
    return 'index\n' + '\n'.join(map(str, tour))


def print_tour(tour):
    print(format_tour(tour))

def calculate_total_distance(tour,dist):
    total_dist = 0
    current_city = tour[0]
    for next_city in tour[1:]:
        total_dist += dist[current_city][next_city]
        current_city = next_city
    total_dist += dist[tour[-1]][tour[0]]
    return total_dist
