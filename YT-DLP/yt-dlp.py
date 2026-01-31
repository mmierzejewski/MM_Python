#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uniwersalny downloader wideo używający yt-dlp z obsługą cookies.

Zaawansowany downloader wideo obsługujący YouTube, TikTok, Vimeo, Facebook i więcej.
Zawiera autoryzację cookie dla prywatnej/ograniczonej zawartości.
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from enum import Enum

try:
    from yt_dlp import YoutubeDL
    from tqdm import tqdm
except ImportError as e:
    print(f"❌ Brak wymaganego pakietu: {e.name}")
    print("\n📦 Zainstaluj zależności:")
    print("   pip install -r requirements.txt")
    print("   lub")
    print("   pip install yt-dlp tqdm")
    sys.exit(1)


MAX_FILENAME_LENGTH = 180  # Maksymalna długość nazwy pliku


class Quality(Enum):
    """Opcje jakości wideo."""
    BEST = "bestvideo+bestaudio/best"
    HIGH = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    MEDIUM = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    LOW = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    AUDIO_ONLY = "bestaudio/best"


class DownloadMode(Enum):
    """Opcje trybu pobierania."""
    VIDEO = "video"
    AUDIO = "audio"


class ProgressBar:
    """Obsługa paska postępu dla pobierania yt-dlp."""

    def __init__(self):
        self.pbar: Optional[tqdm] = None
        self.last_downloaded: int = 0

    def hook(self, d: dict) -> None:
        """Funkcja hook wywoływana przez yt-dlp podczas pobierania."""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)

            if not self.pbar and total_bytes:
                self.pbar = tqdm(
                    total=total_bytes,
                    unit='B',
                    unit_scale=True,
                    desc='Pobieranie',
                    ascii=True,
                    ncols=80
                )
                self.last_downloaded = 0

            if self.pbar:
                increment = downloaded - self.last_downloaded
                if increment > 0:
                    self.pbar.update(increment)
                    self.last_downloaded = downloaded

        elif d['status'] == 'finished':
            if self.pbar:
                if self.pbar.total:
                    remaining = self.pbar.total - self.pbar.n
                    if remaining > 0:
                        self.pbar.update(remaining)
                self.pbar.close()
                self.pbar = None
                self.last_downloaded = 0

    def reset(self) -> None:
        """Resetuje pasek postępu dla kolejnego pobierania."""
        if self.pbar:
            self.pbar.close()
            self.pbar = None
        self.last_downloaded = 0


def check_dependencies() -> bool:
    """Sprawdza czy wymagane zależności są dostępne."""
    all_ok = True

    try:
        import yt_dlp
        logging.info(f"Wersja yt-dlp: {yt_dlp.version.__version__}")
    except ImportError:
        print("❌ yt-dlp nie jest zainstalowany!")
        print("   pip install yt-dlp")
        all_ok = False

    if not shutil.which("ffmpeg"):
        print("❌ ffmpeg nie został znaleziony!")
        print("\n📦 Instalacja:")
        print("   macOS:    brew install ffmpeg")
        print("   Ubuntu:   sudo apt install ffmpeg")
        print("   Windows:  choco install ffmpeg")
        all_ok = False

    return all_ok


