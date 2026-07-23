#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prime Number Generator using the Sieve of Eratosthenes.

Efficiently generates all prime numbers up to a given limit with
performance timing and detailed statistics. Includes a segmented sieve
for very large ranges.
"""

from datetime import datetime
from typing import Optional
import sys
import math
import logging


def generate_primes_segmented(limit: int, verbose: bool = False) -> list[int]:
    """
    Generates prime numbers using a segmented sieve for very large limits.
    Uses significantly less memory than the standard sieve.

    Args:
        limit: Upper bound for prime generation (inclusive)
        verbose: If True, displays progress

    Returns:
        A list of all prime numbers from 2 to limit

    Complexity:
        Time: O(n log log n)
        Memory: O(√n) instead of O(n)
    """
    if limit < 2:
        return []

    sqrt_limit = int(math.sqrt(limit))

    # Step 1: Find small primes up to √limit using the standard sieve
    if verbose:
        print(f"Phase 1/2: Finding base primes up to {sqrt_limit:,}...")

    result = generate_primes(sqrt_limit, verbose=False)

    # Step 2: Process segments
    segment_size = max(sqrt_limit, 1_000_000)  # At least 1M for performance
    low = sqrt_limit + 1

    total_segments = math.ceil((limit - sqrt_limit) / segment_size)

    if verbose:
        print(f"Phase 2/2: Processing {total_segments} segments of size {segment_size:,}...")

    segment_num = 0
    while low <= limit:
        high = min(low + segment_size - 1, limit)
        segment_num += 1

        # Create the segment sieve
        segment = [True] * (high - low + 1)

        # Mark multiples of the base primes within this segment
        for prime in result:
            if prime > sqrt_limit:
                break
            # Find the first multiple of the prime within [low, high]
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)

            for j in range(start, high + 1, prime):
                segment[j - low] = False

        # Collect primes from this segment
        for i in range(len(segment)):
            if segment[i]:
                result.append(low + i)

        if verbose:
            progress = (segment_num / total_segments) * 100
            print(f"Progress: {progress:.1f}% (processed up to {high:,})", end='\r', flush=True)

        low = high + 1

    if verbose:
        print(" " * 70, end='\r', flush=True)  # Clear the progress line

    return result


def generate_primes(limit: int, verbose: bool = False) -> list[int]:
    """
    Generates a list of prime numbers up to a given limit using the Sieve of Eratosthenes.

    Args:
        limit: Upper bound for prime generation (inclusive)
        verbose: If True, displays progress for large limits

    Returns:
        A list of all prime numbers from 2 to limit

    Raises:
        MemoryError: If the limit is too large for the available memory

    Complexity:
        Time: O(n log log n)
        Memory: O(n)
    """
    if limit < 2:
        return []

    try:
        # Initialize the sieve
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
    except MemoryError:
        estimated_mb = (limit + 1) / 1024 / 1024
        raise MemoryError(
            f"Not enough memory to create sieve for {limit:,}. "
            f"Estimated memory needed: ~{estimated_mb:.1f} MB"
        )

    sqrt_limit = math.isqrt(limit)

    # Sieve of Eratosthenes
    for i in range(2, sqrt_limit + 1):
        if is_prime[i]:
            # Mark multiples of i as composite
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

            if verbose and i % 1000 == 0:
                progress = (i / sqrt_limit) * 100
                print(f"Progress: {progress:.1f}% (checking {i:,})", end='\r', flush=True)

    if verbose:
        print(" " * 50, end='\r', flush=True)  # Clear the progress line

    # Extract the primes
    return [num for num, prime in enumerate(is_prime) if prime]


def get_divisors(n: int, exclude_trivial: bool = False) -> list[int]:
    """
    Finds all divisors of the given number.

    Args:
        n: The number to check
        exclude_trivial: If True, exclude 1 and the number n itself

    Returns:
        A list of all divisors of n

    Complexity:
        Time: O(√n)
    """
    if n < 1:
        return []
    
    divisors = []
    sqrt_n = int(math.sqrt(n))
    
    for i in range(1, sqrt_n + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:  # Avoid duplicates for perfect squares
                divisors.append(n // i)
    
    divisors = sorted(divisors)
    
    if exclude_trivial:
        # Remove 1 and the number n itself
        if len(divisors) > 2:
            return divisors[1:-1]
        else:
            # For prime numbers (only 1 and n), return an empty list
            return []
    
    return divisors


def is_prime(n: int) -> bool:
    """
    Checks whether the given number is prime.

    Args:
        n: The number to check

    Returns:
        True if the number is prime, False otherwise

    Complexity:
        Time: O(√n)
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to √n
    sqrt_n = int(math.sqrt(n))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    
    return True


