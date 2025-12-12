#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prime Number Generator using Sieve of Eratosthenes.

Efficiently generates all prime numbers up to a given limit with
performance timing and detailed statistics. Includes segmented sieve
for very large ranges.
"""

from datetime import datetime
from typing import Optional
import sys
import math


def generate_primes_segmented(limit: int, verbose: bool = False) -> list[int]:
    """
    Generate primes using segmented sieve for very large limits.
    Uses much less memory than standard sieve.

    Args:
        limit: Upper bound for prime generation (inclusive)
        verbose: If True, print progress

    Returns:
        List of all prime numbers from 2 to limit

    Complexity:
        Time: O(n log log n)
        Space: O(√n) instead of O(n)
    """
    if limit < 2:
        return []

    sqrt_limit = int(math.sqrt(limit))

    # Step 1: Find small primes up to √limit using standard sieve
    if verbose:
        print(f"Phase 1/2: Finding base primes up to {sqrt_limit:,}...")

    small_primes = generate_primes(sqrt_limit, verbose=False)
    result = small_primes.copy()

    # Step 2: Process segments
    segment_size = max(sqrt_limit, 1_000_000)  # At least 1M for efficiency
    low = sqrt_limit + 1

    total_segments = math.ceil((limit - sqrt_limit) / segment_size)

    if verbose:
        print(f"Phase 2/2: Processing {total_segments} segments of size {segment_size:,}...")

    segment_num = 0
    while low <= limit:
        high = min(low + segment_size - 1, limit)
        segment_num += 1

        # Create segment sieve
        segment = [True] * (high - low + 1)

        # Mark multiples of small primes in this segment
        for prime in small_primes:
            # Find first multiple of prime in [low, high]
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)

            for j in range(start, high + 1, prime):
                segment[j - low] = False

        # Collect primes from this segment
        for i in range(len(segment)):
            if segment[i]:
                result.append(low + i)

        if verbose:
            progress = (segment_num / total_segments) * 100
            print(f"Progress: {progress:.1f}% (processed up to {high:,})", end='\r')

        low = high + 1

    if verbose:
        print(" " * 70, end='\r')  # Clear progress line

    return result


def generate_primes(limit: int, verbose: bool = False) -> list[int]:
    """
    Generate a list of prime numbers up to a given limit using the Sieve of Eratosthenes.

    Args:
        limit: Upper bound for prime generation (inclusive)
        verbose: If True, print progress for large limits

    Returns:
        List of all prime numbers from 2 to limit

    Raises:
        MemoryError: If limit is too large for available memory

    Complexity:
        Time: O(n log log n)
        Space: O(n)
    """
    if limit < 2:
        return []

    try:
        # Initialize sieve
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
    except MemoryError:
        estimated_mb = (limit + 1) / 1024 / 1024
        raise MemoryError(
            f"Not enough memory to create sieve for {limit:,}. "
            f"Estimated memory needed: ~{estimated_mb:.1f} MB"
        )

    sqrt_limit = int(limit ** 0.5)

    # Sieve of Eratosthenes
    for i in range(2, sqrt_limit + 1):
        if is_prime[i]:
            # Mark multiples of i as composite
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

            if verbose and i % 1000 == 0:
                progress = (i / sqrt_limit) * 100
                print(f"Progress: {progress:.1f}% (checking {i:,})", end='\r')

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

        # Memory estimation: ~1 byte per number
        estimated_mb = limit / 1024 / 1024

        if limit > 1_000_000_000:
            print(f"⚠️  VERY LARGE limit ({limit:,})!")
            sqrt_limit = int(math.sqrt(limit))
            segmented_mb = sqrt_limit / 1024 / 1024
            print(f"   Standard sieve: ~{estimated_mb:.0f} MB (~{estimated_mb/1024:.1f} GB)")
            print(f"   Segmented sieve: ~{segmented_mb:.0f} MB (recommended!)")
            print(f"\n   💡 Segmented sieve uses much less memory for large ranges")
            confirm = input("   Use segmented sieve? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Operation cancelled.")
                return None
            return (limit, True)  # Return tuple: (limit, use_segmented)
        elif limit > 10_000_000:
            print(f"⚠️  Large limit ({limit:,}) may take significant time and memory!")
            print(f"   Estimated memory: ~{estimated_mb:.0f} MB")
            confirm = input("   Continue? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Operation cancelled.")
                return None

        return (limit, False)  # Return tuple: (limit, use_segmented)

    except ValueError:
        print("❌ Invalid input! Please enter a valid positive integer.")
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
    result = get_valid_limit()
    if result is None:
        return 1

    # Unpack result - can be (limit, use_segmented) or just limit
    if isinstance(result, tuple):
        limit, use_segmented = result
    else:
        limit, use_segmented = result, False

    print(f"\n🔍 Searching for primes up to {limit:,}...")
    if use_segmented:
        print("   Using segmented sieve (memory optimized)")

    # Generate primes with timing
    start_time = datetime.now()
    verbose = limit > 1_000_000

    try:
        if use_segmented:
            primes = generate_primes_segmented(limit, verbose=verbose)
        else:
            primes = generate_primes(limit, verbose=verbose)
    except MemoryError as e:
        print(f"\n❌ Memory Error: {e}")
        print("\n💡 Suggestions:")
        print("   • Try a smaller limit")
        print("   • Use segmented sieve option for large ranges")
        print("   • Close other applications to free memory")
        return 1

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