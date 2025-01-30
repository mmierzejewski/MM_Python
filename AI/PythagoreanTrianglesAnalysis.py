import math


def czy_pierwsza(liczba):
    """Check if a number is prime."""
    if liczba <= 1:
        return False
    for i in range(2, int(math.sqrt(liczba)) + 1):
        if liczba % i == 0:
            return False
    return True


def liczby_pierwsze_do(limit):
    """Generate all prime numbers up to the specified limit."""
    return [i for i in range(2, limit + 1) if czy_pierwsza(i)]


def zawiera_liczbe_pierwsza(trojkat, liczby_pierwsze):
    """Check if a triangle contains any prime number."""
    return any(liczba in liczby_pierwsze for liczba in trojkat)


def trojkaty_pitagorejskie(limit):
    """Generate all Pythagorean triangles with perimeter less than the limit."""
    trojkaty = []
    for a in range(1, limit):
        for b in range(a, limit):
            c = math.sqrt(a ** 2 + b ** 2)
            if c == int(c) and a + b + int(c) < limit:
                trojkaty.append((a, b, int(c)))
    return trojkaty


def main():
    try:
        limit = int(input("Podaj wartość limitu: "))
        if limit <= 0:
            print("Limit musi być liczbą dodatnią. Spróbuj ponownie.")
            return
    except ValueError:
        print("Nieprawidłowa wartość! Wprowadź liczbę całkowitą.")
        return

    # Generate all Pythagorean triangles
    trojkaty = trojkaty_pitagorejskie(limit)
    if not trojkaty:
        print("Nie znaleziono trójkątów pitagorejskich dla podanego limitu.")
        return

    # Sort triangles by their perimeter
    trojkaty.sort(key=lambda x: sum(x))

    print("\nTrójkąty pitagorejskie od najmniejszego do największego obwodu:")
    for a, b, c in trojkaty:
        print(f"({a}, {b}, {c})\tobwód: {sum((a, b, c))}")

    # Find the largest number in any of the triangles
    maksymalna_wartosc = max(max(trojkat) for trojkat in trojkaty)

    # Generate all prime numbers up to the largest value
    liczby_pierwsze = liczby_pierwsze_do(maksymalna_wartosc)

    print("\nWszystkie liczby pierwsze w zakresie od 1 do największej wartości w trójkątach:")
    print(", ".join(map(str, liczby_pierwsze)))

    print("\nTrójkąty pitagorejskie zawierające jedną lub więcej liczb pierwszych:")
    for a, b, c in trojkaty:
        if zawiera_liczbe_pierwsza((a, b, c), liczby_pierwsze):
            print(f"({a}, {b}, {c})\tobwód: {sum((a, b, c))}")


if __name__ == "__main__":
    main()