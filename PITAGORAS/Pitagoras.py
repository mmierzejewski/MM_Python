#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pythagorean Triple Generator with Prime Number Analysis

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
        Initializes a Pythagorean triple.
        
        Args:
            a, b, c: Sides of the triangle where a² + b² = c²
        """
        self.a = a
        self.b = b
        self.c = c
    
    @property
    def perimeter(self) -> int:
        """Calculates the perimeter."""
        return self.a + self.b + self.c
    
    @property
    def area(self) -> float:
        """Calculates the area using the formula: (a × b) / 2."""
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
    Generates all prime numbers up to the limit using the Sieve of Eratosthenes.
    
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
    Generates primitive (unique) Pythagorean triples using Euclid's formula.
    
    Primitive triples have gcd(a, b, c) = 1, which eliminates duplicates
    such as (3,4,5) and (6,8,10).
    
    Args:
        count: Number of primitive triples to generate
    
    Returns:
        List of PythagoreanTriple objects sorted by perimeter
    
    Algorithm:
        For coprime numbers m > n > 0 of different parity:
        a = m² - n²
        b = 2mn
        c = m² + n²
    """
    triples = []
    m = 2
    
    # Continue until there are enough triples
    while len(triples) < count:
        for n in range(1, m):
            # Check the conditions for a primitive triple
            if (m - n) % 2 == 0:  # m and n must have different parity
                continue
            if math.gcd(m, n) != 1:  # m and n must be coprime
                continue
            
            # Euclid's formula for a primitive triple
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
        
        # Safety limit to prevent an infinite loop
        if m > 10000:
            print(f"⚠️  Warning: Search limit reached. Only {len(triples)} triples found.")
            break
    
    # Sort by perimeter (smallest first)
    triples.sort(key=lambda t: (t.perimeter, t.a, t.b))
    
    return triples[:count]


def analyze_primes_in_triple(triple: PythagoreanTriple, primes: Set[int]) -> List[int]:
    """
    Finds which numbers in the triple are prime.
    
    Args:
        triple: PythagoreanTriple object
        primes: Set of prime numbers
    
    Returns:
        List of prime numbers found in the triple
    """
    return [num for num in (triple.a, triple.b, triple.c) if num in primes]


def get_user_choice() -> str:
    """Gets the user's choice: generate triples or exit.
    
    Returns:
        '1' for generation, '2' for exit, None if the choice is invalid
    """
    print("\nChoose an option:")
    print("  1. Generate Pythagorean triples")
    print("  2. Exit (quit the program)")
    choice = input("\nYour choice (1/2): ").strip()
    
    if choice not in ['1', '2']:
        print("❌ Invalid choice!")
        return None
    
    return choice


def get_valid_count() -> int:
    """Gets and validates the number of triples from the user."""
    while True:
        try:
            count_str = input("Enter the number of Pythagorean triples to generate (1-1000): ").strip()
            count = int(count_str)
            
            if count < 1:
                print("❌ The number must be at least 1")
                continue
            
            if count > 1000:
                print(f"⚠️  A large number ({count:,}) may take some time!")
                confirm = input("   Continue? (Y/N): ").strip().upper()
                if confirm != 'Y':
                    continue
            
            return count
        
        except ValueError:
            print("❌ Please enter a valid integer")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Cancelled")
            return None


def display_triples(triples: List[PythagoreanTriple], primes: Set[int]) -> None:
    """
    Displays the triples in a formatted table.
    
    Args:
        triples: List of PythagoreanTriple objects
        primes: Set of prime numbers for detection
    """
    print(f"\n{'='*90}")
    print(f"{'#':<4} {'a':>5} {'b':>5} {'c':>5} {'Perimeter':>10} {'Area':>15} {'Primes':<30}")
    print(f"{'='*90}")
    
    for idx, triple in enumerate(triples, 1):
        prime_nums = analyze_primes_in_triple(triple, primes)
        prime_str = f"[{', '.join(map(str, prime_nums))}]" if prime_nums else "-"
        
        print(f"{idx:<4} {triple.a:>5} {triple.b:>5} {triple.c:>5} "
              f"{triple.perimeter:>10} {triple.area:>12.1f} {prime_str:<30}")
    
    print(f"{'='*90}")


