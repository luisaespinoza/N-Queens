import random
import time

# Constants for the genetic algorithm
POPULATION_SIZE = 100
MAX_GENERATIONS_PER_STEP = 100
MUTATION_RATE = 0.1

# Represents a partial solution with k queens
class Individual:
    def __init__(self, size, board_size):
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

    def mutate(self):
        """Mutate by swapping two positions with probability MUTATION_RATE."""
        if random.random() < MUTATION_RATE:
            pos1, pos2 = random.sample(range(len(self.queens)), 2)
            self.queens[pos1], self.queens[pos2] = self.queens[pos2], self.queens[pos1]

    def extend(self, used_columns, board_size):
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

def crossover(parent1, parent2):
    """Perform order crossover (OX1) to produce a child permutation."""
    size = len(parent1.queens)
    child = Individual(0, board_size)  # board_size is accessed globally here
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

def print_solution(solution, size, board_size):
    """Print the chessboard with queens placed according to the solution for the given size."""
    print("\nSolution Board:")
    for i in range(size):
        for j in range(board_size):
            if solution.queens[i] == j:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

def validate_solution(individual, size):
    """Validate that the solution has exactly 'size' queens, unique columns, and no diagonal conflicts."""
    if len(individual.queens) != size:
        return False
    if len(set(individual.queens)) != size:  # Check for unique columns
        return False
    if individual.fitness() != 0:  # Check for no diagonal conflicts
        return False
    return True

def run_single_iteration(board_size):
    """Run a single iteration of the incremental genetic algorithm for N-Queens."""
    current_size = 1
    population = [Individual(current_size, board_size) for _ in range(POPULATION_SIZE)]
    solution_found = False
    start_time = time.time()

    while current_size <= board_size:
        for generation in range(MAX_GENERATIONS_PER_STEP):
            for ind in population:
                if ind.fitness() == 0:
                    if current_size == board_size:
                        solution_found = True
                    # Extend population to current_size + 1 queens
                    for p in population:
                        used_columns = [False] * board_size
                        for col in p.queens:
                            used_columns[col] = True
                        p.extend(used_columns, board_size)
                    current_size += 1
                    break
            else:
                # Create new population via selection, crossover, and mutation
                new_population = []
                for _ in range(POPULATION_SIZE):
                    parent1 = select(population)
                    parent2 = select(population)
                    child = crossover(parent1, parent2)
                    child.mutate()
                    new_population.append(child)
                population = new_population
                continue
            break  # Break out of the generation loop if solution is found

    end_time = time.time()
    time_taken = end_time - start_time

    if solution_found:
        # Find the individual with fitness 0 for board_size queens
        solution = next(ind for ind in population if len(ind.queens) == board_size and ind.fitness() == 0)
        is_valid = validate_solution(solution, board_size)
        return solution, time_taken, is_valid
    else:
        return None, time_taken, False

# Backtracking N-Queens solver
def solve_n_queens(n):
    """Solve N-Queens using backtracking algorithm and return all solutions."""
    def is_safe(board, row, col):
        # Check row on left side
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

    def place_queens(n, col, board):
        if col == n:
            result.append([row[:] for row in board])  # Append a deep copy of the board
            return
        for row in range(n):
            if is_safe(board, row, col):
                board[row][col] = 1
                place_queens(n, col + 1, board)
                board[row][col] = 0  # Backtrack by resetting the position

    result = []
    board = [[0] * n for _ in range(n)]  # Initialize an NxN board with zeros
    place_queens(n, 0, board)
    return result

def print_backtracking_solution(board):
    """Print a single backtracking solution board."""
    print("\nSolution Board:")
    for row in board:
        for cell in row:
            if cell == 1:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

def main():
    """Main function to run multiple iterations and summarize results for a given board size."""
    global board_size  # Declare board_size as global to use in crossover
    print("N-Queens Solver: Genetic Algorithm vs Backtracking")
    print("------------------------------------------------")
    
    # Get board size from user
    try:
        board_size = int(input("Enter the board size (N for N-Queens, default 8): ") or 8)
    except ValueError:
        print("Invalid input. Using default board size of 8.")
        board_size = 8

    if board_size < 1:
        print("Board size must be at least 1. Using default of 8.")
        board_size = 8

    # Get number of iterations from user
    try:
        num_iterations = int(input("Enter the number of iterations to run (default 10): ") or 10)
    except ValueError:
        print("Invalid input. Using default of 10 iterations.")
        num_iterations = 10

    if num_iterations <= 0:
        print("Number of iterations must be positive. Using default of 10.")
        num_iterations = 10

    # Genetic Algorithm Results
    ga_successes = 0
    ga_total_time = 0
    ga_valid_solutions = 0

    for run in range(1, num_iterations + 1):
        print(f"\nGenetic Algorithm Run {run}:")
        solution, time_taken, is_valid = run_single_iteration(board_size)
        ga_total_time += time_taken
        if solution:
            print(f"  Solution found: {solution.queens}")
            print(f"  Fitness: {solution.fitness()}")
            print(f"  Time taken: {time_taken:.2f} seconds")
            print_solution(solution, board_size, board_size)
            if is_valid:
                ga_valid_solutions += 1
            ga_successes += 1
        else:
            print("  No solution found within generation limits.")
            print(f"  Time taken: {time_taken:.2f} seconds")

    # Backtracking Algorithm
    print("\nRunning Backtracking Algorithm...")
    start_time = time.time()
    backtracking_solutions = solve_n_queens(board_size)
    end_time = time.time()
    backtracking_time = end_time - start_time
    backtracking_success = len(backtracking_solutions) > 0

    # Print one backtracking solution (if available)
    if backtracking_solutions:
        print(f"  First solution found:")
        print_backtracking_solution(backtracking_solutions[0])

    # Summary
    print("\nSummary of Results")
    print("------------------")
    print(f"Board size: {board_size}")
    print(f"Genetic Algorithm Results:")
    print(f"  Total runs: {num_iterations}")
    print(f"  Successful runs (solution found): {ga_successes}")
    print(f"  Valid solutions (correct format and no conflicts): {ga_valid_solutions}")
    print(f"  Average time per run: {ga_total_time / num_iterations:.2f} seconds")
    if ga_successes > 0:
        print(f"  Success rate: {(ga_successes / num_iterations) * 100:.2f}%")
    else:
        print("  Success rate: 0%")

    print("\nBacktracking Algorithm Results:")
    print(f"  Solutions found: {len(backtracking_solutions)}")
    print(f"  Time taken: {backtracking_time:.2f} seconds")
    if backtracking_success:
        print("  Success: Yes")
    else:
        print("  Success: No")

if __name__ == "__main__":
    random.seed()  # Seed with system time
    main()