# 📐 Trójkąt 3D

**Zaawansowany wizualizator trójkątów w przestrzeni 3D** z pełną walidacją geometryczną.

## 🎯 Opis

Program wykorzystuje bibliotekę Matplotlib do profesjonalnej wizualizacji trójkąta w przestrzeni trójwymiarowej. Interaktywnie pobiera współrzędne (X, Y, Z) dla trzech wierzchołków i tworzy szczegółową wizualizację 3D z pełną analizą geometryczną.

## ✨ Features

- ✅ **Walidacja geometryczna** - sprawdzanie czy punkty nie są identyczne i nie są współliniowe
- 📏 **Obliczanie długości boków** - automatyczne wyświetlanie wszystkich wymiarów
- 📐 **Obliczanie pola powierzchni** - wykorzystanie iloczynu wektorowego
- 🎨 **Profesjonalna wizualizacja**:
  - Wypełniony trójkąt z przezroczystością
  - Oznaczone wierzchołki (czerwone kropki)
  - Opisane długości boków (zielone etykiety)
  - Automatyczne dopasowanie skali z marginesem 10%
  - Punkt (0,0,0) zawsze widoczny jako odniesienie
- 💾 **Eksport do PNG** - automatyczny zapis wykresu w katalogu skryptu
- 📊 **Szczegółowe statystyki** - współrzędne, długości boków, pole powierzchni
- 🛡️ **Pełna obsługa błędów** - walidacja inputu i obsługa wyjątków
- 🔢 **Type hints** - pełne adnotacje typów dla lepszej czytelności kodu
- 📈 **Interaktywny wykres** - możliwość obracania i zoomowania w trybie `plt.show()`

## 🛠️ Wymagania

- Python 3.10+
- matplotlib >= 3.5.0
- numpy >= 1.21.0

## Instalacja zależności

```bash
pip install -r requirements.txt
```

## Uruchomienie

```bash
python triangle_3d.py
```

Program poprosi Cię o podanie współrzędnych X, Y, Z dla każdego z trzech wierzchołków (A, B, C).

## Przykład użycia

```
============================================================
Rysowanie trójkąta w przestrzeni 3D
============================================================

Program narysuje trójkąt na podstawie podanych współrzędnych
trzech wierzchołków w przestrzeni 3D (X, Y, Z).

Podaj współrzędne wierzchołka A:
  XA: 0
  YA: 0
  ZA: 0

Podaj współrzędne wierzchołka B:
  XB: 3
  YB: 0
  ZB: 0

Podaj współrzędne wierzchołka C:
  XC: 0
  YC: 4
  ZC: 0
```

```

**Program wyświetli:**
```
Współrzędne wierzchołków:
A = (0.00, 0.00, 0.00)
B = (3.00, 0.00, 0.00)
C = (0.00, 4.00, 0.00)

Długości boków trójkąta:
AB = 3.00
AC = 4.00
BC = 5.00

Pole trójkąta: 6.00

Wykres zapisany jako /home/mmierzejewski/GitHub/MM_Python/TRIANGLE/triangle_3d.png
```

## 🔧 Funkcjonalność

### Walidacja Geometryczna
- ✅ Sprawdzenie czy punkty nie są identyczne
- ✅ Sprawdzenie współliniowości (iloczyn wektorowy z jawną tolerancją)
- ⚠️ Komunikaty błędów dla nieprawidłowych konfiguracji

### Obliczenia
- 📏 Długości wszystkich trzech boków (norma euklidesowa)
- 📐 Pole powierzchni trójkąta (½ |AB × AC|)
- 📊 Automatyczne formatowanie wyników (2 miejsca po przecinku)

### Wizualizacja
- 🎨 Trójkąt wypełniony kolorem cyan z alpha=0.3
- 🔴 Czerwone markery wierzchołków (rozmiar 100)
- 🏷️ Etykiety współrzędnych przy każdym wierzchołku
- 🟢 Zielone etykiety długości na środkach boków
- 📏 Automatyczne zakresy osi obejmujące (0,0,0) i wszystkie wierzchołki
- ⚙️ Siatka z alpha=0.3 dla lepszej orientacji przestrzennej

### Eksport i Wyświetlanie
- 💾 Automatyczny zapis do `triangle_3d.png` w katalogu skryptu
- 🖥️ Interaktywne okno matplotlib (rotacja, zoom, pan)
- 📍 Pełna ścieżka do zapisanego pliku w komunikacie

## 🏗️ Architektura Kodu

### Funkcje pomocnicze

**`calculate_axis_ranges(points, margin_factor=0.1)`**
- Oblicza zakresy osi dla wykresu 3D
- Zawsze zawiera punkt (0,0,0)
- Dodaje margines 10% (konfigurowalny)
- Zwraca tuple z zakresami dla X, Y, Z

**`draw_triangle_3d(A, B, C)`**
- Główna funkcja rysowania
- Pełna walidacja wejścia
- Obliczenia geometryczne
- Tworzenie i konfiguracja wykresu
- Eksport i wyświetlanie

**`get_vertex_coordinates(vertex_name)`**
- Interaktywne pobieranie współrzędnych
- Obsługa ValueError (nieprawidłowy format)
- Obsługa KeyboardInterrupt (Ctrl+C)
- Pętla ponawiania przy błędach

## 🔍 Szczegóły Techniczne

- **Type hints**: Pełne adnotacje typów (`List[float]`, `Tuple`, `np.ndarray`)
- **Tolerancja współliniowości**: `1e-10` (jawnie zdefiniowana stała)
- **Format obrazu**: PNG z DPI domyślnym matplotlib
- **Układ współrzędnych**: Standard prawoskrętny (X-prawo, Y-przód, Z-góra)

## 💡 Przykłady użycia

### Trójkąt prostokątny 3-4-5
```
A: (0, 0, 0)
B: (3, 0, 0)
C: (0, 4, 0)
Wynik: Pole = 6.00
```

### Trójkąt równoboczny
```
A: (0, 0, 0)
B: (1, 0, 0)
C: (0.5, 0.866, 0)
Wynik: Pole ≈ 0.43
```

### Trójkąt w pełnej przestrzeni 3D
```
A: (1, 2, 3)
B: (4, 5, 6)
C: (7, 1, 2)
```

## ⚠️ Obsługa błędów

**Identyczne wierzchołki:**
```
Błąd: Dwa lub więcej wierzchołków mają identyczne współrzędne. To nie jest trójkąt.
```

**Punkty współliniowe:**
```
Błąd: Punkty są współliniowe. To nie jest trójkąt.
```

**Nieprawidłowy format danych:**
```
Błąd! Podaj liczby (np. 1.5, 2, -3.14)
```

## 🚀 Przyszłe ulepszenia (TODO)

- [ ] Obliczanie kątów między bokami
- [ ] Klasyfikacja typu trójkąta (prostokątny, równoramienny, równoboczny)
- [ ] Argumenty wiersza poleceń dla trybu nieinteraktywnego
- [ ] Export do wielu formatów (SVG, PDF)
- [ ] Batch processing z pliku CSV
- [ ] Animacje obrotu

---

**Autor**: [@mmierzejewski](https://github.com/mmierzejewski)  
**Projekt**: [MM_Python/TRIANGLE](https://github.com/mmierzejewski/MM_Python/tree/developer/TRIANGLE)
