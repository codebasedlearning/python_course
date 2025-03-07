# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" Task 'Wild Vine' """

import heapq

GRAPH = {
    1: {2: 5, 3: 1},
    2: {1: 5, 3: 3},
    3: {1: 1, 2: 3, 4: 2},
    4: {3: 2}
}

def find_min_weight_neighbor(start_node):
    """ find minimum weight neighbor and corresponding weight """

    # --- short variant ---
    # min_neighbor = min(GRAPH[start_node], key=GRAPH[start_node].get)
    # min_weight = GRAPH[start_node][min_neighbor]

    # --- explicit variant ---
    min_weight = float('inf')                                   # ensures any weight is smaller
    min_neighbor = None

    for neighbor, weight in GRAPH[start_node].items():
        if weight < min_weight:
            min_weight = weight
            min_neighbor = neighbor

    return min_neighbor, min_weight


def shortest_path_dijkstra(start_node):
    """ Dijkstra's algorithm """

    distances = {node: float('inf') for node in GRAPH}
    distances[start_node] = 0

    # Use a priority queue to always process the closest node first
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)

        for neighbor, weight in GRAPH[current].items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances

def solve():
    print(f" 1| {GRAPH.keys()=}")
    for node in GRAPH.keys():
        min_neighbor, min_weight = find_min_weight_neighbor(node)
        print(f" 2| ({node=}: {min_neighbor=},{min_weight=})")

    distances = shortest_path_dijkstra(1)
    print(f" 3| {distances=}")

if __name__ == "__main__":
    solve()
