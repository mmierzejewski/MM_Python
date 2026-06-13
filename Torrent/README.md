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
python torrent_downloader.py /sciezka/do/pliku.torrent
```

Plik tekstowy z wieloma wpisami:

```bash
python torrent_downloader.py --batch-file lista.txt
```

Tryb interaktywny:

```bash
python torrent_downloader.py --interactive
```

Uruchomienie bez argumentow:

```bash
python torrent_downloader.py
```

Skrypt zapyta wtedy o katalog docelowy oraz o magnet link lub sciezke do pliku `.torrent`, podobnie jak `YT-DLP` pyta o katalog i adresy URL.
Domyslnie pyta tylko o te dwa elementy.

Dodatkowe opcje:

- `--listen-port 6881` - port nasluchu klienta BitTorrent
- `--listen-port-end 6891` - koniec zakresu portow BitTorrent i DHT
- `--rpc-port 0` - port RPC aria2 dostepny na interfejsach hosta; domyslnie losowy wolny port
- `--listen-address 0.0.0.0` - zakres nasluchu RPC: `0.0.0.0` albo `localhost`
- `--local-only` - skrot dla `--listen-address localhost`
- `--public-rpc` - skrot dla `--listen-address 0.0.0.0`
- `--timeout 120` - maksymalny czas oczekiwania na metadane
- `--seed` - pozostawia klient w trybie seedowania po zakonczeniu pobierania
- `--allow-overwrite` - pozwala nadpisac istniejacy plik docelowy, gdy brak pliku `*.aria2`
- `--interactive` - wymusza pytania o zrodlo oraz dodatkowe opcje w terminalu
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

Skrypt uruchamia `aria2c` w trybie RPC na porcie hosta i zamyka go po zakonczonej pracy.
RPC jest chronione losowym `rpc-secret`, ale port pozostaje wystawiony na interfejsach hosta.
Porty BitTorrent i DHT domyslnie uzywaja zakresu `6881-6891`, ktory mozna zmienic przez `--listen-port` i `--listen-port-end`.
Jesli chcesz ograniczyc RPC tylko do tej maszyny, uzyj `--local-only`.
Jesli chcesz jawnie wystawic RPC na interfejsach hosta, uzyj `--public-rpc`.
Flag `--local-only` i `--public-rpc` nie mozna laczyc w jednym uruchomieniu.
Opcja `--listen-address` steruje tylko ekspozycja RPC: `localhost` ogranicza RPC do tej maszyny, a `0.0.0.0` wystawia RPC na interfejsach hosta. `aria2c` nie udostepnia rownowaznej opcji dla IPv4 BitTorrent bind do konkretnego adresu.
Jesli nie podasz `--rpc-port`, skrypt automatycznie wybiera losowy wolny port RPC na hoście. Jawnie podany `--rpc-port` powoduje twardy blad przy konflikcie.
W trybie interaktywnym skrypt pyta tez, czy ma nadpisac istniejace pliki docelowe.

Podczas pracy skrypt zapisuje logi do pliku `torrent_downloader.log` w biezacym katalogu, chyba ze podasz inna sciezke przez `--log-file`.
