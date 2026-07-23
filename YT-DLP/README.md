# 🎬 Universal Video Downloader

Universal video downloader using yt-dlp, supporting YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter and over 1000 other sites.

## ✨ Features

- 📥 Download videos from over 1000 websites
- 🍪 **Cookie authorization support** (private/members-only content)
- 🎵 Audio-only mode (MP3 extraction)
- 🔊 **Advanced audio track selection** with detailed technical information
- 📋 Display all available audio tracks (format_id, bitrate, size, language)
- 🎯 Automatic audio description filtering
- 📊 Always the best video quality (automatic)
- 📦 Batch download with individual audio selection for each URL
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

Or download from: <https://ffmpeg.org/download.html>

## 💻 Usage

### Basic usage

```bash
python yt-dlp.py
```

### Interactive prompts

1. **Cookie file (optional):** Automatically detected, or provide your own path
2. **Enter URL(s):** Paste video URLs (one per line, empty line to finish)
3. **Audio track selection:** For each URL, the program will detect and display the available audio tracks with their parameters:
   - Format ID (e.g. f6-a1-x3, f7-a2-x3)
   - Extension (m4a, m3u8)
   - File size
   - Bitrate (kbps)
   - Language
   - Type (DASH audio, HLS, etc.)
   - Audio description marker (if present)
4. **Output directory:** Choose where to save the files

**Note:** Video quality is always set to the BEST - there is no option to choose a lower quality.

### Downloading a single video

```bash
python yt-dlp.py

# Enter URL: https://www.youtube.com/watch?v=example

# Press Enter (finish)

# Choose quality: 1

# Press Enter (current directory)

```

### Batch download

```bash
python yt-dlp.py

# Enter multiple URLs

# URL: https://www.youtube.com/watch?v=video1

# URL: https://www.youtube.com/watch?v=video2

# URL: https://www.youtube.com/watch?v=video3

# URL: [press Enter]

# Choose quality: 2

```

### Selecting a specific audio track

```bash
python yt-dlp.py

# Enter URL: https://vod.tvp.pl/seriale/...

# 

# 🔊 Available audio tracks

# 1. f7-a2-x3            m4a   ~42.07MiB  132kbps [pl] Polish (DASH) DASH audio

# 2. f6-a1-x3            m4a   ~41.76MiB  131kbps [pl] Polish (DASH) DASH audio

# 3. audio0-Polski       m3u8      ?MiB    ?kbps [pl] Polish HLS

#

# Choice [1-3]: 1

# ✅ Selected: f7-a2-x3 - Polish (DASH) (m4a, 132kbps)

```

**Audio selection features:**

- Automatic detection of all available audio tracks
- Detailed technical parameters (format_id, bitrate, size)
- Audio description filtering (not displayed automatically)
- Individual selection for each URL in batch mode
- Sorted by bitrate (best at the top)

### Batch download with different audio tracks

```bash
python yt-dlp.py

# URL #1: https://vod.tvp.pl/video1

# [select audio track for video1]

# URL #2: https://vod.tvp.pl/video2

# [select audio track for video2]

# URL #3: [Enter - finish]

# Output directory: ./downloaded

```

### Using cookies for private/restricted content

#### What are cookies used for?

- Private videos
- Age-restricted content
- Members-only content (YouTube memberships, Patreon, etc.)
- Channel-restricted videos
- Regionally blocked content (with VPN)

#### How to export cookies

##### Method 1: Browser extension (Recommended)

1. Install the extension:
   - Chrome/Edge: [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid)
   - Firefox: [cookies.txt](https://addons.mozilla.org/firefox/addon/cookies-txt/)
2. Go to the site (e.g. YouTube)
3. Log in to your account
4. Click the extension icon → Export cookies
5. Save as `cookies.txt`

##### Method 2: Built-in yt-dlp feature

```bash
yt-dlp --cookies-from-browser chrome
```

#### Cookie file locations (auto-detected)

- Current directory: `./cookies.txt`
- Script directory: `/path/to/script/cookies.txt`
- Home directory: `~/cookies.txt`
- Working directory: `~/WORK/cookies.txt`
- Downloads: `~/Downloads/cookies.txt`

#### Example with cookies

```bash

# Place cookies.txt in one of the auto-detected locations

python yt-dlp.py

# Found cookie file: cookies.txt

# Use this cookie file? yes

# Enter URL: https://www.youtube.com/watch?v=private_video

```

## 📊 Supported Sites

YouTube, TikTok, Vimeo, Facebook, Instagram, Twitter, Twitch, Dailymotion, Reddit and over 1000 others!

Full list: <https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md>

## 📝 Logging

All downloads are logged to `yt-dlp-downloader.log` in the current directory.

Enable debug mode:

```bash
DEBUG=1 python yt-dlp.py
```

## 🔧 Quality and Audio Tracks

### Video quality

The script **always uses the best available video quality** (bestvideo+bestaudio). There is no option to choose a lower quality - this ensures the maximum quality of downloaded videos.

### Audio tracks

For each URL the script:

1. **Detects** all available audio tracks
2. **Displays** technical details:
   - `format_id` - format identifier (e.g. f6-a1-x3)
   - `ext` - extension (m4a, m3u8)
   - `size` - file size (if available)
   - `bitrate` - audio quality in kbps
   - `language` - language code [pl], [en], etc.
   - `type` - technology (DASH audio, HLS, etc.)
3. **Filters** audio description (does not display these tracks)
4. **Sorts** by bitrate (best quality at the top)

The user selects a specific audio track for each video.

### Example of track display

```text
🔊 Available audio tracks:
   1. f7-a2-x3            m4a   ~42.07MiB   132kbps [pl] Polish (DASH) DASH audio
   2. f6-a1-x3            m4a   ~41.76MiB   131kbps [pl] Polish (DASH) DASH audio
   3. audio0-Polski       m3u8      ?MiB     ?kbps [pl] Polish HLS
```

## 🛠️ Troubleshooting

### "ffmpeg not found"

Install ffmpeg using the instructions above.

### "Import error: yt_dlp"

```bash
pip install yt-dlp tqdm
```

### "Download error: HTTP Error 403" or "Private video"

The video requires authentication. Solutions:

1. Export cookies from your browser (see the "Using cookies" section)
2. Place `cookies.txt` in the script directory
3. Run the script and confirm using cookies
4. Make sure you are logged in on the site while exporting cookies

### The cookie file doesn't work

- Check that the file is in Netscape format (starts with `# Netscape HTTP Cookie File`)
- Make sure the cookies are fresh (not expired)
- Export the cookies again after logging in
- Check the file encoding (should be UTF-8)
- Make sure there are no extra spaces or formatting errors

### "Invalid cookie file format"

The cookie file must be in Netscape format. Use the browser extensions mentioned above, or:

```bash

# Export from browser using yt-dlp

yt-dlp --cookies-from-browser firefox --cookies cookies.txt "https://youtube.com"
```

### Long filenames

Filenames are automatically shortened to 180 characters for compatibility.

### Audio track doesn't download correctly

If the selected audio track (e.g. f6-a1-x3) downloads the wrong audio:

1. Check all available tracks - sometimes the format_id can be misleading
2. Try a different track from the list (preferably the one with the highest bitrate)
3. Some sites may require cookies for full access to audio tracks
4. DASH format (m4a) is usually more reliable than HLS (m3u8)

## 📄 License

Free to use and modify.

## 🤝 Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The best video downloader
- [tqdm](https://github.com/tqdm/tqdm) - Progress bar library
