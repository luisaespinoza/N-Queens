import random

# Constants
BOARD_SIZE = 8
POPULATION_SIZE = 100
MAX_GENERATIONS_PER_STEP = 500
MUTATION_RATE = 0.15

# Represents a partial solution with k queens
class Individual:
    def __init__(self, size):
        """Initialize with a random permutation of columns for the first 'size' rows."""
        columns = list(range(BOARD_SIZE))
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

    def extend(self, used_columns):
        """Extend by adding a queen in an unused column that minimizes conflicts."""
        available_columns = [col for col in range(BOARD_SIZE) if not used_columns[col]]
        if not available_columns:
            return

        min_conflicts = BOARD_SIZE + 1
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

def print_solution(solution, size):
    """Print the chessboard with queens placed according to the solution for the given size."""
    for i in range(size):
        for j in range(BOARD_SIZE):
            if solution.queens[i] == j:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

# Main execution
if __name__ == "__main__":
    random.seed()  # Seed with system time

    current_size = 1
    population = [Individual(current_size) for _ in range(POPULATION_SIZE)]

    while current_size <= BOARD_SIZE:
        print(f"Evolving solutions with {current_size} queens...")

        # Evolve for up to MAX_GENERATIONS_PER_STEP generations
        for generation in range(MAX_GENERATIONS_PER_STEP):
            # Check for a perfect solution
            for ind in population:
                if ind.fitness() == 0:
                    print(f"Solution found for {current_size} queens: {ind.queens}")
                    if current_size == BOARD_SIZE:
                        print("Final solution for 8 queens:")
                        print_solution(ind, BOARD_SIZE)
                        exit()
                    # Extend population to current_size + 1 queens
                    for p in population:
                        used_columns = [False] * BOARD_SIZE
                        for col in p.queens:
                            used_columns[col] = True
                        p.extend(used_columns)
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

    # If no perfect solution is found, print the best one
    print("No perfect solution found.")
    best = min(population, key=lambda ind: ind.fitness())
    print(f"Best solution (conflicts = {best.fitness()}): {best.queens}")
    print_solution(best, BOARD_SIZE)