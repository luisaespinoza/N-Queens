import random
from individual import Individual

def crossover(parent1, parent2):
    """Perform order crossover (OX1) to produce a child permutation."""
    size = len(parent1.queens)
    child = Individual(0)
    child.queens = [None] * size

    # Choose two crossover points
    start = random.randint(0, size - 1)
    end = random.randint(start, size - 1)

    # Copy segment from parent1
    for i in range(start, end + 1):
        child.queens[i] = parent1.queens[i]

    # Fill remaining positions with unused columns from parent2
    segment = set(child.queens[start:end + 1])
    parent2_filtered = [col for col in parent2.queens if col not in segment]
    index = 0
    for i in range(size):
        if child.queens[i] is None:
            child.queens[i] = parent2_filtered[index]
            index += 1

    return child

def select(population):
    """Perform tournament selection with tournament size 3."""
    tournament_size = 3
    tournament = random.sample(population, tournament_size)
    return min(tournament, key=lambda ind: ind.fitness())

# analytic solution using backtracking algorithm
# for comparison/benchmarking
def solve_n_queens(n):
    def is_safe(board, row, col):
        # Check this row on left side
        for i in range(col):
            if board[row][i] == 1:
                return False

        # Check upper diagonal on left side
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        # Check lower diagonal on left side
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        return True

    def place_queens(n, row, board):
        if row == n:
            result.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row][col] = 1
                place_queens(n, row + 1, board)
                board[row][col] = 0

    result = []
    board = [[0]*n for _ in range(n)]
    place_queens(n, 0, board)
    return result