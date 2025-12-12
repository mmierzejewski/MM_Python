# 🔢 Generator Liczb Pierwszych - PNA.py

## 📋 Opis

**PNA.py** (Prime Numbers Analyzer) to wydajny generator liczb pierwszych wykorzystujący **Sito Eratostenesa**. Program znajduje wszystkie liczby pierwsze w zadanym zakresie z pomiarem wydajności i szczegółowymi statystykami. Zawiera optymalizację dla bardzo dużych zakresów w postaci **sita segmentowanego**.

### Czym jest Liczba Pierwsza?

**Liczba pierwsza** to liczba naturalna większa od 1, która ma dokładnie dwa dzielniki: 1 i samą siebie.

**Przykłady:**
- ✅ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...
- ❌ 1 (ma tylko jeden dzielnik)
- ❌ 4 = 2 × 2 (ma więcej niż dwa dzielniki)
- ❌ 6 = 2 × 3 (ma więcej niż dwa dzielniki)

## ⭐ Kluczowe Funkcje

### 🚀 Dwie Metody Generowania

#### 1. Standardowe Sito Eratostenesa
- **Zakres**: Do ~100 milionów
- **Pamięć**: O(n) - ~100 MB na 100 milionów
- **Szybkość**: Bardzo szybkie dla małych i średnich zakresów
- **Użycie**: Automatyczne dla zakresów < 10 milionów

#### 2. Sito Segmentowane (Zaawansowane)
- **Zakres**: Powyżej 1 miliarda
- **Pamięć**: O(√n) - oszczędność pamięci!
- **Szybkość**: Optymalne dla bardzo dużych zakresów
- **Użycie**: Zalecane/automatyczne dla zakresów > 1 miliarda

### 📊 Szczegółowe Statystyki
- **Zakres**: Od-do
- **Liczba znalezionych**: Ile liczb pierwszych
- **Gęstość**: Procent liczb pierwszych w zakresie
- **Najmniejsza/Największa**: Ekstremalne wartości
- **Czas generowania**: Pomiar wydajności

### 💾 Eksport do Pliku
- Automatyczne zapisywanie do katalogu PNA/
- Format: `primes_up_to_{limit}_{timestamp}.txt`
- Zawartość: Header + liczby pierwsze (10 na linię)
- Oferowane dla zestawów > 100 liczb

### ⚡ Optymalizacje Wydajności
- Progress bar dla dużych zakresów (> 1M)
- Ostrzeżenia o czasie/pamięci dla dużych limitów
- Automatyczna sugestia sita segmentowanego
- Formatowanie czasu (μs, ms, s, m)

## 🔬 Algorytm: Sito Eratostenesa

### Zasada Działania

**Sito Eratostenesa** (III wiek p.n.e.) to jeden z najstarszych i najwydajniejszych algorytmów znajdowania liczb pierwszych.

#### Kroki Algorytmu:
1. Utwórz listę liczb od 2 do n
2. Zacznij od pierwszej liczby (2)
3. Oznacz wszystkie wielokrotności tej liczby jako złożone
4. Przejdź do kolejnej nieoznaczonej liczby
5. Powtarzaj kroki 3-4 aż do √n

#### Wizualizacja (dla n=30):
```
Start: 2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30

Krok 1 (2): 2  3  ✗  5  ✗  7  ✗  9  ✗  11 ✗  13 ✗  15 ✗  17 ✗  19 ✗  21 ✗  23 ✗  25 ✗  27 ✗  29 ✗

Krok 2 (3): 2  3  ✗  5  ✗  7  ✗  ✗  ✗  11 ✗  13 ✗  ✗  ✗  17 ✗  19 ✗  ✗  ✗  23 ✗  ✗  ✗  ✗  ✗  29 ✗

Krok 3 (5): 2  3  ✗  5  ✗  7  ✗  ✗  ✗  11 ✗  13 ✗  ✗  ✗  17 ✗  19 ✗  ✗  ✗  23 ✗  ✗  ✗  ✗  ✗  29 ✗

Wynik: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
```

### Złożoność Czasowa
- **Standardowe sito**: O(n log log n)
- **Sito segmentowane**: O(n log log n) z O(√n) pamięci

## 🚀 Instalacja i Uruchomienie

### Wymagania
```bash
Python 3.10+
# Brak zewnętrznych zależności - tylko biblioteka standardowa
```

