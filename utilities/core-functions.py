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