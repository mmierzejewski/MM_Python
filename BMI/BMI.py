#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kalkulator BMI (Body Mass Index) - Advanced Version

Oblicza wskaźnik masy ciała i podaje rekomendacje zdrowotne.
Uwzględnia płeć, oferuje wielokrotne obliczenia i eksport wyników.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from enum import Enum


# Konfiguracja loggingu
log_file = Path.cwd() / 'bmi_calculator.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)


class Gender(Enum):
    """Płeć użytkownika."""
    MALE = "mężczyzna"
    FEMALE = "kobieta"
    OTHER = "inna"


# Kategorie BMI według WHO
BMI_CATEGORIES = {
    'starvation': {
        'range': (0, 16),
        'name': 'wygłodzenie',
        'emoji': '🚨',
        'severity': 'critical'
    },
    'severe_underweight': {
        'range': (16, 17),
        'name': 'wychudzenie',
        'emoji': '⚠️',
        'severity': 'high'
    },
    'underweight': {
        'range': (17, 18.5),
        'name': 'niedowaga',
        'emoji': '⚠️',
        'severity': 'medium'
    },
    'normal': {
        'range': (18.5, 25),
        'name': 'waga prawidłowa',
        'emoji': '✅',
        'severity': 'none'
    },
    'overweight': {
        'range': (25, 30),
        'name': 'nadwaga',
        'emoji': '⚠️',
        'severity': 'medium'
    },
    'obesity_1': {
        'range': (30, 35),
        'name': 'I stopień otyłości',
        'emoji': '🚨',
        'severity': 'high'
    },
    'obesity_2': {
        'range': (35, 40),
        'name': 'II stopień otyłości',
        'emoji': '🚨',
        'severity': 'critical'
    },
    'obesity_3': {
        'range': (40, float('inf')),
        'name': 'otyłość skrajna',
        'emoji': '🔴',
        'severity': 'critical'
    }
}

# Zakresy prawidłowe (różne dla kobiet i mężczyzn)
HEALTHY_BMI_RANGE = {
    Gender.MALE: (20, 25),
    Gender.FEMALE: (19, 24),
    Gender.OTHER: (18.5, 24.99)
}


def oblicz_bmi(waga: float, wzrost: float) -> float:
    """Oblicza BMI na podstawie wagi (kg) i wzrostu (cm)."""
    return waga / ((wzrost / 100) ** 2)


def klasyfikuj_bmi(bmi: float, gender: Gender = Gender.OTHER) -> tuple[str, str, tuple[float, float], str]:
    """
    Zwraca kategorię BMI, opis i zakres prawidłowy.
    
    Args:
        bmi: Wartość BMI
        gender: Płeć użytkownika

    Returns:
        (kategoria, kolor_emoji, (min_bmi, max_bmi), severity)
    """
    # Znajdź odpowiednią kategorię
    for category_data in BMI_CATEGORIES.values():
        min_val, max_val = category_data['range']
        if min_val <= bmi < max_val:
            healthy_range = HEALTHY_BMI_RANGE[gender]
            return (
                category_data['name'],
                category_data['emoji'],
                healthy_range,
                category_data['severity']
            )
    
    # Fallback (nie powinno się zdarzyć)
    healthy_range = HEALTHY_BMI_RANGE[gender]
    return ("nieznana kategoria", "❓", healthy_range, "unknown")


def oblicz_procentowa_roznice(bmi: float, cel: float) -> float:
    """Oblicza różnicę procentową między BMI a celem."""
    return round(((bmi / cel) - 1) * 100, 2)


def oblicz_docelowa_wage(wzrost_cm: float, cel_bmi: float) -> float:
    """
    Oblicza docelową wagę dla określonego BMI.
    
    Args:
        wzrost_cm: Wzrost w centymetrach
        cel_bmi: Docelowe BMI
    
    Returns:
        Docelowa waga w kilogramach
    """
    wzrost_m = wzrost_cm / 100
    return cel_bmi * (wzrost_m ** 2)


