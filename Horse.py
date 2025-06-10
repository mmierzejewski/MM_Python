def is_safe(x, y, board, height, width):
    """Check if the position is safe for the knight to move."""
    return 0 <= x < height and 0 <= y < width and board[x][y] == -1

def print_board(board, height, width):
    """Print the chessboard."""
    print(f"Board dimensions: {height}x{width}")
    for row in board:
        print(' '.join(str(cell).rjust(2) for cell in row))
    print()

def solve_knights_tour(height, width):
    """Solve the Knight's Tour problem using backtracking and Warnsdorff's rule."""
    if height < 3 or width < 3:
        print("Board dimensions must be at least 3x3.")
        return

    # Initialize the chessboard with -1
    board = [[-1 for _ in range(width)] for _ in range(height)]

    # Possible moves for a knight
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Start from the first cell
    board[0][0] = 1

    # Track the best board state
    best_board = [[-1 for _ in range(width)] for _ in range(height)]
    best_moves = [1]  # Use a list to allow modification within the utility function

    # Start the tour from the first cell
    knights_tour_util(0, 0, 2, board, move_x, move_y, height, width, best_board, best_moves)

    if best_moves[0] == height * width:
        print("Complete solution found:")
    else:
        print("Solution does not exist. Best result achieved:")
    print_board(best_board, height, width)

def knights_tour_util(x, y, move_i, board, move_x, move_y, height, width, best_board, best_moves):
    """Utility function to solve the Knight's Tour problem using Warnsdorff's rule."""
    if move_i == height * width + 1:
        return True

    # Get all possible moves and sort them by Warnsdorff's rule
    possible_moves = []
    for i in range(8):
        next_x = x + move_x[i]
        next_y = y + move_y[i]
        if is_safe(next_x, next_y, board, height, width):
            degree = count_onward_moves(next_x, next_y, board, move_x, move_y, height, width)
            possible_moves.append((degree, next_x, next_y))

    possible_moves.sort()  # Sort by degree (Warnsdorff's rule)

    for _, next_x, next_y in possible_moves:
        board[next_x][next_y] = move_i
        if move_i > best_moves[0]:
            best_moves[0] = move_i
            for r in range(height):
                for c in range(width):
                    best_board[r][c] = board[r][c]
        if knights_tour_util(next_x, next_y, move_i + 1, board, move_x, move_y, height, width, best_board, best_moves):
            return True
        # Backtrack
        board[next_x][next_y] = -1

    return False

def count_onward_moves(x, y, board, move_x, move_y, height, width):
    """Count the number of onward moves from a given position."""
    count = 0
    for i in range(8):
        next_x = x + move_x[i]
        next_y = y + move_y[i]
        if is_safe(next_x, next_y, board, height, width):
            count += 1
    return count

# Set the dimensions of the chessboard
height = 8
width = 8
solve_knights_tour(height, width)