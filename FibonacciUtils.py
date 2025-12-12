"""
FibonacciUtils - Narzędzia do generowania i analizy ciągu Fibonacciego.

Ciąg Fibonacciego: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)
"""

from typing import List, Union
import sys


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


def get_nth_fibonacci(n: int) -> int:
    """
    Zwraca n-tą liczbę Fibonacciego (indeksacja od 1).

    Args:
        n: Pozycja w ciągu (1-indexed: F(1)=0, F(2)=1, F(3)=1, F(4)=2...)

    Returns:
        n-ta liczba Fibonacciego

    Raises:
        FibonacciError: Gdy n <= 0

    Example:
        >>> get_nth_fibonacci(7)
        8
    """
    if n <= 0:
        raise FibonacciError("Pozycja musi być dodatnią liczbą całkowitą!")

    if n == 1:
        return 0
    if n == 2:
        return 1

    fib_prev, fib_curr = 0, 1
    for _ in range(2, n):
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


def fibonacci_fast(n: int) -> int:
    """
    Szybkie obliczanie n-tej liczby Fibonacciego metodą macierzową.
    Złożoność: O(log n)

    Args:
        n: Pozycja w ciągu (0-indexed: F(0)=0, F(1)=1, F(2)=1...)

    Returns:
        n-ta liczba Fibonacciego
    """
    if n <= 0:
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


def print_fibonacci_info(n: int) -> None:
    """Wyświetla szczegółowe informacje o n-tej liczbie Fibonacciego."""
    try:
        fib_n = get_nth_fibonacci(n)
        fib_seq = generate_first_n_fibonacci(n)

        print(f"\n{'=' * 60}")
        print(f"📊 INFORMACJE O F({n})")
        print(f"{'=' * 60}")
        print(f"Wartość: {fib_n:,}")
        print(f"Liczba cyfr: {len(str(fib_n))}")
        print(f"Ciąg do F({n}): {fib_seq[:10]}{'...' if n > 10 else ''}")

        if n > 1:
            ratio = fib_seq[-1] / fib_seq[-2]
            golden_ratio = (1 + 5 ** 0.5) / 2
            print(f"Stosunek F({n})/F({n-1}): {ratio:.10f}")
            print(f"Złoty podział φ: {golden_ratio:.10f}")
            print(f"Różnica: {abs(ratio - golden_ratio):.10e}")

        print(f"{'=' * 60}\n")
    except FibonacciError as e:
        print(f"❌ Błąd: {e}")


def main():
    """Główna funkcja programu."""
    print("=" * 60)
    print("🔢 KALKULATOR CIĄGU FIBONACCIEGO".center(60))
    print("=" * 60)

    while True:
        print("\nWybierz opcję:")
        print("1. Generuj liczby Fibonacciego do wartości")
        print("2. Pobierz n-tą liczbę Fibonacciego")
        print("3. Generuj pierwsze n liczb Fibonacciego")
        print("4. Szybkie obliczanie (algorytm O(log n))")
        print("5. Sprawdź, czy liczba jest liczbą Fibonacciego")
        print("6. Szczegółowe informacje o F(n)")
        print("0. Wyjście")

        try:
            choice = input("\n👉 Twój wybór (0-6): ").strip()

            if choice == "0":
                print("\n👋 Do zobaczenia!")
                break

            elif choice == "1":
                max_val = int(input("Podaj wartość maksymalną: "))
                result = generate_fibonacci_upto(max_val)
                print(f"\n✅ Liczby Fibonacciego ≤ {max_val}:")
                print(f"   {result}")
                print(f"   Znaleziono: {len(result)} liczb")

            elif choice == "2":
                n = int(input("Podaj pozycję n (1-indexed): "))
                result = get_nth_fibonacci(n)
                print(f"\n✅ F({n}) = {result:,}")

            elif choice == "3":
                n = int(input("Ile liczb wygenerować: "))
                result = generate_first_n_fibonacci(n)
                if len(result) <= 20:
                    print(f"\n✅ Pierwsze {n} liczby: {result}")
                else:
                    print(f"\n✅ Pierwsze 10: {result[:10]}")
                    print(f"   Ostatnie 10: {result[-10:]}")
                    print(f"   (pominięto {len(result) - 20} środkowych)")

            elif choice == "4":
                n = int(input("Podaj n (0-indexed, dla dużych n): "))
                result = fibonacci_fast(n)
                print(f"\n✅ F({n}) = {result:,}")
                print(f"   Liczba cyfr: {len(str(result))}")

            elif choice == "5":
                num = int(input("Podaj liczbę do sprawdzenia: "))
                if is_fibonacci(num):
                    print(f"\n✅ {num:,} JEST liczbą Fibonacciego!")
                else:
                    print(f"\n❌ {num:,} NIE JEST liczbą Fibonacciego.")

            elif choice == "6":
                n = int(input("Podaj n: "))
                print_fibonacci_info(n)

            else:
                print("\n❌ Nieprawidłowy wybór! Wybierz 0-6.")

        except ValueError:
            print("\n❌ Nieprawidłowe dane! Podaj liczbę całkowitą.")
        except FibonacciError as e:
            print(f"\n❌ Błąd: {e}")
        except KeyboardInterrupt:
            print("\n\n👋 Przerwano przez użytkownika.")
            break
        except Exception as e:
            print(f"\n❌ Nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    main()