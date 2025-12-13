# 🎬 Uniwersalny Downloader Wideo

Uniwersalny downloader wideo używający yt-dlp obsługujący YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter i ponad 1000 innych stron.

## ✨ Funkcje

- 📥 Pobieranie wideo z ponad 1000 stron internetowych
- 🍪 **Obsługa autoryzacji cookies** (treści prywatne/tylko dla członków)
- 🎵 Tryb tylko audio (ekstrakcja MP3)
- � **Zaawansowany wybór ścieżek audio** z szczegółowymi informacjami technicznymi
- 📋 Wyświetlanie wszystkich dostępnych ścieżek audio (format_id, bitrate, rozmiar, język)
- 🎯 Automatyczne filtrowanie audiodeskrypcji
- 📊 Zawsze najlepsza jakość wideo (automatycznie)
- 📦 Pobieranie wsadowe z indywidualnym wyborem audio dla każdego URL
- 📈 Pasek postępu w czasie rzeczywistym
- 🔄 Automatyczna konwersja formatów
- 📝 Logowanie do pliku
- ✅ Walidacja danych wejściowych
- 🛡️ Obsługa błędów

## 📋 Wymagania

- Python 3.8+
- ffmpeg (wymagany do konwersji formatów)

## 🚀 Instalacja

### 1. Instalacja zależności Python

```bash
pip install -r requirements.txt
```

Lub ręcznie:
```bash
pip install yt-dlp tqdm
```

### 2. Instalacja ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
```bash
choco install ffmpeg
```

Lub pobierz z: https://ffmpeg.org/download.html

## 💻 Użycie

### Podstawowe użycie

```bash
python yt-dlp.py
```

### Interaktywne pytania

1. **Plik cookie (opcjonalny):** Automatycznie wykrywany lub podaj własną ścieżkę
2. **Wprowadź URL(e):** Wklej adresy URL wideo (jeden w linii, pusta linia kończy)
3. **Wybór ścieżki audio:** Dla każdego URL program wykryje i wyświetli dostępne ścieżki audio z parametrami:
   - Format ID (np. f6-a1-x3, f7-a2-x3)
   - Rozszerzenie (m4a, m3u8)
   - Rozmiar pliku
   - Bitrate (kbps)
   - Język
   - Typ (DASH audio, HLS, itp.)
   - Oznaczenie audiodeskrypcji (jeśli występuje)
4. **Katalog wyjściowy:** Wybierz gdzie zapisać pliki

**Uwaga:** Jakość wideo jest zawsze ustawiona na NAJLEPSZĄ - nie ma możliwości wyboru niższej jakości.

### Pobieranie pojedynczego wideo

```bash
python yt-dlp.py
# Wprowadź URL: https://www.youtube.com/watch?v=example
# Naciśnij Enter (zakończ)
# Wybierz jakość: 1
# Naciśnij Enter (bieżący katalog)
```

### Pobieranie wsadowe

```bash
python yt-dlp.py
# Wprowadź wiele URL-i:
# URL: https://www.youtube.com/watch?v=video1
# URL: https://www.youtube.com/watch?v=video2
# URL: https://www.youtube.com/watch?v=video3
# URL: [naciśnij Enter]
# Wybierz jakość: 2
```
### Wybór konkretnej ścieżki audio

```bash
python yt-dlp.py
# Wprowadź URL: https://vod.tvp.pl/seriale/...
# 
# 🔊 Dostępne ścieżki dźwiękowe:
#    1. f7-a2-x3            m4a   ~42.07MiB  132kbps [pl] Polski (DASH) DASH audio
#    2. f6-a1-x3            m4a   ~41.76MiB  131kbps [pl] Polski (DASH) DASH audio
#    3. audio0-Polski       m3u8      ?MiB    ?kbps [pl] Polski HLS
#
#    Wybór [1-3]: 1
#    ✅ Wybrano: f7-a2-x3 - Polski (DASH) (m4a, 132kbps)
```

**Funkcje wyboru audio:**
- Automatyczne wykrywanie wszystkich dostępnych ścieżek audio
- Szczegółowe parametry techniczne (format_id, bitrate, rozmiar)
- Filtrowanie audiodeskrypcji (nie są wyświetlane automatycznie)
- Indywidualny wybór dla każdego URL w trybie wsadowym
- Sortowanie według bitrate (najlepsze na górze)

### Pobieranie wsadowe z różnymi ścieżkami audio

```bash
python yt-dlp.py
# URL #1: https://vod.tvp.pl/video1
# [wybierz ścieżkę audio dla video1]
# URL #2: https://vod.tvp.pl/video2
# [wybierz ścieżkę audio dla video2]
# URL #3: [Enter - zakończ]
# Katalog wyjściowy: ./pobrane
```

### Używanie cookies do treści prywatnych/z ograniczeniami

#### Do czego służą cookies?
- Prywatne filmy
- Treści z ograniczeniem wiekowym
- Treści tylko dla członków (członkostwa YouTube, Patreon, itp.)
- Filmy z ograniczeniami kanału
- Treści zablokowane regionalnie (z VPN)

#### Jak wyeksportować cookies:

