#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMI (Body Mass Index) Calculator - Advanced Version

Calculates the body mass index and provides health recommendations.
Takes gender into account, offers multiple calculations and result export.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from enum import Enum


# Logging configuration
log_file = Path.cwd() / 'bmi_calculator.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)


class Gender(Enum):
    """User's gender."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


# BMI categories according to WHO
BMI_CATEGORIES = {
    'starvation': {
        'range': (0, 16),
        'name': 'starvation',
        'emoji': '🚨',
        'severity': 'critical'
    },
    'severe_underweight': {
        'range': (16, 17),
        'name': 'severe underweight',
        'emoji': '⚠️',
        'severity': 'high'
    },
    'underweight': {
        'range': (17, 18.5),
        'name': 'underweight',
        'emoji': '⚠️',
        'severity': 'medium'
    },
    'normal': {
        'range': (18.5, 25),
        'name': 'normal weight',
        'emoji': '✅',
        'severity': 'none'
    },
    'overweight': {
        'range': (25, 30),
        'name': 'overweight',
        'emoji': '⚠️',
        'severity': 'medium'
    },
    'obesity_1': {
        'range': (30, 35),
        'name': 'obesity class I',
        'emoji': '🚨',
        'severity': 'high'
    },
    'obesity_2': {
        'range': (35, 40),
        'name': 'obesity class II',
        'emoji': '🚨',
        'severity': 'critical'
    },
    'obesity_3': {
        'range': (40, float('inf')),
        'name': 'extreme obesity',
        'emoji': '🔴',
        'severity': 'critical'
    }
}

# Healthy ranges (different for women and men)
HEALTHY_BMI_RANGE = {
    Gender.MALE: (20, 25),
    Gender.FEMALE: (19, 24),
    Gender.OTHER: (18.5, 24.99)
}


def oblicz_bmi(waga: float, wzrost: float) -> float:
    """Calculates BMI based on weight (kg) and height (cm)."""
    return waga / ((wzrost / 100) ** 2)


def klasyfikuj_bmi(bmi: float, gender: Gender = Gender.OTHER) -> tuple[str, str, tuple[float, float], str]:
    """
    Returns the BMI category, description and the healthy range.
    
    Args:
        bmi: BMI value
        gender: User's gender

    Returns:
        (category, emoji_color, (min_bmi, max_bmi), severity)
    """
    # Find the matching category
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
    
    # Fallback (should not happen)
    healthy_range = HEALTHY_BMI_RANGE[gender]
    return ("unknown category", "❓", healthy_range, "unknown")


def oblicz_procentowa_roznice(bmi: float, cel: float) -> float:
    """Calculates the percentage difference between BMI and the target."""
    return round(((bmi / cel) - 1) * 100, 2)


def oblicz_docelowa_wage(wzrost_cm: float, cel_bmi: float) -> float:
    """
    Calculates the target weight for a given BMI.
    
    Args:
        wzrost_cm: Height in centimeters
        cel_bmi: Target BMI
    
    Returns:
        Target weight in kilograms
    """
    wzrost_m = wzrost_cm / 100
    return cel_bmi * (wzrost_m ** 2)


def pobierz_plec() -> Gender:
    """Gets the user's gender."""
    print("\n👤 Gender (affects the healthy range):")
    print("   1. Male")
    print("   2. Female")
    print("   3. Other / Prefer not to say")
    
    while True:
        wybor = input("   Choice [3]: ").strip() or "3"
        if wybor == "1":
            return Gender.MALE
        elif wybor == "2":
            return Gender.FEMALE
        elif wybor == "3":
            return Gender.OTHER
        else:
            print("❌ Invalid choice! Enter 1, 2 or 3.")


