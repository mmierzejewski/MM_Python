#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Znajdowanie trójek pitagorejskich (a² + b² = c²) do zadanego limitu.
"""

from datetime import datetime
from typing import List, Tuple
import math


def find_pythagorean_triples(max_value: int) -> List[Tuple[int, int, int]]:
    """
    Znajduje wszystkie trójki pitagorejskie gdzie c < max_value.

    Trójka pitagorejska to (a, b, c) gdzie a² + b² = c² oraz a < b < c.

    Args:
        max_value: Maksymalna wartość dla c

    Returns:
        Lista krotek (a, b, c) reprezentujących trójki pitagorejskie
    """
    result = []

    # Dla każdego możliwego c
    for c in range(1, max_value):
        c2 = c * c

        # Dla każdego możliwego b (b < c)
        for b in range(1, c):
            b2 = b * b

            # Oblicz a z równania: a² = c² - b²
            a2 = c2 - b2

            if a2 <= 0:
                continue

            # Sprawdź czy a jest liczbą całkowitą
            a = int(math.sqrt(a2))

            # Weryfikacja: czy to rzeczywiście trójka pitagorejska i a < b
            if a < b and a * a == a2:
                result.append((a, b, c))

    return result


def find_pythagorean_triples_fast(max_value: int) -> List[Tuple[int, int, int]]:
    """
    Szybsza wersja używająca generowania prymitywnych trójek (wzór Euklidesa).

    Złożoność: O(n²) zamiast O(n³)
    """
    result = []

    # Generuj prymitywne trójki używając wzoru Euklidesa
    m_limit = int(math.sqrt(max_value)) + 1

    for m in range(2, m_limit):
        for n in range(1, m):
            if (m - n) % 2 == 0:  # m i n muszą mieć różną parzystość
                continue
            if math.gcd(m, n) != 1:  # m i n muszą być względnie pierwsze
                continue

            # Wzór Euklidesa na prymitywne trójki
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n

            # Upewnij się że a < b
            if a > b:
                a, b = b, a

            # Dodaj prymitywną trójkę i jej wielokrotności
            k = 1
            while k * c < max_value:
                result.append((k * a, k * b, k * c))
                k += 1

    # Sortuj wyniki
    result.sort(key=lambda x: (x[2], x[1], x[0]))

    return result


def get_valid_limit() -> int:
    """Pobiera i waliduje limit od użytkownika."""
    while True:
        try:
            limit_str = input("Podaj wartość limitu: ").strip()
            limit = int(limit_str)

            if limit <= 0:
                print("Limit musi być liczbą dodatnią!")
                continue
            if limit > 10000:
                print("Uwaga: duże wartości mogą zająć dużo czasu!")
                confirm = input("Kontynuować? (tak/nie): ").strip().lower()
                if confirm not in ['tak', 't', 'yes', 'y']:
                    continue

            return limit
        except ValueError:
            print("Proszę wpisać liczbę całkowitą!")


def main():
    """Główna funkcja programu."""
    print("=== Znajdowanie trójek pitagorejskich ===\n")

    limit = get_valid_limit()

    start_time = datetime.now()
    print(f'\nStart: {start_time}')

    # Użyj szybszej wersji dla dużych wartości
    if limit > 100:
        triples = find_pythagorean_triples_fast(limit)
        print("(używam zoptymalizowanego algorytmu)")
    else:
        triples = find_pythagorean_triples(limit)

    print(f'\nZnaleziono {len(triples)} trójek pitagorejskich:\n')

    for triple in triples:
        a, b, c = triple
        print(f"({a:4d}, {b:4d}, {c:4d}) -> {a}² + {b}² = {a**2} + {b**2} = {c**2} = {c}²")

    end_time = datetime.now()
    elapsed_time = end_time - start_time

    print(f'\nStop: {end_time}')
    print(f'Czas wykonania: {elapsed_time}')
    print(f'Średni czas na trójkę: {elapsed_time.total_seconds() / max(len(triples), 1):.6f}s')


if __name__ == "__main__":
    main()