**Metoda 1: Rozszerzenie przeglądarki (Zalecane)**
1. Zainstaluj rozszerzenie:
   - Chrome/Edge: [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid)
   - Firefox: [cookies.txt](https://addons.mozilla.org/firefox/addon/cookies-txt/)
2. Przejdź na stronę (np. YouTube)
3. Zaloguj się na swoje konto
4. Kliknij ikonę rozszerzenia → Eksportuj cookies
5. Zapisz jako `cookies.txt`

**Metoda 2: Wbudowana funkcja yt-dlp**
```bash
yt-dlp --cookies-from-browser chrome
```

#### Lokalizacje pliku cookie (auto-wykrywane):
- Bieżący katalog: `./cookies.txt`
- Katalog skryptu: `/ścieżka/do/skryptu/cookies.txt`
- Katalog domowy: `~/cookies.txt`
- Katalog roboczy: `~/WORK/cookies.txt`
- Pobrane: `~/Downloads/cookies.txt`

#### Przykład z cookies:

```bash
# Umieść cookies.txt w jednej z auto-wykrywanych lokalizacji
python yt-dlp.py
# Znaleziono plik cookie: cookies.txt
# Użyć tego pliku cookie? tak
# Wprowadź URL: https://www.youtube.com/watch?v=private_video
```

## 📊 Obsługiwane Strony

YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter, Twitch, Dailymotion, Reddit i ponad 1000 innych!

Pełna lista: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## 📝 Logowanie

Wszystkie pobierania są logowane do `yt-dlp-downloader.log` w bieżącym katalogu.

Włącz tryb debugowania:
```bash
DEBUG=1 python yt-dlp.py
```

## 🔧 Jakość i Ścieżki Audio

### Jakość wideo
Skrypt **zawsze używa najlepszej dostępnej jakości wideo** (bestvideo+bestaudio). Nie ma możliwości wyboru niższej jakości - to zapewnia maksymalną jakość pobieranych filmów.

### Ścieżki audio
Dla każdego URL skrypt:
1. **Wykrywa** wszystkie dostępne ścieżki audio
2. **Wyświetla** szczegóły techniczne:
   - `format_id` - identyfikator formatu (np. f6-a1-x3)
   - `ext` - rozszerzenie (m4a, m3u8)
   - `rozmiar` - wielkość pliku (jeśli dostępna)
   - `bitrate` - jakość audio w kbps
   - `język` - kod języka [pl], [en], itp.
   - `typ` - technologia (DASH audio, HLS, itp.)
3. **Filtruje** audiodeskrypcję (nie wyświetla tych ścieżek)
4. **Sortuje** według bitrate (najlepsza jakość na górze)

Użytkownik wybiera konkretną ścieżkę audio dla każdego wideo.

### Przykład wyświetlania ścieżek

```
🔊 Dostępne ścieżki dźwiękowe:
   1. f7-a2-x3            m4a   ~42.07MiB   132kbps [pl] Polski (DASH) DASH audio
   2. f6-a1-x3            m4a   ~41.76MiB   131kbps [pl] Polski (DASH) DASH audio
   3. audio0-Polski       m3u8      ?MiB     ?kbps [pl] Polski HLS
```

## 🛠️ Rozwiązywanie Problemów

### "ffmpeg not found"
Zainstaluj ffmpeg korzystając z powyższych instrukcji.

### "Import error: yt_dlp"
```bash
pip install yt-dlp tqdm
```

### "Download error: HTTP Error 403" lub "Private video"
Film wymaga uwierzytelnienia. Rozwiązania:
1. Wyeksportuj cookies z przeglądarki (zobacz sekcję "Używanie cookies")
2. Umieść `cookies.txt` w katalogu skryptu
3. Uruchom skrypt i potwierdź użycie cookies
4. Upewnij się, że jesteś zalogowany na stronie podczas eksportu cookies

### Plik cookie nie działa
- Sprawdź czy plik jest w formacie Netscape (zaczyna się od `# Netscape HTTP Cookie File`)
- Upewnij się, że cookies są świeże (niewygasałe)
- Wyeksportuj cookies ponownie po zalogowaniu
- Sprawdź kodowanie pliku (powinno być UTF-8)
- Upewnij się, że nie ma dodatkowych spacji lub błędów formatowania

### "Invalid cookie file format"
Plik cookie musi być w formacie Netscape. Użyj rozszerzeń przeglądarki wymienionych powyżej lub:
```bash
# Eksport z przeglądarki używając yt-dlp
yt-dlp --cookies-from-browser firefox --cookies cookies.txt "https://youtube.com"
```

### Długie nazwy plików
Nazwy plików są automatycznie skracane do 180 znaków dla kompatybilności.

### Ścieżka audio nie pobiera się poprawnie
Jeśli wybrana ścieżka audio (np. f6-a1-x3) pobiera niewłaściwe audio:
1. Sprawdź wszystkie dostępne ścieżki - czasem format_id może być mylący
2. Spróbuj innej ścieżki z listy (najlepiej z najwyższym bitrate)
3. Niektóre strony mogą wymagać cookies dla pełnego dostępu do ścieżek audio
4. Format DASH (m4a) zwykle jest bardziej niezawodny niż HLS (m3u8)

## 📄 Licencja

Wolne do użycia i modyfikacji.

## 🤝 Podziękowania

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Najlepszy downloader wideo
- [tqdm](https://github.com/tqdm/tqdm) - Biblioteka paska postępu
