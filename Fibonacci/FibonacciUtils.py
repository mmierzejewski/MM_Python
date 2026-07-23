#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FibonacciUtils - Utilities for generating and analyzing the Fibonacci sequence.

Fibonacci sequence: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)

All functions use consistent 0-based indexing:
F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5...
"""

from typing import List, Union, Optional
from functools import lru_cache
from datetime import datetime
from pathlib import Path
import logging
import sys

# Logging configuration
log_file = Path.cwd() / 'fibonacci.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)

# Mathematical constants
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2  # φ ≈ 1.618033988749...


class FibonacciError(Exception):
    """Exception for errors related to the Fibonacci sequence."""
    pass


def generate_fibonacci_upto(max_value: int) -> List[int]:
    """
    Generates Fibonacci numbers up to a given maximum value.

    Args:
        max_value: Maximum value (inclusive)

    Returns:
        List of Fibonacci numbers <= max_value

    Raises:
        FibonacciError: When max_value < 0

    Example:
        >>> generate_fibonacci_upto(10)
        [0, 1, 1, 2, 3, 5, 8]
    """
    if max_value < 0:
        raise FibonacciError("The maximum value must be non-negative!")

    if max_value == 0:
        return [0]

    fib_prev, fib_curr = 0, 1
    results = [0]

    while fib_curr <= max_value:
        results.append(fib_curr)
        fib_prev, fib_curr = fib_curr, fib_prev + fib_curr

    return results


def get_nth_fibonacci(n: int, zero_indexed: bool = True) -> int:
    """
    Returns the nth Fibonacci number.

    Args:
        n: Position in the sequence
        zero_indexed: If True (default): F(0)=0, F(1)=1, F(2)=1...
                     If False: F(1)=0, F(2)=1, F(3)=1... (backwards compatibility)

    Returns:
        The nth Fibonacci number

    Raises:
        FibonacciError: When n < 0 (0-indexed) or n <= 0 (1-indexed)

    Example:
        >>> get_nth_fibonacci(6)  # 0-indexed
        8
        >>> get_nth_fibonacci(7, zero_indexed=False)  # 1-indexed
        8
    """
    if zero_indexed:
        if n < 0:
            raise FibonacciError("Position must be a non-negative integer!")
        actual_n = n
    else:
        if n <= 0:
            raise FibonacciError("Position must be a positive integer!")
        actual_n = n - 1
    
    logging.info(f"Calculating F({actual_n})")
    
    if actual_n == 0:
        return 0
    if actual_n == 1:
        return 1

    fib_prev, fib_curr = 0, 1
    for _ in range(2, actual_n + 1):
        fib_prev, fib_curr = fib_curr, fib_prev + fib_curr

    return fib_curr


def generate_first_n_fibonacci(n: int) -> List[int]:
    """
    Generates the first n Fibonacci numbers.

    Args:
        n: Number of elements to generate

    Returns:
        List of the first n Fibonacci numbers

    Raises:
        FibonacciError: When n < 0

    Example:
        >>> generate_first_n_fibonacci(5)
        [0, 1, 1, 2, 3]
    """
    if n < 0:
        raise FibonacciError("The number of elements cannot be negative!")

    if n == 0:
        return []
    if n == 1:
        return [0]

    results = [0, 1]

    for _ in range(2, n):
        results.append(results[-1] + results[-2])

    return results


@lru_cache(maxsize=1024)
def fibonacci_fast(n: int) -> int:
    """
    Fast calculation of the nth Fibonacci number using the matrix method.
    Complexity: O(log n)
    Uses memoization (@lru_cache) for optimization.

    Args:
        n: Position in the sequence (0-indexed: F(0)=0, F(1)=1, F(2)=1...)

    Returns:
        The nth Fibonacci number
    """
    logging.info(f"fibonacci_fast: calculating F({n})")
    
    if n < 0:
        return 0
    if n == 0:
        return 0
    if n == 1:
        return 1

    def matrix_multiply(a, b):
        """Multiplies two 2x2 matrices."""
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0],
             a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0],
             a[1][0] * b[0][1] + a[1][1] * b[1][1]]
        ]

    def matrix_power(matrix, n):
        """Raises a matrix to the power n using fast exponentiation."""
        if n == 1:
            return matrix
        if n % 2 == 0:
            half = matrix_power(matrix, n // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, n - 1))

    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    return result_matrix[0][1]


def is_fibonacci(num: int) -> bool:
    """
    Checks whether a number belongs to the Fibonacci sequence.

    A number n is a Fibonacci number if and only if
    5*n^2 + 4 or 5*n^2 - 4 is a perfect square.

    Args:
        num: Number to check

    Returns:
        True if num is a Fibonacci number
    """
    if num < 0:
        return False

    def is_perfect_square(x):
        root = int(x ** 0.5)
        return root * root == x

    return is_perfect_square(5 * num * num + 4) or \
           is_perfect_square(5 * num * num - 4)


def export_fibonacci_sequence(sequence: List[int], filename: Optional[str] = None) -> None:
    """
    Exports the Fibonacci sequence to a text file.
    
    Args:
        sequence: List of Fibonacci numbers
        filename: File name (optional, defaults to a timestamped name)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fibonacci_sequence_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Fibonacci sequence\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Number of elements: {len(sequence)}\n")
            f.write("=" * 60 + "\n\n")
            
            # Write numbers, 10 per line
            for i in range(0, len(sequence), 10):
                line = ', '.join(map(str, sequence[i:i+10]))
                f.write(f"F({i})-F({min(i+9, len(sequence)-1)}): {line}\n")
            
            # Statistics
            if sequence:
                f.write("\n" + "=" * 60 + "\n")
                f.write("STATISTICS:\n")
                f.write(f"Smallest: {min(sequence):,}\n")
                f.write(f"Largest: {max(sequence):,}\n")
                f.write(f"Sum: {sum(sequence):,}\n")
                if len(sequence) > 1:
                    ratio = sequence[-1] / sequence[-2] if sequence[-2] != 0 else 0
                    f.write(f"Last ratio: {ratio:.10f}\n")
                    f.write(f"Golden ratio φ: {GOLDEN_RATIO:.10f}\n")
        
        print(f"✅ Exported to: {filename}")
        logging.info(f"Exported sequence to {filename}")
    except IOError as e:
        print(f"❌ File write error: {e}")
        logging.error(f"Export error: {e}")


