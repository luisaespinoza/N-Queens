import random
import time
from utilities.core_functions import run_single_iteration, solve_n_queens
from utilities.helpers import print_backtracking_solution, print_solution
def run_tests():
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
    # print("\nRunning Backtracking Algorithm...")
    # cProfile.run('solutions = solve_n_queens(board_size)')
    # for i, solution in enumerate(solutions):
    #     print(f"Solution {i + 1}:")
    #     for row in solution:
    #         print(row)
    #     print()
     # Backtracking Algorithm
    print("\nRunning Backtracking Algorithm...")
    start_time = time.time()
    backtracking_solutions = solve_n_queens(board_size,num_iterations)
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

    print("\nBacktracking Algorithm Results:")
    print(f"  Solutions found: {len(backtracking_solutions)}")
    print(f"  Time taken: {backtracking_time:.2f} seconds")
    if backtracking_success:
        print("  Success: Yes")
    else:
        print("  Success: No")

# Main execution
if __name__ == "__main__":
    random.seed()  # Seed with system time
    run_tests()