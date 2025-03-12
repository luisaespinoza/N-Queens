import random
import time
from utilities.core_functions import run_single_iteration, solve_n_queens
from utilities.helpers import print_backtracking_solution, print_solution
def run_tests(auto_mode=False, board_size=8, num_iterations=10, population_size=100, max_generations_per_step=500, mutation_rate=0.15, print_boards=True, run_backtracking=False):
    """Main function to run multiple iterations and summarize results for a given board size."""

    print("N-Queens Solver: Genetic Algorithm vs Backtracking")
    print("------------------------------------------------")

    if not auto_mode:
        # global board_size, population_size  # Declare board_size, population_size as global to use in crossover
        # Get board size from user
        try:
            board_size = int(input("Enter the board size (N for N-Queens, default 8): ") or board_size)
        except ValueError:
            print("Invalid input. Using default board size of 8.")
            board_size = 8

        if board_size < 1:
            print("Board size must be at least 1. Using default of 8.")
            board_size = 8

        # Get number of iterations from user
        try:
            num_iterations = int(input("Enter the number of iterations to run (default 10): ") or num_iterations)
        except ValueError:
            print("Invalid input. Using default of 10 iterations.")
            num_iterations = 10

        if num_iterations <= 0:
            print("Number of iterations must be positive. Using default of 10.")
            num_iterations = 10

        try:
            population_size = int(input("Enter the population size (default 100): ") or population_size)
        except ValueError:
            print("Invalid input. Using default population size of 100.")
            population_size = 100

        if population_size < 1:
            print("Population size must be at least 1. Using default of 100.")
            population_size = 100

        # Get max generations per step from user
        try:
            max_generations_per_step = int(input("Enter the max generations per step (default 500): ") or max_generations_per_step)
        except ValueError:
            print("Invalid input. Using default max generations per step of 500.")
            max_generations_per_step = 500

        if max_generations_per_step < 1:
            print("Max generations per step must be at least 1. Using default of 500.")
            max_generations_per_step = 500

        # Get mutation rate from user
        try:
            mutation_rate = float(input("Enter the mutation rate (default 0.15): ") or mutation_rate)
        except ValueError:
            print("Invalid input. Using default mutation rate of 0.15.")
            mutation_rate = 0.15

        if mutation_rate < 0 or mutation_rate > 1:
            print("Mutation rate must be between 0 and 1. Using default of 0.15.")
            mutation_rate = 0.15

        run_backtracking_input = input("Run backtracking algorithm? (default no): ").strip().lower() or "no"
        run_backtracking = run_backtracking_input in ["yes", "y"]

    # Genetic Algorithm Results
    ga_successes = 0
    ga_total_time = 0
    ga_valid_solutions = 0

    for run in range(1, num_iterations + 1):

        if print_boards:
            print(f"\nGenetic Algorithm Run {run}:")
        solution, time_taken, is_valid = run_single_iteration(board_size, population_size, max_generations_per_step,
                                                                  mutation_rate)
        ga_total_time += time_taken
        if solution:
                if print_boards:
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
    if run_backtracking:

        if print_boards:
            print("\nRunning Backtracking Algorithm...")
            start_time = time.time()
            backtracking_solutions = solve_n_queens(board_size, num_iterations)
            end_time = time.time()
            backtracking_time = end_time - start_time
            backtracking_success = len(backtracking_solutions) > 0
            # Print one backtracking solution (if available)
            if backtracking_solutions:
                for solution in backtracking_solutions:
                    print(f"  Solution found:")
                    print_backtracking_solution(solution)

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

    if run_backtracking:
        print("\nBacktracking Algorithm Results:")
        print(f"  Solutions found: {len(backtracking_solutions)}")
        print(f"  Time taken: {backtracking_time:.2f} seconds")
        print("  Success:", "Yes" if backtracking_success else "No")

# Main execution
if __name__ == "__main__":
    random.seed()  # Seed with system time
    # run_tests() #this runs in user prompt mode

    # this is an automated version
    start = 0.1
    end = .9
    increment = 0.05
    current = start
    while current <= end:
        print(f"mutation_rate= {current}")
        run_tests(auto_mode=True, board_size=8, num_iterations=100, population_size=100, max_generations_per_step=500, mutation_rate=current, print_boards=False,run_backtracking=False)
        current += increment