def print_fibonacci_info(n: int, zero_indexed: bool = True) -> None:
    """
    Displays detailed information about the nth Fibonacci number.
    
    Args:
        n: Position in the sequence
        zero_indexed: Indexing (0-based by default)
    """
    try:
        fib_n = get_nth_fibonacci(n, zero_indexed=zero_indexed)
        display_n = n if zero_indexed else n - 1
        fib_seq = generate_first_n_fibonacci(display_n + 1 if display_n >= 0 else 1)

        print(f"\n{'=' * 60}")
        print(f"📊 INFORMATION ABOUT F({display_n})")
        print(f"{'=' * 60}")
        print(f"Value: {fib_n:,}")
        print(f"Number of digits: {len(str(fib_n))}")
        print(f"Sequence up to F({display_n}): {fib_seq[:10]}{'...' if len(fib_seq) > 10 else ''}")

        if len(fib_seq) > 1 and fib_seq[-2] != 0:
            ratio = fib_seq[-1] / fib_seq[-2]
            print(f"Ratio F({display_n})/F({display_n-1}): {ratio:.10f}")
            print(f"Golden ratio φ: {GOLDEN_RATIO:.10f}")
            print(f"Difference: {abs(ratio - GOLDEN_RATIO):.10e}")

        print(f"{'=' * 60}\n")
        logging.info(f"Displayed information for F({display_n}) = {fib_n}")
    except FibonacciError as e:
        print(f"❌ Error: {e}")
        logging.error(f"Error in print_fibonacci_info: {e}")


