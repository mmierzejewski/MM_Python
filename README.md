# MM Python

A collection of advanced Python scripts with full documentation and professional organization.

## 📚 Projects

### [BMI Calculator](BMI/)

**Advanced BMI calculator** with health recommendations.

**Features:**

- 👥 Gender-aware calculation (different norms for M/F)
- 🎯 Accurate target weight calculation
- 💾 Export results to file
- 📝 Session logging
- 🔄 Multiple calculations
- 🛡️ Full error handling

```bash
cd BMI && python BMI.py
```

---

### 🔢 [Fibonacci Calculator](Fibonacci/)

**Advanced tools for the Fibonacci sequence** with multiple algorithms.

**Features:**

- ⚡ O(log n) matrix algorithm for large numbers
- 📊 7 different calculation modes
- 🔄 **Menu loop** - continuous operation without restarting the program ⭐ NEW!
- 🚪 "Exit" option - clean program exit
- 🎯 Sequence membership test
- 📈 Convergence analysis toward the golden ratio φ
- 🔢 Support for very large numbers
- 🎨 Interactive menu (8 options)
- 📋 **Option to display all n numbers** (10 per line) or just the first/last 10
- 💾 Export sequences to file with timestamp

```bash
cd Fibonacci && python FibonacciUtils.py
```

---

### 🐴 [Knight's Tour Problem](Horse/)

**Knight's tour solver** using the Warnsdorff heuristic.

**Features:**

- ♟️ Warnsdorff heuristic (smart optimization)
- 🔄 Backtracking with timeout protection
- 🔄 **Menu loop** - continuous operation without restarting the program ⭐ NEW!
- 🚪 "Exit" option - clean program exit
- 📊 Detailed statistics (time, backtracks, depth)
- 💾 Export solutions to file
- 📝 Logging of all operations
- 🎯 Board visualization with Unicode
- ⏱️ Progress tracking for large boards

```bash
cd Horse && python Horse.py
```

---

### 🔺 [Pythagorean Triples Generator](PITAGORAS/)

**Generator of primitive Pythagorean triples** with prime number analysis.

**Features:**

- ✅ Primitive triples only (eliminates duplicates like 3,4,5 and 6,8,10)
- 🔄 **Menu loop** - continuous operation without restarting the program ⭐ NEW!
- 🚪 "Exit" option - clean program exit
- 📊 Dimensions, perimeter, area
- 🔢 Prime number detection
- 📈 Detailed statistics
- ⚡ Fast Euclid's algorithm

```bash
cd PITAGORAS && python Pitagoras.py
```

---

### 📐 [3D Triangle Visualizer](TRIANGLE/)

**Advanced 3D triangle visualizer** with full geometric validation.

**Features:**

- ✅ **Geometric validation** - checks for identical points and collinearity
- 📏 Calculates the length of all sides
- 📐 **Surface area calculation** - uses the cross product
- 🎨 **Professional 3D visualization**:
  - Filled triangle with transparency
  - Marked vertices and edges
  - Labels with side lengths
  - Point (0,0,0) always visible as reference
- 💾 **Automatic PNG export** in the script directory
- 📊 Detailed statistics (coordinates, lengths, area)
- 📈 **Interactive plot** - rotate, zoom, pan
- 🔢 **Type hints** - full type annotations
- 🛡️ Full error handling and input validation

```bash
cd TRIANGLE && python triangle_3d.py
```

---

### 🔢 [Prime Numbers Generator](PNA/)

**Efficient prime number generator** using the Sieve of Eratosthenes.

**Features:**

- 🎯 **Four modes**:
  - Primes up to a limit
  - First n prime numbers
  - **Single number check** ⭐ NEW!
  - **Exit** - quit the program
- ⚡ Memory optimization (segmented sieve)
- 🧮 Automatic limit estimation for the first n primes
- ✅ Fast primality test O(√n)
- 🔢 **Displays proper divisors** (excluding 1 and the number itself) for non-prime numbers ⭐ NEW!
- 🔄 **Menu loop** - continuous operation without restarting the program ⭐ NEW!
- 📊 Detailed statistics for all modes
- 💾 Save to file
- 📈 Progress bar for large ranges
- ⏱️ Performance measurement (μs, ms, s)

```bash
cd PNA && python PNA.py
```

---

### 🚴 [Bike Service Proxy](Courses/BIKE/)

**Proxy for the rowermevo.pl bike rental service** with location and battery monitoring.

**Features:**

- 📍 Real-time bike location retrieval
- 🔋 Battery level monitoring
- 🗺️ Data from the rowermevo.pl API
- 💾 CSV export
- 🌐 Integration with requests
- 📊 Bike station data analysis

```bash
cd Courses/BIKE && python bike_service_proxy.py
```

---

### 📚 [Python Course](Courses/python-course-master/)

**Comprehensive Python course** with interactive Jupyter notebooks and Docker.

**Features:**

- 🐳 Docker environment (easy setup)
- 📓 Jupyter Notebooks (interactive learning)
- 📖 Training materials
- 🎯 Practical examples
- 💻 Ready-to-use development environment

```bash
cd Courses/python-course-master && docker-compose up
```

---

### 🎬 [Video Downloader (YT-DLP)](YT-DLP/)

**Universal video downloader** supporting 1000+ sites with advanced audio track selection.

**Features:**

- 🍪 Cookie support (private/members-only content)
- 🎬 Always the best video quality (automatic)
- 🔊 **Advanced audio track selection** - detailed technical parameters:
  - Format ID (f6-a1-x3, f7-a2-x3)
  - Bitrate (kbps), file size, language
  - Track type (DASH, HLS)
  - Automatic audio-description filtering
