#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quiz o Harry Potterze - interaktywna gra sprawdzająca wiedzę użytkownika.
"""

CORRECT_PLATFORM = "9 i 3/4"
MAX_AGE = 100
MIN_READING_AGE = 6


def get_valid_age():
    """Pobiera i waliduje wiek użytkownika."""
    while True:
        try:
            age_str = input("Ile masz lat?\n").strip()
            age = int(age_str)
            if age < 0:
                print("Wiek nie może być ujemny!")
                continue
            if age > 150:
                print("Wpisz realny wiek!")
                continue
            return age
        except ValueError:
            print("Proszę wpisać liczbę!")


def main():
    """Główna funkcja quizu."""
    # Powitanie
    imie = input("Jak masz na imię?\n").strip()
    komputer = "Laptop"
    print(f"Miło mi Cię poznać, {imie}!")
    print(f"Mam na imię {komputer}.")

    # Sprawdzenie wieku
    wiek = get_valid_age()

    if wiek <= MIN_READING_AGE:
        print(f"{imie}, jesteś za młody(-a) aby samodzielnie przeczytać książkę.")
    elif wiek >= MAX_AGE:
        print(f"Jesteś już za stary(-a) na czytanie, {imie}.")
        print("Lepiej siedź w domu.")
    else:
        lata_do_setki = MAX_AGE - wiek
        print(f"To bardzo dobry wiek! Do setki masz jeszcze {lata_do_setki} lat.")
        print("Z jakiego peronu dostaniesz się do Hogwartu?")

        peron = input().strip()

        if peron == CORRECT_PLATFORM:
            print(f"{imie}, to bardzo dobra odpowiedź!")
        else:
            print(f"{imie}, prawidłowa nazwa peronu to '{CORRECT_PLATFORM}'.")
            print("Nie przeczytałeś(-aś) książek o HP. Czas na lekturę.")

    print(f"\nDziękuję za miłą rozmowę.\nPozdrawiam, {komputer}.")


if __name__ == "__main__":
    main()