def main() -> None:
    """Main program function."""
    print("=" * 60)
    print("🔢 FIBONACCI SEQUENCE CALCULATOR".center(60))
    print("=" * 60)
    print("📌 All functions use 0-based indexing")
    print("   (F(0)=0, F(1)=1, F(2)=1, F(3)=2...)\n")
    
    logging.info("Fibonacci calculator started")
    
    # Store the last sequence for export
    last_sequence: List[int] = []

    while True:
        print("\nChoose an option:")
        print("1. Generate Fibonacci numbers up to a value")
        print("2. Get the nth Fibonacci number (0-indexed)")
        print("3. Generate the first n Fibonacci numbers")
        print("4. Fast calculation (O(log n) algorithm)")
        print("5. Check whether a number is a Fibonacci number")
        print("6. Detailed information about F(n)")
        print("7. Export the last sequence to a file")
        print("8. Quit (exit the program)")

        try:
            choice = input("\n👉 Your choice (1-8): ").strip()

            if choice == "8":
                print("\n👋 Goodbye!")
                logging.info("Calculator terminated")
                break

            elif choice == "1":
                max_val = int(input("Enter the maximum value: "))
                result = generate_fibonacci_upto(max_val)
                print(f"\n✅ Fibonacci numbers ≤ {max_val}:")
                print(f"   {result}")
                print(f"   Found: {len(result)} numbers")

            elif choice == "2":
                n = int(input("Enter position n (0-indexed, e.g. F(0)=0, F(6)=8): "))
                result = get_nth_fibonacci(n, zero_indexed=True)
                print(f"\n✅ F({n}) = {result:,}")
                last_sequence = [result]

            elif choice == "3":
                n = int(input("How many numbers to generate: "))
                result = generate_first_n_fibonacci(n)
                last_sequence = result
                if len(result) <= 20:
                    print(f"\n✅ First {n} numbers: {result}")
                else:
                    show_all = input("Show all numbers? (Y/N) [N]: ").strip().upper()
                    if show_all == "Y":
                        print(f"\n✅ All {n} numbers:")
                        # Display numbers, 10 per line
                        for i in range(0, len(result), 10):
                            line = ', '.join(map(str, result[i:i+10]))
                            print(f"   F({i})-F({min(i+9, len(result)-1)}): {line}")
                    else:
                        print(f"\n✅ First 10: {result[:10]}")
                        print(f"   Last 10: {result[-10:]}")
                        print(f"   ({len(result) - 20} middle numbers omitted)")

            elif choice == "4":
                n = int(input("Enter n (0-indexed, for large n): "))
                result = fibonacci_fast(n)
                print(f"\n✅ F({n}) = {result:,}")
                print(f"   Number of digits: {len(str(result))}")
                last_sequence = [result]

            elif choice == "5":
                num = int(input("Enter the number to check: "))
                if is_fibonacci(num):
                    print(f"\n✅ {num:,} IS a Fibonacci number!")
                else:
                    print(f"\n❌ {num:,} is NOT a Fibonacci number.")

            elif choice == "6":
                n = int(input("Enter n (0-indexed): "))
                print_fibonacci_info(n, zero_indexed=True)
            
            elif choice == "7":
                if not last_sequence:
                    print("\n❌ No sequence to export! Generate numbers first.")
                else:
                    export_choice = input("\nExport to a file? (Y/N) [Y]: ").strip().upper() or "Y"
                    if export_choice == "Y":
                        custom_name = input("File name (Enter = auto): ").strip()
                        export_fibonacci_sequence(
                            last_sequence,
                            custom_name if custom_name else None
                        )

            else:
                print("\n❌ Invalid choice! Choose 1-8.")

        except ValueError as e:
            print("\n❌ Invalid input! Enter an integer.")
            logging.warning(f"ValueError: {e}")
        except FibonacciError as e:
            print(f"\n❌ Error: {e}")
            logging.error(f"FibonacciError: {e}")
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user.")
            logging.info("Interrupted by user (KeyboardInterrupt)")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            logging.error(f"Unexpected error: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        logging.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)