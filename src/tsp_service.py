from itertools import permutations


class TSPService:
    """Класс, решающий задачу коммивояжера."""

    def __init__(self, matrix):
        self.matrix = matrix
        """Матрица путей"""
        self.path_length = 0
        """Длина оптимального пути"""
        self.route = []
        """Список обхода городов"""

    def get_route(self):
        """Возвращает список обхода городов."""
        return self.route

    def get_path_length(self):
        """Возвращает длину оптимального пути"""
        return self.path_length

    def tsp_brute_force(self):
        """Нахождение оптимального пути."""
        num_vertices = len(self.matrix)
        min_distance = float('inf')
        optimal_path = []

        # генерация всех перестановок вершин
        all_permutations = permutations(range(1, num_vertices))

        for path in all_permutations:
            path = (0,) + path + (0,)  # начало и конец в точке 0

            distance = sum(self.matrix[path[i]][path[i + 1]] for i in range(num_vertices))

            if distance < min_distance:
                min_distance = distance
                optimal_path = path

        self.route = [i+1 for i in optimal_path[:-1]]
        self.path_length = optimal_path

        return min_distance, optimal_path
