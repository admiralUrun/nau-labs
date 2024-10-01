import random

class TwoDimensionalArray:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.array = [[0 for _ in range(cols)] for _ in range(rows)]

    def fill_random(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.array[i][j] = random.randint(0, 100)

    def print_array(self):
        for row in self.array:
            print(row)

    def find_min_max(self) -> (int, int):
        flat_list = [item for sublist in self.array for item in sublist]
        return min(flat_list), max(flat_list)

    def average_positive_negative(self) -> (int, int):
        positives = []
        negatives = []

        for row in self.array:
            for value in row:
                if value > 0:
                    positives.append(value)
                elif value < 0:
                    negatives.append(value)

        avg_positive = sum(positives) / len(positives) if positives else 0
        avg_negative = sum(negatives) / len(negatives) if negatives else 0

        return avg_positive, avg_negative

    def create_difference_array(self) -> list[list[int]]:
        avg, _ = self.average_positive_negative()
        diff_array = [[self.array[i][j] - avg for j in range(self.cols)] for i in range(self.rows)]
        return diff_array

    def print_difference_array(self):
        diff_array = self.create_difference_array()
        for row in diff_array:
            print(row)
