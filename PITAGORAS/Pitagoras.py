#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator Trójek Pitagorejskich z Analizą Liczb Pierwszych

Generuje unikalne (prymitywne) trójki pitagorejskie ze szczegółową analizą:
- Wymiary (a, b, c)
- Obwód (a + b + c)
- Powierzchnia (a × b / 2)
- Detekcja liczb pierwszych
"""

import math
from typing import List, Tuple, Set, Dict
from datetime import datetime


class PythagoreanTriple:
    """Reprezentuje trójkę pitagorejską z obliczonymi właściwościami."""
    
    def __init__(self, a: int, b: int, c: int):
        """
        Inicjalizuje trójkę pitagorejską.
        
        Args:
            a, b, c: Boki trójkąta gdzie a² + b² = c²
        """
        self.a = a
        self.b = b
        self.c = c
    
    @property
    def perimeter(self) -> int:
        """Oblicza obwód."""
        return self.a + self.b + self.c
    
    @property
    def area(self) -> float:
        """Oblicza powierzchnię używając wzoru: (a × b) / 2."""
        return (self.a * self.b) / 2
    
    def __repr__(self) -> str:
        return f"PythagoreanTriple({self.a}, {self.b}, {self.c})"
    
    def __eq__(self, other) -> bool:
        """Dwie trójki są równe, jeśli mają te same boki."""
        if not isinstance(other, PythagoreanTriple):
            return False
        return (self.a, self.b, self.c) == (other.a, other.b, other.c)
    
    def __hash__(self) -> int:
        return hash((self.a, self.b, self.c))


def sieve_of_eratosthenes(limit: int) -> Set[int]:
    """
    Generuje wszystkie liczby pierwsze do limitu używając Sita Eratostenesa.
    
    Args:
        limit: Górna granica (włącznie)
    
    Returns:
        Zbiór liczb pierwszych dla wyszukiwania O(1)
    
    Złożoność: O(n log log n)
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
    Generuje prymitywne (unikalne) trójki pitagorejskie używając wzoru Euklidesa.
    
    Trójki prymitywne mają gcd(a, b, c) = 1, co eliminuje duplikaty
    takie jak (3,4,5) i (6,8,10).
    
    Args:
        count: Liczba trójek prymitywnych do wygenerowania
    
    Returns:
        Lista obiektów PythagoreanTriple posortowana według obwodu
    
    Algorytm:
        Dla liczb względnie pierwszych m > n > 0 o różnej parzystości:
        a = m² - n²
        b = 2mn
        c = m² + n²
    """
    triples = []
    m = 2
    
    # Kontynuuj, dopóki nie będzie wystarczająco trójek
    while len(triples) < count:
        for n in range(1, m):
            # Sprawdź warunki dla trójki prymitywnej
            if (m - n) % 2 == 0:  # m i n muszą mieć różną parzystość
                continue
            if math.gcd(m, n) != 1:  # m i n muszą być względnie pierwsze
                continue
            
            # Wzór Euklidesa dla trójki prymitywnej
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            
            # Upewnij się, że a < b dla spójności
            if a > b:
                a, b = b, a
            
            triple = PythagoreanTriple(a, b, c)
            triples.append(triple)
            
            # Sprawdź, czy mamy wystarczająco
            if len(triples) >= count:
                break
        
        m += 1
        
        # Limit bezpieczeństwa, aby zapobiec nieskończonej pętli
        if m > 10000:
            print(f"⚠️  Ostrzeżenie: Osiągnięto limit wyszukiwania. Znaleziono tylko {len(triples)} trójek.")
            break
    
    # Sortuj według obwodu (najmniejszy najpierw)
    triples.sort(key=lambda t: (t.perimeter, t.a, t.b))
    
    return triples[:count]


def analyze_primes_in_triple(triple: PythagoreanTriple, primes: Set[int]) -> List[int]:
    """
    Znajduje, które liczby w trójce są pierwsze.
    
    Args:
        triple: Obiekt PythagoreanTriple
        primes: Zbiór liczb pierwszych
    
    Returns:
        Lista liczb pierwszych znalezionych w trójce
    """
    return [num for num in (triple.a, triple.b, triple.c) if num in primes]


def get_valid_count() -> int:
    """Pobiera i waliduje liczbę trójek od użytkownika."""
    while True:
        try:
            count_str = input("Podaj liczbę trójek pitagorejskich do wygenerowania (1-1000): ").strip()
            count = int(count_str)
            
            if count < 1:
                print("❌ Liczba musi wynosić co najmniej 1")
                continue
            
            if count > 1000:
                print(f"⚠️  Duża liczba ({count:,}) może zająć trochę czasu!")
                confirm = input("   Kontynuować? (T/N): ").strip().upper()
                if confirm != 'T':
                    continue
            
            return count
        
        except ValueError:
            print("❌ Proszę podać poprawną liczbę całkowitą")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Anulowano")
            exit(0)


def display_triples(triples: List[PythagoreanTriple], primes: Set[int]) -> None:
    """
    Wyświetla trójki w sformatowanej tabeli.
    
    Args:
        triples: Lista obiektów PythagoreanTriple
        primes: Zbiór liczb pierwszych do detekcji
    """
    print(f"\n{'='*90}")
    print(f"{'#':<4} {'a':>5} {'b':>5} {'c':>5} {'Obwód':>10} {'Powierzchnia':>15} {'L. pierwsze':<30}")
    print(f"{'='*90}")
    
    for idx, triple in enumerate(triples, 1):
        prime_nums = analyze_primes_in_triple(triple, primes)
        prime_str = f"[{', '.join(map(str, prime_nums))}]" if prime_nums else "-"
        
        print(f"{idx:<4} {triple.a:>5} {triple.b:>5} {triple.c:>5} "
              f"{triple.perimeter:>10} {triple.area:>12.1f} {prime_str:<30}")
    
    print(f"{'='*90}")


def display_statistics(triples: List[PythagoreanTriple], primes: Set[int]) -> None:
    """
    Wyświetla analizę statystyczną trójek.
    
    Args:
        triples: Lista obiektów PythagoreanTriple
        primes: Zbiór liczb pierwszych
    """
    if not triples:
        return
    
    # Policz trójki z liczbami pierwszymi
    triples_with_primes = sum(1 for t in triples if analyze_primes_in_triple(t, primes))
    
    # Znajdź ekstrema
    min_perimeter = min(t.perimeter for t in triples)
    max_perimeter = max(t.perimeter for t in triples)
    min_area = min(t.area for t in triples)
    max_area = max(t.area for t in triples)
    avg_perimeter = sum(t.perimeter for t in triples) / len(triples)
    avg_area = sum(t.area for t in triples) / len(triples)
    
    # Największa wartość
    max_value = max(max(t.a, t.b, t.c) for t in triples)
    
    print(f"\n{'='*90}")
    print("STATYSTYKI:")
    print(f"{'='*90}")
    print(f"Trójki prymitywne łącznie:         {len(triples)}")
    print(f"Trójki zawierające liczby pierwsze: {triples_with_primes} ({triples_with_primes/len(triples)*100:.1f}%)")
    print(f"Liczby pierwsze do {max_value}:             {len([p for p in primes if p <= max_value])}")
    print(f"\nObwód:")
    print(f"  Najmniejszy:                     {min_perimeter}")
    print(f"  Największy:                      {max_perimeter}")
    print(f"  Średni:                          {avg_perimeter:.1f}")
    print(f"\nPowierzchnia:")
    print(f"  Najmniejsza:                     {min_area:.1f}")
    print(f"  Największa:                      {max_area:.1f}")
    print(f"  Średnia:                         {avg_area:.1f}")
    print(f"{'='*90}")


def verify_no_duplicates(triples: List[PythagoreanTriple]) -> None:
    """
    Weryfikuje, że nie ma wielokrotności (np. 3,4,5 i 6,8,10).
    
    Args:
        triples: Lista obiektów PythagoreanTriple
    """
    print(f"\n{'='*90}")
    print("WERYFIKACJA DUPLIKATÓW:")
    print(f"{'='*90}")
    
    # Sprawdź GCD > 1 (wskazuje na nieprymitywność)
    non_primitive = []
    for triple in triples:
        gcd = math.gcd(math.gcd(triple.a, triple.b), triple.c)
        if gcd > 1:
            non_primitive.append((triple, gcd))
    
    if non_primitive:
        print("⚠️  Znaleziono trójki nieprymitywne (wielokrotności):")
        for triple, gcd in non_primitive:
            print(f"   ({triple.a}, {triple.b}, {triple.c}) - NWD = {gcd}")
    else:
        print("✅ Wszystkie trójki są prymitywne (brak wielokrotności jak 3,4,5 i 6,8,10)")
    
    # Sprawdź dokładne duplikaty
    unique_triples = len(set(triples))
    if unique_triples < len(triples):
        print(f"⚠️  Znaleziono {len(triples) - unique_triples} dokładnych duplikatów")
    else:
        print("✅ Nie znaleziono dokładnych duplikatów")
    
    print(f"{'='*90}")


def main():
    """Funkcja główna."""
    print("╔" + "═" * 88 + "╗")
    print("║" + " " * 16 + "GENERATOR TRÓJEK PITAGOREJSKICH" + " " * 41 + "║")
    print("║" + " " * 25 + "(Tylko prymitywne)" + " " * 46 + "║")
    print("╚" + "═" * 88 + "╝\n")
    
    # Pobierz dane wejściowe
    count = get_valid_count()
    
    print(f"\n🔍 Generowanie {count} prymitywnych trójek pitagorejskich...")
    print("   (Eliminacja wielokrotności takich jak 3,4,5 i 6,8,10)\n")
    
    # Rozpocznij pomiar czasu
    start_time = datetime.now()
    
    # Generuj trójki prymitywne
    triples = generate_primitive_triples(count)
    
    if not triples:
        print("❌ Nie udało się wygenerować trójek pitagorejskich")
        return
    
    print(f"✅ Wygenerowano {len(triples)} trójek prymitywnych")
    
    # Generuj liczby pierwsze do analizy
    max_value = max(max(t.a, t.b, t.c) for t in triples)
    print(f"🔢 Wyszukiwanie liczb pierwszych do {max_value}...")
    primes = sieve_of_eratosthenes(max_value)
    
    end_time = datetime.now()
    elapsed = end_time - start_time
    
    # Wyświetl wyniki
    display_triples(triples, primes)
    
    # Weryfikuj brak duplikatów
    verify_no_duplicates(triples)
    
    # Wyświetl statystyki
    display_statistics(triples, primes)
    
    # Informacje o czasie
    print(f"\n⏱️  Czas generowania: {elapsed.total_seconds():.3f}s")
    print(f"   Średnio na trójkę: {elapsed.total_seconds() / len(triples):.6f}s\n")
    
    # Pokaż pierwsze przykłady z pełnym wzorem
    print("\n💡 Przykładowa weryfikacja (pierwsze 3 trójki):")
    for i, triple in enumerate(triples[:3], 1):
        print(f"   {i}. {triple.a}² + {triple.b}² = {triple.a**2} + {triple.b**2} = "
              f"{triple.a**2 + triple.b**2} = {triple.c**2} = {triple.c}²  ✓")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Anulowano przez użytkownika")
        exit(130)
    except Exception as e:
        print(f"\n❌ Nieoczekiwany błąd: {e}")
        exit(1)