### Uruchomienie
```bash
cd PNA
python PNA.py
```

## 💻 Sposób Użycia

### Krok 1: Uruchom program
```bash
python PNA.py
```

### Krok 2: Wprowadź zakres
```
╔══════════════════════════════════════════════════════╗
║        GENERATOR LICZB PIERWSZYCH                    ║
║            (Sito Eratostenesa)                       ║
╚══════════════════════════════════════════════════════╝

Podaj zakres (liczba całkowita >= 2): 100
```

### Krok 3: Otrzymaj wyniki

#### Małe Zakresy (< 10M)
```
🔍 Wyszukiwanie liczb pierwszych do 100...

⏱️  Czas generowania: 0.145 ms

============================================================
📊 STATYSTYKI LICZB PIERWSZYCH
============================================================
Zakres:              2 do 100
Liczby pierwsze:     25
Gęstość:             25.0000%
Najmniejsza:         2
Największa:          97
Wszystkie liczby:    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
============================================================
```

#### Średnie Zakresy (10M - 1B)
```
⚠️  Duży zakres (50,000,000) może wymagać znacznego czasu i pamięci!
   Szacowana pamięć: ~48 MB
   Kontynuować? (T/N) [N]: T

🔍 Wyszukiwanie liczb pierwszych do 50,000,000...
Postęp: 100.0% (sprawdzanie 7,071)

⏱️  Czas generowania: 2.847 s

============================================================
📊 STATYSTYKI LICZB PIERWSZYCH
============================================================
Zakres:              2 do 50,000,000
Liczby pierwsze:     3,001,134
Gęstość:             6.0023%
Najmniejsza:         2
Największa:          49,999,991
============================================================

💾 Zapisać liczby pierwsze do pliku? (T/N) [T]: T
✅ Liczby pierwsze zapisano do: /Users/.../PNA/primes_up_to_50000000_20251212_143052.txt
```

#### Bardzo Duże Zakresy (> 1B) - Sito Segmentowane
```
⚠️  BARDZO DUŻY zakres (2,000,000,000)!
   Standardowe sito: ~1907 MB (~1.9 GB)
   Sito segmentowane: ~43 MB (zalecane!)

   💡 Sito segmentowane używa znacznie mniej pamięci dla dużych zakresów
   Użyć sita segmentowanego? (T/N) [T]: T

🔍 Wyszukiwanie liczb pierwszych do 2,000,000,000...
   Używanie sita segmentowanego (optymalizacja pamięci)
Faza 1/2: Wyszukiwanie podstawowych liczb pierwszych do 44,721...
Faza 2/2: Przetwarzanie 1,955 segmentów o rozmiarze 1,000,000...
Postęp: 100.0% (przetworzono do 2,000,000,000)

⏱️  Czas generowania: 2m 15.34s

============================================================
📊 STATYSTYKI LICZB PIERWSZYCH
============================================================
Zakres:              2 do 2,000,000,000
Liczby pierwsze:     98,222,287
Gęstość:             4.9111%
Najmniejsza:         2
Największa:          1,999,999,973
============================================================

💾 Zapisać liczby pierwsze do pliku? (T/N) [T]: T
✅ Liczby pierwsze zapisano do: /Users/.../PNA/primes_up_to_2000000000_20251212_144523.txt
```

## 📊 Przykłady Użycia

### Przykład 1: Małe Zakresy
```bash
python PNA.py
# Wejście: 1000
# Wyjście: 168 liczb pierwszych (16.8%)
# Czas: < 1 ms
```

### Przykład 2: Średnie Zakresy
```bash
python PNA.py
# Wejście: 10000000 (10 milionów)
# Wyjście: 664,579 liczb pierwszych (6.6%)
# Czas: ~0.5s
# Pamięć: ~10 MB
```

### Przykład 3: Duże Zakresy
```bash
python PNA.py
# Wejście: 100000000 (100 milionów)
# Wyjście: 5,761,455 liczb pierwszych (5.76%)
# Czas: ~5s
# Pamięć: ~100 MB
```

### Przykład 4: Bardzo Duże Zakresy (Sito Segmentowane)
```bash
python PNA.py
# Wejście: 1000000000 (1 miliard)
# Metoda: Sito segmentowane (automatycznie)
# Wyjście: 50,847,534 liczb pierwszych (5.08%)
# Czas: ~1 minuta
# Pamięć: ~32 MB (zamiast ~950 MB!)
```