def first_n_primes(n: int, verbose: bool = False) -> list[int]:
    """
    Generates the first n prime numbers.

    Args:
        n: The number of primes to generate
        verbose: If True, displays progress

    Returns:
        A list of the first n prime numbers

    Complexity:
        Uses the n * ln(n) approximation for the upper bound and generates primes
        using the standard sieve.
    """
    if n <= 0:
        return []
    if n == 1:
        return [2]
    if n == 2:
        return [2, 3]

    # Approximate upper bound for the n-th prime
    # For n >= 6: p_n < n * (ln(n) + ln(ln(n)))
    # We use a larger coefficient for safety
    if n < 6:
        limit = 15
    else:
        limit = int(n * (math.log(n) + math.log(math.log(n))) * 1.3)

    if verbose:
        print(f"Estimated limit for the first {n} primes: {limit:,}")

    primes = []
    while len(primes) < n:
        if verbose:
            print(f"Generating primes up to {limit:,}...", end='\r', flush=True)
        
        primes = generate_primes(limit, verbose=False)
        
        if len(primes) < n:
            # Increase the limit if not enough primes were found
            limit = int(limit * 1.5)
            if verbose:
                print(f"Increasing limit to {limit:,}...", end='\r', flush=True)

    if verbose:
        print(" " * 70, end='\r', flush=True)  # Clear the progress line

    return primes[:n]


def format_duration(duration) -> str:
    """Formats a duration in a human-readable format."""
    total_seconds = duration.total_seconds()

    if total_seconds < 0.001:
        return f"{total_seconds * 1_000_000:.2f} μs"
    elif total_seconds < 1:
        return f"{total_seconds * 1000:.2f} ms"
    elif total_seconds < 60:
        return f"{total_seconds:.3f} s"
    else:
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        return f"{minutes}m {seconds:.2f}s"


def display_timing(label: str, start: datetime, end: datetime) -> None:
    """Displays timing information for a process."""
    duration = end - start
    formatted_duration = format_duration(duration)
    print(f"⏱️  {label}: {formatted_duration}")


def get_user_choice() -> Optional[str]:
    """Gets the operation mode choice from the user.

    Returns:
        '1' for limit, '2' for first n, '3' to check a single number, '4' to exit, None if the choice is invalid
    """
    print("Choose the operation mode:")
    print("  1. Find all primes up to a given limit")
    print("  2. Find the first n primes")
    print("  3. Check whether a number is prime")
    print("  4. Exit (quit the program)")
    choice = input("\nYour choice (1/2/3/4): ").strip()
    
    if choice not in ['1', '2', '3', '4']:
        print("❌ Invalid choice!")
        return None
    
    return choice


def get_first_n_count() -> Optional[int]:
    """Gets and validates the number of primes to generate.

    Returns:
        The count n or None if cancelled/invalid
    """
    try:
        n_str = input("Enter the number of primes to generate (n >= 1): ").strip()
        n = int(n_str)

        if n < 1:
            print("❌ The number must be at least 1.")
            return None

        if n > 10_000_000:
            print(f"⚠️  VERY LARGE number ({n:,})!")
            print(f"   This may take a long time...")
            confirm = input("   Continue? (Y/N) [N]: ").strip().upper() or "N"
            if confirm != "Y":
                print("Operation cancelled.")
                return None
        elif n > 100_000:
            print(f"⚠️  Large number ({n:,}) may take some time!")
            confirm = input("   Continue? (Y/N) [N]: ").strip().upper() or "N"
            if confirm != "Y":
                print("Operation cancelled.")
                return None

        return n

    except ValueError:
        print("❌ Invalid input! Please enter a valid positive integer.")
        return None


