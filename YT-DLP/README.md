# 🎬 Universal Video Downloader

Universal video downloader using yt-dlp supporting YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter, and 1000+ other sites.

## ✨ Features

- 📥 Download videos from 1000+ websites
- 🍪 **Cookie authentication support** (private/member-only content)
- 🎵 Audio-only mode (MP3 extraction)
- 📊 Multiple quality options (Best, 1080p, 720p, 480p)
- 📦 Batch download support (multiple URLs)
- 📈 Real-time progress bar
- 🔄 Automatic format conversion
- 📝 Logging to file
- ✅ Input validation
- 🛡️ Error handling

## 📋 Requirements

- Python 3.8+
- ffmpeg (required for format conversion)

## 🚀 Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install yt-dlp tqdm
```

### 2. Install ffmpeg

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

Or download from: https://ffmpeg.org/download.html

## 💻 Usage

### Basic usage

```bash
python yt-dlp.py
```

### Interactive prompts

1. **Cookie file (optional):** Automatically detected or specify custom path
2. **Enter URL(s):** Paste video URLs (one per line, empty line to finish)
3. **Select quality:**
   - 1: Best (highest available)
   - 2: High (1080p)
   - 3: Medium (720p)
   - 4: Low (480p)
   - 5: Audio only (MP3)
4. **Output directory:** Choose where to save files

### Single video download

```bash
python yt-dlp.py
# Enter URL: https://www.youtube.com/watch?v=example
# Press Enter (finish)
# Select quality: 1
# Press Enter (current directory)
```

### Batch download

```bash
python yt-dlp.py
# Enter multiple URLs:
# URL: https://www.youtube.com/watch?v=video1
# URL: https://www.youtube.com/watch?v=video2
# URL: https://www.youtube.com/watch?v=video3
# URL: [press Enter]
# Select quality: 2
```
### Audio-only download (MP3)

```bash
python yt-dlp.py
# Cookie file: [no/skip]
# Enter URL: https://www.youtube.com/watch?v=music
# Press Enter
# Select quality: 5 (Audio only)
```

### Using cookies for private/restricted content

#### What are cookies used for?
- Private videos
- Age-restricted content
- Member-only content (YouTube memberships, Patreon, etc.)
- Channel-specific restricted videos
- Region-locked content (with VPN)

#### How to export cookies:

**Method 1: Browser extension (Recommended)**
1. Install extension:
   - Chrome/Edge: [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid)
   - Firefox: [cookies.txt](https://addons.mozilla.org/firefox/addon/cookies-txt/)
2. Navigate to the website (e.g., YouTube)
3. Log in to your account
4. Click extension icon → Export cookies
5. Save as `cookies.txt`

**Method 2: yt-dlp built-in**
```bash
yt-dlp --cookies-from-browser chrome
```

#### Cookie file locations (auto-detected):
- Current directory: `./cookies.txt`
- Script directory: `/path/to/script/cookies.txt`
- Home directory: `~/cookies.txt`
- Work directory: `~/WORK/cookies.txt`
- Downloads: `~/Downloads/cookies.txt`

#### Example with cookies:

```bash
# Place cookies.txt in one of the auto-detected locations
python yt-dlp.py
# Cookie file found: cookies.txt
# Use this cookie file? yes
# Enter URL: https://www.youtube.com/watch?v=private_video
```elect quality: 5 (Audio only)
```

## 📊 Supported Sites

YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter, Twitch, Dailymotion, Reddit, and 1000+ more!

Full list: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## 📝 Logging

All downloads are logged to `yt-dlp-downloader.log` in the current directory.

Enable debug mode:
```bash
DEBUG=1 python yt-dlp.py
```

## 🔧 Quality Options

| Option | Description | Resolution |
|--------|-------------|------------|
| Best | Highest quality available | Any |
| High | HD quality | 1080p |
| Medium | Good quality | 720p |
| Low | Lower quality, smaller file | 480p |
| Audio Only | MP3 audio extraction | N/A |

## 🛠️ Troubleshooting

### "ffmpeg not found"
Install ffmpeg using the instructions above.

### "Import error: yt_dlp"
```bash
pip install yt-dlp tqdm
```

### "Download error: HTTP Error 403" or "Private video"
The video requires authentication. Solutions:
1. Export cookies from your browser (see "Using cookies" section)
2. Place `cookies.txt` in the script directory
3. Run script and confirm cookie usage
4. Make sure you're logged in to the website when exporting cookies

### Cookie file not working
- Verify file is in Netscape format (starts with `# Netscape HTTP Cookie File`)
- Make sure cookies are fresh (not expired)
- Re-export cookies after logging in again
- Check file encoding is UTF-8
- Ensure no extra spaces or formatting issues

### "Invalid cookie file format"
The cookie file must be in Netscape format. Use browser extensions listed above or:
```bash
# Export from browser using yt-dlp
yt-dlp --cookies-from-browser firefox --cookies cookies.txt "https://youtube.com"
```

### Long filenames
Filenames are automatically truncated to 180 characters for compatibility.

## 📄 License

Free to use and modify.

## 🤝 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The best video downloader
- [tqdm](https://github.com/tqdm/tqdm) - Progress bar library