def find_cookie_file() -> Optional[Path]:
    """
    Znajduje plik cookie w typowych lokalizacjach.
    """
    possible_locations = [
        Path.cwd() / 'cookies.txt',
        Path(__file__).parent / 'cookies.txt',
        Path.home() / 'cookies.txt',
        Path.home() / 'WORK' / 'cookies.txt',
        Path.home() / 'Downloads' / 'cookies.txt',
    ]

    for location in possible_locations:
        if location.exists() and location.is_file():
            try:
                with open(location, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#') or '\t' in first_line:
                        logging.info(f"Znaleziono plik cookie: {location}")
                        return location
            except Exception as e:
                logging.warning(f"Błąd podczas czytania pliku cookie {location}: {e}")
                continue

    return None


def validate_cookie_file(cookie_path: Path) -> bool:
    """
    Waliduje format pliku cookie.
    """
    if not cookie_path.exists() or not cookie_path.is_file():
        return False

    try:
        with open(cookie_path, 'r', encoding='utf-8') as f:
            content = f.read(500)
            return ('# Netscape HTTP Cookie File' in content or
                    '# HTTP Cookie File' in content or
                    '\t' in content)
    except Exception:
        return False


def validate_url(url: str) -> bool:
    """
    Waliduje czy ciąg znaków jest prawidłowym URL.
    """
    url = url.strip()
    if not url:
        return False

    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False


def get_audio_tracks(url: str, cookie_file: Optional[Path] = None) -> list[dict]:
    """
    Pobiera listę dostępnych ścieżek dźwiękowych z wideo.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }

    if cookie_file and validate_cookie_file(cookie_file):
        ydl_opts['cookiefile'] = str(cookie_file)

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return []

            audio_tracks = []
            formats = info.get('formats', [])

            for fmt in formats:
                acodec = fmt.get('acodec', 'none')
                vcodec = fmt.get('vcodec', 'none')

                if acodec == 'none' or not acodec:
                    continue
                if vcodec != 'none':
                    continue

                format_id = fmt.get('format_id', '')
                format_note = fmt.get('format_note', '')
                ext = fmt.get('ext', 'unknown')
                abr = fmt.get('abr', 0) or 0

                lang = fmt.get('language', '')
                if not lang or lang == 'und':
                    format_lower = format_id.lower()
                    if 'pol' in format_lower or 'pl' in format_lower:
                        lang = 'pl'
                    elif 'eng' in format_lower or 'en' in format_lower:
                        lang = 'en'
                    else:
                        lang = 'und'

                display_name = format_note
                if not display_name or display_name in ['DASH audio', 'audio only', 'm4a_dash']:
                    if 'audiodeskrypcja' in format_id.lower():
                        display_name = 'Audiodeskrypcja'
                    elif 'polski' in format_id.lower():
                        display_name = 'Polski'
                    elif 'english' in format_id.lower() or 'eng' in format_id.lower():
                        display_name = 'Angielski'
                    else:
                        lang_map = {
                            'pl': 'Polski',
                            'en': 'Angielski',
                            'de': 'Niemiecki',
                            'fr': 'Francuski',
                            'es': 'Hiszpański',
                            'it': 'Włoski',
                            'ru': 'Rosyjski',
                            'uk': 'Ukraiński',
                            'und': 'Nieokreślony'
                        }
                        display_name = lang_map.get(lang, lang)

                tech_details = []
                if 'dash' in format_note.lower() or 'dash' in format_id.lower():
                    tech_details.append('DASH')
                if 'm3u8' in ext or 'hls' in format_note.lower():
                    tech_details.append('HLS')
                if tech_details:
                    display_name = f"{display_name} ({', '.join(tech_details)})"

                if 'audiodeskrypcja' in display_name.lower() or 'audiodeskrypcja' in format_id.lower():
                    continue

                audio_tracks.append({
                    'language': lang,
                    'language_name': display_name,
                    'format_id': format_id,
                    'format_note': format_note,
                    'ext': ext,
                    'abr': abr,
                })

            audio_tracks.sort(key=lambda x: -x['abr'])
            logging.info(f"Znaleziono {len(audio_tracks)} ścieżek audio dla {url}")
            return audio_tracks

    except Exception as e:
        logging.error(f"Błąd podczas pobierania informacji o ścieżkach audio: {e}")
        return []


def select_audio_track(audio_tracks: list[dict]) -> Optional[str]:
    """
    Pozwala użytkownikowi wybrać ścieżkę dźwiękową z szczegółowymi informacjami.
    """
    if not audio_tracks:
        print("\nℹ️  Nie znaleziono informacji o ścieżkach dźwiękowych.")
        print("   Zostanie użyta domyślna ścieżka audio.\n")
        return None

    print("\n🔊 Dostępne ścieżki dźwiękowe:")

    for i, track in enumerate(audio_tracks, 1):
        format_id = track.get('format_id', 'unknown')
        ext = track.get('ext', 'unknown')
        abr = track.get('abr', 0) or 0
        filesize = track.get('filesize', 0)
        lang = track.get('language', 'und')
        lang_name = track.get('language_name', 'Nieokreślony')
        format_note = track.get('format_note', '')

        if filesize and filesize > 0:
            size_mb = filesize / (1024 * 1024)
            size_str = f"~{size_mb:.2f}MiB"
        else:
            size_str = "?MiB"

        bitrate_str = f"{abr}kbps" if abr > 0 else "?kbps"

        print(f"   {i}. {format_id:20} {ext:4} {size_str:>12} {bitrate_str:>8} [{lang}] {lang_name} {format_note}")

    while True:
        choice = input(f"\n   Wybór [1-{len(audio_tracks)}]: ").strip()

        try:
            idx = int(choice)
            if 1 <= idx <= len(audio_tracks):
                selected = audio_tracks[idx - 1]
                print(f"   ✅ Wybrano: {selected['format_id']} - {selected['language_name']} "
                      f"({selected['ext']}, {selected.get('abr', 0)}kbps)\n")
                logging.info(f"Wybrano ścieżkę audio: {selected['format_id']}")
                return selected['format_id']
            else:
                print(f"   ⚠️  Nieprawidłowy wybór. Podaj liczbę od 1 do {len(audio_tracks)}")
        except ValueError:
            print("   ⚠️  Nieprawidłowe dane. Podaj liczbę.")


def download_video(
    url: str,
    output_path: Path,
    quality: Quality = Quality.BEST,
    mode: DownloadMode = DownloadMode.VIDEO,
    cookie_file: Optional[Path] = None,
    audio_format_id: Optional[str] = None
) -> bool:
    """
    Pobiera wideo z URL.
    """
    output_path.mkdir(parents=True, exist_ok=True)
    progress = ProgressBar()

    ydl_opts = {
        'format': quality.value,
        'outtmpl': str(output_path / '%(title).180B.%(ext)s'),
        'progress_hooks': [progress.hook],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        'windowsfilenames': True,
    }

    if audio_format_id:
        ydl_opts['format'] = f"bestvideo+{audio_format_id}/{quality.value}"
        logging.info(f"Wybrany format audio: {audio_format_id}")

    if cookie_file and validate_cookie_file(cookie_file):
        ydl_opts['cookiefile'] = str(cookie_file)
        logging.info(f"Używam pliku cookie: {cookie_file}")

    if mode == DownloadMode.AUDIO or quality == Quality.AUDIO_ONLY:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        ydl_opts['outtmpl'] = str(output_path / '%(title).180B.%(ext)s')
    else:
        ydl_opts['merge_output_format'] = 'mp4'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

    mode_str = "🎵 Audio" if mode == DownloadMode.AUDIO else "🎬 Wideo"
    print(f"📥 Pobieranie {mode_str} z: {url}")
    print(f"📂 Katalog wyjściowy: {output_path}")
    print(f"⚙️  Jakość: {quality.name}")
    if audio_format_id:
        print(f"🔊 Format audio: {audio_format_id}")
    if cookie_file and validate_cookie_file(cookie_file):
        print(f"🍪 Cookies: {cookie_file.name}")
    print()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Rozpoczynam pobieranie: {url}")
            info = ydl.extract_info(url, download=True)
            if info:
                filename = ydl.prepare_filename(info)
                if mode == DownloadMode.AUDIO or quality == Quality.AUDIO_ONLY:
                    filename = Path(filename).with_suffix('.mp3')
                print(f"\n✅ Zapisano do: {filename}")
                logging.info(f"Pobieranie zakończone sukcesem: {filename}")
                return True
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Błąd pobierania: {error_msg}")
        logging.error(f"Pobieranie nieudane dla {url}: {error_msg}")
        return False
    finally:
        progress.reset()

    return False


def get_output_directory() -> Path:
    """Pobiera katalog wyjściowy od użytkownika lub używa bieżącego katalogu."""
    current_dir = Path.cwd()

    print(f"📂 Katalog wyjściowy [domyślnie: {current_dir}]:")
    user_input = input("   (wciśnij Enter, aby użyć bieżącego katalogu): ").strip()

    if user_input:
        path = Path(user_input).expanduser().resolve()
        if not path.exists():
            print(f"⚠️  Katalog nie istnieje: {path}")
            create = input("   Utworzyć katalog? (T/N): ").strip().lower()
            if create not in ['t', 'tak']:
                print("Używam bieżącego katalogu.")
                return current_dir
        return path

    return current_dir


def download_batch(
    url_audio_pairs: list[tuple[str, Optional[str]]],
    output_path: Path,
    quality: Quality,
    mode: DownloadMode,
    cookie_file: Optional[Path] = None
) -> tuple[int, int]:
    """Pobiera wiele filmów z odpowiednimi ścieżkami audio."""
    successful = 0
    failed = 0
    total = len(url_audio_pairs)

    print(f"\n📦 Pobieranie wsadowe: {total} URL(i)\n")

    for i, (url, audio_format) in enumerate(url_audio_pairs, 1):
        print(f"\n[{i}/{total}] {'='*50}")
        if download_video(url, output_path, quality, mode, cookie_file, audio_format):
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"📊 Zakończono wsadowo: ✅ {successful} sukcesów, ❌ {failed} błędów")
    print(f"{'='*60}")

    return successful, failed


def setup_logging() -> None:
    """Konfiguruje logowanie (raz na start)."""
    log_file = Path.cwd() / 'yt-dlp-downloader.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout) if os.getenv('DEBUG') else logging.NullHandler()
        ]
    )


def setup_session() -> tuple[Optional[Path], bool, Path]:
    """
    Ustawienia wybierane raz (cookies + katalog wyjściowy).
    Zwraca: (cookie_file, use_cookies, output_path)
    """
    cookie_file = find_cookie_file()
    use_cookies = False

    if cookie_file:
        print(f"\n🍪 Znaleziono plik cookie: {cookie_file}")
        print("   (Przydatne dla prywatnych filmów, treści z ograniczeniem wiekowym, tylko dla członków)")
        response = input("   Użyć tego pliku cookie? (T/N) [T]: ").strip().lower()
        use_cookies = response in ['', 't', 'tak']
        if use_cookies:
            logging.info(f"Użytkownik wybrał użycie pliku cookie: {cookie_file}")
        else:
            cookie_file = None
            logging.info("Użytkownik zrezygnował z użycia pliku cookie")
    else:
        print("\nℹ️  Nie znaleziono pliku cookie (opcjonalne - potrzebne tylko do treści z ograniczeniami)")
        response = input("   Wskazać własną ścieżkę do pliku cookie? (T/N) [N]: ").strip().lower()
        if response in ['t', 'tak']:
            custom_path = input("   Ścieżka do cookies.txt: ").strip()
            if custom_path:
                cookie_file = Path(custom_path).expanduser().resolve()
                if not validate_cookie_file(cookie_file):
                    print("   ⚠️  Nieprawidłowy format pliku cookie, kontynuuję bez cookies")
                    cookie_file = None
                else:
                    print(f"   ✅ Plik cookie poprawny: {cookie_file}")
                    use_cookies = True

    output_path = get_output_directory()
    return cookie_file, use_cookies, output_path


def run_download_round(cookie_file: Optional[Path], use_cookies: bool, output_path: Path) -> int:
    """Jedna runda pobierania (zbieranie URL-i i pobranie)."""
    print("🔗 Obsługiwane: YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter, itd.")
    print("📺 Jakość: Zawsze NAJLEPSZA (wideo + audio)")
    print("🔊 Audio: Automatyczny wybór najlepszej ścieżki (bez audiodeskrypcji)")
    print(f"📂 Katalog wyjściowy: {output_path}")
    if cookie_file and use_cookies and validate_cookie_file(cookie_file):
        print(f"🍪 Cookies: {cookie_file}")
    else:
        print("🍪 Cookies: brak / wyłączone")
    print("\n   Wprowadź adresy URL (każdy w nowej linii, pusta linia kończy):\n")

    url_audio_pairs: list[tuple[str, Optional[str]]] = []
    url_count = 0

    while True:
        url_count += 1
        url = input(f"   URL #{url_count}: ").strip()

        if not url:
            if url_audio_pairs:
                break
            else:
                print("   Wprowadź przynajmniej jeden adres URL")
                url_count -= 1
                continue

        if not validate_url(url):
            print("   ⚠️  Nieprawidłowy adres URL, spróbuj ponownie...")
            url_count -= 1
            continue

        print("🔍 Sprawdzanie ścieżek audio...")
        audio_tracks = get_audio_tracks(url, cookie_file if use_cookies else None)
        audio_format_id = select_audio_track(audio_tracks)

        url_audio_pairs.append((url, audio_format_id))

        print(f"✅ URL #{url_count} dodany")
        if url_count == 1:
            print("   (wciśnij Enter, aby zakończyć lub podaj kolejny URL)\n")

    quality = Quality.BEST
    mode = DownloadMode.VIDEO

    logging.info(f"Rozpoczęcie pobierania: {len(url_audio_pairs)} URL(i), cookies: {use_cookies}, output: {output_path}")

    if len(url_audio_pairs) == 1:
        print()
        url, audio_format = url_audio_pairs[0]
        success = download_video(
            url,
            output_path,
            quality,
            mode,
            cookie_file if use_cookies else None,
            audio_format
        )
        return 0 if success else 1
    else:
        _, failed = download_batch(
            url_audio_pairs,
            output_path,
            quality,
            mode,
            cookie_file if use_cookies else None
        )
        return 0 if failed == 0 else 1


def main() -> int:
    """Główna funkcja programu (menu po każdej rundzie)."""
    setup_logging()

    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 21 + "POBIERANIE WIDEO" + " " * 21 + "║")
    print("║" + " " * 25 + "(yt-dlp)" + " " * 25 + "║")
    print("╚" + "═" * 58 + "╝\n")

    if not check_dependencies():
        return 1

    cookie_file, use_cookies, output_path = setup_session()

    last_rc: int = 0

    while True:
        print()
        last_rc = run_download_round(cookie_file, use_cookies, output_path)

        print("\nCo dalej?")
        print("   1. Nowe pobranie")
        print("   2. Wyjście")
        print("   3. Zmień ustawienia (cookies / katalog wyjściowy)")

        choice = input("   Wybór [1]: ").strip() or "1"
        if choice == "1":
            continue
        elif choice == "2":
            return last_rc
        elif choice == "3":
            print("\n⚙️  Zmiana ustawień...\n")
            cookie_file, use_cookies, output_path = setup_session()
            continue
        else:
            print("   ⚠️  Nieprawidłowy wybór. Wpisz 1, 2 lub 3.\n")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Przerwano przez użytkownika")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Nieoczekiwany błąd: {e}")
        sys.exit(1)
