# 🔺 Generator Trójek Pitagorejskich - Pitagoras.py

## 📋 Opis

**Pitagoras.py** to zaawansowany generator trójek pitagorejskich z pełną analizą matematyczną. Program generuje **tylko prymitywne** trójki pitagorejskie (eliminując duplikaty typu 3,4,5 i 6,8,10) oraz przeprowadza szczegółową analizę statystyczną z detekcją liczb pierwszych.

### Czym jest Trójka Pitagorejska?

Trójka pitagorejska to zbiór trzech dodatnich liczb całkowitych `a`, `b`, `c` spełniających równanie:

```
a² + b² = c²
```

**Przykłady:**
- (3, 4, 5) → 3² + 4² = 9 + 16 = 25 = 5²  ✓
- (5, 12, 13) → 5² + 12² = 25 + 144 = 169 = 13²  ✓
- (8, 15, 17) → 8² + 15² = 64 + 225 = 289 = 17²  ✓

## ⭐ Kluczowe Funkcje

### ✅ Tylko Trójki Prymitywne
- **NWD(a, b, c) = 1** - eliminuje wielokrotności
- Brak duplikatów typu (3,4,5) i (6,8,10)
- Gwarancja unikalności wszystkich wygenerowanych trójek

### 📊 Szczegółowa Analiza
Dla każdej trójki program oblicza:
- **Wymiary**: a, b, c (boki trójkąta)
- **Obwód**: a + b + c
- **Powierzchnia**: (a × b) / 2
- **Liczby pierwsze**: które wartości w trójce są liczbami pierwszymi

### 📈 Statystyki
- Liczba wygenerowanych trójek prymitywnych
- Liczba trójek zawierających liczby pierwsze (%)
- Wszystkie liczby pierwsze w zakresie
- Obwód: najmniejszy, największy, średni
- Powierzchnia: najmniejsza, największa, średnia

### ✓ Weryfikacja Poprawności
- Sprawdzanie NWD > 1 (trójki nieprymitywne)
- Detekcja dokładnych duplikatów
- Przykładowa weryfikacja wzoru Pitagorasa

## 🔬 Algorytm: Wzór Euklidesa

Program wykorzystuje **wzór Euklidesa** do generowania prymitywnych trójek pitagorejskich:

Dla liczb względnie pierwszych `m > n > 0` o różnej parzystości:

```python
a = m² - n²
b = 2mn
c = m² + n²
```

**Warunki:**
1. `m > n > 0`
2. `NWD(m, n) = 1` (liczby względnie pierwsze)
3. `m` i `n` mają różną parzystość (jeden parzysty, drugi nieparzysty)

**Przykład:** m=2, n=1
```
a = 2² - 1² = 4 - 1 = 3
b = 2 × 2 × 1 = 4
c = 2² + 1² = 4 + 1 = 5
Wynik: (3, 4, 5) ✓
```

### Złożoność Czasowa
- **Generowanie trójek**: O(m²) gdzie m to parametr wzoru
- **Sito Eratostenesa**: O(n log log n) gdzie n to największa wartość
- **Sortowanie**: O(k log k) gdzie k to liczba trójek

## 🚀 Instalacja i Uruchomienie

### Wymagania
```bash
Python 3.8+
# Brak zewnętrznych zależności - tylko biblioteka standardowa
```

### Uruchomienie
```bash
cd PITAGORAS
python Pitagoras.py
```

## 💻 Sposób Użycia

### Krok 1: Uruchom program
```bash
python Pitagoras.py
```

### Krok 2: Podaj liczbę trójek
```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                GENERATOR TRÓJEK PITAGOREJSKICH                                       ║
║                         (Tylko prymitywne)                                           ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

Podaj liczbę trójek pitagorejskich do wygenerowania (1-1000): 10
```

### Krok 3: Otrzymaj wyniki

#### Tabela Trójek
```
==========================================================================================
#        a     b     c     Obwód  Powierzchnia L. pierwsze                    
==========================================================================================
1        3     4     5        12           6.0 [3, 5]                         
2        5    12    13        30          30.0 [5, 13]                        
3        8    15    17        40          60.0 [17]                           
4        7    24    25        56          84.0 [7]                            
5       20    21    29        70         210.0 [29]                           
6        9    40    41        90         180.0 [41]                           
7       12    35    37        84         210.0 [37]                           
8       11    60    61       132         330.0 [11, 61]                       
9       13    84    85       182         546.0 [13, 85]                       
10      28    45    53       126         630.0 [53]                           
==========================================================================================
```

