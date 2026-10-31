# macOS Clear Cache

A single-file Python script that safely cleans up cache and log files on
macOS, with per-category selection, dry-run preview, and optional post-clean
system reindexing.

## Features

- **Category-based targets** – dozens of well-known cache/log locations grouped
  into 13 categories: `system`, `trash`, `browsers`, `apps`, `mail`,
  `ios_backups`, `quicklook`, `crashreports`, `developer`, `packages`,
  `logs`, `stale`, `maintenance`.
- **Safe by default** – only a curated subset of low-risk categories runs
  unless you opt in with `--all` or `--categories`.
- **Dry-run mode** – preview exactly what would be removed before deleting
  anything.
- **Force-close running applications** – force-quits known target
  applications whose caches are cleaned (browsers, Slack, Spotify, etc.) so
  that cache files are unlocked and not immediately recreated. Other apps,
  terminals, shells, and host IDEs are never closed. Each PID is re-checked
  against the same app name and bundle ID right before signalling, which
  greatly reduces (but cannot fully eliminate) the risk of signalling a PID
  reused after confirmation. Scheduled
  runs never close applications.
- **Automatic deduplication** – if an enabled target is nested inside another
  enabled target (e.g. `~/Library/Caches/pip` under `~/Library/Caches`), the
  child is skipped to avoid double counting/deletion.
- **Browser profile discovery** – automatically finds per-profile `Cache`,
  `Code Cache`, and `Service Worker/CacheStorage` folders for Chrome, Edge,
  and Brave under `Application Support`.
- **Additional app cache discovery** – finds conventional Chromium caches
  under `Application Support` and `Library/Containers` cache folders for
  third-party sandboxed apps. Persistent stores such as `blob_storage`,
  Service Worker storage, and Drive content caches are excluded, and large
  private folders such as `MobileSync` are not scanned.
- **Age filtering** – `--older-than DAYS` removes a directory only when every
  item in its tree is older than the threshold. If any item is newer or its
  age cannot be checked, the whole top-level item is skipped.
- **Move to Trash option** – `--to-trash` moves items to `~/.Trash` instead of
  permanently deleting them.
