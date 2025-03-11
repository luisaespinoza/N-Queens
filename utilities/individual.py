import random
# this is a test
# hi daniela
# default argument values
BOARD_SIZE = 8
POPULATION_SIZE = 100
MAX_GENERATIONS_PER_STEP = 500
MUTATION_RATE = 0.15
# Represents a partial solution with k queens
class Individual:
    def __init__(self, size,board_size=BOARD_SIZE):
        """Initialize with a random permutation of columns for the first 'size' rows."""
        columns = list(range(board_size))
        random.shuffle(columns)
        self.queens = columns[:size]  # queens[i] is the column for the queen in row i

    def fitness(self):
        """Calculate the number of diagonal conflicts."""
        conflicts = 0
        for i in range(len(self.queens)):
            for j in range(i + 1, len(self.queens)):
                if abs(i - j) == abs(self.queens[i] - self.queens[j]):
                    conflicts += 1
        return conflicts

    def mutate(self,mutation_rate=MUTATION_RATE):
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
                           if abs(i - len(self.queens)) == abs(self.queens[i] - col))
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_col = col
        self.queens.append(best_col)