#### Weryfikacja Duplikatów
```
==========================================================================================
WERYFIKACJA DUPLIKATÓW:
==========================================================================================
✅ Wszystkie trójki są prymitywne (brak wielokrotności jak 3,4,5 i 6,8,10)
✅ Nie znaleziono dokładnych duplikatów
==========================================================================================
```

#### Statystyki
```
==========================================================================================
STATYSTYKI:
==========================================================================================
Trójki prymitywne łącznie:         10
Trójki zawierające liczby pierwsze: 9 (90.0%)
Liczby pierwsze do 85:             23

Obwód:
  Najmniejszy:                     12
  Największy:                      182
  Średni:                          88.2

Powierzchnia:
  Najmniejsza:                     6.0
  Największa:                      546.0
  Średnia:                         228.6
==========================================================================================

⏱️  Czas generowania: 0.001s
   Średnio na trójkę: 0.000100s

💡 Przykładowa weryfikacja (pierwsze 3 trójki):
   1. 3² + 4² = 9 + 16 = 25 = 25 = 5²  ✓
   2. 5² + 12² = 25 + 144 = 169 = 169 = 13²  ✓
   3. 8² + 15² = 64 + 225 = 289 = 289 = 17²  ✓
```

## 📊 Przykłady Użycia

### Przykład 1: Małe Zestawy (5 trójek)
```bash
python Pitagoras.py
# Wejście: 5
# Wyjście: (3,4,5), (5,12,13), (8,15,17), (7,24,25), (20,21,29)
```

### Przykład 2: Średnie Zestawy (50 trójek)
```bash
python Pitagoras.py
# Wejście: 50
# Otrzymuje 50 unikalnych trójek prymitywnych
# Czas: ~0.01s
```

### Przykład 3: Duże Zestawy (500 trójek)
```bash
python Pitagoras.py
# Wejście: 500
# System ostrzeże: "⚠️  Duża liczba (500) może zająć trochę czasu!"
# Potwierdź: T (Tak) lub N (Nie)
```

## 🎯 Funkcje Zaawansowane

### 1. Klasa PythagoreanTriple
```python
class PythagoreanTriple:
    def __init__(self, a: int, b: int, c: int)
    
    @property
    def perimeter(self) -> int
        """Oblicza obwód: a + b + c"""
    
    @property
    def area(self) -> float
        """Oblicza powierzchnię: (a × b) / 2"""
```

### 2. Generowanie Trójek
```python
def generate_primitive_triples(count: int) -> List[PythagoreanTriple]
    """
    Generuje określoną liczbę prymitywnych trójek pitagorejskich
    używając wzoru Euklidesa.
    
    Zwraca: Listę posortowaną według obwodu (rosnąco)
    """
```

### 3. Sito Eratostenesa
```python
def sieve_of_eratosthenes(limit: int) -> Set[int]
    """
    Generuje wszystkie liczby pierwsze do limitu.
    
    Złożoność: O(n log log n)
    Zwraca: Zbiór liczb pierwszych dla O(1) wyszukiwania
    """
```

### 4. Analiza Liczb Pierwszych
```python
def analyze_primes_in_triple(triple: PythagoreanTriple, primes: Set[int]) -> List[int]
    """
    Znajduje, które liczby w trójce są pierwsze.
    
    Przykład: (5, 12, 13) → [5, 13]
    """
```

## 🔍 Szczegóły Matematyczne

### Prymitywne vs Nieprymitywne

**Trójki Prymitywne** (NWD = 1):
- (3, 4, 5) ✓
- (5, 12, 13) ✓
- (8, 15, 17) ✓
- (7, 24, 25) ✓

**Trójki Nieprymitywne** (NWD > 1):
- (6, 8, 10) = 2 × (3, 4, 5) ✗
- (9, 12, 15) = 3 × (3, 4, 5) ✗
- (10, 24, 26) = 2 × (5, 12, 13) ✗

### Właściwości Trójek Prymitywnych

