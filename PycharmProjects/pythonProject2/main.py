import heapq
import networkx as nx
import random


def count_scooters_with_low_charge(graph):
    low_charge_count = 0
    # Перебираем все узлы, которые являются самокатами
    for node, data in graph.nodes(data=True):
        if node.startswith('Scooter_') and data['charge'] < 55:
            low_charge_count += 1
    return low_charge_count


def dijkstra_shortest_path(graph, start, end, scooters_to_charge=20):
    # Создаем словарь для хранения расстояний от начальной вершины
    distances = {vertex: float('infinity') for vertex in graph.nodes}
    # Расстояние до начальной вершины равно 0
    distances[start] = 0
    # Приоритетная очередь для отслеживания вершин для посещения
    priority_queue = [(0, start)]

    count_less55 = count_scooters_with_low_charge(graph)

    # Словарь для восстановления пути
    previous_vertices = {vertex: None for vertex in graph.nodes}
    charged_scooters = 0  # Счетчик заряженных самокатов
    while priority_queue:
        # Извлекаем вершину с минимальным расстоянием
        current_distance, current_vertex = heapq.heappop(priority_queue)
        # Если текущая вершина - конечная, мы закончили
        if current_vertex == end:
            break
        # Перебираем соседей текущей вершины
        for neighbor, attributes in graph[current_vertex].items():
            weight = attributes['weight']
            distance = current_distance + weight
            if neighbor.startswith('Scooter_') and graph.nodes[neighbor][
                'charge'] < 55 and charged_scooters <= scooters_to_charge:
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
                    # Увеличиваем заряд до 100% и увеличиваем счетчик
                    graph.nodes[neighbor]['charge'] = 100
                    charged_scooters += 1
                    count_less55 -= 1
            else:
                if distance < distances[neighbor] and (
                        charged_scooters > scooters_to_charge or count_less55 <= scooters_to_charge):
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
    # Восстанавливаем кратчайший путь
    path = []
    current_vertex = end
    while previous_vertices[current_vertex] is not None:
        path.insert(0, current_vertex)
        current_vertex = previous_vertices[current_vertex]
    path.insert(0, start)

    return distances[end], path


def calculate_total_route(graph, stations_count):
    total_distance = 0
    total_path = []
    average_charge = sum(
        [data['charge'] for node, data in graph.nodes(data=True) if node.startswith('Scooter_')]) / scooters_count
    # Если средний заряд самокатов больше 80, возвращаем пустой маршрут
    if average_charge > 80:
        return total_distance, total_path
    # Получаем список станций на основе stations_count
    stations = ['Station_' + str(i) for i in range(1, stations_count + 1)]
    # Применяем функцию dijkstra_shortest_path для каждой пары станций
    for i in range(stations_count):
        start = stations[i]
        end = stations[(i + 1) % stations_count]  # Циклический переход к первой станции
        distance, path = dijkstra_shortest_path(graph, start, end)
        total_distance += distance
        # Добавляем путь, исключая последнюю вершину, чтобы избежать повторения
        total_path.extend(path[:-1])

    # Добавляем последнюю вершину последнего пути
    total_path.append(path[-1])

    return total_distance, total_path


# Создание графа
stations_count = 10
scooters_count = 150
G = nx.Graph()
# Добавление узлов станций
for i in range(1, stations_count + 1):
    G.add_node(f"Station_{i}")
# Добавление узлов самокатов с уровнем заряда
for i in range(1, scooters_count + 1):
    charge = random.randint(0, 100)
    G.add_node(f"Scooter_{i}", charge=charge)
# Добавление рёбер между всеми самокатами
for i in range(1, scooters_count + 1):
    for j in range(i + 1, scooters_count + 1):
        distance = random.randint(1, 100)
        G.add_edge(f"Scooter_{i}", f"Scooter_{j}", weight=distance)
# Добавление рёбер между каждым самокатом и каждой станцией
for i in range(1, scooters_count + 1):
    for j in range(1, stations_count + 1):
        distance = random.randint(1, 100)
        G.add_edge(f"Scooter_{i}", f"Station_{j}", weight=distance)

print()
print("Узлы графа с атрибутами в начале пути:", G.nodes(data=True))
print("Рёбра графа с весами:", G.edges(data=True))
print()
# Вызов функции для создания маршрута
distance, route = calculate_total_route(G, stations_count)
print("Маршрут:", route)
print("Общая длина маршрута:", distance)

