#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Video Downloader using yt-dlp with cookie support.

Downloads videos from YouTube, TikTok, Vimeo, Facebook and other platforms
using yt-dlp with authentication cookies.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional
from yt_dlp import YoutubeDL
from tqdm import tqdm


class ProgressBar:
    """Progress bar handler for yt-dlp downloads."""

    def __init__(self):
        self.pbar: Optional[tqdm] = None

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
                    ascii=True
                )

            if self.pbar:
                self.pbar.n = downloaded
                self.pbar.refresh()

        elif d['status'] == 'finished':
            if self.pbar:
                self.pbar.n = self.pbar.total
                self.pbar.refresh()
                self.pbar.close()
                self.pbar = None
                print("✅ Download completed")

    def reset(self) -> None:
        """Reset progress bar for next download."""
        if self.pbar:
            self.pbar.close()
            self.pbar = None


def find_cookie_file() -> Optional[Path]:
    """
    Find cookie file in common locations.

    Returns:
        Path to cookie file or None if not found
    """
    possible_locations = [
        Path.home() / 'cookies.txt',
        Path.home() / 'WORK' / 'cookies.txt',
        Path.cwd() / 'cookies.txt',
        Path(__file__).parent / 'cookies.txt',
    ]

    for location in possible_locations:
        if location.exists():
            return location

    return None


def check_dependencies() -> bool:
    """Check if required dependencies are available."""
    if not shutil.which("ffmpeg"):
        print("❌ ffmpeg not found!")
        print("   Install: brew install ffmpeg  (macOS)")
        print("           apt install ffmpeg   (Ubuntu)")
        print("           choco install ffmpeg (Windows)")
        return False
    return True


def validate_url(url: str) -> bool:
    """Basic URL validation."""
    url = url.strip()
    if not url:
        return False

    valid_schemes = ['http://', 'https://', 'www.']
    return any(url.startswith(scheme) for scheme in valid_schemes)


def download_video(url: str, output_path: Path, cookie_file: Optional[Path] = None) -> bool:
    """
    Download video from URL.

    Args:
        url: Video URL
        output_path: Output directory
        cookie_file: Optional path to cookies.txt file

    Returns:
        True if successful, False otherwise
    """
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    progress = ProgressBar()

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(output_path / '%(title).180s.%(ext)s'),
        'progress_hooks': [progress.hook],
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
    }

    # Add cookie file if available
    if cookie_file and cookie_file.exists():
        ydl_opts['cookiefile'] = str(cookie_file)
        print(f"🍪 Using cookies from: {cookie_file}")
    else:
        print("⚠️  No cookie file found - some videos may not be accessible")

    print(f"📥 Starting download from: {url}")
    print(f"📂 Output directory: {output_path}\n")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                filename = ydl.prepare_filename(info)
                print(f"\n✅ Saved to: {filename}")
                return True
    except Exception as e:
        print(f"\n❌ Download error: {str(e)}")
        return False
    finally:
        progress.reset()

    return False


def get_output_directory() -> Path:
    """Get output directory from user or use default."""
    default_path = Path.home() / 'Downloads' / 'yt-dlp'

    print(f"📂 Output directory [default: {default_path}]:")
    user_input = input("   (press Enter for default): ").strip()

    if user_input:
        return Path(user_input).expanduser().resolve()

    return default_path


def main():
    """Main function."""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "VIDEO DOWNLOADER" + " " * 27 + "║")
    print("║" + " " * 17 + "(yt-dlp)" + " " * 32 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # Check dependencies
    if not check_dependencies():
        return 1

    # Find cookie file
    cookie_file = find_cookie_file()

    # Get URL
    print("🔗 Supported: YouTube, TikTok, Vimeo, Facebook, Instagram, etc.")
    url = input("   Video URL: ").strip()

    if not validate_url(url):
        print("❌ Invalid URL!")
        return 1

    # Get output directory
    output_path = get_output_directory()

    # Download
    print()
    success = download_video(url, output_path, cookie_file)

    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)