#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pythagorean Triples Generator with Prime Analysis

Generates unique (primitive) Pythagorean triples with detailed analysis:
- Dimensions (a, b, c)
- Perimeter (a + b + c)
- Area (a × b / 2)
- Prime number detection
"""

import math
from typing import List, Tuple, Set, Dict
from datetime import datetime


class PythagoreanTriple:
    """Represents a Pythagorean triple with computed properties."""
    
    def __init__(self, a: int, b: int, c: int):
        """
        Initialize Pythagorean triple.
        
        Args:
            a, b, c: Triangle sides where a² + b² = c²
        """
        self.a = a
        self.b = b
        self.c = c
    
    @property
    def perimeter(self) -> int:
        """Calculate perimeter (obwód)."""
        return self.a + self.b + self.c
    
    @property
    def area(self) -> float:
        """Calculate area (powierzchnia) using formula: (a × b) / 2."""
        return (self.a * self.b) / 2
    
    def __repr__(self) -> str:
        return f"PythagoreanTriple({self.a}, {self.b}, {self.c})"
    
    def __eq__(self, other) -> bool:
        """Two triples are equal if they have the same sides."""
        if not isinstance(other, PythagoreanTriple):
            return False
        return (self.a, self.b, self.c) == (other.a, other.b, other.c)
    
    def __hash__(self) -> int:
        return hash((self.a, self.b, self.c))


def sieve_of_eratosthenes(limit: int) -> Set[int]:
    """
    Generate all primes up to limit using Sieve of Eratosthenes.
    
    Args:
        limit: Upper bound (inclusive)
    
    Returns:
        Set of prime numbers for O(1) lookup
    
    Complexity: O(n log log n)
    """
    if limit < 2:
        return set()
    
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, math.isqrt(limit) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    
    return {num for num, prime in enumerate(is_prime) if prime}


def generate_primitive_triples(count: int) -> List[PythagoreanTriple]:
    """
    Generate primitive (unique) Pythagorean triples using Euclid's formula.
    
    Primitive triples have gcd(a, b, c) = 1, which eliminates duplicates
    like (3,4,5) and (6,8,10).
    
    Args:
        count: Number of primitive triples to generate
    
    Returns:
        List of PythagoreanTriple objects sorted by perimeter
    
    Algorithm:
        For coprime integers m > n > 0 with different parity:
        a = m² - n²
        b = 2mn
        c = m² + n²
    """
    triples = []
    m = 2
    
    # Continue until we have enough triples
    while len(triples) < count:
        for n in range(1, m):
            # Check conditions for primitive triple
            if (m - n) % 2 == 0:  # m and n must have different parity
                continue
            if math.gcd(m, n) != 1:  # m and n must be coprime
                continue
            
            # Euclid's formula for primitive triple
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            
            # Ensure a < b for consistency
            if a > b:
                a, b = b, a
            
            triple = PythagoreanTriple(a, b, c)
            triples.append(triple)
            
            # Check if we have enough
            if len(triples) >= count:
                break
        
        m += 1
        
        # Safety limit to prevent infinite loop
        if m > 10000:
            print(f"⚠️  Warning: Reached search limit. Found only {len(triples)} triples.")
            break
    
    # Sort by perimeter (smallest first)
    triples.sort(key=lambda t: (t.perimeter, t.a, t.b))
    
    return triples[:count]


def analyze_primes_in_triple(triple: PythagoreanTriple, primes: Set[int]) -> List[int]:
    """
    Find which numbers in the triple are prime.
    
    Args:
        triple: PythagoreanTriple object
        primes: Set of prime numbers
    
    Returns:
        List of prime numbers found in the triple
    """
    return [num for num in (triple.a, triple.b, triple.c) if num in primes]


def get_valid_count() -> int:
    """Get and validate number of triples from user."""
    while True:
        try:
            count_str = input("Enter number of Pythagorean triples to generate (1-1000): ").strip()
            count = int(count_str)
            
            if count < 1:
                print("❌ Number must be at least 1")
                continue
            
            if count > 1000:
                print(f"⚠️  Large count ({count:,}) may take some time!")
                confirm = input("   Continue? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    continue
            
            return count
        
        except ValueError:
            print("❌ Please enter a valid integer")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Cancelled")
            exit(0)


def display_triples(triples: List[PythagoreanTriple], primes: Set[int]) -> None:
    """
    Display triples in a formatted table.
    
    Args:
        triples: List of PythagoreanTriple objects
        primes: Set of prime numbers for prime detection
    """
    print(f"\n{'='*90}")
    print(f"{'#':<4} {'a':>5} {'b':>5} {'c':>5} {'Perimeter':>10} {'Area':>12} {'Primes':<30}")
    print(f"{'='*90}")
    
    for idx, triple in enumerate(triples, 1):
        prime_nums = analyze_primes_in_triple(triple, primes)
        prime_str = f"[{', '.join(map(str, prime_nums))}]" if prime_nums else "-"
        
        print(f"{idx:<4} {triple.a:>5} {triple.b:>5} {triple.c:>5} "
              f"{triple.perimeter:>10} {triple.area:>12.1f} {prime_str:<30}")
    
    print(f"{'='*90}")


def display_statistics(triples: List[PythagoreanTriple], primes: Set[int]) -> None:
    """
    Display statistical analysis of the triples.
    
    Args:
        triples: List of PythagoreanTriple objects
        primes: Set of prime numbers
    """
    if not triples:
        return
    
    # Count triples with primes
    triples_with_primes = sum(1 for t in triples if analyze_primes_in_triple(t, primes))
    
    # Find extremes
    min_perimeter = min(t.perimeter for t in triples)
    max_perimeter = max(t.perimeter for t in triples)
    min_area = min(t.area for t in triples)
    max_area = max(t.area for t in triples)
    avg_perimeter = sum(t.perimeter for t in triples) / len(triples)
    avg_area = sum(t.area for t in triples) / len(triples)
    
    # Largest value
    max_value = max(max(t.a, t.b, t.c) for t in triples)
    
    print(f"\n{'='*90}")
    print("STATISTICS:")
    print(f"{'='*90}")
    print(f"Total primitive triples:           {len(triples)}")
    print(f"Triples containing primes:         {triples_with_primes} ({triples_with_primes/len(triples)*100:.1f}%)")
    print(f"Prime numbers up to {max_value}:             {len([p for p in primes if p <= max_value])}")
    print(f"\nPerimeter (Obwód):")
    print(f"  Smallest:                        {min_perimeter}")
    print(f"  Largest:                         {max_perimeter}")
    print(f"  Average:                         {avg_perimeter:.1f}")
    print(f"\nArea (Powierzchnia):")
    print(f"  Smallest:                        {min_area:.1f}")
    print(f"  Largest:                         {max_area:.1f}")
    print(f"  Average:                         {avg_area:.1f}")
    print(f"{'='*90}")


def verify_no_duplicates(triples: List[PythagoreanTriple]) -> None:
    """
    Verify that there are no multiples (e.g., 3,4,5 and 6,8,10).
    
    Args:
        triples: List of PythagoreanTriple objects
    """
    print(f"\n{'='*90}")
    print("DUPLICATE VERIFICATION:")
    print(f"{'='*90}")
    
    # Check for GCD > 1 (would indicate non-primitive)
    non_primitive = []
    for triple in triples:
        gcd = math.gcd(math.gcd(triple.a, triple.b), triple.c)
        if gcd > 1:
            non_primitive.append((triple, gcd))
    
    if non_primitive:
        print("⚠️  Found non-primitive triples (multiples):")
        for triple, gcd in non_primitive:
            print(f"   ({triple.a}, {triple.b}, {triple.c}) - GCD = {gcd}")
    else:
        print("✅ All triples are primitive (no multiples like 3,4,5 and 6,8,10)")
    
    # Check for exact duplicates
    unique_triples = len(set(triples))
    if unique_triples < len(triples):
        print(f"⚠️  Found {len(triples) - unique_triples} exact duplicates")
    else:
        print("✅ No exact duplicates found")
    
    print(f"{'='*90}")


def main():
    """Main function."""
    print("╔" + "═" * 88 + "╗")
    print("║" + " " * 20 + "PYTHAGOREAN TRIPLES GENERATOR" + " " * 39 + "║")
    print("║" + " " * 25 + "(Primitive Only)" + " " * 48 + "║")
    print("╚" + "═" * 88 + "╝\n")
    
    # Get input
    count = get_valid_count()
    
    print(f"\n🔍 Generating {count} primitive Pythagorean triple(s)...")
    print("   (Eliminating multiples like 3,4,5 and 6,8,10)\n")
    
    # Start timing
    start_time = datetime.now()
    
    # Generate primitive triples
    triples = generate_primitive_triples(count)
    
    if not triples:
        print("❌ No Pythagorean triples could be generated")
        return
    
    print(f"✅ Generated {len(triples)} primitive triple(s)")
    
    # Generate primes for analysis
    max_value = max(max(t.a, t.b, t.c) for t in triples)
    print(f"🔢 Finding primes up to {max_value}...")
    primes = sieve_of_eratosthenes(max_value)
    
    end_time = datetime.now()
    elapsed = end_time - start_time
    
    # Display results
    display_triples(triples, primes)
    
    # Verify no duplicates
    verify_no_duplicates(triples)
    
    # Display statistics
    display_statistics(triples, primes)
    
    # Timing info
    print(f"\n⏱️  Generation time: {elapsed.total_seconds():.3f}s")
    print(f"   Average per triple: {elapsed.total_seconds() / len(triples):.6f}s\n")
    
    # Show first few examples with full formula
    print("\n💡 Example verification (first 3 triples):")
    for i, triple in enumerate(triples[:3], 1):
        print(f"   {i}. {triple.a}² + {triple.b}² = {triple.a**2} + {triple.b**2} = "
              f"{triple.a**2 + triple.b**2} = {triple.c**2} = {triple.c}²  ✓")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
