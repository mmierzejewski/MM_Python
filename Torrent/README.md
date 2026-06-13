# Torrent Downloader

Prosty skrypt Python do pobierania torrentow z magnet linku albo pliku `.torrent`.

## Wymagania

- Python 3.14.5
- `aria2` 1.37+
- biblioteka `aria2p` 0.12.1

Instalacja:

```bash
brew install aria2
python3.14 -m venv ~/.venv
~/.venv/bin/python -m pip install -r requirements.txt
```

## Uzycie

Magnet link:

```bash
python torrent_downloader.py "magnet:?xt=urn:btih:..."
```

Plik `.torrent`:

```bash
python torrent_downloader.py /sciezka/do/pliku.torrent -o ./pobrane
```

Plik tekstowy z wieloma wpisami:

```bash
python torrent_downloader.py --batch-file lista.txt -o ./pobrane
```

Tryb interaktywny:

```bash
python torrent_downloader.py --interactive
```

Dodatkowe opcje:

- `--listen-port 6881` - port nasluchu klienta BitTorrent
- `--timeout 120` - maksymalny czas oczekiwania na metadane
- `--seed` - pozostawia klient w trybie seedowania po zakonczeniu pobierania
- `--interactive` - pyta o zrodlo i podstawowe opcje w terminalu
- `--batch-file lista.txt` - czyta wiele zrodel z pliku tekstowego, po jednym na linie
- `--log-file ./torrent.log` - zapisuje logi do wskazanego pliku

Przyklad pliku `lista.txt`:

```text
# komentarze sa ignorowane
magnet:?xt=urn:btih:...
/sciezka/do/archiwum.torrent
```

## Uwagi

Skrypt nie omija zabezpieczen i powinien byc uzywany tylko do pobierania tresci, do ktorych masz prawa.

Skrypt uruchamia lokalnie `aria2c` w trybie RPC i zamyka go po zakonczonej pracy.

Podczas pracy skrypt zapisuje logi do pliku `torrent_downloader.log` w biezacym katalogu, chyba ze podasz inna sciezke przez `--log-file`.
