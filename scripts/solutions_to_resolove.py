import random
import utilities
import cProfile



# Main execution
if __name__ == "__main__":
    # testing the backtracking algorithm for benchmarking
    n = 8
    cProfile.run('solutions = solve_n_queens(n)')
    for i, solution in enumerate(solutions):
        print(f"Solution {i + 1}:")
        for row in solution:
            print(row)
        print()

    #     running our solution
    def ourSolutionTest():
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


    cProfile.run('ourSolutionTest()')
    # If no perfect solution is found, print the best one
    print("No perfect solution found.")
    best = min(population, key=lambda ind: ind.fitness())
    print(f"Best solution (conflicts = {best.fitness()}): {best.queens}")
    print_solution(best, BOARD_SIZE)