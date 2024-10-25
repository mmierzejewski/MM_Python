import math


def czy_pierwsza(liczba):
    if liczba <= 1:
        return False
    for i in range(2, int(math.sqrt(liczba)) + 1):
        if liczba % i == 0:
            return False
    return True


def liczby_pierwsze_do(limit):
    liczby = []
    for i in range(2, limit + 1):
        if czy_pierwsza(i):
            liczby.append(i)
    return liczby


def zawiera_liczbe_pierwsza(trojkat, liczby_pierwsze):
    for liczba in trojkat:
        if liczba in liczby_pierwsze:
            return True
    return False


def trojkaty_pitagorejskie(limit):
    trojkaty = []
    for a in range(1, limit):
        for b in range(a, limit):
            c = math.sqrt(a ** 2 + b ** 2)
            if c == int(c) and a + b + int(c) < limit:
                trojkaty.append((a, b, int(c)))
    return trojkaty


def main():
    limit = int(input("Podaj wartość limitu: "))
    trojkaty = trojkaty_pitagorejskie(limit)
    trojkaty.sort(key=lambda x: sum(x))

    print("\nTrójkąty pitagorejskie od najmniejszego do największego obwodu:")

    for a, b, c in trojkaty:
        obwod = sum((a, b, c))
        print(f"({a}, {b}, {c})\tobwod: {obwod}")

    najwieksza_wartosc = max(max(trojkat) for trojkat in trojkaty)

   # print(f"\nNajwiększa wartość w tabeli: {najwieksza_wartosc}")

    liczby_pierwsze = liczby_pierwsze_do(najwieksza_wartosc)
    # print("\nWszystkie liczby pierwsze:")

    for liczba in liczby_pierwsze:
        print(liczba)

    print("\nTrójkąty pitagorejskie zawierające jedną lub więcej liczb pierwszych:")
    for a, b, c in trojkaty:
        obwod1 = sum((a, b, c))
        if zawiera_liczbe_pierwsza((a, b, c), liczby_pierwsze):
            print(f"({a}, {b}, {c})\tobwod: {obwod1}")

if __name__ == "__main__":
    main()
