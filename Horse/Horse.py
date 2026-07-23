#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knight's Tour Problem - finding the route of a chess knight.

The problem is to find a sequence of knight moves that visits
every square of the chessboard exactly once.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import logging
import time
import signal


# Logging configuration
log_file = Path(__file__).parent / 'knights_tour.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)

# Type aliases
Board = List[List[int]]

# Constants
UNVISITED = -1
START_POSITION = 1
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


@dataclass
class SolutionStats:
    """Solution statistics."""
    time_elapsed: float = 0.0
    backtracks: int = 0
    max_depth: int = 0
    total_attempts: int = 0
    timeout_occurred: bool = False


@dataclass
class BoardState:
    """Board state used to track the best solution found."""
    board: Board
    moves_count: int


class KnightsTour:
    """Solves the chess knight's tour problem."""

    def __init__(self, height: int, width: int, verbose: bool = False):
        """
        Initializes the solver for the given board size.

        Args:
            height: Board height
            width: Board width
            verbose: Whether to display detailed logs

        Raises:
            ValueError: If the dimensions are invalid
        """
        if not isinstance(height, int) or not isinstance(width, int):
            raise ValueError("Board dimensions must be integers")

        if height < 3 or width < 3:
            raise ValueError("Board dimensions must be >= 3x3")

        self.height = height
        self.width = width
        self.verbose = verbose
        self.board: Board = [[UNVISITED] * width for _ in range(height)]
        self.best_state = BoardState(
            board=[[UNVISITED] * width for _ in range(height)],
            moves_count=START_POSITION
        )
        self.stats = SolutionStats()
        self.start_time = 0.0
        self.timeout_limit = 300  # 5 minutes by default
        
        logging.info(f"Created solver for a {height}x{width} board")
        self.stats = SolutionStats()
        self.start_time = 0.0
        self.timeout_limit = 300  # 5 minutes by default
        
        logging.info(f"Created solver for a {height}x{width} board")

    def is_safe(self, x: int, y: int) -> bool:
        """Checks whether a position is safe for the knight."""
        return (0 <= x < self.height and
                0 <= y < self.width and
                self.board[x][y] == UNVISITED)

    def count_onward_moves(self, x: int, y: int) -> int:
        """
        Counts the number of possible moves from a given position (Warnsdorff's heuristic).

        Args:
            x, y: Position coordinates

        Returns:
            Number of possible moves
        """
        count = 0
        for dx, dy in KNIGHT_MOVES:
            if self.is_safe(x + dx, y + dy):
                count += 1
        return count

    def get_possible_moves(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        """
        Returns possible moves sorted according to Warnsdorff's heuristic.

        Args:
            x, y: Current position

        Returns:
            List of tuples (degree, next_x, next_y)
        """
        possible_moves = []
        for dx, dy in KNIGHT_MOVES:
            next_x, next_y = x + dx, y + dy
            if self.is_safe(next_x, next_y):
                degree = self.count_onward_moves(next_x, next_y)
                possible_moves.append((degree, next_x, next_y))

        return sorted(possible_moves)  # Sort by degree (Warnsdorff)

    def update_best_state(self, move_num: int) -> None:
        """Updates the best solution found so far."""
        if move_num > self.best_state.moves_count:
            self.best_state.moves_count = move_num
            for r in range(self.height):
                self.best_state.board[r] = self.board[r].copy()

            if self.verbose:
                progress = (move_num / (self.height * self.width)) * 100
                print(f"Progress: {move_num}/{self.height * self.width} ({progress:.1f}%)")

    def solve_recursive(self, x: int, y: int, move_num: int, depth: int = 0) -> bool:
        """
        Recursive function that solves the problem using backtracking.

        Args:
            x, y: Current position
            move_num: Number of the current move
            depth: Recursion depth (for statistics)

        Returns:
            True if a complete solution was found
        """
        # Check timeout
        if time.time() - self.start_time > self.timeout_limit:
            self.stats.timeout_occurred = True
            logging.warning(f"Time limit exceeded ({self.timeout_limit}s)")
            raise TimeoutError(f"Time limit of {self.timeout_limit}s exceeded")
        
        # Update statistics
        self.stats.max_depth = max(self.stats.max_depth, depth)
        self.stats.total_attempts += 1
        
        # Have we visited all squares?
        if move_num == self.height * self.width + 1:
            logging.info("Complete solution found!")
            return True

        # Get possible moves (sorted according to Warnsdorff)
        for _, next_x, next_y in self.get_possible_moves(x, y):
            # Make the move
            self.board[next_x][next_y] = move_num
            self.update_best_state(move_num)

            # Recurse
            if self.solve_recursive(next_x, next_y, move_num + 1, depth + 1):
                return True

            # Backtrack
            self.board[next_x][next_y] = UNVISITED
            self.stats.backtracks += 1

        return False

    def solve(self, start_x: int = 0, start_y: int = 0, timeout: int = 300) -> bool:
        """
        Solves the knight's tour problem.

        Args:
            start_x, start_y: Starting position of the knight
            timeout: Time limit in seconds (default 300s = 5min)

        Returns:
            True if a complete solution was found
        """
        if not (0 <= start_x < self.height and 0 <= start_y < self.width):
            raise ValueError("Starting position is outside the board")

        self.timeout_limit = timeout
        self.start_time = time.time()
        
        # Set the starting position
        self.board[start_x][start_y] = START_POSITION
        self.update_best_state(START_POSITION)

        print(f"Solving for a {self.height}x{self.width} board...")
        logging.info(f"Starting to solve: board {self.height}x{self.width}, start=({start_x},{start_y}), timeout={timeout}s")

        # Start solving
        try:
            solution_found = self.solve_recursive(start_x, start_y, START_POSITION + 1, depth=0)
        except TimeoutError:
            solution_found = False
        
        self.stats.time_elapsed = time.time() - self.start_time
        logging.info(f"Finished after {self.stats.time_elapsed:.2f}s")

        return solution_found

    def print_board(self, board: Optional[List[List[int]]] = None) -> None:
        """Displays the board."""
        if board is None:
            board = self.best_state.board

        print(f"\nBoard {self.height}x{self.width}:")
        print("┌" + "─" * (self.width * 3 + 1) + "┐")

        for row in board:
            print("│ " + ' '.join(str(cell).rjust(2) for cell in row) + " │")

        print("└" + "─" * (self.width * 3 + 1) + "┘")

    def print_result(self) -> None:
        """Displays the solution result."""
        total_cells = self.height * self.width

        if self.best_state.moves_count == total_cells:
            print("\n✓ Complete solution found!")
            logging.info("Complete solution found")
        else:
            coverage = (self.best_state.moves_count / total_cells) * 100
            print(f"\n✗ No complete solution found.")
            print(f"  Best result: {self.best_state.moves_count}/{total_cells} "
                  f"({coverage:.1f}% of the board)")
            logging.info(f"Partial solution: {self.best_state.moves_count}/{total_cells} ({coverage:.1f}%)")
        
        if self.stats.timeout_occurred:
            print(f"  ⏱️  Stopped after {self.stats.time_elapsed:.2f}s (timeout)")

        self.print_board()
        self.print_stats()
    
    def print_stats(self) -> None:
        """Displays solution statistics."""
        print(f"\n📊 Statistics:")
        print(f"  Execution time: {self.stats.time_elapsed:.2f}s")
        print(f"  Number of attempts: {self.stats.total_attempts:,}")
        print(f"  Backtracks: {self.stats.backtracks:,}")
        print(f"  Maximum depth: {self.stats.max_depth}")
        
        if self.stats.total_attempts > 0:
            success_rate = (1 - self.stats.backtracks / self.stats.total_attempts) * 100
            print(f"  Success rate: {success_rate:.1f}%")
    
    def export_solution(self, filename: Optional[str] = None) -> None:
        """Exports the solution to a file.
        
        Args:
            filename: File name (optional, defaults to a timestamped name)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Save in the directory where the script is located (Horse/)
            script_dir = Path(__file__).parent
            filename = script_dir / f"knights_tour_{self.height}x{self.width}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Knight's Tour Solution\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Board: {self.height}x{self.width}\n")
                f.write(f"="*60 + "\n\n")
                
                # Board
                total_cells = self.height * self.width
                if self.best_state.moves_count == total_cells:
                    f.write("✓ COMPLETE SOLUTION\n\n")
                else:
                    coverage = (self.best_state.moves_count / total_cells) * 100
                    f.write(f"✗ Partial solution: {self.best_state.moves_count}/{total_cells} ({coverage:.1f}%)\n\n")
                
                # Board visualization
                for row in self.best_state.board:
                    f.write(' '.join(str(cell).rjust(3) for cell in row) + '\n')
                
                # Statistics
                f.write("\n" + "="*60 + "\n")
                f.write("STATISTICS:\n")
                f.write(f"Execution time: {self.stats.time_elapsed:.2f}s\n")
                f.write(f"Number of attempts: {self.stats.total_attempts:,}\n")
                f.write(f"Backtracks: {self.stats.backtracks:,}\n")
                f.write(f"Maximum recursion depth: {self.stats.max_depth}\n")
                if self.stats.timeout_occurred:
                    f.write(f"Status: TIMEOUT after {self.timeout_limit}s\n")
            
            print(f"\n✅ Exported to: {filename}")
            logging.info(f"Exported solution to {filename}")
        except IOError as e:
            print(f"\n❌ File write error: {e}")
            logging.error(f"Export error: {e}")


def get_user_choice() -> Optional[str]:
    """Gets the user's choice: solve the problem or exit.
    
    Returns:
        '1' to solve, '2' to exit, None if the choice is invalid
    """
    print("\nChoose an option:")
    print("  1. Solve the knight's tour problem")
    print("  2. Quit (exit the program)")
    choice = input("\nYour choice (1/2): ").strip()
    
    if choice not in ['1', '2']:
        print("❌ Invalid choice!")
        return None
    
    return choice


def get_board_dimensions():
    """Gets and validates the board dimensions from the user."""
    while True:
        try:
            height = int(input("Enter board height (min 3, recommended max 8): ").strip())
            width = int(input("Enter board width (min 3, recommended max 8): ").strip())

            if height < 3 or width < 3:
                print("⚠️  Board dimensions must be >= 3. Please try again.\n")
                continue

            if height > 10 or width > 10:
                print(f"⚠️  A large board {height}x{width} may take a very long time!")
                confirm = input("   Continue? (Y/N) [N]: ").strip().upper() or "N"
                if confirm != "Y":
                    continue

            return height, width

        except ValueError:
            print("❌ Please enter integers!\n")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Cancelled.")
            return None


def main():
    """Main program function."""
    print("=== Knight's Tour Problem ===")
    logging.info("Started the Knight's Tour program")

    # Main program loop
    while True:
        choice = get_user_choice()
        if choice is None:
            continue  # Invalid choice, show the menu again
        
        # Exit option
        if choice == '2':
            print("\n👋 Goodbye!")
            logging.info("Program terminated by the user")
            return

        # Solving the problem
        dimensions = get_board_dimensions()
        if dimensions is None:
            print()  # Add an empty line before returning to the menu
            continue
        
        height, width = dimensions

        print(f"\n{'='*50}")
        try:
            solver = KnightsTour(height, width, verbose=True)
            solver.solve(start_x=0, start_y=0, timeout=300)
            solver.print_result()
            
            # Export option
            export = input("\nExport the solution to a file? (Y/N) [Y]: ").strip().upper() or "Y"
            if export == "Y":
                custom_name = input("File name (Enter = auto): ").strip()
                solver.export_solution(custom_name if custom_name else None)
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            logging.error(f"ValueError: {e}")
        except TimeoutError as e:
            print(f"⏱️  {e}")
            logging.error(f"TimeoutError: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            logging.error(f"Unexpected error: {e}", exc_info=True)
        
        print(f"{'='*50}\n")
        # The program returns to the main menu


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by the user.")
        logging.info("Interrupted by the user (KeyboardInterrupt)")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        logging.critical(f"Critical error: {e}", exc_info=True)