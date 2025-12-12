# 📊 BMI Calculator - Advanced

Zaawansowany kalkulator BMI (Body Mass Index) z rekomendacjami zdrowotnymi, uwzględnieniem płci i opcją eksportu wyników.

## ✨ Features

- 📏 **Dokładne obliczenia BMI** - wzór: waga(kg) / (wzrost(m))²
- 👥 **Uwzględnienie płci** - różne zakresy prawidłowe dla mężczyzn i kobiet
- 🎯 **Dokładne rekomendacje** - obliczanie docelowej wagi
- 🔄 **Wielokrotne obliczenia** - możliwość wykonania wielu pomiarów w jednej sesji
- 💾 **Eksport do pliku** - zapisanie wyników z timestampem
- 📝 **Logging** - śledzenie sesji w pliku log
- 🛡️ **Obsługa błędów** - pełna walidacja i error handling
- 🌈 **Przyjazny UI** - emoji, kolory, czytelne komunikaty

## 📋 Kategorie BMI (według WHO)

| BMI Range | Kategoria | Status |
|-----------|-----------|--------|
| < 16.0 | Wygłodzenie | 🚨 Krytyczne |
| 16.0 - 17.0 | Wychudzenie | ⚠️ Wysokie ryzyko |
| 17.0 - 18.5 | Niedowaga | ⚠️ Średnie ryzyko |
| 18.5 - 25.0 | Waga prawidłowa | ✅ Zdrowe |
| 25.0 - 30.0 | Nadwaga | ⚠️ Średnie ryzyko |
| 30.0 - 35.0 | Otyłość I° | 🚨 Wysokie ryzyko |
| 35.0 - 40.0 | Otyłość II° | 🚨 Krytyczne |
| ≥ 40.0 | Otyłość skrajna III° | 🔴 Bardzo krytyczne |

## 🎯 Zakresy prawidłowe według płci

- **Mężczyźni**: BMI 20.0 - 25.0
- **Kobiety**: BMI 19.0 - 24.0
- **Inne/Ogólne**: BMI 18.5 - 24.99

## 💻 Użycie

### Podstawowe uruchomienie

```bash
python BMI.py
```

### Interaktywny flow

1. **Podaj imię** (opcjonalne)
2. **Wybierz płeć** (1-Mężczyzna, 2-Kobieta, 3-Inna)
3. **Waga** w kilogramach
4. **Wzrost** w centymetrach
5. **Eksport** wyników (opcjonalnie)
6. **Oblicz ponownie** lub zakończ

### Przykład sesji

```
📊 KALKULATOR BMI - ADVANCED

👤 Jak masz na imię? Jan

🤝 Miło mi Cię poznać, Jan!

👤 Płeć (wpływa na zakres prawidłowy):
   1. Mężczyzna
   2. Kobieta
   3. Inna / Wolę nie podawać
   Wybór [3]: 1

⚖️  Podaj swoją wagę (kg): 75
📏 Podaj swój wzrost (cm): 175

==================================================
✅  Twoje BMI: 24.49
   Kategoria: waga prawidłowa
   Zakres prawidłowy: 20 - 25
==================================================

🎉 Gratulacje, Jan! Twoja waga jest prawidłowa!
   Jesteś w zdrowym zakresie 20 - 25.
   Utrzymuj zdrowy styl życia! 💪

💾 Zapisać wynik do pliku? (tak/nie) [nie]: tak
💾 Wynik zapisany do pliku: bmi_wynik_20251212_143022.txt

🔄 Obliczyć ponownie? (tak/nie) [nie]: nie

👋 Dziękuję za skorzystanie z kalkulatora BMI!
   Dbaj o zdrowie! 💚
```

## 📁 Generowane pliki

### Log file: `bmi_calculator.log`
```
2025-12-12 14:30:15 - INFO - Uruchomiono kalkulator BMI
2025-12-12 14:30:22 - INFO - Obliczono BMI: 24.49 dla Jan (płeć: mężczyzna)
2025-12-12 14:30:25 - INFO - Wynik wyeksportowany do bmi_wynik_20251212_143022.txt
2025-12-12 14:30:30 - INFO - Zakończono działanie kalkulatora
```

