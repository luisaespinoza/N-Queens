BOARD_SIZE = 8
def print_solution(solution, size, board_size=BOARD_SIZE):
    """Print the chessboard with queens placed according to the solution for the given size."""
    for i in range(size):
        for j in range(board_size):
            if solution.queens[i] == j:
                print("Q", end=" ")
            else:
                print("█", end=" ")
        print()

def print_backtracking_solution(board):
    """Print a single backtracking solution board."""
    n = len(board)
    print("\nSolution Board:")
    for row in range(n):
        for col in range(n):
            if col == board[row]:
                print("Q", end=" ")
            else:
                print("█", end=" ")
        print()