def pobierz_float(prompt: str, min_val: float = 0) -> float:
    """Gets a floating-point number with validation."""
    while True:
        try:
            wartosc = float(input(prompt))
            if wartosc <= min_val:
                print(f"❌ The value must be greater than {min_val}!")
                continue
            return wartosc
        except ValueError:
            print("❌ Invalid value! Enter a number.")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Interrupted")
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
    Exports the result to a text file.
    
    Args:
        imie: User's name
        waga: Weight in kg
        wzrost: Height in cm
        bmi: Calculated BMI
        kategoria: BMI category
        gender: Gender
        rekomendacje: Recommendations text
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bmi_wynik_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*50 + "\n")
            f.write("📊 BMI CALCULATION RESULT\n")
            f.write("="*50 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Name: {imie}\n")
            f.write(f"Gender: {gender.value}\n")
            f.write(f"Weight: {waga} kg\n")
            f.write(f"Height: {wzrost} cm\n\n")
            f.write(f"BMI: {bmi:.2f}\n")
            f.write(f"Category: {kategoria}\n\n")
            f.write("RECOMMENDATIONS:\n")
            f.write(rekomendacje + "\n\n")
            f.write("="*50 + "\n")
            f.write("ℹ️  Remember: BMI is only an approximate indicator.\n")
            f.write("   Consult a doctor about health matters!\n")
            f.write("="*50 + "\n")
        
        print(f"\n💾 Result saved to file: {filename}")
        logging.info(f"Result exported to {filename}")
    except IOError as e:
        print(f"\n❌ File write error: {e}")
        logging.error(f"Export error: {e}")


def oblicz_bmi_session(
    imie: str,
    waga: float,
    wzrost: float,
    gender: Gender
) -> tuple[float, str, str, str]:
    """
    Performs a BMI calculation session.
    
    Returns:
        (bmi, kategoria, emoji, rekomendacje_text)
    """
    # Calculate BMI
    bmi = oblicz_bmi(waga, wzrost)
    kategoria, emoji, (min_bmi, max_bmi), severity = klasyfikuj_bmi(bmi, gender)
    
    logging.info(f"Calculated BMI: {bmi:.2f} for {imie} (gender: {gender.value})")
    
    # Display the result
    print("\n" + "=" * 50)
    print(f"{emoji}  Your BMI: {bmi:.2f}")
    print(f"   Category: {kategoria}")
    print(f"   Healthy range: {min_bmi} - {max_bmi}")
    print("=" * 50)
    
    # Generate recommendations
    rekomendacje_lines = []
    
    if bmi < min_bmi:
        roznica = oblicz_procentowa_roznice(bmi, min_bmi)
        docelowa_waga = oblicz_docelowa_wage(wzrost, min_bmi)
        roznica_wagi = docelowa_waga - waga
        
        print(f"\n💡 {imie}, you are underweight.")
        print(f"   Your BMI is {abs(roznica):.2f}% below the normal range.")
        print(f"   Target weight (BMI {min_bmi}): {docelowa_waga:.2f} kg")
        print(f"   You should gain ~{roznica_wagi:.2f} kg.")
        
        rekomendacje_lines = [
            f"{imie}, you are underweight.",
            f"Your BMI is {abs(roznica):.2f}% below the normal range.",
            f"Target weight (BMI {min_bmi}): {docelowa_waga:.2f} kg",
            f"You should gain ~{roznica_wagi:.2f} kg."
        ]
        
    elif bmi > max_bmi:
        roznica = oblicz_procentowa_roznice(bmi, max_bmi)
        docelowa_waga = oblicz_docelowa_wage(wzrost, max_bmi)
        roznica_wagi = waga - docelowa_waga
        
        print(f"\n💡 {imie}, you are overweight.")
        print(f"   Your BMI is {roznica:.2f}% above the normal range.")
        print(f"   Target weight (BMI {max_bmi}): {docelowa_waga:.2f} kg")
        print(f"   You should lose ~{roznica_wagi:.2f} kg.")
        
        rekomendacje_lines = [
            f"{imie}, you are overweight.",
            f"Your BMI is {roznica:.2f}% above the normal range.",
            f"Target weight (BMI {max_bmi}): {docelowa_waga:.2f} kg",
            f"You should lose ~{roznica_wagi:.2f} kg."
        ]
        
    else:
        print(f"\n🎉 Congratulations, {imie}! Your weight is normal!")
        print(f"   You are in the healthy range {min_bmi} - {max_bmi}.")
        print(f"   Keep up a healthy lifestyle! 💪")
        
        rekomendacje_lines = [
            f"Congratulations, {imie}! Your weight is normal!",
            f"You are in the healthy range {min_bmi} - {max_bmi}.",
            "Keep up a healthy lifestyle!"
        ]
    
    rekomendacje_text = "\n".join(rekomendacje_lines)
    
    return bmi, kategoria, emoji, rekomendacje_text


def main() -> None:
    """Main program function."""
    print("=" * 50)
    print("📊 BMI CALCULATOR - ADVANCED".center(50))
    print("=" * 50)
    
    logging.info("BMI calculator started")
    
    try:
        while True:
            # Get data
            imie = input("\n👤 What's your name? ").strip()
            if not imie:
                imie = "Friend"
            
            print(f"\n🤝 Nice to meet you, {imie}!")
            
            # Get gender
            gender = pobierz_plec()
            
            print()
            waga = pobierz_float("⚖️  Enter your weight (kg): ", min_val=0)
            wzrost = pobierz_float("📏 Enter your height (cm): ", min_val=0)
            
            # Calculate BMI and display the results
            bmi, kategoria, emoji, rekomendacje = oblicz_bmi_session(
                imie, waga, wzrost, gender
            )
            
            print("\n" + "=" * 50)
            print("ℹ️  Remember: BMI is only an approximate indicator.")
            print("   Consult a doctor about health matters!")
            print("=" * 50)
            
            # Export option
            eksport = input("\n💾 Save the result to a file? (Y/N) [N]: ").strip().upper()
            if eksport == 'Y':
                eksportuj_wynik(imie, waga, wzrost, bmi, kategoria, gender, rekomendacje)
            
            # Ask about another calculation
            print("\n" + "-" * 50)
            ponownie = input("🔄 Calculate again? (Y/N) [N]: ").strip().upper()
            if ponownie != 'Y':
                print("\n👋 Thank you for using the BMI calculator!")
                print("   Take care of your health! 💚\n")
                logging.info("Calculator stopped")
                break
            
            print("\n" + "=" * 50)
    
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Interrupted by the user")
        logging.info("Interrupted by the user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        logging.critical(f"Critical error: {e}", exc_info=True)
        exit(1)