class TSPService:
    def __init__(self, matrix):
        self.matrix = matrix
        self.matrix_size = len(matrix)
        for i in range(self.matrix_size):
            self.matrix[i][i] = float('inf')
        self.H = 0
        self.path_length = 0
        self.Str = [i for i in range(self.matrix_size)]
        self.Stb = [i for i in range(self.matrix_size)]
        self.res = []
        self.route = []
        self.start_matrix = [row.copy() for row in self.matrix]

    def _min(self, lst, index):
        return min(x for idx, x in enumerate(lst) if idx != index)

    def delete(self, matrix, index1, index2):
        del matrix[index1]
        for i in matrix:
            del i[index2]
        return matrix

    def solve(self):
        """
        Solve the TSP problem using an algorithm.

        :return: None
        """
        while True:
            # Редуцируем
            # --------------------------------------
            # Вычитаем минимальный элемент в строках
            for i in range(len(self.matrix)):
                min_row = min(self.matrix[i])
                min_column = min(row[i] for row in self.matrix)
                self.H += min_row + min_column
                for j in range(len(self.matrix)):
                    self.matrix[i][j] -= min_row
                    self.matrix[j][i] -= min_column

            # Оцениваем нулевые клетки и ищем нулевую клетку с максимальной оценкой
            # --------------------------------------
            null_max = 0
            index1 = 0
            index2 = 0
            tmp = 0
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix)):
                    if self.matrix[i][j] == 0:
                        tmp = self._min(self.matrix[i], j) + self._min((row[j] for row in self.matrix), i)
                        if tmp >= null_max:
                            null_max = tmp
                            index1 = i
                            index2 = j
            # --------------------------------------
            # Находим нужный нам путь, записываем его в res и удаляем все ненужное
            self.res.append(self.Str[index1] + 1)
            self.res.append(self.Stb[index2] + 1)

            old_index1 = self.Str[index1]
            old_index2 = self.Stb[index2]
            if old_index2 in self.Str and old_index1 in self.Stb:
                new_index1 = self.Str.index(old_index2)
                new_index2 = self.Stb.index(old_index1)
                self.matrix[new_index1][new_index2] = float('inf')
            del self.Str[index1]
            del self.Stb[index2]
            self.matrix = self.delete(self.matrix, index1, index2)
            if len(self.matrix) == 1:
                break

        # Формируем порядок пути
        for i in range(0, len(self.res) - 1, 2):
            if self.res.count(self.res[i]) < 2:
                self.route.append(self.res[i])
                self.route.append(self.res[i + 1])
        for i in range(0, len(self.res) - 1, 2):
            for j in range(0, len(self.res) - 1, 2):
                if self.route[len(self.route) - 1] == self.res[j]:
                    # self.route.append(self.res[j])
                    self.route.append(self.res[j + 1])

        # Считаем длину пути
        for i in range(0, len(self.route) - 1):
            if i == len(self.route) - 2:
                self.path_length += self.start_matrix[self.route[i] - 1][self.route[i + 1] - 1]
                self.path_length += self.start_matrix[self.route[i + 1] - 1][self.route[0] - 1]
            else:
                self.path_length += self.start_matrix[self.route[i] - 1][self.route[i + 1] - 1]

    def get_route(self):
        return self.route

    def get_path_length(self):
        return self.path_length


if __name__ == '__main__':
    matrix = [[0.0, 3944.0, 4139.0, 1147.0, 306.0], [3944.0, 0.0, 559.0, 2809.0, 4178.0], [4139.0, 559.0, 0.0, 2992.0, 4344.0], [1147.0, 2809.0, 2992.0, 0.0, 1369.0], [306.0, 4178.0, 4344.0, 1369.0, 0.0]]
    matrix = [[0.0, 3944.0, 4139.0, 1147.0, 306.0, 1201.0, 8.0, 3966.0, 2283.0, 1151.0], [3944.0, 0.0, 559.0, 2809.0, 4178.0, 3117.0, 3947.0, 23.0, 2210.0, 2804.0], [4139.0, 559.0, 0.0, 2992.0, 4344.0, 3444.0, 4140.0, 546.0, 2647.0, 2987.0], [1147.0, 2809.0, 2992.0, 0.0, 1369.0, 946.0, 1148.0, 2831.0, 1513.0, 6.0], [306.0, 4178.0, 4344.0, 1369.0, 0.0, 1507.0, 299.0, 4200.0, 2583.0, 1374.0], [1201.0, 3117.0, 3444.0, 946.0, 1507.0, 0.0, 1208.0, 3140.0, 1129.0, 943.0], [8.0, 3947.0, 4140.0, 1148.0, 299.0, 1208.0, 0.0, 3969.0, 2289.0, 1153.0], [3966.0, 23.0, 546.0, 2831.0, 4200.0, 3140.0, 3969.0, 0.0, 2233.0, 2826.0], [2283.0, 2210.0, 2647.0, 1513.0, 2583.0, 1129.0, 2289.0, 2233.0, 0.0, 1507.0], [1151.0, 2804.0, 2987.0, 6.0, 1374.0, 943.0, 1153.0, 2826.0, 1507.0, 0.0]]

    service = TSPService(matrix)
    service.solve()

    print("----------------------------------")
    print(service.get_route())
    print(service.get_path_length())
    print("----------------------------------")
