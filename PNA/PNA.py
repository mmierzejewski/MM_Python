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
        print(f"Faza 1/2: Wyszukiwanie podstawowych liczb pierwszych do {sqrt_limit:,}...")

    result = generate_primes(sqrt_limit, verbose=False)

    # Krok 2: Przetwarzaj segmenty
    segment_size = max(sqrt_limit, 1_000_000)  # Co najmniej 1M dla wydajności
    low = sqrt_limit + 1

    total_segments = math.ceil((limit - sqrt_limit) / segment_size)

    if verbose:
        print(f"Faza 2/2: Przetwarzanie {total_segments} segmentów o rozmiarze {segment_size:,}...")

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
            print(f"Postęp: {progress:.1f}% (przetworzono do {high:,})", end='\r', flush=True)

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
                print(f"Postęp: {progress:.1f}% (sprawdzanie {i:,})", end='\r', flush=True)

    if verbose:
        print(" " * 50, end='\r', flush=True)  # Wyczyść linię postępu

    # Wyodrębnij liczby pierwsze
    return [num for num, prime in enumerate(is_prime) if prime]


def get_divisors(n: int) -> list[int]:
    """
    Znajduje wszystkie dzielniki podanej liczby.

    Args:
        n: Liczba do sprawdzenia

    Returns:
        Lista wszystkich dzielników liczby n

    Złożoność:
        Czas: O(√n)
    """
    if n < 1:
        return []
    
    divisors = []
    sqrt_n = int(math.sqrt(n))
    
    for i in range(1, sqrt_n + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:  # Unikaj duplikatów dla liczb kwadratowych
                divisors.append(n // i)
    
    return sorted(divisors)


def is_prime(n: int) -> bool:
    """
    Sprawdza, czy podana liczba jest liczbą pierwszą.

    Args:
        n: Liczba do sprawdzenia

    Returns:
        True jeśli liczba jest pierwsza, False w przeciwnym razie

    Złożoność:
        Czas: O(√n)
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Sprawdź nieparzystych dzielników do √n
    sqrt_n = int(math.sqrt(n))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    
    return True


def first_n_primes(n: int, verbose: bool = False) -> list[int]:
    """
    Generuje pierwsze n liczb pierwszych.

    Args:
        n: Liczba pierwszych liczb pierwszych do wygenerowania
        verbose: Jeśli True, wyświetla postęp

    Returns:
        Lista pierwszych n liczb pierwszych

    Złożoność:
        Używa przybliżenia n * ln(n) dla górnej granicy i generuje liczby pierwsze
        używając standardowego sita.
    """
    if n <= 0:
        return []
    if n == 1:
        return [2]
    if n == 2:
        return [2, 3]

    # Przybliżona górna granica dla n-tej liczby pierwszej
    # Dla n >= 6: p_n < n * (ln(n) + ln(ln(n)))
    # Dla bezpieczeństwa używamy większego współczynnika
    if n < 6:
        limit = 15
    else:
        limit = int(n * (math.log(n) + math.log(math.log(n))) * 1.3)

    if verbose:
        print(f"Szacowany limit dla pierwszych {n} liczb pierwszych: {limit:,}")

    primes = []
    while len(primes) < n:
        if verbose:
            print(f"Generowanie liczb pierwszych do {limit:,}...", end='\r', flush=True)
        
        primes = generate_primes(limit, verbose=False)
        
        if len(primes) < n:
            # Zwiększ limit jeśli nie znaleziono wystarczającej liczby
            limit = int(limit * 1.5)
            if verbose:
                print(f"Zwiększanie limitu do {limit:,}...", end='\r', flush=True)

    if verbose:
        print(" " * 70, end='\r', flush=True)  # Wyczyść linię postępu

    return primes[:n]


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


def get_user_choice() -> Optional[str]:
    """Pobiera wybór trybu od użytkownika.

    Returns:
        '1' dla limitu, '2' dla pierwszych n, '3' dla sprawdzenia pojedynczej liczby, '4' dla wyjścia, None jeśli nieprawidłowy wybór
    """
    print("Wybierz tryb działania:")
    print("  1. Znajdź wszystkie liczby pierwsze do podanego limitu")
    print("  2. Znajdź pierwsze n liczb pierwszych")
    print("  3. Sprawdź czy liczba jest pierwsza")
    print("  4. Koniec (wyjście z programu)")
    choice = input("\nTwój wybór (1/2/3/4): ").strip()
    
    if choice not in ['1', '2', '3', '4']:
        print("❌ Nieprawidłowy wybór!")
        return None
    
    return choice


def get_first_n_count() -> Optional[int]:
    """Pobiera i waliduje liczbę pierwszych liczb pierwszych do wygenerowania.

    Returns:
        Liczba n lub None jeśli anulowano/nieprawidłowe
    """
    try:
        n_str = input("Podaj liczbę pierwszych liczb pierwszych (n >= 1): ").strip()
        n = int(n_str)

        if n < 1:
            print("❌ Liczba musi wynosić co najmniej 1.")
            return None

        if n > 10_000_000:
            print(f"⚠️  BARDZO DUŻA liczba ({n:,})!")
            print(f"   Może to zająć dużo czasu...")
            confirm = input("   Kontynuować? (T/N) [N]: ").strip().upper() or "N"
            if confirm != "T":
                print("Operacja anulowana.")
                return None
        elif n > 100_000:
            print(f"⚠️  Duża liczba ({n:,}) może wymagać trochę czasu!")
            confirm = input("   Kontynuować? (T/N) [N]: ").strip().upper() or "N"
            if confirm != "T":
                print("Operacja anulowana.")
                return None

        return n

    except ValueError:
        print("❌ Nieprawidłowe dane! Proszę podać poprawną liczbę całkowitą dodatnią.")
        return None


def get_valid_limit() -> Optional[tuple[int, bool]]:
    """Pobiera i waliduje limit od użytkownika.

    Returns:
        Krotka (limit, use_segmented) lub None jeśli anulowano/nieprawidłowe
    """
    try:
        limit_str = input("Podaj zakres (liczba całkowita >= 2): ").strip()
        limit = int(limit_str)

        if limit < 2:
            print("❌ Zakres musi wynosić co najmniej 2.")
            return None

        # Szacowanie pamięci: ~1 bajt na liczbę
        estimated_mb = limit / 1024 / 1024

        if limit > 1_000_000_000:
            print(f"⚠️  BARDZO DUŻY zakres ({limit:,})!")
            sqrt_limit = int(math.sqrt(limit))
            segmented_mb = sqrt_limit / 1024 / 1024
            print(f"   Standardowe sito: ~{estimated_mb:.0f} MB (~{estimated_mb/1024:.1f} GB)")
            print(f"   Sito segmentowane: ~{segmented_mb:.0f} MB (zalecane!)")
            print(f"\n   💡 Sito segmentowane używa znacznie mniej pamięci dla dużych zakresów")
            confirm = input("   Użyć sita segmentowanego? (T/N) [T]: ").strip().upper() or "T"
            if confirm != "T":
                print("Operacja anulowana.")
                return None
            return (limit, True)  # Zwróć krotkę: (limit, use_segmented)
        elif limit > 10_000_000:
            print(f"⚠️  Duży zakres ({limit:,}) może wymagać znacznego czasu i pamięci!")
            print(f"   Szacowana pamięć: ~{estimated_mb:.0f} MB")
            confirm = input("   Kontynuować? (T/N) [N]: ").strip().upper() or "N"
            if confirm != "T":
                print("Operacja anulowana.")
                return None

        return (limit, False)  # Zwróć krotkę: (limit, use_segmented)

    except ValueError:
        print("❌ Nieprawidłowe dane! Proszę podać poprawną liczbę całkowitą dodatnią.")
        return None


def save_primes_to_file(primes: list[int], limit: int, filename: Optional[str] = None) -> None:
    """Zapisuje liczby pierwsze do pliku tekstowego."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Zapisz w katalogu gdzie jest skrypt (PNA/)
        script_dir = sys.path[0] if sys.path[0] else '.'
        filename = f"{script_dir}/primes_up_to_{limit}_{timestamp}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Liczby pierwsze do {limit:,}\n")
            f.write(f"Liczba znalezionych: {len(primes):,}\n")
            f.write(f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            # Zapisz liczby pierwsze, 10 na linię
            for i in range(0, len(primes), 10):
                line = ', '.join(map(str, primes[i:i+10]))
                f.write(line + '\n')

        print(f"✅ Liczby pierwsze zapisano do: {filename}")
    except IOError as e:
        print(f"❌ Błąd podczas zapisu pliku: {e}")


def analyze_primes(primes: list[int], limit: Optional[int] = None, first_n: Optional[int] = None) -> None:
    """Wyświetla szczegółową analizę znalezionych liczb pierwszych.

    Args:
        primes: Lista liczb pierwszych
        limit: Górny limit użyty do generowania (dla trybu z limitem)
        first_n: Liczba pierwszych n liczb pierwszych (dla trybu first n)
    """
    if not primes:
        print("\n📊 Nie znaleziono liczb pierwszych w tym zakresie.")
        return

    prime_count = len(primes)

    print(f"\n{'='*60}")
    print("📊 STATYSTYKI LICZB PIERWSZYCH")
    print(f"{'='*60}")
    
    if first_n is not None:
        print(f"Tryb:                Pierwsze {first_n:,} liczb pierwszych")
        print(f"Znaleziono:          {prime_count:,}")
    else:
        print(f"Zakres:              2 do {limit:,}")
        print(f"Liczby pierwsze:     {prime_count:,}")
        if limit:
            density = (prime_count / limit) * 100
            print(f"Gęstość:             {density:.4f}%")
    
    print(f"Najmniejsza:         {primes[0]:,}")
    print(f"Największa:          {primes[-1]:,}")

    # Pokaż pierwsze i ostatnie liczby pierwsze
    if prime_count <= 20:
        print(f"Wszystkie liczby:    {', '.join(map(str, primes))}")
    elif prime_count <= 100:
        first_10 = ', '.join(map(str, primes[:10]))
        last_10 = ', '.join(map(str, primes[-10:]))
        print(f"Pierwsze 10:         {first_10}")
        print(f"Ostatnie 10:         {last_10}")

    print(f"{'='*60}\n")

    # Zapytaj użytkownika o zapis po wyświetleniu statystyk
    save_option = input("💾 Zapisać liczby pierwsze do pliku? (T/N) [N]: ").strip().upper() or "N"
    if save_option == "T":
        if first_n is not None:
            save_primes_to_file(primes, primes[-1], filename=None)
        else:
            save_primes_to_file(primes, limit)


def main() -> int:
    """
    Główna funkcja uruchamiająca generator liczb pierwszych.

    Returns:
        0 w przypadku sukcesu, 1 w przypadku błędu
    """
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 8 + "GENERATOR LICZB PIERWSZYCH" + " " * 24 + "║")
    print("║" + " " * 12 + "(Sito Eratostenesa)" + " " * 27 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # Pętla główna programu
    while True:
        # Pobierz wybór trybu
        choice = get_user_choice()
        if choice is None:
            continue  # Nieprawidłowy wybór, pokaż menu ponownie
        
        # Opcja wyjścia
        if choice == '4':
            print("\n👋 Do widzenia!")
            return 0

        print()  # Dodaj pustą linię

        if choice == '1':
            # Tryb: liczby pierwsze do limitu
            result = get_valid_limit()
            if result is None:
                print()  # Dodaj pustą linię przed powrotem do menu
                continue

            # Rozpakuj wynik - może być (limit, use_segmented) lub tylko limit
            if isinstance(result, tuple):
                limit, use_segmented = result
            else:
                limit, use_segmented = result, False

            print(f"\n🔍 Wyszukiwanie liczb pierwszych do {limit:,}...")
            if use_segmented:
                print("   Używanie sita segmentowanego (optymalizacja pamięci)")

            # Generuj liczby pierwsze z pomiarem czasu
            start_time = datetime.now()
            verbose = limit > 1_000_000

            try:
                if use_segmented:
                    primes = generate_primes_segmented(limit, verbose=verbose)
                else:
                    primes = generate_primes(limit, verbose=verbose)
            except MemoryError as e:
                print(f"\n❌ Błąd pamięci: {e}")
                print("\n💡 Sugestie:")
                print("   • Spróbuj mniejszego zakresu")
                print("   • Użyj opcji sita segmentowanego dla dużych zakresów")
                print("   • Zamknij inne aplikacje, aby zwolnić pamięć")
                print()  # Dodaj pustą linię przed powrotem do menu
                continue

            end_time = datetime.now()

            # Wyświetl wyniki
            display_timing("Czas generowania", start_time, end_time)
            analyze_primes(primes, limit=limit)
            print()  # Dodaj pustą linię przed powrotem do menu

        elif choice == '2':
            # Tryb: pierwsze n liczb pierwszych
            n = get_first_n_count()
            if n is None:
                print()  # Dodaj pustą linię przed powrotem do menu
                continue

            print(f"\n🔍 Wyszukiwanie pierwszych {n:,} liczb pierwszych...")

            # Generuj pierwsze n liczb pierwszych z pomiarem czasu
            start_time = datetime.now()
            verbose = n > 10_000

            try:
                primes = first_n_primes(n, verbose=verbose)
            except MemoryError as e:
                print(f"\n❌ Błąd pamięci: {e}")
                print("\n💡 Sugestia: Spróbuj mniejszej liczby n")
                print()  # Dodaj pustą linię przed powrotem do menu
                continue

            end_time = datetime.now()

            # Wyświetl wyniki
            display_timing("Czas generowania", start_time, end_time)
            analyze_primes(primes, first_n=n)
            print()  # Dodaj pustą linię przed powrotem do menu

        else:
            # Tryb: sprawdzanie czy liczba jest pierwsza
            try:
                n_str = input("Podaj liczbę do sprawdzenia: ").strip()
                n = int(n_str)

                print(f"\n🔍 Sprawdzanie czy {n:,} jest liczbą pierwszą...")

                start_time = datetime.now()
                result = is_prime(n)
                end_time = datetime.now()

                print(f"\n{'='*60}")
                if result:
                    print(f"✅ Liczba {n:,} JEST liczbą pierwszą")
                else:
                    print(f"❌ Liczba {n:,} NIE JEST liczbą pierwszą")
                    
                    # Znajdź i wyświetl dzielniki
                    divisors = get_divisors(n)
                    print(f"\n📋 Dzielniki liczby {n:,}:")
                    
                    # Wyświetl dzielniki w czytelnym formacie
                    if len(divisors) <= 20:
                        print(f"   {', '.join(map(str, divisors))}")
                    else:
                        # Dla dużej liczby dzielników, pokaż pierwsze i ostatnie
                        first_10 = ', '.join(map(str, divisors[:10]))
                        last_10 = ', '.join(map(str, divisors[-10:]))
                        print(f"   Pierwsze 10: {first_10}")
                        print(f"   ...")
                        print(f"   Ostatnie 10: {last_10}")
                    
                    print(f"   Liczba dzielników: {len(divisors)}")
                print(f"{'='*60}")

                display_timing("Czas sprawdzania", start_time, end_time)
                print()  # Dodaj pustą linię przed powrotem do menu

            except ValueError:
                print("❌ Nieprawidłowe dane! Proszę podać poprawną liczbę całkowitą.")
                print()  # Dodaj pustą linię przed powrotem do menu
                continue


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Nieoczekiwany błąd: {e}")
        sys.exit(1)