### Export file: `bmi_wynik_YYYYMMDD_HHMMSS.txt`
```
==================================================
📊 WYNIK KALKULACJI BMI
==================================================

Data: 2025-12-12 14:30:22
Imię: Jan
Płeć: mężczyzna
Waga: 75.0 kg
Wzrost: 175.0 cm

BMI: 24.49
Kategoria: waga prawidłowa

REKOMENDACJE:
Gratulacje, Jan! Twoja waga jest prawidłowa!
Jesteś w zdrowym zakresie 20 - 25.
Utrzymuj zdrowy styl życia!

==================================================
ℹ️  Pamiętaj: BMI to tylko orientacyjny wskaźnik.
   Skonsultuj się z lekarzem w sprawach zdrowia!
==================================================
```

## 🔬 Obliczenia

### Wzór BMI
```
BMI = waga(kg) / (wzrost(m))²
```

### Docelowa waga
```
Docelowa waga = BMI_cel × (wzrost(m))²
```

### Przykład
- Wzrost: 175 cm (1.75 m)
- Waga: 85 kg
- BMI = 85 / (1.75)² = 27.76 → **Nadwaga**

Dla osiągnięcia BMI 25 (górna granica prawidłowa dla mężczyzn):
- Docelowa waga = 25 × (1.75)² = 76.56 kg
- Należy zrzucić: 85 - 76.56 = **8.44 kg**

## 🆚 Porównanie wersji

| Feature | Stara wersja | Nowa wersja |
|---------|--------------|-------------|
| Shebang & encoding | ❌ | ✅ |
| Type hints | ⚠️ Częściowe | ✅ Pełne |
| Uwzględnienie płci | ❌ | ✅ |
| Wielokrotne obliczenia | ❌ | ✅ |
| Dokładne obliczenia wagi | ❌ | ✅ |
| Eksport do pliku | ❌ | ✅ |
| Logging | ❌ | ✅ |
| Error handling | ⚠️ Podstawowy | ✅ Kompletny |
| Stałe vs magic numbers | ❌ | ✅ |
| Kategorie jako dict | ❌ | ✅ |

## ⚠️ Ważne informacje

### Ograniczenia BMI

BMI jest **orientacyjnym wskaźnikiem** i nie uwzględnia:
- Masy mięśniowej (sportowcy mogą mieć "nadwagę")
- Rozkładu tkanki tłuszczowej
- Wieku (inne normy dla dzieci i osób starszych)
- Budowy kości
- Stanu zdrowia

### Kiedy skonsultować się z lekarzem?

- BMI < 18.5 lub > 30
- Nagła zmiana wagi
- Problemy zdrowotne
- Planowanie diety/treningu
- Ciąża

## 🔧 Wymagania

```bash
# Python 3.10+
# Tylko standardowa biblioteka - bez zewnętrznych zależności
```

## 📖 Źródła

- [WHO BMI Classification](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight)
- [CDC BMI Information](https://www.cdc.gov/healthyweight/assessing/bmi/index.html)
- [NIH BMI Calculator](https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmicalc.htm)

## 📝 Changelog

### Version 2.0 (2025-12-12)
- ✨ Dodano uwzględnienie płci
- ✨ Wielokrotne obliczenia w jednej sesji
- ✨ Eksport wyników do pliku
- ✨ Logging do pliku
- ✨ Dokładne obliczenia docelowej wagi
- 🔧 Poprawiono type hints
- 🔧 Refaktoryzacja na stałe i Enum
- 🔧 Pełna obsługa błędów
- 📚 Rozszerzona dokumentacja

### Version 1.0
- Podstawowy kalkulator BMI
- Kategorie WHO
- Proste rekomendacje

## 📄 Licencja

Free to use and modify.

---

**⚕️ Disclaimer**: Ten kalkulator jest narzędziem edukacyjnym. Zawsze konsultuj się z lekarzem lub dietetykiem w sprawach zdrowia i diety.
