# MM Python

Kolekcja zaawansowanych skryptów Python z pełną dokumentacją i profesjonalną organizacją.

## 📚 Projekty

### 📊 [BMI Calculator](BMI/)
**Zaawansowany kalkulator BMI** z rekomendacjami zdrowotnymi.

**Features:**
- 👥 Uwzględnienie płci (różne normy dla M/K)
- 🎯 Dokładne obliczenia docelowej wagi
- 💾 Eksport wyników do pliku
- 📝 Logging sesji
- 🔄 Wielokrotne obliczenia
- 🛡️ Pełna obsługa błędów

```bash
cd BMI && python BMI.py
```

---

### 🚴 [Bike Service Proxy](BIKE/)
**Proxy do serwisu rowerowego rowermevo.pl** z monitoringiem lokalizacji i baterii.

**Features:**
- 📍 Pobieranie lokalizacji rowerów w czasie rzeczywistym
- 🔋 Monitoring poziomu baterii
- 🗺️ Dane z API rowermevo.pl
- 💾 Zapis do CSV
- 🌐 Integracja z requests
- 📊 Analiza danych stacji rowerowych

```bash
cd BIKE && python bike_service_proxy.py
```

---

### 🔺 [Pythagorean Triples Generator](PITAGORAS/)
**Generator prymitywnych trójek pitagorejskich** z analizą liczb pierwszych.

**Features:**
- ✅ Tylko trójki prymitywne (eliminacja duplikatów 3,4,5 i 6,8,10)
- 📊 Wymiary, obwód, powierzchnia
- 🔢 Detekcja liczb pierwszych
- 📈 Szczegółowe statystyki
- ⚡ Szybki algorytm Euklidesa

```bash
cd PITAGORAS && python Pitagoras_unified.py
```

---

### 🎬 [Video Downloader (YT-DLP)](YT-DLP/)
**Uniwersalny downloader wideo** obsługujący 1000+ stron.

**Features:**
- 🍪 Obsługa cookies (prywatne treści)
- 📊 5 poziomów jakości (Best, 1080p, 720p, 480p, Audio)
- 🎵 Tryb audio-only (MP3)
- 📦 Batch download
- 📈 Real-time progress bar
- 🔄 Automatyczna konwersja formatów

```bash
cd YT-DLP && python yt-dlp.py
```

---

### 🔢 [Prime Numbers Generator](PNA/)
**Efektywny generator liczb pierwszych** używający sita Eratostenesa.

**Features:**
- ⚡ Optymalizacja pamięci (sito segmentowane)
- 📊 Szczegółowe statystyki
- 💾 Zapis do pliku
- 📈 Progress bar dla dużych zakresów
- ⏱️ Pomiar wydajności

```bash
cd PNA && python PNA2a.py
```

---

### 🔢 [Fibonacci Calculator](Fibonacci/)
**Zaawansowane narzędzia do ciągu Fibonacciego** z wieloma algorytmami.

**Features:**
- ⚡ Algorytm macierzowy O(log n) dla dużych liczb
- 📊 6 różnych trybów obliczeniowych
- 🎯 Test przynależności do ciągu
- 📈 Analiza zbieżności do złotego podziału φ
- 🔢 Obsługa bardzo dużych liczb
- 🎨 Interaktywne menu

```bash
cd Fibonacci && python FibonacciUtils.py
```

---

### 🐴 [Knight's Tour Problem](Horse/)
**Solver problemu trasy skoczka szachowego** z algorytmem Warnsdorffa.

**Features:**
- ♟️ Heurystyka Warnsdorffa (inteligentna optymalizacja)
- 🔄 Backtracking z timeout protection
- 📊 Szczegółowe statystyki (czas, backtracki, głębokość)
- 💾 Eksport rozwiązań do pliku
- 📝 Logging wszystkich operacji
- 🎯 Wizualizacja planszy z Unicode
- ⏱️ Progress tracking dla dużych plansz

```bash
cd Horse && python Horse.py
```

---

## 🛠️ Wymagania

- Python 3.10+
- Standardowa biblioteka (większość projektów)
- Specyficzne zależności w `requirements.txt` w każdym projekcie

## 📖 Dokumentacja

Każdy projekt zawiera własny `README.md` z:
- Szczegółowym opisem funkcji
- Przykładami użycia
- Instrukcjami instalacji
- Rozwiązywaniem problemów

## 🚀 Quick Start

```bash
# Klonowanie repozytorium
git clone https://github.com/mmierzejewski/MM_Python.git
cd MM_Python

# Wybierz projekt i uruchom
cd BMI
python BMI.py
```

## 📁 Struktura

```
MM_Python/
├── BMI/                    # Kalkulator BMI z rekomendacjami
├── BIKE/                   # Proxy do rowermevo.pl (lokalizacje rowerów)
├── Fibonacci/              # Kalkulator Fibonacciego (6 algorytmów)
├── Horse/                  # Knight's Tour Problem (Warnsdorff)
├── PITAGORAS/              # Generator trójek pitagorejskich
├── PNA/                    # Liczby pierwsze (Sito Eratostenesa)
├── YT-DLP/                 # Universal video downloader (1000+ stron)
└── python-course-master/   # Kurs Python (Docker + Jupyter)
```

## 🤝 Kontakt

- GitHub: [@mmierzejewski](https://github.com/mmierzejewski)
- Repository: [MM_Python](https://github.com/mmierzejewski/MM_Python)

## 📄 Licencja

Free to use and modify.

---

**💡 Tip:** Każdy skrypt zawiera pełną walidację inputu, error handling i przyjazny interfejs użytkownika z emoji!
