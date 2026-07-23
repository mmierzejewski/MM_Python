#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal video downloader using yt-dlp with cookie support.

Advanced video downloader supporting YouTube, TikTok, Vimeo, Facebook and more.
Includes cookie authorization for private/restricted content.
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


MAX_FILENAME_LENGTH = 180  # Maximum filename length


class Quality(Enum):
    """Video quality options."""
    BEST = "bestvideo+bestaudio/best"
    HIGH = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    MEDIUM = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    LOW = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    AUDIO_ONLY = "bestaudio/best"


class DownloadMode(Enum):
    """Download mode options."""
    VIDEO = "video"
    AUDIO = "audio"


class ProgressBar:
    """Progress bar handling for yt-dlp downloads."""

    def __init__(self):
        self.pbar: Optional[tqdm] = None
        self.last_downloaded: int = 0

    def hook(self, d: dict) -> None:
        """Hook function called by yt-dlp during download."""
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
        """Resets the progress bar for the next download."""
        if self.pbar:
            self.pbar.close()
            self.pbar = None
        self.last_downloaded = 0


def check_dependencies() -> bool:
    """Checks whether the required dependencies are available."""
    all_ok = True

    try:
        import yt_dlp
        logging.info(f"yt-dlp version: {yt_dlp.version.__version__}")
    except ImportError:
        print("❌ yt-dlp is not installed!")
        print("   pip install yt-dlp")
        all_ok = False

    if not shutil.which("ffmpeg"):
        print("❌ ffmpeg was not found!")
        print("\n📦 Installation:")
        print("   macOS:    brew install ffmpeg")
        print("   Ubuntu:   sudo apt install ffmpeg")
        print("   Windows:  choco install ffmpeg")
        all_ok = False

    return all_ok