def display_statistics(triples: List[PythagoreanTriple], primes: Set[int]) -> None:
    """
    Displays statistical analysis of the triples.
    
    Args:
        triples: List of PythagoreanTriple objects
        primes: Set of prime numbers
    """
    if not triples:
        return
    
    # Count triples with prime numbers
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
    print(f"Triples containing prime numbers:  {triples_with_primes} ({triples_with_primes/len(triples)*100:.1f}%)")
    print(f"Primes up to {max_value}:             {len([p for p in primes if p <= max_value])}")
    print(f"\nPerimeter:")
    print(f"  Smallest:                        {min_perimeter}")
    print(f"  Largest:                         {max_perimeter}")
    print(f"  Average:                         {avg_perimeter:.1f}")
    print(f"\nArea:")
    print(f"  Smallest:                        {min_area:.1f}")
    print(f"  Largest:                         {max_area:.1f}")
    print(f"  Average:                         {avg_area:.1f}")
    print(f"{'='*90}")


def verify_no_duplicates(triples: List[PythagoreanTriple]) -> None:
    """
    Verifies that there are no multiples (e.g. 3,4,5 and 6,8,10).
    
    Args:
        triples: List of PythagoreanTriple objects
    """
    print(f"\n{'='*90}")
    print("DUPLICATE VERIFICATION:")
    print(f"{'='*90}")
    
    # Check GCD > 1 (indicates non-primitive)
    non_primitive = []
    for triple in triples:
        gcd = math.gcd(math.gcd(triple.a, triple.b), triple.c)
        if gcd > 1:
            non_primitive.append((triple, gcd))
    
    if non_primitive:
        print("⚠️  Non-primitive triples found (multiples):")
        for triple, gcd in non_primitive:
            print(f"   ({triple.a}, {triple.b}, {triple.c}) - GCD = {gcd}")
    else:
        print("✅ All triples are primitive (no multiples such as 3,4,5 and 6,8,10)")
    
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
    print("║" + " " * 16 + "PYTHAGOREAN TRIPLE GENERATOR" + " " * 44 + "║")
    print("║" + " " * 25 + "(Primitive only)" + " " * 47 + "║")
    print("╚" + "═" * 88 + "╝")
    
    # Main program loop
    while True:
        choice = get_user_choice()
        if choice is None:
            continue  # Invalid choice, show the menu again
        
        # Exit option
        if choice == '2':
            print("\n👋 Goodbye!")
            return
        
        # Get input data
        count = get_valid_count()
        if count is None:
            print()  # Add a blank line before returning to the menu
            continue
        
        print(f"\n🔍 Generating {count} primitive Pythagorean triples...")
        print("   (Eliminating multiples such as 3,4,5 and 6,8,10)\n")
        
        # Start timing
        start_time = datetime.now()
        
        # Generate primitive triples
        triples = generate_primitive_triples(count)
        
        if not triples:
            print("❌ Failed to generate Pythagorean triples")
            print()  # Add a blank line before returning to the menu
            continue
        
        print(f"✅ Generated {len(triples)} primitive triples")
        
        # Generate primes for analysis
        max_value = max(max(t.a, t.b, t.c) for t in triples)
        print(f"🔢 Searching for primes up to {max_value}...")
        primes = sieve_of_eratosthenes(max_value)
        
        end_time = datetime.now()
        elapsed = end_time - start_time
        
        # Display results
        display_triples(triples, primes)
        
        # Verify no duplicates
        verify_no_duplicates(triples)
        
        # Display statistics
        display_statistics(triples, primes)
        
        # Timing information
        print(f"\n⏱️  Generation time: {elapsed.total_seconds():.3f}s")
        print(f"   Average per triple: {elapsed.total_seconds() / len(triples):.6f}s\n")
        
        # Show the first examples with the full formula
        print("\n💡 Sample verification (first 3 triples):")
        for i, triple in enumerate(triples[:3], 1):
            print(f"   {i}. {triple.a}² + {triple.b}² = {triple.a**2} + {triple.b**2} = "
                  f"{triple.a**2 + triple.b**2} = {triple.c**2} = {triple.c}²  ✓")
        
        print()  # Add a blank line before returning to the menu


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
