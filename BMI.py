"""
Kalkulator BMI (Body Mass Index)
Oblicza wskaźnik masy ciała i podaje rekomendacje zdrowotne.
"""

def oblicz_bmi(waga: float, wzrost: float) -> float:
    """Oblicza BMI na podstawie wagi (kg) i wzrostu (cm)."""
    return waga / ((wzrost / 100) ** 2)


def klasyfikuj_bmi(bmi: float) -> tuple[str, str, tuple[float, float]]:
    """
    Zwraca kategorię BMI, opis i zakres prawidłowy.

    Returns:
        (kategoria, kolor_emoji, (min_bmi, max_bmi))
    """
    if bmi < 16:
        return ("wygłodzenie", "🚨", (18.5, 24.99))
    elif bmi < 17:
        return ("wychudzenie", "⚠️", (18.5, 24.99))
    elif bmi < 18.5:
        return ("niedowaga", "⚠️", (18.5, 24.99))
    elif bmi < 25:
        return ("waga prawidłowa", "✅", (18.5, 24.99))
    elif bmi < 30:
        return ("nadwaga", "⚠️", (18.5, 24.99))
    elif bmi < 35:
        return ("I stopień otyłości", "🚨", (18.5, 24.99))
    elif bmi < 40:
        return ("II stopień otyłości", "🚨", (18.5, 24.99))
    else:
        return ("otyłość skrajna", "🔴", (18.5, 24.99))


def oblicz_procentowa_roznice(bmi: float, cel: float) -> float:
    """Oblicza różnicę procentową między BMI a celem."""
    return round(((bmi / cel) - 1) * 100, 2)


def pobierz_float(prompt: str, min_val: float = 0) -> float:
    """Pobiera liczbę zmiennoprzecinkową z walidacją."""
    while True:
        try:
            wartosc = float(input(prompt))
            if wartosc <= min_val:
                print(f"❌ Wartość musi być większa niż {min_val}!")
                continue
            return wartosc
        except ValueError:
            print("❌ Niepoprawna wartość! Podaj liczbę.")


def main():
    """Główna funkcja programu."""
    print("=" * 50)
    print("📊 KALKULATOR BMI".center(50))
    print("=" * 50)

    # Pobierz dane
    imie = input("\n👤 Jak masz na imię? ").strip()
    if not imie:
        imie = "Przyjacielu"

    print(f"\n🤝 Miło mi Cię poznać, {imie}!\n")

    waga = pobierz_float("⚖️  Podaj swoją wagę (kg): ", min_val=0)
    wzrost = pobierz_float("📏 Podaj swój wzrost (cm): ", min_val=0)

    # Oblicz BMI
    bmi = oblicz_bmi(waga, wzrost)
    kategoria, emoji, (min_bmi, max_bmi) = klasyfikuj_bmi(bmi)

    # Wyświetl wynik
    print("\n" + "=" * 50)
    print(f"{emoji} Twoje BMI: {bmi:.2f}")
    print(f"   Kategoria: {kategoria}")
    print("=" * 50)

    # Rekomendacje
    if bmi < min_bmi:
        roznica = oblicz_procentowa_roznice(bmi, min_bmi)
        brakujaca_waga = round((min_bmi / bmi - 1) * waga, 2)
        print(f"\n💡 {imie}, masz niedowagę.")
        print(f"   Twoje BMI jest o {abs(roznica):.2f}% poniżej normy.")
        print(f"   Aby osiągnąć BMI {min_bmi}, należy zwiększyć wagę o ~{brakujaca_waga} kg.")
    elif bmi > max_bmi:
        roznica = oblicz_procentowa_roznice(bmi, max_bmi)
        nadmiar_wagi = round((1 - max_bmi / bmi) * waga, 2)
        print(f"\n💡 {imie}, masz nadwagę.")
        print(f"   Twoje BMI jest o {roznica:.2f}% powyżej normy.")
        print(f"   Aby osiągnąć BMI {max_bmi}, należy zmniejszyć wagę o ~{nadmiar_wagi} kg.")
    else:
        print(f"\n🎉 Gratulacje, {imie}! Twoja waga jest prawidłowa!")
        print(f"   Jesteś w zdrowym zakresie {min_bmi} - {max_bmi}.")

    print("\n" + "=" * 50)
    print("ℹ️  Pamiętaj: BMI to tylko orientacyjny wskaźnik.")
    print("   Skonsultuj się z lekarzem w sprawach zdrowia!")
    print("=" * 50)


if __name__ == "__main__":
    main()