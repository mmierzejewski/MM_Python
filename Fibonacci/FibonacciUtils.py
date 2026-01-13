#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FibonacciUtils - Narzędzia do generowania i analizy ciągu Fibonacciego.

Ciąg Fibonacciego: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)

Wszystkie funkcje używają spójnego indeksowania 0-based:
F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5...
"""

from typing import List, Union, Optional
from functools import lru_cache
from datetime import datetime
from pathlib import Path
import logging
import sys

# Konfiguracja loggingu
log_file = Path.cwd() / 'fibonacci.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)

# Stałe matematyczne
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2  # φ ≈ 1.618033988749...


class FibonacciError(Exception):
    """Wyjątek dla błędów związanych z ciągiem Fibonacciego."""
    pass


def generate_fibonacci_upto(max_value: int) -> List[int]:
    """
    Generuje liczby Fibonacciego do podanej wartości maksymalnej.

    Args:
        max_value: Maksymalna wartość (włącznie)

    Returns:
        Lista liczb Fibonacciego <= max_value

    Raises:
        FibonacciError: Gdy max_value < 0

    Example:
        >>> generate_fibonacci_upto(10)
        [0, 1, 1, 2, 3, 5, 8]
    """
    if max_value < 0:
        raise FibonacciError("Wartość maksymalna musi być nieujemna!")

    if max_value == 0:
        return [0]

    fib_prev, fib_curr = 0, 1
    results = [0]

    while fib_curr <= max_value:
        results.append(fib_curr)
        fib_prev, fib_curr = fib_curr, fib_prev + fib_curr

    return results


def get_nth_fibonacci(n: int, zero_indexed: bool = True) -> int:
    """
    Zwraca n-tą liczbę Fibonacciego.

    Args:
        n: Pozycja w ciągu
        zero_indexed: Jeśli True (domyślnie): F(0)=0, F(1)=1, F(2)=1...
                     Jeśli False: F(1)=0, F(2)=1, F(3)=1... (backwards compatibility)

    Returns:
        n-ta liczba Fibonacciego

    Raises:
        FibonacciError: Gdy n < 0 (0-indexed) lub n <= 0 (1-indexed)

    Example:
        >>> get_nth_fibonacci(6)  # 0-indexed
        8
        >>> get_nth_fibonacci(7, zero_indexed=False)  # 1-indexed
        8
    """
    if zero_indexed:
        if n < 0:
            raise FibonacciError("Pozycja musi być nieujemną liczbą całkowitą!")
        actual_n = n
    else:
        if n <= 0:
            raise FibonacciError("Pozycja musi być dodatnią liczbą całkowitą!")
        actual_n = n - 1
    
    logging.info(f"Obliczanie F({actual_n})")
    
    if actual_n == 0:
        return 0
    if actual_n == 1:
        return 1

    fib_prev, fib_curr = 0, 1
    for _ in range(2, actual_n + 1):
        fib_prev, fib_curr = fib_curr, fib_prev + fib_curr

    return fib_curr


def generate_first_n_fibonacci(n: int) -> List[int]:
    """
    Generuje pierwsze n liczb Fibonacciego.

    Args:
        n: Liczba elementów do wygenerowania

    Returns:
        Lista pierwszych n liczb Fibonacciego

    Raises:
        FibonacciError: Gdy n < 0

    Example:
        >>> generate_first_n_fibonacci(5)
        [0, 1, 1, 2, 3]
    """
    if n < 0:
        raise FibonacciError("Liczba elementów nie może być ujemna!")

    if n == 0:
        return []
    if n == 1:
        return [0]

    results = [0, 1]

    for _ in range(2, n):
        results.append(results[-1] + results[-2])

    return results


@lru_cache(maxsize=1024)
def fibonacci_fast(n: int) -> int:
    """
    Szybkie obliczanie n-tej liczby Fibonacciego metodą macierzową.
    Złożoność: O(log n)
    Używa memoizacji (@lru_cache) dla optymalizacji.

    Args:
        n: Pozycja w ciągu (0-indexed: F(0)=0, F(1)=1, F(2)=1...)

    Returns:
        n-ta liczba Fibonacciego
    """
    logging.info(f"fibonacci_fast: obliczanie F({n})")
    
    if n < 0:
        return 0
    if n == 0:
        return 0
    if n == 1:
        return 1

    def matrix_multiply(a, b):
        """Mnoży dwie macierze 2x2."""
        return [
            [a[0][0] * b[0][0] + a[0][1] * b[1][0],
             a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0],
             a[1][0] * b[0][1] + a[1][1] * b[1][1]]
        ]

    def matrix_power(matrix, n):
        """Podnosi macierz do potęgi n metodą szybkiego potęgowania."""
        if n == 1:
            return matrix
        if n % 2 == 0:
            half = matrix_power(matrix, n // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, n - 1))

    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    return result_matrix[0][1]


def is_fibonacci(num: int) -> bool:
    """
    Sprawdza, czy liczba należy do ciągu Fibonacciego.

    Liczba n jest liczbą Fibonacciego wtedy i tylko wtedy, gdy
    5*n^2 + 4 lub 5*n^2 - 4 jest kwadratem doskonałym.

    Args:
        num: Liczba do sprawdzenia

    Returns:
        True jeśli num jest liczbą Fibonacciego
    """
    if num < 0:
        return False

    def is_perfect_square(x):
        root = int(x ** 0.5)
        return root * root == x

    return is_perfect_square(5 * num * num + 4) or \
           is_perfect_square(5 * num * num - 4)


def export_fibonacci_sequence(sequence: List[int], filename: Optional[str] = None) -> None:
    """
    Eksportuje ciąg Fibonacciego do pliku tekstowego.
    
    Args:
        sequence: Lista liczb Fibonacciego
        filename: Nazwa pliku (opcjonalna, domyślnie z timestampem)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fibonacci_sequence_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Ciąg Fibonacciego\n")
            f.write(f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Liczba elementów: {len(sequence)}\n")
            f.write("=" * 60 + "\n\n")
            
            # Zapisz liczby, 10 na linię
            for i in range(0, len(sequence), 10):
                line = ', '.join(map(str, sequence[i:i+10]))
                f.write(f"F({i})-F({min(i+9, len(sequence)-1)}): {line}\n")
            
            # Statystyki
            if sequence:
                f.write("\n" + "=" * 60 + "\n")
                f.write("STATYSTYKI:\n")
                f.write(f"Najmniejsza: {min(sequence):,}\n")
                f.write(f"Największa: {max(sequence):,}\n")
                f.write(f"Suma: {sum(sequence):,}\n")
                if len(sequence) > 1:
                    ratio = sequence[-1] / sequence[-2] if sequence[-2] != 0 else 0
                    f.write(f"Ostatni stosunek: {ratio:.10f}\n")
                    f.write(f"Złoty podział φ: {GOLDEN_RATIO:.10f}\n")
        
        print(f"✅ Eksportowano do: {filename}")
        logging.info(f"Wyeksportowano ciąg do {filename}")
    except IOError as e:
        print(f"❌ Błąd zapisu pliku: {e}")
        logging.error(f"Błąd eksportu: {e}")


def print_fibonacci_info(n: int, zero_indexed: bool = True) -> None:
    """
    Wyświetla szczegółowe informacje o n-tej liczbie Fibonacciego.
    
    Args:
        n: Pozycja w ciągu
        zero_indexed: Indeksowanie (domyślnie 0-based)
    """
    try:
        fib_n = get_nth_fibonacci(n, zero_indexed=zero_indexed)
        display_n = n if zero_indexed else n - 1
        fib_seq = generate_first_n_fibonacci(display_n + 1 if display_n >= 0 else 1)

        print(f"\n{'=' * 60}")
        print(f"📊 INFORMACJE O F({display_n})")
        print(f"{'=' * 60}")
        print(f"Wartość: {fib_n:,}")
        print(f"Liczba cyfr: {len(str(fib_n))}")
        print(f"Ciąg do F({display_n}): {fib_seq[:10]}{'...' if len(fib_seq) > 10 else ''}")

        if len(fib_seq) > 1 and fib_seq[-2] != 0:
            ratio = fib_seq[-1] / fib_seq[-2]
            print(f"Stosunek F({display_n})/F({display_n-1}): {ratio:.10f}")
            print(f"Złoty podział φ: {GOLDEN_RATIO:.10f}")
            print(f"Różnica: {abs(ratio - GOLDEN_RATIO):.10e}")

        print(f"{'=' * 60}\n")
        logging.info(f"Wyświetlono informacje dla F({display_n}) = {fib_n}")
    except FibonacciError as e:
        print(f"❌ Błąd: {e}")
        logging.error(f"Błąd w print_fibonacci_info: {e}")


def main() -> None:
    """Główna funkcja programu."""
    print("=" * 60)
    print("🔢 KALKULATOR CIĄGU FIBONACCIEGO".center(60))
    print("=" * 60)
    print("📌 Wszystkie funkcje używają indeksowania 0-based")
    print("   (F(0)=0, F(1)=1, F(2)=1, F(3)=2...)\n")
    
    logging.info("Uruchomiono kalkulator Fibonacciego")
    
    # Przechowywanie ostatniego ciągu do eksportu
    last_sequence: List[int] = []

    while True:
        print("\nWybierz opcję:")
        print("1. Generuj liczby Fibonacciego do wartości")
        print("2. Pobierz n-tą liczbę Fibonacciego (0-indexed)")
        print("3. Generuj pierwsze n liczb Fibonacciego")
        print("4. Szybkie obliczanie (algorytm O(log n))")
        print("5. Sprawdź, czy liczba jest liczbą Fibonacciego")
        print("6. Szczegółowe informacje o F(n)")
        print("7. Eksportuj ostatni ciąg do pliku")
        print("8. Koniec (wyjście z programu)")

        try:
            choice = input("\n👉 Twój wybór (1-8): ").strip()

            if choice == "8":
                print("\n👋 Do widzenia!")
                logging.info("Zakończono działanie kalkulatora")
                break

            elif choice == "1":
                max_val = int(input("Podaj wartość maksymalną: "))
                result = generate_fibonacci_upto(max_val)
                print(f"\n✅ Liczby Fibonacciego ≤ {max_val}:")
                print(f"   {result}")
                print(f"   Znaleziono: {len(result)} liczb")

            elif choice == "2":
                n = int(input("Podaj pozycję n (0-indexed, np. F(0)=0, F(6)=8): "))
                result = get_nth_fibonacci(n, zero_indexed=True)
                print(f"\n✅ F({n}) = {result:,}")
                last_sequence = [result]

            elif choice == "3":
                n = int(input("Ile liczb wygenerować: "))
                result = generate_first_n_fibonacci(n)
                last_sequence = result
                if len(result) <= 20:
                    print(f"\n✅ Pierwsze {n} liczby: {result}")
                else:
                    show_all = input("Wyświetlić wszystkie liczby? (T/N) [N]: ").strip().upper()
                    if show_all == "T":
                        print(f"\n✅ Wszystkie {n} liczby:")
                        # Wyświetl liczby, 10 na linię
                        for i in range(0, len(result), 10):
                            line = ', '.join(map(str, result[i:i+10]))
                            print(f"   F({i})-F({min(i+9, len(result)-1)}): {line}")
                    else:
                        print(f"\n✅ Pierwsze 10: {result[:10]}")
                        print(f"   Ostatnie 10: {result[-10:]}")
                        print(f"   (pominięto {len(result) - 20} środkowych)")

            elif choice == "4":
                n = int(input("Podaj n (0-indexed, dla dużych n): "))
                result = fibonacci_fast(n)
                print(f"\n✅ F({n}) = {result:,}")
                print(f"   Liczba cyfr: {len(str(result))}")
                last_sequence = [result]

            elif choice == "5":
                num = int(input("Podaj liczbę do sprawdzenia: "))
                if is_fibonacci(num):
                    print(f"\n✅ {num:,} JEST liczbą Fibonacciego!")
                else:
                    print(f"\n❌ {num:,} NIE JEST liczbą Fibonacciego.")

            elif choice == "6":
                n = int(input("Podaj n (0-indexed): "))
                print_fibonacci_info(n, zero_indexed=True)
            
            elif choice == "7":
                if not last_sequence:
                    print("\n❌ Brak ciągu do eksportu! Wygeneruj najpierw liczby.")
                else:
                    eksport = input("\nEksportować do pliku? (T/N) [T]: ").strip().upper() or "T"
                    if eksport == "T":
                        custom_name = input("Nazwa pliku (Enter = auto): ").strip()
                        export_fibonacci_sequence(
                            last_sequence,
                            custom_name if custom_name else None
                        )

            else:
                print("\n❌ Nieprawidłowy wybór! Wybierz 1-8.")

        except ValueError as e:
            print("\n❌ Nieprawidłowe dane! Podaj liczbę całkowitą.")
            logging.warning(f"ValueError: {e}")
        except FibonacciError as e:
            print(f"\n❌ Błąd: {e}")
            logging.error(f"FibonacciError: {e}")
        except KeyboardInterrupt:
            print("\n\n👋 Przerwano przez użytkownika.")
            logging.info("Przerwano przez użytkownika (KeyboardInterrupt)")
            break
        except Exception as e:
            print(f"\n❌ Nieoczekiwany błąd: {e}")
            logging.error(f"Nieoczekiwany błąd: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except Exception as e:
        print(f"\n❌ Krytyczny błąd: {e}")
        logging.critical(f"Krytyczny błąd: {e}", exc_info=True)
        sys.exit(1)