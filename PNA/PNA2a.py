#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prime Number Generator using Sieve of Eratosthenes.

Efficiently generates all prime numbers up to a given limit with
performance timing and detailed statistics.
"""

from datetime import datetime
from typing import Optional
import sys


def generate_primes(limit: int, verbose: bool = False) -> list[int]:
    """
    Generate a list of prime numbers up to a given limit using the Sieve of Eratosthenes.

    Args:
        limit: Upper bound for prime generation (inclusive)
        verbose: If True, print progress for large limits

    Returns:
        List of all prime numbers from 2 to limit

    Complexity:
        Time: O(n log log n)
        Space: O(n)
    """
    if limit < 2:
        return []

    # Initialize sieve
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    sqrt_limit = int(limit ** 0.5)

    # Sieve of Eratosthenes
    for i in range(2, sqrt_limit + 1):
        if is_prime[i]:
            # Mark multiples of i as composite
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

            if verbose and i % 1000 == 0:
                progress = (i / sqrt_limit) * 100
                print(f"Progress: {progress:.1f}% (checking {i})", end='\r')

    if verbose:
        print(" " * 50, end='\r')  # Clear progress line

    # Extract primes
    return [num for num, prime in enumerate(is_prime) if prime]


def format_duration(duration) -> str:
    """Format duration in human-readable format."""
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
    """Display timing information for a process."""
    duration = end - start
    formatted_duration = format_duration(duration)
    print(f"⏱️  {label}: {formatted_duration}")


def get_valid_limit() -> Optional[int]:
    """Get and validate limit from user input."""
    try:
        limit_str = input("Enter the range (positive integer >= 2): ").strip()
        limit = int(limit_str)

        if limit < 2:
            print("❌ The range must be at least 2.")
            return None

        if limit > 10_000_000:
            print(f"⚠️  Large limit ({limit:,}) may take significant time and memory!")
            confirm = input("   Continue? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Operation cancelled.")
                return None

        return limit

    except ValueError:
        print("❌ Invalid input! Please enter a valid positive integer.")
        return None
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Operation cancelled by user.")
        return None


def analyze_primes(primes: list[int], limit: int) -> None:
    """Display detailed analysis of found primes."""
    if not primes:
        print("\n📊 No primes found in this range.")
        return

    prime_count = len(primes)
    density = (prime_count / limit) * 100

    print(f"\n{'='*60}")
    print("📊 PRIME STATISTICS")
    print(f"{'='*60}")
    print(f"Range:           2 to {limit:,}")
    print(f"Total primes:    {prime_count:,}")
    print(f"Density:         {density:.4f}%")
    print(f"Smallest prime:  {primes[0]:,}")
    print(f"Largest prime:   {primes[-1]:,}")

    # Show first and last few primes
    if prime_count <= 10:
        print(f"All primes:      {', '.join(map(str, primes))}")
    else:
        first_few = ', '.join(map(str, primes[:5]))
        last_few = ', '.join(map(str, primes[-5:]))
        print(f"First 5:         {first_few}")
        print(f"Last 5:          {last_few}")

    print(f"{'='*60}\n")


def main() -> int:
    """
    Main function to run the prime number generator.

    Returns:
        0 on success, 1 on error
    """
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "PRIME NUMBER GENERATOR" + " " * 26 + "║")
    print("║" + " " * 10 + "(Sieve of Eratosthenes)" + " " * 25 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # Get input
    limit = get_valid_limit()
    if limit is None:
        return 1

    print(f"\n🔍 Searching for primes up to {limit:,}...")

    # Generate primes with timing
    start_time = datetime.now()
    verbose = limit > 1_000_000
    primes = generate_primes(limit, verbose=verbose)
    end_time = datetime.now()

    # Display results
    display_timing("Generation time", start_time, end_time)
    analyze_primes(primes, limit)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)