## 🎯 Funkcje Zaawansowane

### 1. Sito Segmentowane
```python
def generate_primes_segmented(limit: int, verbose: bool = False) -> list[int]
    """
    Generuje liczby pierwsze dla bardzo dużych zakresów.
    
    Zalety:
    - Pamięć: O(√n) zamiast O(n)
    - Dla 1 miliarda: ~32 MB zamiast ~950 MB
    - Progress bar dla monitorowania postępu
    
    Algorytm:
    1. Znajdź bazowe liczby pierwsze do √n
    2. Przetwarzaj zakres w segmentach (domyślnie 1M)
    3. W każdym segmencie oznacz wielokrotności
    """
```

### 2. Standardowe Sito
```python
def generate_primes(limit: int, verbose: bool = False) -> list[int]
    """
    Klasyczne Sito Eratostenesa.
    
    Zalety:
    - Bardzo szybkie dla zakresów < 100M
    - Proste i sprawdzone
    - Progress bar dla zakresów > 1M
    
    Złożoność: O(n log log n)
    """
```

### 3. Formatowanie Czasu
```python
def format_duration(duration) -> str
    """
    Automatyczne formatowanie czasu:
    - μs (mikrosekundy): < 1ms
    - ms (milisekundy): < 1s
    - s (sekundy): < 60s
    - m (minuty) + s: ≥ 60s
    """
```

### 4. Zapis do Pliku
```python
def save_primes_to_file(primes: list[int], limit: int, filename: Optional[str] = None)
    """
    Zapisuje liczby pierwsze do pliku tekstowego.
    
    Format pliku:
    - Header z metadanymi (zakres, liczba, data)
    - Liczby pierwsze: 10 na linię, oddzielone przecinkami
    - Kodowanie UTF-8
    """
```

## 📈 Wydajność

### Benchmarki (Apple M1/Intel i5)

| Zakres | Liczby pierwsze | Czas | Pamięć | Metoda |
|--------|----------------|------|--------|--------|
| 1,000 | 168 | < 1 ms | < 1 MB | Standardowe |
| 10,000 | 1,229 | < 5 ms | < 1 MB | Standardowe |
| 100,000 | 9,592 | ~20 ms | ~1 MB | Standardowe |
| 1,000,000 | 78,498 | ~50 ms | ~5 MB | Standardowe |
| 10,000,000 | 664,579 | ~500 ms | ~10 MB | Standardowe |
| 100,000,000 | 5,761,455 | ~5s | ~100 MB | Standardowe |
| 1,000,000,000 | 50,847,534 | ~60s | ~32 MB | **Segmentowane** |
| 2,000,000,000 | 98,222,287 | ~135s | ~44 MB | **Segmentowane** |

### Gęstość Liczb Pierwszych

Zgodnie z **Twierdzeniem o liczbach pierwszych**:
```
π(n) ≈ n / ln(n)
```

Gęstość maleje wraz ze wzrostem n:
- **n = 100**: 25% liczb pierwszych
- **n = 1,000**: 16.8%
- **n = 10,000**: 12.3%
- **n = 100,000**: 9.6%
- **n = 1,000,000**: 7.8%
- **n = 10,000,000**: 6.6%
- **n = 100,000,000**: 5.8%
- **n = 1,000,000,000**: 5.1%

## 🔍 Szczegóły Techniczne

### Optymalizacje Pamięci

#### Standardowe Sito
```python
is_prime = [True] * (limit + 1)  # O(n) pamięci
# Dla 1 miliarda: ~950 MB
```

#### Sito Segmentowane
```python
result = generate_primes(sqrt_limit)  # O(√n) pamięci dla bazy
segment = [True] * segment_size        # Tylko 1M elementów na raz
# Dla 1 miliarda: ~32 MB (30x oszczędność!)
```

### Progress Bar

Dla zakresów > 1,000,000:
```
Postęp: 45.3% (sprawdzanie 3,207)
```

Dla sita segmentowanego:
```
Faza 1/2: Wyszukiwanie podstawowych liczb pierwszych do 44,721...
Faza 2/2: Przetwarzanie 1,955 segmentów o rozmiarze 1,000,000...
Postęp: 67.8% (przetworzono do 678,000,000)
```

## 🐛 Obsługa Błędów

