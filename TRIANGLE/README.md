# Trójkąt 3D

Skrypt rysujący trójkąt w przestrzeni 3D z dowolnymi współrzędnymi wierzchołków.

## Opis

Program wykorzystuje bibliotekę Matplotlib do wizualizacji trójkąta w przestrzeni trójwymiarowej. Program interaktywnie pyta użytkownika o współrzędne (X, Y, Z) dla trzech wierzchołków trójkąta.

## Wymagania

- Python 3.x
- matplotlib
- numpy

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

## Funkcjonalność

- Interaktywne pobieranie współrzędnych wierzchołków od użytkownika
- Rysuje trójkąt w przestrzeni 3D z dowolnymi współrzędnymi
- Automatycznie oblicza długości boków
- Wyświetla współrzędne wierzchołków i długości boków
- Wypełnia trójkąt kolorem z przezroczystością
- Oznacza wierzchołki i krawędzie
- Automatycznie dopasowuje skalę wykresu do rozmiaru trójkąta
- Obsługa błędów przy wprowadzaniu danych
