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
    print(f"❌ Missing required package: {e.name}")
    print("\n📦 Install dependencies:")
    print("   pip install -r requirements.txt")
    print("   or")
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
                    desc='Downloading',
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
    
    # Sprawdź yt-dlp
    try:
        import yt_dlp
        logging.info(f"yt-dlp version: {yt_dlp.version.__version__}")
    except ImportError:
        print("❌ yt-dlp not installed!")
        print("   pip install yt-dlp")
        all_ok = False
    
    # Sprawdź ffmpeg
    if not shutil.which("ffmpeg"):
        print("❌ ffmpeg not found!")
        print("\n📦 Installation:")
        print("   macOS:    brew install ffmpeg")
        print("   Ubuntu:   sudo apt install ffmpeg")
        print("   Windows:  choco install ffmpeg")
        all_ok = False
    
    return all_ok


def find_cookie_file() -> Optional[Path]:
    """
    Znajduje plik cookie w typowych lokalizacjach.
    
    Szuka cookies.txt w:
    - Bieżący katalog
    - Katalog skryptu
    - Katalog domowy
    - Katalog ~/WORK
    
    Returns:
        Ścieżka do pliku cookie lub None jeśli nie znaleziono
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
            # Podstawowa walidacja - sprawdź czy plik wygląda jak format Netscape cookie
            try:
                with open(location, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    # Prawidłowy plik cookie powinien zaczynać się od komentarza lub wpisu cookie
                    if first_line.startswith('#') or '\t' in first_line:
                        logging.info(f"Found cookie file: {location}")
                        return location
            except Exception as e:
                logging.warning(f"Error reading cookie file {location}: {e}")
                continue
    
    return None


def validate_cookie_file(cookie_path: Path) -> bool:
    """
    Waliduje format pliku cookie.
    
    Args:
        cookie_path: Ścieżka do pliku cookie
    
    Returns:
        True jeśli prawidłowy format Netscape, False w przeciwnym razie
    """
    if not cookie_path.exists() or not cookie_path.is_file():
        return False
    
    try:
        with open(cookie_path, 'r', encoding='utf-8') as f:
            content = f.read(500)  # Czytaj pierwsze 500 znaków
            # Sprawdź markery formatu Netscape cookie
            return ('# Netscape HTTP Cookie File' in content or 
                    '# HTTP Cookie File' in content or
                    '\t' in content)  # Wartości rozdzielone tabulatorami
    except Exception:
        return False


def validate_url(url: str) -> bool:
    """
    Waliduje czy ciąg znaków jest prawidłowym URL.

    Args:
        url: Ciąg URL do walidacji

    Returns:
        True jeśli prawidłowy URL, False w przeciwnym razie
    """
    url = url.strip()
    if not url:
        return False

    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False


def download_video(
    url: str,
    output_path: Path,
    quality: Quality = Quality.BEST,
    mode: DownloadMode = DownloadMode.VIDEO,
    cookie_file: Optional[Path] = None
) -> bool:
    """
    Pobiera wideo z URL.

    Args:
        url: URL wideo
        output_path: Katalog wyjściowy
        quality: Ustawienie jakości wideo
        mode: Tryb pobierania (wideo lub audio)
        cookie_file: Opcjonalna ścieżka do pliku cookie w formacie Netscape

    Returns:
        True jeśli sukces, False w przeciwnym razie
    """
    # Upewnij się że katalog wyjściowy istnieje
    output_path.mkdir(parents=True, exist_ok=True)

    progress = ProgressBar()

    # Opcje podstawowe
    ydl_opts = {
        'format': quality.value,
        'outtmpl': str(output_path / '%(title).180B.%(ext)s'),
        'progress_hooks': [progress.hook],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        'windowsfilenames': True,  # Bezpieczne nazwy plików na wszystkich platformach
    }
    
    # Dodaj plik cookie jeśli podano i jest prawidłowy
    if cookie_file and validate_cookie_file(cookie_file):
        ydl_opts['cookiefile'] = str(cookie_file)
        logging.info(f"Using cookie file: {cookie_file}")

    # Ustawienia tylko audio
    if mode == DownloadMode.AUDIO or quality == Quality.AUDIO_ONLY:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        ydl_opts['outtmpl'] = str(output_path / '%(title).180B.%(ext)s')
    else:
        # Ustawienia wideo
        ydl_opts['merge_output_format'] = 'mp4'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

    mode_str = "🎵 Audio" if mode == DownloadMode.AUDIO else "🎬 Video"
    print(f"📥 Downloading {mode_str} from: {url}")
    print(f"📂 Output directory: {output_path}")
    print(f"⚙️  Quality: {quality.name}")
    if cookie_file and validate_cookie_file(cookie_file):
        print(f"🍪 Cookies: {cookie_file.name}")
    print()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Starting download: {url}")
            info = ydl.extract_info(url, download=True)
            if info:
                filename = ydl.prepare_filename(info)
                # Dla audio, zaktualizuj rozszerzenie
                if mode == DownloadMode.AUDIO or quality == Quality.AUDIO_ONLY:
                    filename = Path(filename).with_suffix('.mp3')
                print(f"\n✅ Saved to: {filename}")
                logging.info(f"Download successful: {filename}")
                return True
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Download error: {error_msg}")
        logging.error(f"Download failed for {url}: {error_msg}")
        return False
    finally:
        progress.reset()

    return False


def get_quality_choice() -> Quality:
    """Pobiera wybór jakości od użytkownika."""
    print("\n📺 Select quality:")
    print("   1. Best (highest available)")
    print("   2. High (1080p)")
    print("   3. Medium (720p)")
    print("   4. Low (480p)")
    print("   5. Audio only (MP3)")
    
    choice = input("   Choice [1]: ").strip() or "1"
    
    quality_map = {
        "1": Quality.BEST,
        "2": Quality.HIGH,
        "3": Quality.MEDIUM,
        "4": Quality.LOW,
        "5": Quality.AUDIO_ONLY,
    }
    
    return quality_map.get(choice, Quality.BEST)


def get_download_mode(quality: Quality) -> DownloadMode:
    """Określa tryb pobierania na podstawie jakości."""
    return DownloadMode.AUDIO if quality == Quality.AUDIO_ONLY else DownloadMode.VIDEO


def get_output_directory() -> Path:
    """Pobiera katalog wyjściowy od użytkownika lub używa bieżącego katalogu."""
    current_dir = Path.cwd()

    print(f"📂 Output directory [current: {current_dir}]:")
    user_input = input("   (press Enter for current directory): ").strip()

    if user_input:
        path = Path(user_input).expanduser().resolve()
        if not path.exists():
            print(f"⚠️  Directory doesn't exist: {path}")
            create = input("   Create it? (yes/no): ").strip().lower()
            if create not in ['yes', 'y']:
                print("Using current directory instead.")
                return current_dir
        return path

    return current_dir


def download_batch(
    urls: list[str],
    output_path: Path,
    quality: Quality,
    mode: DownloadMode,
    cookie_file: Optional[Path] = None
) -> tuple[int, int]:
    """Pobiera wiele filmów.
    
    Args:
        urls: Lista URL-i wideo
        output_path: Katalog wyjściowy
        quality: Jakość wideo
        mode: Tryb pobierania
        cookie_file: Opcjonalny plik cookie dla autoryzacji
    
    Returns:
        Krotka (liczba_sukces, liczba_błąd)
    """
    successful = 0
    failed = 0
    total = len(urls)
    
    print(f"\n📦 Batch download: {total} URL(s)\n")
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{total}] {'='*50}")
        if download_video(url, output_path, quality, mode, cookie_file):
            successful += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Batch complete: ✅ {successful} successful, ❌ {failed} failed")
    print(f"{'='*60}")
    
    return successful, failed


def main() -> int:
    """Główna funkcja programu."""
    # Konfiguracja loggingu
    log_file = Path.cwd() / 'yt-dlp-downloader.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout) if os.getenv('DEBUG') else logging.NullHandler()
        ]
    )
    
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "VIDEO DOWNLOADER" + " " * 27 + "║")
    print("║" + " " * 17 + "(yt-dlp)" + " " * 32 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # Sprawdź zależności
    if not check_dependencies():
        return 1
    
    # Znajdź i opcjonalnie użyj pliku cookie
    cookie_file = find_cookie_file()
    use_cookies = False
    
    if cookie_file:
        print(f"\n🍪 Found cookie file: {cookie_file}")
        print("   (Useful for private videos, age-restricted content, member-only content)")
        response = input("   Use this cookie file? (yes/no) [yes]: ").strip().lower()
        use_cookies = response in ['', 'yes', 'y']
        if use_cookies:
            logging.info(f"User selected to use cookie file: {cookie_file}")
        else:
            cookie_file = None
            logging.info("User declined to use cookie file")
    else:
        print("\nℹ️  No cookie file found (optional - only needed for restricted content)")
        response = input("   Specify custom cookie file path? (yes/no) [no]: ").strip().lower()
        if response in ['yes', 'y']:
            custom_path = input("   Path to cookies.txt: ").strip()
            if custom_path:
                cookie_file = Path(custom_path).expanduser().resolve()
                if not validate_cookie_file(cookie_file):
                    print("   ⚠️  Invalid cookie file format, proceeding without cookies")
                    cookie_file = None
                else:
                    print(f"   ✅ Cookie file validated: {cookie_file}")
                    use_cookies = True

    # Pobierz URL-e
    print("🔗 Supported: YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter, etc.")
    print("   Enter URLs (one per line, empty line to finish):")
    
    urls = []
    while True:
        url = input("   URL: ").strip()
        if not url:
            if urls:
                break
            else:
                print("   Please enter at least one URL")
                continue
        
        if validate_url(url):
            urls.append(url)
            if len(urls) == 1:
                print("   (press Enter to finish, or add more URLs)")
        else:
            print("   ⚠️  Invalid URL, skipping...")
    
    # Pobierz jakość
    quality = get_quality_choice()
    mode = get_download_mode(quality)
    
    # Pobierz katalog wyjściowy
    output_path = get_output_directory()

    # Pobierz wideo
    logging.info(f"Starting download session: {len(urls)} URL(s), cookies: {use_cookies}")
    
    if len(urls) == 1:
        print()
        success = download_video(urls[0], output_path, quality, mode, cookie_file if use_cookies else None)
        return 0 if success else 1
    else:
        successful, failed = download_batch(urls, output_path, quality, mode, cookie_file if use_cookies else None)
        return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)