- 📦 Batch download with individual audio selection per URL
- 📈 Real-time progress bar with tqdm
- 🔄 Automatic format conversion (ffmpeg)
- 📝 Logging of all operations to a file
- ✅ Full URL and cookie file validation
- 🛡️ Comprehensive error handling

**Audio selection example:**

```text
🔊 Available audio tracks:
   1. f7-a2-x3   m4a   ~42.07MiB   132kbps [pl] Polish (DASH)
   2. f6-a1-x3   m4a   ~41.76MiB   131kbps [pl] Polish (DASH)
   Choice [1-2]: 1
```

```bash
cd YT-DLP && python yt-dlp.py
```

---

### 🧹 [macOS Clear Cache](MacOSClearCache/)

**Cache, log, and temporary file cleaner** for macOS with category-based selection and dry-run preview.

**Features:**

- 🗂️ 12 cleanup categories (system, browsers, apps, developer, package managers, logs, and more)
- 👁️ Dry-run mode to preview what would be removed
- 🧭 Automatic browser profile discovery (Chrome, Edge, Brave)
- 📅 Age-based filtering (`--older-than`)
- 🗑️ Optional move-to-Trash instead of permanent deletion
- 🧾 JSON run log and macOS notifications
- ⏰ Scheduled daily cleanup via `launchd`
- 🔄 Post-clean system reindexing (Spotlight, DNS, Launch Services, Homebrew, Docker…)

```bash
cd MacOSClearCache && python3 clear_caches.py --dry-run
```

---

### 🌊 [Torrent Downloader](Torrent/)

**Torrent downloader** driven by `aria2`/`aria2p`, supporting magnet links and `.torrent` files.

**Features:**

- 🔗 Magnet link and `.torrent` file support
- 📦 Batch downloads from a text file list
- 🎮 Interactive mode
- 📝 Logging of all download operations
- ⚙️ Built on `aria2` for fast, resumable downloads

```bash
cd Torrent && python torrent_downloader.py "magnet:?xt=urn:btih:..."
```

---

## 🛠️ Requirements

- Python 3.10+
- Standard library (most projects)
- Specific dependencies in `requirements.txt` for each project
- **ffmpeg** (required for YT-DLP - video format conversion)
- **Docker** (optional for python-course-master)

## 📖 Documentation

Each project has its own `README.md` with:

- A detailed description of its features
- Usage examples
- Installation instructions
- Troubleshooting

## 🚀 Quick Start

```bash

# Clone the repository

git clone https://github.com/mmierzejewski/MM_Python.git
cd MM_Python

# Pick a project and run it (example - prime number generator)

cd PNA
python PNA.py

# Example - Fibonacci

cd Fibonacci
python FibonacciUtils.py
```

## 📁 Structure

```text
MM_Python/
├── .gitignore              # Ignored files (logs, exports, venv)
├── README.md               # Main documentation
│
├── BMI/                    # BMI calculator with recommendations
│   ├── BMI.py
│   └── README.md
│
├── Fibonacci/              # Fibonacci calculator (8 options + menu loop)
│   ├── FibonacciUtils.py
│   └── README.md
│
├── Horse/                  # Knight's Tour Problem (Warnsdorff + menu loop)
│   ├── Horse.py
│   └── README.md
│
├── PITAGORAS/              # Pythagorean triples generator (menu loop)
│   ├── Pitagoras.py
│   └── README.md
│
├── PNA/                    # Prime numbers (Sieve of Eratosthenes + menu loop)
│   ├── PNA.py
│   └── README.md
│
├── TRIANGLE/               # 3D triangle visualizer (validation + area)
│   ├── triangle_3d.py
│   ├── triangle_3d.png
│   ├── requirements.txt
│   └── README.md
│
├── Courses/                # Educational projects and courses
│   ├── BIKE/              # Proxy for rowermevo.pl (bike locations)
│   │   ├── bike_service_proxy.py
│   │   ├── locations.csv
│   │   └── requirements.txt
│   │
│   └── python-course-master/  # Python course (Docker + Jupyter)
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── requirements.txt
│       ├── README.md
│       ├── part_1/        # Python basics
│       ├── part_2/        # Advanced topics
│       └── workshops/     # Practical exercises
│
├── YT-DLP/                 # Universal video downloader (audio track selection)
│   ├── yt-dlp.py
│   ├── cookies.txt.example
│   ├── README.md
│   └── requirements.txt
│
├── MacOSClearCache/         # macOS cache/log/temp file cleaner (dry-run, scheduling)
│   ├── clear_caches.py
│   └── README.md
│
└── Torrent/                 # Torrent downloader (aria2/aria2p, magnet + .torrent)
    ├── torrent_downloader.py
    ├── requirements.txt
    └── README.md
```

## 🎯 Common Features of the Main Projects

All the main scripts (PNA, Fibonacci, Horse, PITAGORAS) have been unified and offer:

- 🔄 **Menu loop** - run in continuous mode without needing to restart
- 🚪 **"Exit" option** - clean program exit
- 🎨 **Interactive interface** - friendly menu with numbered options
- 📊 **Detailed statistics** - full analysis of results
- 💾 **Export to file** - ability to save results
- ⏱️ **Performance measurement** - precise timing of operations
- 🛡️ **Error handling** - input validation and exception catching

## 🤝 Contact

- GitHub: [@mmierzejewski](https://github.com/mmierzejewski)
- Repository: [MM_Python](https://github.com/mmierzejewski/MM_Python)

## 📄 License

Free to use and modify.

---

**💡 Tip:** Every script includes full input validation, error handling, and a friendly emoji-based user interface!
