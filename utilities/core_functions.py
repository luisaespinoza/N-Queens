import random
import time
from utilities import individual

Individual = individual.Individual
BOARD_SIZE=individual.BOARD_SIZE
POPULATION_SIZE =  individual.POPULATION_SIZE
MAX_GENERATIONS_PER_STEP = individual.MAX_GENERATIONS_PER_STEP
MUTATION_RATE = individual.MUTATION_RATE
Geometry = individual.Geometry

def crossover(parent1, parent2):
    """Perform order crossover (OX1) to produce a child permutation."""
    size = len(parent1.queens)
    child = Individual(0, geometry=parent1.geometry)  # Inherit geometry from parent
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

def extend_population(population, board_size):
    """Extend each individual in the population to have `current_size + 1` queens."""
    for p in population:
        used_columns = [False] * board_size
        for col in p.queens:
            used_columns[col] = True
        p.extend(used_columns, board_size)

def select_parents(population):
    """Return two parents selected from the population using some selection strategy."""
    parent1 = random.choice(population)
    parent2 = random.choice(population)
    return parent1, parent2
def validate_solution(individ, size):
    """Validate that the solution has exactly 'size' queens, unique columns, and no diagonal conflicts."""
    if len(individ.queens) != size:
        return False
    if len(set(individ.queens)) != size:  # Check for unique columns
        return False
    if individ.fitness() != 0:  # Check for no diagonal conflicts
        return False
    return True
# analytic solution using backtracking algorithm
# for comparison/benchmarking


def check_euclidean_conflict(i, row, c, col):
    """Check for diagonal conflict in Euclidean geometry."""
    return abs(i - row) == abs(c - col)

def check_toroidal_conflict(i, row, c, col, board_length):
    """Check for diagonal conflict in Toroidal geometry."""
    return abs(i - row) == abs(c - col) or abs(i - row) == (board_length - abs(c - col))

def is_safe(board, row, col, geometry):
    """Check if placing a queen at (row, col) is safe based on the geometry."""
    for i, c in enumerate(board):
        if c == col:  # Column conflict
            return False
        if geometry == Geometry.EUCLIDEAN:
            if check_euclidean_conflict(i, row, c, col):
                return False
        elif geometry == Geometry.TOROIDAL:
            if check_toroidal_conflict(i, row, c,col, len(board)):
                return False
    return True
def place_queens(n, row, board, result, m, geometry):
    if len(result) == m:
        return
    if row == n:
        result.append(board[:])
        return
    for col in range(n):
        if is_safe(board, row, col, geometry):
            board.append(col)
            place_queens(n, row + 1, board, result, m, geometry)
            board.pop()


def solve_n_queens(n, m, geometry=Geometry.EUCLIDEAN):
    result = []
    place_queens(n, 0, [], result, m, geometry)
    return result


def run_single_iteration(board_size,population_size=POPULATION_SIZE,max_generations_per_step=MAX_GENERATIONS_PER_STEP,mutation_rate=MUTATION_RATE, geometry=Geometry.EUCLIDEAN):
    """Run a single iteration of the incremental genetic algorithm for N-Queens."""
    current_size = 1
    population = [Individual(current_size, board_size,geometry) for _ in range(population_size)]
    solution_found = False
    start_time = time.perf_counter()
    def has_solution(population_a):
        """Return True if any individual in the population has a fitness of 0."""
        return any(ind.fitness() == 0 for ind in population_a)


    while current_size <= board_size:
        for generation in range(max_generations_per_step):
            # Check if a solution is found in the current generation
            if has_solution(population):
                solution_found=True
                # Extend population to current_size + 1 queens
                extend_population(population, board_size)
                current_size += 1
                break  # Break out of the generation loop if solution is found

            # Create new population via selection, crossover, and mutation
            new_population = []
            for _ in range(population_size):
                parent1, parent2 = select_parents(population)
                child = crossover(parent1, parent2)
                child.mutate(mutation_rate)
                new_population.append(child)
            population = new_population
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    solution = None
    if solution_found:
        for ind in population:
            if ind.fitness() == 0:
                solution = ind
                break
    return solution, time_taken, solution_found
