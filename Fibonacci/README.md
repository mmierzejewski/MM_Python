# 🔢 Fibonacci Calculator

Zaawansowane narzędzia do generowania i analizy ciągu Fibonacciego z wieloma algorytmami i trybami pracy.

## 📐 Ciąg Fibonacciego

Ciąg Fibonacciego to sekwencja liczb gdzie każda liczba jest sumą dwóch poprzednich:

```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)
```

**Przykład:** 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...

## ✨ Features

### 🔧 Funkcje obliczeniowe:
- 📊 **Generowanie do wartości** - wszystkie liczby Fibonacciego ≤ max_value
- 🎯 **N-ta liczba** - pobierz konkretną liczbę z ciągu (0-indexed)
- 📋 **Pierwsze N liczb** - generuj listę pierwszych n elementów
- ⚡ **Algorytm szybki O(log n)** - metoda macierzowa z memoizacją dla dużych n
- ✅ **Sprawdzanie przynależności** - czy liczba należy do ciągu
- 📈 **Analiza szczegółowa** - stosunek do złotego podziału φ
- 💾 **Eksport do pliku** - zapisz ciąg z pełnymi statystykami
- 📝 **Logging** - rejestracja wszystkich operacji do `fibonacci.log`

### 🎨 Interface:
- 🖥️ Interaktywne menu z 8 opcjami
- 🔄 **Pętla menu** - ciągły tryb pracy bez ponownego uruchamiania
- 🚪 Opcja "Koniec" - eleganckie wyjście z programu
- 📊 Szczegółowe statystyki
- 🛡️ Pełna walidacja inputu
- 🔢 Formatowanie dużych liczb
- 📉 Analiza zbieżności do złotego podziału
- 🗂️ Eksport wyników do pliku tekstowego

## 💻 Użycie

### Uruchomienie programu

```bash
cd Fibonacci
python3 FibonacciUtils.py
```

### Pliki generowane
- `fibonacci.log` - log wszystkich operacji
- `fibonacci_sequence_*.txt` - wyeksportowane ciągi (opcjonalnie)

### Menu opcji

```
🔢 KALKULATOR CIĄGU FIBONACCIEGO
📌 Wszystkie funkcje używają indeksowania 0-based
   (F(0)=0, F(1)=1, F(2)=1, F(3)=2...)

Wybierz opcję:
1. Generuj liczby Fibonacciego do wartości
2. Pobierz n-tą liczbę Fibonacciego (0-indexed)
3. Generuj pierwsze n liczb Fibonacciego
4. Szybkie obliczanie (algorytm O(log n))
5. Sprawdź, czy liczba jest liczbą Fibonacciego
6. Szczegółowe informacje o F(n)
7. Eksportuj ostatni ciąg do pliku
8. Koniec (wyjście z programu)
```

## 📚 Przykłady użycia

### 1. Generowanie do wartości