def pobierz_plec() -> Gender:
    """Pobiera płeć użytkownika."""
    print("\n👤 Płeć (wpływa na zakres prawidłowy):")
    print("   1. Mężczyzna")
    print("   2. Kobieta")
    print("   3. Inna / Wolę nie podawać")
    
    while True:
        wybor = input("   Wybór [3]: ").strip() or "3"
        if wybor == "1":
            return Gender.MALE
        elif wybor == "2":
            return Gender.FEMALE
        elif wybor == "3":
            return Gender.OTHER
        else:
            print("❌ Niepoprawny wybór! Podaj 1, 2 lub 3.")


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
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Przerwano")
            raise


def eksportuj_wynik(
    imie: str,
    waga: float,
    wzrost: float,
    bmi: float,
    kategoria: str,
    gender: Gender,
    rekomendacje: str
) -> None:
    """
    Eksportuje wynik do pliku tekstowego.
    
    Args:
        imie: Imię użytkownika
        waga: Waga w kg
        wzrost: Wzrost w cm
        bmi: Obliczone BMI
        kategoria: Kategoria BMI
        gender: Płeć
        rekomendacje: Tekst rekomendacji
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bmi_wynik_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*50 + "\n")
            f.write("📊 WYNIK KALKULACJI BMI\n")
            f.write("="*50 + "\n\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Imię: {imie}\n")
            f.write(f"Płeć: {gender.value}\n")
            f.write(f"Waga: {waga} kg\n")
            f.write(f"Wzrost: {wzrost} cm\n\n")
            f.write(f"BMI: {bmi:.2f}\n")
            f.write(f"Kategoria: {kategoria}\n\n")
            f.write("REKOMENDACJE:\n")
            f.write(rekomendacje + "\n\n")
            f.write("="*50 + "\n")
            f.write("ℹ️  Pamiętaj: BMI to tylko orientacyjny wskaźnik.\n")
            f.write("   Skonsultuj się z lekarzem w sprawach zdrowia!\n")
            f.write("="*50 + "\n")
        
        print(f"\n💾 Wynik zapisany do pliku: {filename}")
        logging.info(f"Wynik wyeksportowany do {filename}")
    except IOError as e:
        print(f"\n❌ Błąd zapisu pliku: {e}")
        logging.error(f"Błąd eksportu: {e}")


def oblicz_bmi_session(
    imie: str,
    waga: float,
    wzrost: float,
    gender: Gender
) -> tuple[float, str, str, str]:
    """
    Wykonuje sesję obliczania BMI.
    
    Returns:
        (bmi, kategoria, emoji, rekomendacje_text)
    """
    # Oblicz BMI
    bmi = oblicz_bmi(waga, wzrost)
    kategoria, emoji, (min_bmi, max_bmi), severity = klasyfikuj_bmi(bmi, gender)
    
    logging.info(f"Obliczono BMI: {bmi:.2f} dla {imie} (płeć: {gender.value})")
    
    # Wyświetl wynik
    print("\n" + "=" * 50)
    print(f"{emoji}  Twoje BMI: {bmi:.2f}")
    print(f"   Kategoria: {kategoria}")
    print(f"   Zakres prawidłowy: {min_bmi} - {max_bmi}")
    print("=" * 50)
    
    # Generuj rekomendacje
    rekomendacje_lines = []
    
    if bmi < min_bmi:
        roznica = oblicz_procentowa_roznice(bmi, min_bmi)
        docelowa_waga = oblicz_docelowa_wage(wzrost, min_bmi)
        roznica_wagi = docelowa_waga - waga
        
        print(f"\n💡 {imie}, masz niedowagę.")
        print(f"   Twoje BMI jest o {abs(roznica):.2f}% poniżej normy.")
        print(f"   Docelowa waga (BMI {min_bmi}): {docelowa_waga:.2f} kg")
        print(f"   Należy zwiększyć wagę o ~{roznica_wagi:.2f} kg.")
        
        rekomendacje_lines = [
            f"{imie}, masz niedowagę.",
            f"Twoje BMI jest o {abs(roznica):.2f}% poniżej normy.",
            f"Docelowa waga (BMI {min_bmi}): {docelowa_waga:.2f} kg",
            f"Należy zwiększyć wagę o ~{roznica_wagi:.2f} kg."
        ]
        
    elif bmi > max_bmi:
        roznica = oblicz_procentowa_roznice(bmi, max_bmi)
        docelowa_waga = oblicz_docelowa_wage(wzrost, max_bmi)
        roznica_wagi = waga - docelowa_waga
        
        print(f"\n💡 {imie}, masz nadwagę.")
        print(f"   Twoje BMI jest o {roznica:.2f}% powyżej normy.")
        print(f"   Docelowa waga (BMI {max_bmi}): {docelowa_waga:.2f} kg")
        print(f"   Należy zmniejszyć wagę o ~{roznica_wagi:.2f} kg.")
        
        rekomendacje_lines = [
            f"{imie}, masz nadwagę.",
            f"Twoje BMI jest o {roznica:.2f}% powyżej normy.",
            f"Docelowa waga (BMI {max_bmi}): {docelowa_waga:.2f} kg",
            f"Należy zmniejszyć wagę o ~{roznica_wagi:.2f} kg."
        ]
        
    else:
        print(f"\n🎉 Gratulacje, {imie}! Twoja waga jest prawidłowa!")
        print(f"   Jesteś w zdrowym zakresie {min_bmi} - {max_bmi}.")
        print(f"   Utrzymuj zdrowy styl życia! 💪")
        
        rekomendacje_lines = [
            f"Gratulacje, {imie}! Twoja waga jest prawidłowa!",
            f"Jesteś w zdrowym zakresie {min_bmi} - {max_bmi}.",
            "Utrzymuj zdrowy styl życia!"
        ]
    
    rekomendacje_text = "\n".join(rekomendacje_lines)
    
    return bmi, kategoria, emoji, rekomendacje_text


def main() -> None:
    """Główna funkcja programu."""
    print("=" * 50)
    print("📊 KALKULATOR BMI - ADVANCED".center(50))
    print("=" * 50)
    
    logging.info("Uruchomiono kalkulator BMI")
    
    try:
        while True:
            # Pobierz dane
            imie = input("\n👤 Jak masz na imię? ").strip()
            if not imie:
                imie = "Przyjacielu"
            
            print(f"\n🤝 Miło mi Cię poznać, {imie}!")
            
            # Pobierz płeć
            gender = pobierz_plec()
            
            print()
            waga = pobierz_float("⚖️  Podaj swoją wagę (kg): ", min_val=0)
            wzrost = pobierz_float("📏 Podaj swój wzrost (cm): ", min_val=0)
            
            # Oblicz BMI i wyświetl wyniki
            bmi, kategoria, emoji, rekomendacje = oblicz_bmi_session(
                imie, waga, wzrost, gender
            )
            
            print("\n" + "=" * 50)
            print("ℹ️  Pamiętaj: BMI to tylko orientacyjny wskaźnik.")
            print("   Skonsultuj się z lekarzem w sprawach zdrowia!")
            print("=" * 50)
            
            # Opcja eksportu
            eksport = input("\n💾 Zapisać wynik do pliku? (T/N) [N]: ").strip().upper()
            if eksport == 'T':
                eksportuj_wynik(imie, waga, wzrost, bmi, kategoria, gender, rekomendacje)
            
            # Pytanie o kolejne obliczenie
            print("\n" + "-" * 50)
            ponownie = input("🔄 Obliczyć ponownie? (T/N) [N]: ").strip().upper()
            if ponownie != 'T':
                print("\n👋 Dziękuję za skorzystanie z kalkulatora BMI!")
                print("   Dbaj o zdrowie! 💚\n")
                logging.info("Zakończono działanie kalkulatora")
                break
            
            print("\n" + "=" * 50)
    
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Przerwano przez użytkownika")
        logging.info("Przerwano przez użytkownika")
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
        exit(1)