def is_safe(x, y, board, N):
    """Check if the position is safe for the knight to move."""
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1


def print_board(board, N):
    """Print the chessboard."""
    for row in board:
        print(' '.join(str(cell).rjust(2) for cell in row))
    print()


def solve_knights_tour(N):
    """Solve the Knight's Tour problem using backtracking."""
    # Initialize the chessboard with -1
    board = [[-1 for _ in range(N)] for _ in range(N)]

    # Possible moves for a knight
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Start from the first cell
    board[0][0] = 1

    # Initialize the best solution
    best_solution = [[-1 for _ in range(N)] for _ in range(N)]
    best_move_count = 0

    # Start the tour from the first cell
    best_move_count = knights_tour_util(0, 0, 2, board, move_x, move_y, N, best_solution, best_move_count)

    if best_move_count == N * N + 1:
        print("Complete solution found:")
    else:
        print(f"Best solution found with {best_move_count - 1} moves:")

    print_board(best_solution, N)


def knights_tour_util(x, y, move_i, board, move_x, move_y, N, best_solution, best_move_count):
    """Utility function to solve the Knight's Tour problem."""
    if move_i > best_move_count:
        # Update the best solution found so far
        for i in range(N):
            for j in range(N):
                best_solution[i][j] = board[i][j]
        best_move_count = move_i

    if move_i == N * N + 1:
        return best_move_count

    for i in range(8):
        next_x = x + move_x[i]
        next_y = y + move_y[i]
        if is_safe(next_x, next_y, board, N):
            board[next_x][next_y] = move_i
            best_move_count = knights_tour_util(next_x, next_y, move_i + 1, board, move_x, move_y, N, best_solution,
                                                best_move_count)
            # Backtrack
            board[next_x][next_y] = -1

    return best_move_count


# Set the size of the chessboard
N =
solve_knights_tour(N)