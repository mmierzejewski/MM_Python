import os
import re
import shutil
from yt_dlp import YoutubeDL
from tqdm import tqdm


def sanitize_filename(filename, max_length=180):
    filename = re.sub(r'[<>:"/\\|?*\n\r]', '_', filename)
    filename = re.sub(r'\s+', '_', filename.strip())
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {f'COM{i}' for i in range(1, 10)} | {f'LPT{i}' for i in range(1, 10)}
    base = filename.split('_')[0].upper()
    if base in reserved:
        filename = f"{filename}_safe"
    return filename[:max_length]


class ProgressBar:
    def __init__(self):
        self.pbar = None

    def hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)

            if not self.pbar and total_bytes:
                self.pbar = tqdm(total=total_bytes, unit='B', unit_scale=True, desc='Pobieranie', ascii=True)

            if self.pbar:
                self.pbar.n = downloaded
                self.pbar.refresh()

        elif d['status'] == 'finished':
            if self.pbar:
                self.pbar.n = self.pbar.total
                self.pbar.refresh()
                self.pbar.close()
                print("✅ Plik pobrany i zapisany.")


def download_with_progress(url, output_path):
    if not shutil.which("ffmpeg"):
        print("❌ ffmpeg nie znaleziony! Zainstaluj i dodaj do PATH.")
        return

    output_path = os.path.normpath(output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    progress = ProgressBar()

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title).180s.%(ext)s'),
        'progress_hooks': [progress.hook],
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        'cookiefile': '/Users/mmierzejewski/WORK/cookies.txt',  # Updated cookie file path
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"❌ Błąd pobierania: {str(e)}")


def main():
    url = input("🔗 Wklej link do filmu (YT, TikTok, Vimeo, FB itd.): ").strip()
    output_path = input("📂 Folder docelowy [/Users/mmierzejewski/WORK]: ").strip()
    if not output_path:
        output_path = "/Users/mmierzejewski/WORK"
    download_with_progress(url, output_path)


if __name__ == "__main__":
    main()