def get_valid_limit() -> Optional[tuple[int, bool]]:
    """Gets and validates the limit from the user.

    Returns:
        A tuple (limit, use_segmented) or None if cancelled/invalid
    """
    try:
        limit_str = input("Enter the range (integer >= 2): ").strip()
        limit = int(limit_str)

        if limit < 2:
            print("❌ The range must be at least 2.")
            return None

        # Memory estimate: ~1 byte per number
        estimated_mb = limit / 1024 / 1024

        if limit > 1_000_000_000:
            print(f"⚠️  VERY LARGE range ({limit:,})!")
            sqrt_limit = int(math.sqrt(limit))
            segmented_mb = sqrt_limit / 1024 / 1024
            print(f"   Standard sieve: ~{estimated_mb:.0f} MB (~{estimated_mb/1024:.1f} GB)")
            print(f"   Segmented sieve: ~{segmented_mb:.0f} MB (recommended!)")
            print(f"\n   💡 The segmented sieve uses significantly less memory for large ranges")
            confirm = input("   Use the segmented sieve? (Y/N) [Y]: ").strip().upper() or "Y"
            if confirm != "Y":
                print("Operation cancelled.")
                return None
            return (limit, True)  # Return the tuple: (limit, use_segmented)
        elif limit > 10_000_000:
            print(f"⚠️  Large range ({limit:,}) may require significant time and memory!")
            print(f"   Estimated memory: ~{estimated_mb:.0f} MB")
            confirm = input("   Continue? (Y/N) [N]: ").strip().upper() or "N"
            if confirm != "Y":
                print("Operation cancelled.")
                return None

        return (limit, False)  # Return the tuple: (limit, use_segmented)

    except ValueError:
        print("❌ Invalid input! Please enter a valid positive integer.")
        return None