- **Interactive mode** – `--interactive` asks for per-category confirmation.
- **External target config** – add extra paths without editing the script via
  a `targets.json` file (see [Custom targets](#custom-targets)).
- **JSON run log** – a summary of each run is written to
  `~/Library/Logs/clear_caches/` unless `--no-log` is passed.
- **macOS notification** – a notification is shown on completion unless
  `--no-notify` is passed.
- **Disk space report** – shows free space before/after an actual (non
  dry-run) cleanup.
- **Single-pass scanning** – each target is scanned once, concurrently, to
  compute sizes and age eligibility; the resulting plan is reused for
  cleaning. With `--older-than`, the estimate only counts eligible items.
- **Scheduling** – `--install-schedule HH:MM` installs (or reinstalls) a
  `launchd` agent via `launchctl bootstrap` to run the cleanup daily;
  `--uninstall-schedule` removes it.
- **System reindexing** – optionally runs DNS cache flush, Launch Services,
  QuickLook, Dock, and Finder maintenance tasks with `--reindex` (off by
  default).
- **No sudo required** – everything runs as the logged-in user; the script
  refuses to run as root.

## Requirements

- Python 3.10+ (uses `from __future__ import annotations` and
  `Path.is_relative_to`)
- macOS.
- No third-party dependencies — standard library only.

## Usage

```bash
python3 clear_caches.py [OPTIONS]
```

### Standalone macOS executable

Build a single-file command-line executable with PyInstaller:

```bash
python3 -m pip install pyinstaller
python3 -m PyInstaller --clean clear_caches.spec
./dist/clear_caches --dry-run
```

The executable runs without a separately installed Python. A `targets.json`
beside the executable and `~/.config/clear_caches/targets.json` are both
supported. Scheduled runs use the executable directly.

Rebuild the executable after every change to `clear_caches.py`; otherwise
`dist/clear_caches` keeps running the old code.

### Common examples

```bash
# Preview what the default (safe) categories would remove
python3 clear_caches.py --dry-run

# Actually clean the default categories, skipping the confirmation prompt
python3 clear_caches.py --yes

# Clean everything, including developer tools and package manager caches
python3 clear_caches.py --all

# Clean only specific categories
python3 clear_caches.py --categories browsers packages

# Clean all categories except iOS backups
python3 clear_caches.py --all --exclude ios_backups

# Remove stale leftovers and run Homebrew cleanup/autoremove (preview first)
python3 clear_caches.py --categories stale maintenance --dry-run

# Clean caches without closing running applications
python3 clear_caches.py --no-kill-apps

# Only remove items untouched for at least 30 days, moving them to Trash
python3 clear_caches.py --older-than 30 --to-trash

# Ask for confirmation before each category is cleaned
python3 clear_caches.py --interactive

# Install a daily 03:00 scheduled run (default categories, no reindex, no app closing)
python3 clear_caches.py --install-schedule 03:00

# Remove the scheduled run
python3 clear_caches.py --uninstall-schedule
```

### CLI options

| Option | Description |
| --- | --- |
| `--dry-run` | Show what would be removed without deleting anything. |
| `--yes` | Skip the confirmation prompt. |
| `--all` | Enable all categories. |
| `--categories CAT [CAT ...]` | Space-separated list of categories to clean (default: `apps browsers crashreports quicklook system`). |
| `--exclude CAT [CAT ...]` | Space-separated list of categories to exclude. |
| `--reindex` | Run DNS/Launch Services/QuickLook/Dock/Finder maintenance after cleaning. |
| `--no-reindex` | Keep the default of skipping reindexing (useful in scripts). |
| `--older-than DAYS` | Only remove top-level items whose complete tree is older than `DAYS` (a non-negative number); newer or unverifiable trees are skipped. |
| `--to-trash` | Move items to `~/.Trash` instead of permanently deleting them. |
| `--interactive` | Ask for confirmation before cleaning each category. |
| `--no-kill-apps` | Do not force-quit running applications before cleaning caches. |
| `--no-log` | Do not write a JSON summary log. |
| `--no-notify` | Do not send a macOS notification when done. |
| `--install-schedule HH:MM` | Install a `launchd` agent to run this script daily at the given time. |
| `--uninstall-schedule` | Remove the previously installed `launchd` agent. |

## Categories

| Category | Description | Enabled by default |
| --- | --- | --- |
| `system` | Generic OS-level caches (`~/Library/Caches`, `~/.cache`) | ✓ |
| `trash` | Trash (`~/.Trash`) | – |
| `browsers` | Web browser caches (Chrome, Firefox, Safari, Edge, Brave, Opera, Vivaldi, Arc) | ✓ |
| `apps` | Popular app caches (Slack, Spotify, Teams, Discord, Steam, WhatsApp, Telegram, Foxit updater downloads) | ✓ |
| `quicklook` | QuickLook thumbnail cache | ✓ |
| `crashreports` | Crash & diagnostic reports | ✓ |
| `mail` | Mail.app cache | – |
| `ios_backups` | iOS/iPadOS backups (MobileSync) ⚠ large & destructive | – |
| `developer` | Xcode/CoreSimulator artefacts, VS Code caches, JetBrains caches (re-generatable) | – |
| `packages` | Package-manager caches: npm, Yarn, pnpm, Gradle, pip, Poetry, Cargo, CocoaPods, Composer, uv, Gem, Bundler, Go modules, Maven, Homebrew, virtualenv (re-downloadable) | – |
| `logs` | JetBrains IDE logs | – |
| `stale` | Leftovers removed as whole items: old per-version JetBrains IDE settings (newest per product is kept) and broken symlinks in `/opt/homebrew/bin` | – |
| `maintenance` | Runs `brew autoremove` and `brew cleanup --prune=all -s` (Homebrew's own dry-run with `--dry-run`) | – |

## Custom targets

Extra cleanup targets can be added without touching the script by creating a
JSON file at either:

- `targets.json` next to `clear_caches.py`, or
- `~/.config/clear_caches/targets.json`

Each entry needs a `path`, `label`, and `category` (existing category names
from the Categories table must be used; custom category names are not supported):

```json
[
  {
    "path": "~/Library/Caches/MyApp",
    "label": "MyApp Cache",
    "category": "apps"
  }
]
```

## Logs

Unless `--no-log` is passed, each run writes a JSON summary to
`~/Library/Logs/clear_caches/clear_caches_<timestamp>.json` containing the
timestamp, dry-run/to-trash flags, total entries/bytes reclaimed, and a
per-category breakdown.

## Safety notes

- Some targets (`~/Library/Containers/com.apple.mail/...`,
  `~/Library/Application Support/MobileSync/Backup`, `~/.Trash`) require
  granting **Full Disk Access** to your terminal/IDE in **System Settings →
  Privacy & Security**, otherwise they are skipped with a warning.
- Browser profile cache discovery skips and reports profiles it cannot read,
  rather than preventing the script from starting.
- The `ios_backups` category deletes iOS/iPadOS device backups and is not
  enabled by default — double-check before using `--all` or explicitly
  selecting it.
- The shared system `/tmp` directory is not a cleanup target because active
  processes may depend on its files and sockets.
- The script never needs `sudo` and exits with an error when run as root,
  because it only cleans the logged-in user's files. Reindex tasks are
  limited to ones that work without elevated privileges; failed tasks are
  reported as warnings and do not stop the cleanup.
- Prefer `--dry-run` first, especially when using `--all` or custom
  `--categories`.
