def is_safe(x, y, board, N):
    """Check if the position is safe for the knight to move."""
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1

def print_board(board, N):
    """Print the chessboard."""
    print(f"Board dimensions: {N}x{N}")
    for row in board:
        print(' '.join(str(cell).rjust(2) for cell in row))
    print()

def solve_knights_tour(N):
    """Solve the Knight's Tour problem using backtracking and Warnsdorff's rule."""
    if N < 3:
        print("Board size must be at least 3x3.")
        return

    # Initialize the chessboard with -1
    board = [[-1 for _ in range(N)] for _ in range(N)]

    # Possible moves for a knight
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Start from the first cell
    board[0][0] = 1

    # Track the best board state
    best_board = [[-1 for _ in range(N)] for _ in range(N)]
    best_moves = [1]  # Use a list to allow modification within the utility function

    # Start the tour from the first cell
    knights_tour_util(0, 0, 2, board, move_x, move_y, N, best_board, best_moves)

    if best_moves[0] == N * N:
        print("Complete solution found:")
    else:
        print("Solution does not exist. Best result achieved:")
    print_board(best_board, N)

def knights_tour_util(x, y, move_i, board, move_x, move_y, N, best_board, best_moves):
    """Utility function to solve the Knight's Tour problem using Warnsdorff's rule."""
    if move_i == N * N + 1:
        return True

    # Get all possible moves and sort them by Warnsdorff's rule
    possible_moves = []
    for i in range(8):
        next_x = x + move_x[i]
        next_y = y + move_y[i]
        if is_safe(next_x, next_y, board, N):
            degree = count_onward_moves(next_x, next_y, board, move_x, move_y, N)
            possible_moves.append((degree, next_x, next_y))

    possible_moves.sort()  # Sort by degree (Warnsdorff's rule)

    for _, next_x, next_y in possible_moves:
        board[next_x][next_y] = move_i
        if move_i > best_moves[0]:
            best_moves[0] = move_i
            for r in range(N):
                for c in range(N):
                    best_board[r][c] = board[r][c]
        if knights_tour_util(next_x, next_y, move_i + 1, board, move_x, move_y, N, best_board, best_moves):
            return True
        # Backtrack
        board[next_x][next_y] = -1

    return False

def count_onward_moves(x, y, board, move_x, move_y, N):
    """Count the number of onward moves from a given position."""
    count = 0
    for i in range(8):
        next_x = x + move_x[i]
        next_y = y + move_y[i]
        if is_safe(next_x, next_y, board, N):
            count += 1
    return count

# Set the size of the chessboard
N = 8
solve_knights_tour(N)