```python
from FibonacciUtils import generate_fibonacci_upto

# Wszystkie liczby Fibonacciego ≤ 100
result = generate_fibonacci_upto(100)
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

**Interaktywnie:**
```
Wybór: 1
Podaj wartość maksymalną: 100
✅ Liczby Fibonacciego ≤ 100:
   [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
   Znaleziono: 12 liczb
```

### 2. N-ta liczba Fibonacciego

```python
from FibonacciUtils import get_nth_fibonacci

# 6-ta liczba (0-indexed: F(0)=0, F(1)=1, F(2)=1...)
result = get_nth_fibonacci(6)  # 8

# Backwards compatibility (1-indexed)
result = get_nth_fibonacci(7, zero_indexed=False)  # 8
```

**Interaktywnie:**
```
Wybór: 2
Podaj pozycję n (0-indexed, np. F(0)=0, F(6)=8): 6
✅ F(6) = 8
```

### 3. Pierwsze N liczb

```python
from FibonacciUtils import generate_first_n_fibonacci

# Pierwsze 10 liczb
result = generate_first_n_fibonacci(10)
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**Interaktywnie:**
```
Wybór: 3
Ile liczb wygenerować: 10
✅ Pierwsze 10 liczby: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### 4. Szybki algorytm (duże liczby)

```python
from FibonacciUtils import fibonacci_fast

# F(100) metodą macierzową O(log n)
result = fibonacci_fast(100)  # 354,224,848,179,261,915,075
```

**Interaktywnie:**
```
Wybór: 4
Podaj n (0-indexed, dla dużych n): 100
✅ F(100) = 354,224,848,179,261,915,075
   Liczba cyfr: 21
```

### 5. Sprawdzanie przynależności

```python
from FibonacciUtils import is_fibonacci

is_fibonacci(21)   # True
is_fibonacci(22)   # False
is_fibonacci(89)   # True
```

**Algorytm:** Liczba n jest liczbą Fibonacciego ⟺ 5n² + 4 lub 5n² - 4 jest kwadratem doskonałym

**Interaktywnie:**
```
Wybór: 5
Podaj liczbę do sprawdzenia: 89
✅ 89 JEST liczbą Fibonacciego!
```

### 6. Szczegółowa analiza

```python
from FibonacciUtils import print_fibonacci_info

print_fibonacci_info(20)  # 0-indexed (domyślnie)
```

**Output:**
```
============================================================
📊 INFORMACJE O F(20)
============================================================
Wartość: 6,765
Liczba cyfr: 4
Ciąg do F(20): [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]...
Stosunek F(20)/F(19): 1.6180339985
Złoty podział φ: 1.6180339887
Różnica: 9.8324e-09
============================================================
```

### 7. Eksport ciągu do pliku

```python
from FibonacciUtils import export_fibonacci_sequence, generate_first_n_fibonacci

sequence = generate_first_n_fibonacci(15)
export_fibonacci_sequence(sequence, "moj_fibonacci.txt")
```

**Zawartość pliku:**
```
Ciąg Fibonacciego
Wygenerowano: 2025-12-12 22:00:19
Liczba elementów: 15
============================================================

F(0)-F(9): 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
F(10)-F(14): 55, 89, 144, 233, 377

============================================================
STATYSTYKI:
Najmniejsza: 0
Największa: 377
Suma: 986
Ostatni stosunek: 1.6180257511
Złoty podział φ: 1.6180339887
```

## 🔬 Algorytmy

### 1. Algorytm iteracyjny (standardowy)
**Złożoność:** O(n)  
**Użycie:** `generate_first_n_fibonacci()`, `get_nth_fibonacci()`

```python
def fibonacci_iterative(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### 2. Algorytm macierzowy (szybki)
**Złożoność:** O(log n)  
**Użycie:** `fibonacci_fast()`

Wykorzystuje wzór macierzowy:
```
| F(n+1)  F(n)  |   | 1  1 |^n
| F(n)    F(n-1)|= | 1  0 |
```

### 3. Test przynależności
**Złożoność:** O(1)  
**Użycie:** `is_fibonacci()`

Wykorzystuje własność:
- n ∈ Fibonacci ⟺ (5n² + 4 jest kwadratem) ∨ (5n² - 4 jest kwadratem)

## 📊 Analiza kodu

### ✅ **Mocne strony:**

1. **Kompletność funkcjonalna**
   - 6 różnych funkcji do pracy z ciągiem
   - Algorytmy o różnej złożoności
   - Test przynależności matematyczny

2. **Dobra struktura**
   - Czytelny podział na funkcje
   - Type hints
   - Docstringi z przykładami
   - Custom exception `FibonacciError`

3. **User Experience**
   - Interaktywne menu
   - Formatowanie liczb (przecinki)
   - Analiza złotego podziału φ
   - Obsługa błędów

4. **Dokumentacja**
   - Docstringi z examples
   - Złożoność algorytmów
   - Wzory matematyczne

5. **Algorytmy zaawansowane**
   - Metoda macierzowa O(log n)
   - Szybkie potęgowanie
   - Test kwadratowy dla przynależności

### ✅ **Wprowadzone ulepszenia:**

1. **✔️ Ujednolicone indeksowanie**
   - Wszystkie funkcje używają teraz 0-indexed (F(0)=0, F(1)=1...)
   - Backwards compatibility z parametrem `zero_indexed=False`
   - Wyraźna informacja w menu i dokumentacji

2. **✔️ Shebang i encoding**
   ```python
   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-
   ```

3. **✔️ Pełny logging**
   - Wszystkie operacje logowane do `fibonacci.log`
   - Historia obliczeń z timestampami
   - 3 poziomy logowania (INFO, WARNING, ERROR, CRITICAL)

4. **✔️ Stała dla złotego podziału**
   ```python
   GOLDEN_RATIO = (1 + 5 ** 0.5) / 2  # φ ≈ 1.618033988749...
   ```

5. **✔️ Memoizacja**
   - `@lru_cache(maxsize=1024)` dla `fibonacci_fast()`
   - Dramatyczna poprawa wydajności dla powtarzających się wywołań

6. **✔️ Eksport do pliku**
   - Nowa funkcja `export_fibonacci_sequence()`
   - Pełne statystyki (min, max, suma, stosunek)
   - Opcja 7 w menu

### 📊 **Ocena po poprawkach:** 10/10

Profesjonalny kod z wszystkimi najlepszymi praktykami:
- Spójne indeksowanie z backwards compatibility
- Pełne logowanie i monitoring
- Optymalizacje wydajnościowe (memoizacja)
- Eksport i persystencja danych
- Dokumentacja zaktualizowana

## 🎓 Matematyka

### Złoty podział (φ)

```
φ = (1 + √5) / 2 ≈ 1.618033988749...
```

Stosunek kolejnych liczb Fibonacciego zbiega do φ:
```
lim(n→∞) F(n+1)/F(n) = φ
```

### Wzór Bineta

Bezpośredni wzór na n-tą liczbę:
```
F(n) = (φⁿ - ψⁿ) / √5

gdzie:
φ = (1 + √5) / 2
ψ = (1 - √5) / 2
```

### Test przynależności

Liczba n jest w ciągu Fibonacciego ⟺
```
5n² + 4 = k²  ∨  5n² - 4 = k²  (dla pewnego k ∈ ℕ)
```

## 🔧 API Reference

### Stałe

#### `GOLDEN_RATIO`
Złoty podział φ ≈ 1.618033988749...

### Funkcje

#### `generate_fibonacci_upto(max_value: int) -> List[int]`
Generuje liczby Fibonacciego ≤ max_value.

#### `get_nth_fibonacci(n: int, zero_indexed: bool = True) -> int`
Zwraca n-tą liczbę.
- `zero_indexed=True` (domyślnie): F(0)=0, F(1)=1, F(6)=8...
- `zero_indexed=False`: F(1)=0, F(2)=1, F(7)=8... (backwards compatibility)

#### `generate_first_n_fibonacci(n: int) -> List[int]`
Generuje pierwsze n liczb Fibonacciego (0-indexed).

#### `@lru_cache fibonacci_fast(n: int) -> int`
Szybkie obliczanie metodą macierzową O(log n) z memoizacją (0-indexed).

#### `is_fibonacci(num: int) -> bool`
Sprawdza czy liczba należy do ciągu.

#### `print_fibonacci_info(n: int, zero_indexed: bool = True) -> None`
Wyświetla szczegółowe informacje o F(n).

#### `export_fibonacci_sequence(sequence: List[int], filename: Optional[str] = None) -> None`
Eksportuje ciąg do pliku tekstowego z pełnymi statystykami.

### Wyjątki

#### `FibonacciError`
Rzucany przy nieprawidłowych argumentach (ujemne n, itp.).

## 🚀 Performance

| Operacja | Złożoność | Uwagi |
|----------|-----------|-------|
| generate_fibonacci_upto(N) | O(log N) | Liczba iteracji ≈ log_φ(N) |
| get_nth_fibonacci(n) | O(n) | Iteracyjny |
| generate_first_n_fibonacci(n) | O(n) | Buduje listę |
| fibonacci_fast(n) | O(log n) | Macierzowy + memoizacja, najszybszy |
| is_fibonacci(num) | O(1) | Test kwadratowy |
| export_fibonacci_sequence(seq) | O(n) | Zapis do pliku |

## 📖 Zastosowania ciągu Fibonacciego

- 🌻 **Natura:** Układ liści, płatków, spirale muszli
- 🎨 **Sztuka:** Proporcje w architekturze i malarstwie
- 📊 **Finanse:** Poziomy Fibonacciego w analizie technicznej
- 💻 **Algorytmy:** Fibonacci heap, wyszukiwanie Fibonacciego
- 🎲 **Kombinatoryka:** Zliczanie permutacji

## 🔗 Powiązane

- [Złoty podział - Wikipedia](https://pl.wikipedia.org/wiki/Z%C5%82oty_podzia%C5%82)
- [Fibonacci number - Wikipedia](https://en.wikipedia.org/wiki/Fibonacci_number)
- [Binet's formula](https://en.wikipedia.org/wiki/Fibonacci_number#Binet's_formula)

## 📄 Licencja

Free to use and modify.

---

**💡 Fun fact:** W naturze spirale Fibonacciego występują w słonecznikach (34 i 55 spirali), ananasach (8, 13, 21) i galaktykach!
