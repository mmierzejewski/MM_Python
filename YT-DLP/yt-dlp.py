#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Video Downloader using yt-dlp.

Simple video downloader supporting YouTube, TikTok, Vimeo, Facebook, and more.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from yt_dlp import YoutubeDL
from tqdm import tqdm


MAX_FILENAME_LENGTH = 180


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
                    ascii=True,
                    ncols=80
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

    def reset(self) -> None:
        """Reset progress bar for next download."""
        if self.pbar:
            self.pbar.close()
            self.pbar = None


def check_dependencies() -> bool:
    """Check if required dependencies are available."""
    if not shutil.which("ffmpeg"):
        print("❌ ffmpeg not found!")
        print("\n📦 Installation:")
        print("   macOS:    brew install ffmpeg")
        print("   Ubuntu:   sudo apt install ffmpeg")
        print("   Windows:  choco install ffmpeg")
        return False
    return True


def validate_url(url: str) -> bool:
    """
    Validate if string is a proper URL.

    Args:
        url: URL string to validate

    Returns:
        True if valid URL, False otherwise
    """
    url = url.strip()
    if not url:
        return False

    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False


def download_video(url: str, output_path: Path) -> bool:
    """
    Download video from URL.

    Args:
        url: Video URL
        output_path: Output directory

    Returns:
        True if successful, False otherwise
    """
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    progress = ProgressBar()

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(output_path / f'%(title).{MAX_FILENAME_LENGTH}s.%(ext)s'),
        'progress_hooks': [progress.hook],
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
    }

    print(f"📥 Downloading from: {url}")
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
    """Get output directory from user or use current directory."""
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


def main() -> int:
    """Main function."""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "VIDEO DOWNLOADER" + " " * 27 + "║")
    print("║" + " " * 17 + "(yt-dlp)" + " " * 32 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # Check dependencies
    if not check_dependencies():
        return 1

    # Get URL
    print("🔗 Supported: YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter, etc.")
    url = input("   Video URL: ").strip()

    if not validate_url(url):
        print("❌ Invalid URL format!")
        return 1

    # Get output directory
    output_path = get_output_directory()

    # Download
    print()
    success = download_video(url, output_path)

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