Program obsługuje:
- ❌ **Nieprawidłowe dane**: Nie-liczby, liczby < 2
- ⚠️ **Ostrzeżenia**: Duże zakresy (> 10M) z szacowaniem pamięci
- 💡 **Sugestie**: Automatyczna rekomendacja sita segmentowanego
- 🚨 **MemoryError**: Łapanie błędów pamięci z sugestiami
- 🛑 **Ctrl+C**: Bezpieczne przerwanie
- 📝 **IOError**: Obsługa błędów zapisu pliku

### Przykłady Obsługi Błędów

#### Zbyt duży zakres (standardowe sito)
```
❌ Błąd pamięci: Not enough memory to create sieve for 5,000,000,000

💡 Sugestie:
   • Spróbuj mniejszego zakresu
   • Użyj opcji sita segmentowanego dla dużych zakresów
   • Zamknij inne aplikacje, aby zwolnić pamięć
```

#### Nieprawidłowe dane
```
Podaj zakres (liczba całkowita >= 2): abc
❌ Nieprawidłowe dane! Proszę podać poprawną liczbę całkowitą dodatnią.
```

## ❓ FAQ

### Q: Jaka jest maksymalna wartość zakresu?
**A:** Teoretycznie nie ma limitu dzięki situ segmentowanemu. Praktycznie ogranicza czas obliczeń (np. 10 miliardów zajmie ~20 minut).

### Q: Czy 1 jest liczbą pierwszą?
**A:** Nie! Liczba pierwsza musi mieć dokładnie dwa dzielniki. 1 ma tylko jeden dzielnik (siebie).

### Q: Dlaczego gęstość liczb pierwszych maleje?
**A:** Zgodnie z Twierdzeniem o liczbach pierwszych, liczby pierwsze stają się rzadsze w miarę wzrostu n, z gęstością ~1/ln(n).

### Q: Co to jest sito segmentowane?
**A:** To optymalizacja Sita Eratostenesa, która przetwarza zakres w małych segmentach zamiast całości naraz, oszczędzając pamięć.

### Q: Czy mogę zapisać wyniki dla małych zakresów?
**A:** Opcja zapisu pojawia się automatycznie dla zakresów > 100 liczb pierwszych.

### Q: Jak działa progress bar?
**A:** Wyświetla się automatycznie dla zakresów > 1,000,000, pokazując procent ukończenia i aktualnie sprawdzaną liczbę.

## 📚 Teoria Matematyczna

### Twierdzenie o Liczbach Pierwszych (Prime Number Theorem)

Dla dużych n, liczba liczb pierwszych ≤ n jest w przybliżeniu:
```
π(n) ≈ n / ln(n)
```

gdzie π(n) to funkcja zliczająca liczby pierwsze.

### Pierwsze Liczby Pierwsze
```
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97...
```

### Ciekawostki
- **2** jest jedyną parzystą liczbą pierwszą
- Każda liczba naturalna > 1 ma unikalny rozkład na czynniki pierwsze
- Między n a 2n zawsze istnieje co najmniej jedna liczba pierwsza (Postulat Bertranda)
- Największa znana liczba pierwsza (2024): 2^82,589,933 - 1 (ponad 24 miliony cyfr!)

### Hipoteza Riemanna
Związana z rozkładem liczb pierwszych, jeden z **Problemów Milenijnych** z nagrodą $1,000,000!

## 🔗 Powiązane Projekty

W tym samym katalogu dostępny jest również:
- **PNA2a.py** - Ulepszona wersja z dodatkowymi funkcjami

## 📖 Bibliografia

1. **Sito Eratostenesa** - Wikipedia PL: https://pl.wikipedia.org/wiki/Sito_Eratostenesa
2. **Liczby pierwsze** - Wikipedia PL: https://pl.wikipedia.org/wiki/Liczba_pierwsza
3. **Prime Number Theorem**: https://en.wikipedia.org/wiki/Prime_number_theorem
4. **Segmented Sieve**: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Segmented_sieve

## 👨‍💻 Autor

**Maciej Mierzejewski**
- GitHub: [@mmierzejewski](https://github.com/mmierzejewski)
- Repository: [MM_Python](https://github.com/mmierzejewski/MM_Python)

## 📄 Licencja

Free to use and modify.

---

**💡 Wskazówka:** Program jest idealny do celów edukacyjnych, eksperymentów z teorią liczb oraz generowania dużych zestawów liczb pierwszych do testów kryptograficznych!
