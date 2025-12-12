#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pythagorean Triples with Prime Analysis

Finds Pythagorean triples and identifies those containing prime numbers.
"""

import math
from typing import List, Tuple, Set


def sieve_of_eratosthenes(limit: int) -> Set[int]:
    """
    Generate all primes up to limit using Sieve of Eratosthenes.

    Args:
        limit: Upper bound (inclusive)

    Returns:
        Set of prime numbers for O(1) lookup
    """
    if limit < 2:
        return set()

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return {num for num, prime in enumerate(is_prime) if prime}


def generate_pythagorean_triples(limit: int) -> List[Tuple[int, int, int]]:
    """
    Generate Pythagorean triples where c < limit using Euclid's formula.

    Much faster than brute force: O(n²) instead of checking all pairs.

    Args:
        limit: Maximum value for c

    Returns:
        List of tuples (a, b, c) where a < b < c and a² + b² = c²
    """
    triples = []

    # Use Euclid's formula to generate primitive triples
    m_limit = int(math.sqrt(limit)) + 1

    for m in range(2, m_limit):
        for n in range(1, m):
            # Check if m and n generate primitive triple
            if (m - n) % 2 == 0:  # m and n must have different parity
                continue
            if math.gcd(m, n) != 1:  # m and n must be coprime
                continue

            # Euclid's formula
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n

            # Ensure a < b
            if a > b:
                a, b = b, a

            # Only add primitive triple (no multiples)
            if c < limit:
                triples.append((a, b, c))

    # Sort by perimeter
    triples.sort(key=lambda t: sum(t))

    return triples


def has_prime(triple: Tuple[int, int, int], primes: Set[int]) -> bool:
    """Check if triple contains at least one prime number."""
    return any(num in primes for num in triple)


def get_valid_limit() -> int:
    """Get and validate limit from user."""
    while True:
        try:
            limit_str = input("Enter limit (min 10, recommended max 10000): ").strip()
            limit = int(limit_str)

            if limit < 10:
                print("❌ Limit must be at least 10")
                continue

            if limit > 100000:
                print(f"⚠️  Large limit ({limit:,}) may take significant time!")
                confirm = input("   Continue? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    continue

            return limit

        except ValueError:
            print("❌ Please enter a valid integer")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Cancelled")
            exit(0)


def main():
    """Main function."""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 7 + "PYTHAGOREAN TRIPLES WITH PRIMES" + " " * 20 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # Get input
    limit = get_valid_limit()

    print(f"\n🔍 Generating Pythagorean triples where c < {limit:,}...\n")

    # Generate triples
    triples = generate_pythagorean_triples(limit)

    if not triples:
        print("❌ No Pythagorean triples found in this range")
        return

    print(f"✓ Found {len(triples)} Pythagorean triples\n")

    # Display all triples
    print(f"{'='*60}")
    print("ALL PYTHAGOREAN TRIPLES (sorted by perimeter):")
    print(f"{'='*60}")

    for a, b, c in triples:
        perimeter = a + b + c
        print(f"({a:4d}, {b:4d}, {c:4d})  →  perimeter: {perimeter:5d}  "
              f"[{a}² + {b}² = {c}²]")

    # Find primes up to max value in triples
    max_value = max(max(triple) for triple in triples)
    primes = sieve_of_eratosthenes(max_value)

    print(f"\n{'='*60}")
    print(f"TRIPLES WITH PRIME NUMBERS (found {len(primes)} primes up to {max_value}):")
    print(f"{'='*60}")

    # Filter triples containing primes
    prime_triples = [(a, b, c) for a, b, c in triples if has_prime((a, b, c), primes)]

    if not prime_triples:
        print("No triples contain prime numbers")
    else:
        for a, b, c in prime_triples:
            perimeter = a + b + c
            prime_nums = [n for n in (a, b, c) if n in primes]
            prime_str = ", ".join(map(str, prime_nums))
            print(f"({a:4d}, {b:4d}, {c:4d})  →  perimeter: {perimeter:5d}  "
                  f"primes: [{prime_str}]")

    # Statistics
    print(f"\n{'='*60}")
    print("STATISTICS:")
    print(f"{'='*60}")
    print(f"Total triples found:          {len(triples)}")
    print(f"Triples with primes:          {len(prime_triples)}")
    percentage = (len(prime_triples) / len(triples)) * 100 if triples else 0
    print(f"Percentage with primes:       {percentage:.1f}%")
    print(f"Largest value in any triple:  {max_value}")
    print(f"Prime numbers up to {max_value}:      {len(primes)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()