# MM Python

Kolekcja zaawansowanych skryptów Python z pełną dokumentacją i profesjonalną organizacją.

## 📚 Projekty

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

### 💪 [BMI Calculator](BMI/)
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

### 🔢 [Fibonacci Calculator](Fibonacci/)
**Zaawansowane narzędzia do ciągu Fibonacciego** z wieloma algorytmami.

**Features:**
- ⚡ Algorytm macierzowy O(log n) dla dużych liczb
- 📊 7 różnych trybów obliczeniowych
- 🎯 Test przynależności do ciągu
- 📈 Analiza zbieżności do złotego podziału φ
- 🔢 Obsługa bardzo dużych liczb
- 🎨 Interaktywne menu
- 📋 **Opcja wyświetlania wszystkich n liczb** (10 na linię) lub tylko pierwszych/ostatnich 10
- 💾 Eksport ciągów do pliku z timestampem

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

### 🔺 [Pythagorean Triples Generator](PITAGORAS/)
**Generator prymitywnych trójek pitagorejskich** z analizą liczb pierwszych.

**Features:**
- ✅ Tylko trójki prymitywne (eliminacja duplikatów 3,4,5 i 6,8,10)
- 📊 Wymiary, obwód, powierzchnia
- 🔢 Detekcja liczb pierwszych
- 📈 Szczegółowe statystyki
- ⚡ Szybki algorytm Euklidesa

```bash
cd PITAGORAS && python Pitagoras.py
```

---

### 🔢 [Prime Numbers Generator](PNA/)
**Efektywny generator liczb pierwszych** używający sita Eratostenesa.

**Features:**
- 🎯 **Trzy tryby**: 
  - Liczby pierwsze do limitu
  - Pierwsze n liczb pierwszych
  - **Sprawdzanie pojedynczej liczby** ⭐ NOWOŚĆ!
- ⚡ Optymalizacja pamięci (sito segmentowane)
- 🧮 Automatyczne szacowanie limitu dla pierwszych n liczb
- ✅ Szybki test pierwszości O(√n)
- 📊 Szczegółowe statystyki dla wszystkich trybów
- 💾 Zapis do pliku
- 📈 Progress bar dla dużych zakresów
- ⏱️ Pomiar wydajności (μs, ms, s)

```bash
cd PNA && python PNA.py
```

---

### 📚 [Python Course](python-course-master/)
**Kompleksowy kurs Python** z interaktywnymi notebookami Jupyter i Docker.

**Features:**
- 🐳 Środowisko Docker (łatwa konfiguracja)
- 📓 Jupyter Notebooks (interaktywna nauka)
- 📖 Materiały szkoleniowe
- 🎯 Przykłady praktyczne
- 💻 Gotowe środowisko deweloperskie

```bash
cd python-course-master && docker-compose up
```

---

### 🎬 [Video Downloader (YT-DLP)](YT-DLP/)
**Uniwersalny downloader wideo** obsługujący 1000+ stron z zaawansowanym wyborem ścieżek audio.

**Features:**
- 🍪 Obsługa cookies (prywatne treści/tylko dla członków)
- 🎬 Zawsze najlepsza jakość wideo (automatycznie)
- 🔊 **Zaawansowany wybór ścieżek audio** - szczegółowe parametry techniczne:
  - Format ID (f6-a1-x3, f7-a2-x3)
  - Bitrate (kbps), rozmiar pliku, język
  - Typ ścieżki (DASH, HLS)
  - Automatyczne filtrowanie audiodeskrypcji
- 📦 Batch download z indywidualnym wyborem audio dla każdego URL
- 📈 Real-time progress bar z tqdm
- 🔄 Automatyczna konwersja formatów (ffmpeg)
- 📝 Logowanie wszystkich operacji do pliku
- ✅ Pełna walidacja URL i plików cookie
- 🛡️ Kompleksowa obsługa błędów

**Przykład wyboru audio:**
```
🔊 Dostępne ścieżki dźwiękowe:
   1. f7-a2-x3   m4a   ~42.07MiB   132kbps [pl] Polski (DASH)
   2. f6-a1-x3   m4a   ~41.76MiB   131kbps [pl] Polski (DASH)
   Wybór [1-2]: 1
```

```bash
cd YT-DLP && python yt-dlp.py
```

---

## 🛠️ Wymagania

- Python 3.10+
- Standardowa biblioteka (większość projektów)
- Specyficzne zależności w `requirements.txt` w każdym projekcie
- **ffmpeg** (wymagany dla YT-DLP - konwersja formatów wideo)
- **Docker** (opcjonalnie dla python-course-master)

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

# Wybierz projekt i uruchom (przykład)
cd YT-DLP
python yt-dlp.py
```

## 📁 Struktura

```
MM_Python/
├── .gitignore              # Ignorowane pliki (logi, eksporty, venv)
├── README.md               # Dokumentacja główna
├── fibonacci.log           # Log generowany przez Fibonacci Calculator
│
├── BIKE/                   # Proxy do rowermevo.pl (lokalizacje rowerów)
│   ├── bike_service_proxy.py
│   ├── locations.csv
│   └── requirements.txt
│
├── BMI/                    # Kalkulator BMI z rekomendacjami
│   ├── BMI.py
│   └── README.md
│
├── Fibonacci/              # Kalkulator Fibonacciego (7 trybów + opcje wyświetlania)
│   ├── FibonacciUtils.py
│   └── README.md
│
├── Horse/                  # Knight's Tour Problem (Warnsdorff)
│   ├── Horse.py
│   └── README.md
│
├── PITAGORAS/              # Generator trójek pitagorejskich
│   ├── Pitagoras.py
│   └── README.md
│
├── PNA/                    # Liczby pierwsze (Sito Eratostenesa)
│   ├── PNA.py
│   └── README.md
│
├── YT-DLP/                 # Universal video downloader (wybór ścieżek audio)
│   ├── yt-dlp.py
│   ├── cookies.txt.example
│   ├── README.md
│   └── requirements.txt
│
└── python-course-master/   # Kurs Python (Docker + Jupyter)
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── README.md
    ├── part_1/             # Podstawy Python
    ├── part_2/             # Zaawansowane tematy
    └── workshops/          # Zadania praktyczne
```

## 🤝 Kontakt

- GitHub: [@mmierzejewski](https://github.com/mmierzejewski)
- Repository: [MM_Python](https://github.com/mmierzejewski/MM_Python)

## 📄 Licencja

Free to use and modify.

---

**💡 Tip:** Każdy skrypt zawiera pełną walidację inputu, error handling i przyjazny interfejs użytkownika z emoji!
