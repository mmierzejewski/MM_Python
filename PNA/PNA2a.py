#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator Liczb Pierwszych używający Sita Eratostenesa.

Wydajnie generuje wszystkie liczby pierwsze do podanego limitu z
pomiarem wydajności i szczegółowymi statystykami. Zawiera segmentowane sito
dla bardzo dużych zakresów.
"""

from datetime import datetime
from typing import Optional
import sys
import math
import logging


def generate_primes_segmented(limit: int, verbose: bool = False) -> list[int]:
    """
    Generuje liczby pierwsze używając segmentowanego sita dla bardzo dużych limitów.
    Używa znacznie mniej pamięci niż standardowe sito.

    Args:
        limit: Górna granica generowania liczb pierwszych (włącznie)
        verbose: Jeśli True, wyświetla postęp

    Returns:
        Lista wszystkich liczb pierwszych od 2 do limit

    Złożoność:
        Czas: O(n log log n)
        Pamięć: O(√n) zamiast O(n)
    """
    if limit < 2:
        return []

    sqrt_limit = int(math.sqrt(limit))

    # Krok 1: Znajdź małe liczby pierwsze do √limit używając standardowego sita
    if verbose:
        print(f"Phase 1/2: Finding base primes up to {sqrt_limit:,}...")

    result = generate_primes(sqrt_limit, verbose=False)

    # Krok 2: Przetwarzaj segmenty
    segment_size = max(sqrt_limit, 1_000_000)  # Co najmniej 1M dla wydajności
    low = sqrt_limit + 1

    total_segments = math.ceil((limit - sqrt_limit) / segment_size)

    if verbose:
        print(f"Phase 2/2: Processing {total_segments} segments of size {segment_size:,}...")

    segment_num = 0
    while low <= limit:
        high = min(low + segment_size - 1, limit)
        segment_num += 1

        # Utwórz sito segmentu
        segment = [True] * (high - low + 1)

        # Oznacz wielokrotności podstawowych liczb pierwszych w tym segmencie
        for prime in result:
            if prime > sqrt_limit:
                break
            # Znajdź pierwszą wielokrotność liczby pierwszej w [low, high]
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)

            for j in range(start, high + 1, prime):
                segment[j - low] = False

        # Zbierz liczby pierwsze z tego segmentu
        for i in range(len(segment)):
            if segment[i]:
                result.append(low + i)

        if verbose:
            progress = (segment_num / total_segments) * 100
            print(f"Progress: {progress:.1f}% (processed up to {high:,})", end='\r', flush=True)

        low = high + 1

    if verbose:
        print(" " * 70, end='\r', flush=True)  # Wyczyść linię postępu

    return result


def generate_primes(limit: int, verbose: bool = False) -> list[int]:
    """
    Generuje listę liczb pierwszych do podanego limitu używając Sita Eratostenesa.

    Args:
        limit: Górna granica generowania liczb pierwszych (włącznie)
        verbose: Jeśli True, wyświetla postęp dla dużych limitów

    Returns:
        Lista wszystkich liczb pierwszych od 2 do limit

    Raises:
        MemoryError: Jeśli limit jest zbyt duży dla dostępnej pamięci

    Złożoność:
        Czas: O(n log log n)
        Pamięć: O(n)
    """
    if limit < 2:
        return []

    try:
        # Inicjalizuj sito
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
    except MemoryError:
        estimated_mb = (limit + 1) / 1024 / 1024
        raise MemoryError(
            f"Not enough memory to create sieve for {limit:,}. "
            f"Estimated memory needed: ~{estimated_mb:.1f} MB"
        )

    sqrt_limit = math.isqrt(limit)

    # Sito Eratostenesa
    for i in range(2, sqrt_limit + 1):
        if is_prime[i]:
            # Oznacz wielokrotności i jako złożone
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

            if verbose and i % 1000 == 0:
                progress = (i / sqrt_limit) * 100
                print(f"Progress: {progress:.1f}% (checking {i:,})", end='\r', flush=True)

    if verbose:
        print(" " * 50, end='\r', flush=True)  # Wyczyść linię postępu

    # Wyodrębnij liczby pierwsze
    return [num for num, prime in enumerate(is_prime) if prime]


def format_duration(duration) -> str:
    """Formatuje czas trwania w czytelnym formacie."""
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
    """Wyświetla informacje o czasie trwania procesu."""
    duration = end - start
    formatted_duration = format_duration(duration)
    print(f"⏱️  {label}: {formatted_duration}")


def get_valid_limit() -> Optional[tuple[int, bool]]:
    """Pobiera i waliduje limit od użytkownika.

    Returns:
        Krotka (limit, use_segmented) lub None jeśli anulowano/nieprawidłowe
    """
    try:
        limit_str = input("Enter the range (positive integer >= 2): ").strip()
        limit = int(limit_str)

        if limit < 2:
            print("❌ The range must be at least 2.")
            return None

        # Szacowanie pamięci: ~1 bajt na liczbę
        estimated_mb = limit / 1024 / 1024

        if limit > 1_000_000_000:
            print(f"⚠️  VERY LARGE limit ({limit:,})!")
            sqrt_limit = int(math.sqrt(limit))
            segmented_mb = sqrt_limit / 1024 / 1024
            print(f"   Standard sieve: ~{estimated_mb:.0f} MB (~{estimated_mb/1024:.1f} GB)")
            print(f"   Segmented sieve: ~{segmented_mb:.0f} MB (recommended!)")
            print(f"\n   💡 Segmented sieve uses much less memory for large ranges")
            confirm = input("   Use segmented sieve? (T/N) [T]: ").strip().upper() or "T"
            if confirm != "T":
                print("Operation cancelled.")
                return None
            return (limit, True)  # Zwróć krotkę: (limit, use_segmented)
        elif limit > 10_000_000:
            print(f"⚠️  Large limit ({limit:,}) may take significant time and memory!")
            print(f"   Estimated memory: ~{estimated_mb:.0f} MB")
            confirm = input("   Continue? (T/N) [N]: ").strip().upper() or "N"
            if confirm != "T":
                print("Operation cancelled.")
                return None

        return (limit, False)  # Zwróć krotkę: (limit, use_segmented)

    except ValueError:
        print("❌ Invalid input! Please enter a valid positive integer.")
        return None


def save_primes_to_file(primes: list[int], limit: int, filename: Optional[str] = None) -> None:
    """Zapisuje liczby pierwsze do pliku tekstowego."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"primes_up_to_{limit}_{timestamp}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Prime numbers up to {limit:,}\n")
            f.write(f"Total count: {len(primes):,}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            # Zapisz liczby pierwsze, 10 na linię
            for i in range(0, len(primes), 10):
                line = ', '.join(map(str, primes[i:i+10]))
                f.write(line + '\n')

        print(f"✅ Primes saved to: {filename}")
    except IOError as e:
        print(f"❌ Error saving file: {e}")


def analyze_primes(primes: list[int], limit: int, save_to_file: bool = False) -> None:
    """Wyświetla szczegółową analizę znalezionych liczb pierwszych.

    Args:
        primes: Lista liczb pierwszych
        limit: Górny limit użyty do generowania
        save_to_file: Jeśli True, oferuje zapisanie wyników do pliku
    """
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

    # Pokaż pierwsze i ostatnie liczby pierwsze
    if prime_count <= 10:
        print(f"All primes:      {', '.join(map(str, primes))}")

    print(f"{'='*60}\n")

    # Zaoferuj zapisanie do pliku dla dużych zestawów wyników
    if save_to_file and prime_count > 100:
        save_option = input("💾 Save primes to file? (T/N) [T]: ").strip().upper() or "T"
        if save_option == "T":
            save_primes_to_file(primes, limit)


def main() -> int:
    """
    Główna funkcja uruchamiająca generator liczb pierwszych.

    Returns:
        0 w przypadku sukcesu, 1 w przypadku błędu
    """
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "PRIME NUMBER GENERATOR" + " " * 26 + "║")
    print("║" + " " * 10 + "(Sieve of Eratosthenes)" + " " * 25 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # Pobierz dane wejściowe
    result = get_valid_limit()
    if result is None:
        return 1

    # Rozpakuj wynik - może być (limit, use_segmented) lub tylko limit
    if isinstance(result, tuple):
        limit, use_segmented = result
    else:
        limit, use_segmented = result, False

    print(f"\n🔍 Searching for primes up to {limit:,}...")
    if use_segmented:
        print("   Using segmented sieve (memory optimized)")

    # Generuj liczby pierwsze z pomiarem czasu
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

    # Wyświetl wyniki
    display_timing("Generation time", start_time, end_time)
    analyze_primes(primes, limit, save_to_file=True)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)