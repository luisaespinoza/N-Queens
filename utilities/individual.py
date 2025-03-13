import random
from enum import Enum

# this is a test
# hi daniela
# default argument values
BOARD_SIZE = 8
POPULATION_SIZE = 100
MAX_GENERATIONS_PER_STEP = 500
MUTATION_RATE = 0.15
# Represents a partial solution with k queens
class Geometry(Enum):
    EUCLIDEAN = 1
    TOROIDAL = 2

class Individual:
    def __init__(self, size, board_size=BOARD_SIZE, geometry=Geometry.EUCLIDEAN):
        """Initialize with a random permutation of columns for the first 'size' rows."""
        self.geometry = geometry
        columns = list(range(board_size))
        random.shuffle(columns)
        self.queens = columns[:size]  # queens[i] is the column for the queen in row i

    def fitness(self):
        """Calculate the number of diagonal conflicts based on the geometry."""
        conflicts = 0
        for i in range(len(self.queens)):
            for j in range(i + 1, len(self.queens)):
                row_distance = abs(i - j)
                col_distance = abs(self.queens[i] - self.queens[j])

                if self.geometry == Geometry.TOROIDAL:
                    col_distance = min(col_distance, BOARD_SIZE - col_distance)

                if row_distance == col_distance:
                    conflicts += 1
        return conflicts

    def mutate(self, mutation_rate=MUTATION_RATE):
        """Mutate by swapping two positions with probability MUTATION_RATE."""
        if random.random() < mutation_rate:
            pos1, pos2 = random.sample(range(len(self.queens)), 2)
            self.queens[pos1], self.queens[pos2] = self.queens[pos2], self.queens[pos1]

    def extend(self, used_columns, board_size=BOARD_SIZE):
        """Extend by adding a queen in an unused column that minimizes conflicts."""
        available_columns = [col for col in range(board_size) if not used_columns[col]]
        if not available_columns:
            return

        min_conflicts = board_size + 1
        best_col = available_columns[0]
        for col in available_columns:
            conflicts = sum(1 for i in range(len(self.queens))
                           if abs(i - len(self.queens)) == abs(self.queens[i] - col) or
                           (self.geometry == Geometry.TOROIDAL and
                            abs(i - len(self.queens)) == (board_size - abs(self.queens[i] - col))))
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_col = col
        self.queens.append(best_col)