def save_primes_to_file(primes: list[int], limit: int, filename: Optional[str] = None) -> None:
    """Saves the prime numbers to a text file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Save in the directory where the script is located (PNA/)
        script_dir = sys.path[0] if sys.path[0] else '.'
        filename = f"{script_dir}/primes_up_to_{limit}_{timestamp}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Primes up to {limit:,}\n")
            f.write(f"Number found: {len(primes):,}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            # Write the primes, 10 per line
            for i in range(0, len(primes), 10):
                line = ', '.join(map(str, primes[i:i+10]))
                f.write(line + '\n')

        print(f"✅ Primes saved to: {filename}")
    except IOError as e:
        print(f"❌ Error while writing the file: {e}")


def analyze_primes(primes: list[int], limit: Optional[int] = None, first_n: Optional[int] = None) -> None:
    """Displays a detailed analysis of the primes found.

    Args:
        primes: The list of primes
        limit: The upper limit used for generation (for limit mode)
        first_n: The number of first n primes (for first n mode)
    """
    if not primes:
        print("\n📊 No primes found in this range.")
        return

    prime_count = len(primes)

    print(f"\n{'='*60}")
    print("📊 PRIME NUMBER STATISTICS")
    print(f"{'='*60}")
    
    if first_n is not None:
        print(f"Mode:                First {first_n:,} primes")
        print(f"Found:               {prime_count:,}")
    else:
        print(f"Range:               2 to {limit:,}")
        print(f"Primes:              {prime_count:,}")
        if limit:
            density = (prime_count / limit) * 100
            print(f"Density:             {density:.4f}%")
    
    print(f"Smallest:            {primes[0]:,}")
    print(f"Largest:             {primes[-1]:,}")

    # Show the first and last primes
    if prime_count <= 20:
        print(f"All numbers:         {', '.join(map(str, primes))}")
    elif prime_count <= 100:
        first_10 = ', '.join(map(str, primes[:10]))
        last_10 = ', '.join(map(str, primes[-10:]))
        print(f"First 10:            {first_10}")
        print(f"Last 10:             {last_10}")

    print(f"{'='*60}\n")

    # Ask the user whether to save after displaying the statistics
    save_option = input("💾 Save the primes to a file? (Y/N) [N]: ").strip().upper() or "N"
    if save_option == "Y":
        if first_n is not None:
            save_primes_to_file(primes, primes[-1], filename=None)
        else:
            save_primes_to_file(primes, limit)


def main() -> int:
    """
    Main function that runs the prime number generator.

    Returns:
        0 on success, 1 on error
    """
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 18 + "PRIME NUMBER GENERATOR" + " " * 18 + "║")
    print("║" + " " * 17 + "(Sieve of Eratosthenes)" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # Main program loop
    while True:
        # Get the mode choice
        choice = get_user_choice()
        if choice is None:
            continue  # Invalid choice, show the menu again
        
        # Exit option
        if choice == '4':
            print("\n👋 Goodbye!")
            return 0

        print()  # Add a blank line

        if choice == '1':
            # Mode: primes up to a limit
            result = get_valid_limit()
            if result is None:
                print()  # Add a blank line before returning to the menu
                continue

            # Unpack the result - can be (limit, use_segmented) or just a limit
            if isinstance(result, tuple):
                limit, use_segmented = result
            else:
                limit, use_segmented = result, False

            print(f"\n🔍 Searching for primes up to {limit:,}...")
            if use_segmented:
                print("   Using segmented sieve (memory optimization)")

            # Generate primes while timing the operation
            start_time = datetime.now()
            verbose = limit > 1_000_000

            try:
                if use_segmented:
                    primes = generate_primes_segmented(limit, verbose=verbose)
                else:
                    primes = generate_primes(limit, verbose=verbose)
            except MemoryError as e:
                print(f"\n❌ Memory error: {e}")
                print("\n💡 Suggestions:")
                print("   • Try a smaller range")
                print("   • Use the segmented sieve option for large ranges")
                print("   • Close other applications to free up memory")
                print()  # Add a blank line before returning to the menu
                continue

            end_time = datetime.now()

            # Display the results
            display_timing("Generation time", start_time, end_time)
            analyze_primes(primes, limit=limit)
            print()  # Add a blank line before returning to the menu

        elif choice == '2':
            # Mode: first n primes
            n = get_first_n_count()
            if n is None:
                print()  # Add a blank line before returning to the menu
                continue

            print(f"\n🔍 Searching for the first {n:,} primes...")

            # Generate the first n primes while timing the operation
            start_time = datetime.now()
            verbose = n > 10_000

            try:
                primes = first_n_primes(n, verbose=verbose)
            except MemoryError as e:
                print(f"\n❌ Memory error: {e}")
                print("\n💡 Suggestion: Try a smaller value of n")
                print()  # Add a blank line before returning to the menu
                continue

            end_time = datetime.now()

            # Display the results
            display_timing("Generation time", start_time, end_time)
            analyze_primes(primes, first_n=n)
            print()  # Add a blank line before returning to the menu

        else:
            # Mode: check whether a number is prime
            try:
                n_str = input("Enter the number to check: ").strip()
                n = int(n_str)

                print(f"\n🔍 Checking whether {n:,} is a prime number...")

                start_time = datetime.now()
                result = is_prime(n)
                end_time = datetime.now()

                print(f"\n{'='*60}")
                if result:
                    print(f"✅ {n:,} IS a prime number")
                else:
                    print(f"❌ {n:,} is NOT a prime number")
                    
                    # Find and display the divisors (excluding 1 and the number itself)
                    divisors = get_divisors(n, exclude_trivial=True)
                    if divisors:
                        print(f"\n📋 Divisors of {n:,} (excluding 1 and {n:,}):")
                        
                        # Display the divisors in a readable format
                        if len(divisors) <= 20:
                            print(f"   {', '.join(map(str, divisors))}")
                        else:
                            # For a large number of divisors, show the first and last
                            first_10 = ', '.join(map(str, divisors[:10]))
                            last_10 = ', '.join(map(str, divisors[-10:]))
                            print(f"   First 10: {first_10}")
                            print(f"   ...")
                            print(f"   Last 10: {last_10}")
                        
                        print(f"   Number of proper divisors: {len(divisors)}")
                    else:
                        print(f"\n📋 No proper divisors (prime number or error)")
                print(f"{'='*60}")

                display_timing("Check time", start_time, end_time)
                print()  # Add a blank line before returning to the menu

            except ValueError:
                print("❌ Invalid input! Please enter a valid integer.")
                print()  # Add a blank line before returning to the menu
                continue


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)