def find_cookie_file() -> Optional[Path]:
    """
    Finds a cookie file in common locations.
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
                        logging.info(f"Found cookie file: {location}")
                        return location
            except Exception as e:
                logging.warning(f"Error reading cookie file {location}: {e}")
                continue

    return None


def validate_cookie_file(cookie_path: Path) -> bool:
    """
    Validates the format of a cookie file.
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
    Validates whether a string is a valid URL.
    """
    url = url.strip()
    if not url:
        return False

    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False


def is_no_formats_error(error_message: str) -> bool:
    """Checks whether the error means there are no formats available at the source."""
    msg = (error_message or "").lower()
    return 'no video formats found' in msg


def print_no_formats_guidance(url: str) -> None:
    """Displays guidance for a no-formats problem on the extractor/service side."""
    print("\n⚠️  The service did not return any supported video formats.")
    print("   This is usually a problem on the yt-dlp extractor side or a change on the service side, not in your script.")
    print(f"   URL: {url}")
    print("\n   What you can do:")
    print("   1) Confirm the version: yt-dlp -U")
    print("   2) If installed via pip: pip install -U yt-dlp")
    print("   3) Report the issue: https://github.com/yt-dlp/yt-dlp/issues?q=")
    print("      (attach the output of: yt-dlp -vU <URL>)")


def get_audio_tracks(url: str, cookie_file: Optional[Path] = None) -> list[dict]:
    """
    Retrieves the list of available audio tracks from a video.
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
                        display_name = 'Audio description'
                    elif 'polski' in format_id.lower():
                        display_name = 'Polish'
                    elif 'english' in format_id.lower() or 'eng' in format_id.lower():
                        display_name = 'English'
                    else:
                        lang_map = {
                            'pl': 'Polish',
                            'en': 'English',
                            'de': 'German',
                            'fr': 'French',
                            'es': 'Spanish',
                            'it': 'Italian',
                            'ru': 'Russian',
                            'uk': 'Ukrainian',
                            'und': 'Undetermined'
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
            logging.info(f"Found {len(audio_tracks)} audio tracks for {url}")
            return audio_tracks

    except Exception as e:
        error_msg = str(e)
        if is_no_formats_error(error_msg):
            logging.warning(
                f"No formats found while detecting audio tracks (most likely an extractor/service issue): {error_msg}"
            )
        else:
            logging.error(f"Error retrieving audio track information: {error_msg}")
        return []


def select_audio_track(audio_tracks: list[dict]) -> Optional[str]:
    """
    Lets the user select an audio track with detailed information.
    """
    if not audio_tracks:
        print("\nℹ️  No audio track information found.")
        print("   The default audio track will be used.\n")
        return None

    print("\n🔊 Available audio tracks:")

    for i, track in enumerate(audio_tracks, 1):
        format_id = track.get('format_id', 'unknown')
        ext = track.get('ext', 'unknown')
        abr = track.get('abr', 0) or 0
        filesize = track.get('filesize', 0)
        lang = track.get('language', 'und')
        lang_name = track.get('language_name', 'Undetermined')
        format_note = track.get('format_note', '')

        if filesize and filesize > 0:
            size_mb = filesize / (1024 * 1024)
            size_str = f"~{size_mb:.2f}MiB"
        else:
            size_str = "?MiB"

        bitrate_str = f"{abr}kbps" if abr > 0 else "?kbps"

        print(f"   {i}. {format_id:20} {ext:4} {size_str:>12} {bitrate_str:>8} [{lang}] {lang_name} {format_note}")

    while True:
        choice = input(f"\n   Choice [1-{len(audio_tracks)}]: ").strip()

        try:
            idx = int(choice)
            if 1 <= idx <= len(audio_tracks):
                selected = audio_tracks[idx - 1]
                print(f"   ✅ Selected: {selected['format_id']} - {selected['language_name']} "
                      f"({selected['ext']}, {selected.get('abr', 0)}kbps)\n")
                logging.info(f"Selected audio track: {selected['format_id']}")
                return selected['format_id']
            else:
                print(f"   ⚠️  Invalid choice. Enter a number from 1 to {len(audio_tracks)}")
        except ValueError:
            print("   ⚠️  Invalid input. Enter a number.")


def download_video(
    url: str,
    output_path: Path,
    quality: Quality = Quality.BEST,
    mode: DownloadMode = DownloadMode.VIDEO,
    cookie_file: Optional[Path] = None,
    audio_format_id: Optional[str] = None
) -> bool:
    """
    Downloads a video from a URL.
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
        logging.info(f"Selected audio format: {audio_format_id}")

    if cookie_file and validate_cookie_file(cookie_file):
        ydl_opts['cookiefile'] = str(cookie_file)
        logging.info(f"Using cookie file: {cookie_file}")

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

    mode_str = "🎵 Audio" if mode == DownloadMode.AUDIO else "🎬 Video"
    print(f"📥 Downloading {mode_str} from: {url}")
    print(f"📂 Output directory: {output_path}")
    print(f"⚙️  Quality: {quality.name}")
    if audio_format_id:
        print(f"🔊 Audio format: {audio_format_id}")
    if cookie_file and validate_cookie_file(cookie_file):
        print(f"🍪 Cookies: {cookie_file.name}")
    print()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Starting download: {url}")
            info = ydl.extract_info(url, download=True)
            if info:
                filename = ydl.prepare_filename(info)
                if mode == DownloadMode.AUDIO or quality == Quality.AUDIO_ONLY:
                    filename = Path(filename).with_suffix('.mp3')
                print(f"\n✅ Saved to: {filename}")
                logging.info(f"Download completed successfully: {filename}")
                return True
    except Exception as e:
        error_msg = str(e)
        if is_no_formats_error(error_msg):
            print_no_formats_guidance(url)
        else:
            print(f"\n❌ Download error: {error_msg}")
        logging.error(f"Download failed for {url}: {error_msg}")
        return False
    finally:
        progress.reset()

    return False


def get_output_directory() -> Path:
    """Gets the output directory from the user, or uses the current directory."""
    current_dir = Path.cwd()

    print(f"📂 Output directory [default: {current_dir}]:")
    user_input = input("   (press Enter to use the current directory): ").strip()

    if user_input:
        path = Path(user_input).expanduser().resolve()
        if not path.exists():
            print(f"⚠️  Directory does not exist: {path}")
            create = input("   Create the directory? (Y/N): ").strip().lower()
            if create not in ['t', 'tak']:
                print("Using the current directory.")
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
    """Downloads multiple videos with their corresponding audio tracks."""
    successful = 0
    failed = 0
    total = len(url_audio_pairs)

    print(f"\n📦 Batch download: {total} URL(s)\n")

    for i, (url, audio_format) in enumerate(url_audio_pairs, 1):
        print(f"\n[{i}/{total}] {'='*50}")
        if download_video(url, output_path, quality, mode, cookie_file, audio_format):
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"📊 Batch completed: ✅ {successful} succeeded, ❌ {failed} failed")
    print(f"{'='*60}")

    return successful, failed


def setup_logging() -> None:
    """Configures logging (once at startup)."""
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
    Settings chosen once (cookies + output directory).
    Returns: (cookie_file, use_cookies, output_path)
    """
    cookie_file = find_cookie_file()
    use_cookies = False

    if cookie_file:
        print(f"\n🍪 Found cookie file: {cookie_file}")
        print("   (Useful for private videos, age-restricted content, members-only content)")
        response = input("   Use this cookie file? (Y/N) [Y]: ").strip().lower()
        use_cookies = response in ['', 't', 'tak']
        if use_cookies:
            logging.info(f"User chose to use the cookie file: {cookie_file}")
        else:
            cookie_file = None
            logging.info("User declined to use the cookie file")
    else:
        print("\nℹ️  No cookie file found (optional - only needed for restricted content)")
        response = input("   Specify a custom path to the cookie file? (Y/N) [N]: ").strip().lower()
        if response in ['t', 'tak']:
            custom_path = input("   Path to cookies.txt: ").strip()
            if custom_path:
                cookie_file = Path(custom_path).expanduser().resolve()
                if not validate_cookie_file(cookie_file):
                    print("   ⚠️  Invalid cookie file format, continuing without cookies")
                    cookie_file = None
                else:
                    print(f"   ✅ Cookie file valid: {cookie_file}")
                    use_cookies = True

    output_path = get_output_directory()
    return cookie_file, use_cookies, output_path


def run_download_round(cookie_file: Optional[Path], use_cookies: bool, output_path: Path) -> int:
    """One download round (collecting URLs and downloading)."""
    print("🔗 Supported: YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter, etc.")
    print("📺 Quality: Always the BEST (video + audio)")
    print("🔊 Audio: Automatic selection of the best track (excluding audio description)")
    print(f"📂 Output directory: {output_path}")
    if cookie_file and use_cookies and validate_cookie_file(cookie_file):
        print(f"🍪 Cookies: {cookie_file}")
    else:
        print("🍪 Cookies: none / disabled")
    print("\n   Enter the URLs (one per line, empty line to finish):\n")

    url_audio_pairs: list[tuple[str, Optional[str]]] = []
    url_count = 0

    while True:
        url_count += 1
        url = input(f"   URL #{url_count}: ").strip()

        if not url:
            if url_audio_pairs:
                break
            else:
                print("   Enter at least one URL")
                url_count -= 1
                continue

        if not validate_url(url):
            print("   ⚠️  Invalid URL, try again...")
            url_count -= 1
            continue

        print("🔍 Checking audio tracks...")
        audio_tracks = get_audio_tracks(url, cookie_file if use_cookies else None)
        audio_format_id = select_audio_track(audio_tracks)

        url_audio_pairs.append((url, audio_format_id))

        print(f"✅ URL #{url_count} added")
        if url_count == 1:
            print("   (press Enter to finish, or enter another URL)\n")

    quality = Quality.BEST
    mode = DownloadMode.VIDEO

    logging.info(f"Starting download: {len(url_audio_pairs)} URL(s), cookies: {use_cookies}, output: {output_path}")

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
    """Main program function (menu after each round)."""
    setup_logging()

    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 21 + "VIDEO DOWNLOAD" + " " * 23 + "║")
    print("║" + " " * 25 + "(yt-dlp)" + " " * 25 + "║")
    print("╚" + "═" * 58 + "╝\n")

    if not check_dependencies():
        return 1

    cookie_file, use_cookies, output_path = setup_session()

    last_rc: int = 0

    while True:
        print()
        last_rc = run_download_round(cookie_file, use_cookies, output_path)

        print("\nWhat's next?")
        print("   1. New download")
        print("   2. Exit")
        print("   3. Change settings (cookies / output directory)")

        choice = input("   Choice [1]: ").strip() or "1"
        if choice == "1":
            continue
        elif choice == "2":
            return last_rc
        elif choice == "3":
            print("\n⚙️  Changing settings...\n")
            cookie_file, use_cookies, output_path = setup_session()
            continue
        else:
            print("   ⚠️  Invalid choice. Enter 1, 2 or 3.\n")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