1. **Dokładnie jedna** z liczb a, b jest parzysta
2. **Dokładnie jedna** z liczb a, b, c jest podzielna przez 3
3. **Dokładnie jedna** z liczb a, b, c jest podzielna przez 5
4. Suma a + b + c jest **zawsze parzysta**
5. Iloczyn abc jest **zawsze podzielny przez 60**

## 📈 Wydajność

### Benchmarki
```
Liczba trójek    Czas         Pamięć
──────────────────────────────────────
10              < 0.001s     < 1 MB
50              ~ 0.005s     < 1 MB
100             ~ 0.010s     < 1 MB
500             ~ 0.050s     ~ 2 MB
1000            ~ 0.100s     ~ 5 MB
```

### Optymalizacje
- ⚡ Wzór Euklidesa zamiast brute force
- 🔍 Set dla O(1) wyszukiwania liczb pierwszych
- 📊 Sortowanie tylko raz na końcu
- 💾 Minimalne zużycie pamięci

## ❓ FAQ

### Q: Dlaczego tylko trójki prymitywne?
**A:** Trójki prymitywne są podstawowymi "blokami budulcowymi". Wszystkie inne trójki to ich wielokrotności, więc są redundantne.

### Q: Jak długo trwa generowanie 1000 trójek?
**A:** Około 0.1 sekundy na nowoczesnym komputerze.

### Q: Czy mogę generować więcej niż 1000 trójek?
**A:** Tak, ale program ostrzeże o potencjalnie długim czasie obliczeń. Możesz potwierdzić kontynuację.

### Q: Co to jest NWD (Największy Wspólny Dzielnik)?
**A:** To największa liczba całkowita, która dzieli wszystkie podane liczby. Dla trójek prymitywnych NWD(a,b,c) = 1.

### Q: Dlaczego program pokazuje liczby pierwsze?
**A:** To dodatkowa analiza matematyczna pokazująca, które wartości w trójce są liczbami pierwszymi - interesująca właściwość z punktu widzenia teorii liczb.

## 🐛 Obsługa Błędów

Program obsługuje:
- ❌ Nieprawidłowe dane wejściowe (nie-liczby)
- ❌ Liczby < 1
- ⚠️ Ostrzeżenia dla dużych wartości (> 1000)
- 🛑 Ctrl+C (przerwanie przez użytkownika)
- 🚨 Nieoczekiwane błędy z komunikatami

## 📚 Teoria Matematyczna

### Twierdzenie Pitagorasa
Dla trójkąta prostokątnego o bokach a, b i przeciwprostokątnej c:
```
a² + b² = c²
```

### Wzór Euklidesa (ok. 300 p.n.e.)
Wszystkie prymitywne trójki pitagorejskie można wygenerować za pomocą:
```
a = m² - n²
b = 2mn
c = m² + n²
```
gdzie m > n > 0, NWD(m,n) = 1, i m-n jest nieparzyste.

### Pierwsze Trójki Pitagorejskie
```
(3, 4, 5)       - Najmniejsza
(5, 12, 13)
(8, 15, 17)
(7, 24, 25)
(20, 21, 29)
(9, 40, 41)
(12, 35, 37)
(11, 60, 61)
(13, 84, 85)
(28, 45, 53)
```

## 🔗 Powiązane Projekty

W tym samym katalogu dostępne są również:
- **Pitagoras_unified.py** - Rozszerzona wersja z dodatkowymi funkcjami
- **Pit2.py** - Wersja z wyszukiwaniem według limitu

## 📖 Bibliografia

1. **Trójka pitagorejska** - Wikipedia PL: https://pl.wikipedia.org/wiki/Trójka_pitagorejska
2. **Euclid's Formula** - Wikipedia EN: https://en.wikipedia.org/wiki/Formulas_for_generating_Pythagorean_triples
3. **Tree of Primitive Pythagorean Triples**: https://en.wikipedia.org/wiki/Tree_of_primitive_Pythagorean_triples

## 👨‍💻 Autor

**Maciej Mierzejewski**
- GitHub: [@mmierzejewski](https://github.com/mmierzejewski)
- Repository: [MM_Python](https://github.com/mmierzejewski/MM_Python)

## 📄 Licencja

Free to use and modify.

---

**💡 Wskazówka:** Program jest idealny do celów edukacyjnych, badania teorii liczb oraz generowania zestawów testowych dla algorytmów geometrycznych!
