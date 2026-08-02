# macOS Clear Cache

A single-file Python script that safely cleans up cache, log, and temporary
files on macOS (and largely on Linux), with per-category selection, dry-run
preview, and optional post-clean system reindexing.

## Features

- **Category-based targets** – dozens of well-known cache/log locations grouped
  into 12 categories: `system`, `trash`, `browsers`, `apps`, `mail`,
  `ios_backups`, `quicklook`, `crashreports`, `tmp`, `developer`, `packages`,
  `logs`.
- **Safe by default** – only a curated subset of low-risk categories runs
  unless you opt in with `--all` or `--categories`.
- **Dry-run mode** – preview exactly what would be removed before deleting
  anything.
- **Automatic deduplication** – if an enabled target is nested inside another
  enabled target (e.g. `~/Library/Caches/pip` under `~/Library/Caches`), the
  child is skipped to avoid double counting/deletion.
- **Browser profile discovery** – automatically finds per-profile `Cache`,
  `Code Cache`, and `Service Worker/CacheStorage` folders for Chrome, Edge,
  and Brave under `Application Support`.
- **Age filtering** – `--older-than DAYS` skips anything modified more
  recently than the given number of days.
- **Move to Trash option** – `--to-trash` moves items to `~/.Trash` instead of
  permanently deleting them.
- **Interactive mode** – `--interactive` asks for per-category confirmation.
- **External target config** – add extra paths without editing the script via
  a `targets.json` file (see [Custom targets](#custom-targets)).
- **JSON run log** – a summary of every run is written to
  `~/Library/Logs/clear_caches/` unless `--no-log` is passed.
- **macOS notification** – a notification is shown on completion unless
  `--no-notify` is passed.
- **Disk space report** – shows free space before/after an actual (non
  dry-run) cleanup.
- **Parallel size scanning** – target sizes are computed concurrently with a
  thread pool for faster planning output.
- **Scheduling** – `--install-schedule HH:MM` installs a `launchd` agent to
  run the cleanup daily; `--uninstall-schedule` removes it.
- **System reindexing** – after cleaning, optionally runs Spotlight, DNS,
  Launch Services, QuickLook, Homebrew, Docker, Dock/Finder maintenance tasks
  (skippable with `--no-reindex`).

## Requirements

- Python 3.10+ (uses `from __future__ import annotations` and
  `Path.is_relative_to`)
- macOS for the notification, reindexing, and scheduling features; the
  cleaning logic itself is portable to Linux.
- No third-party dependencies — standard library only.

## Usage

```bash
python3 clear_caches.py [OPTIONS]
```

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

# Only remove items untouched for at least 30 days, moving them to Trash
python3 clear_caches.py --older-than 30 --to-trash

# Ask for confirmation before each category is cleaned
python3 clear_caches.py --interactive

# Install a daily 03:00 scheduled run (safe categories, no reindex)
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
| `--categories CAT [CAT ...]` | Space-separated list of categories to clean (default: `apps browsers crashreports quicklook system tmp trash`). |
| `--exclude CAT [CAT ...]` | Space-separated list of categories to exclude. |
| `--no-reindex` | Skip Spotlight/DNS/Launch Services/etc. maintenance after cleaning. |
| `--older-than DAYS` | Only remove items last modified more than `DAYS` days ago. |
| `--to-trash` | Move items to `~/.Trash` instead of permanently deleting them. |
| `--interactive` | Ask for confirmation before cleaning each category. |
| `--no-log` | Do not write a JSON summary log. |
| `--no-notify` | Do not send a macOS notification when done. |
| `--install-schedule HH:MM` | Install a `launchd` agent to run this script daily at the given time. |
| `--uninstall-schedule` | Remove the previously installed `launchd` agent. |

## Categories

| Category | Description | Enabled by default |
| --- | --- | --- |
| `system` | Generic OS-level caches (`~/Library/Caches`, `~/.cache`) | ✓ |
| `trash` | Kosz / Trash (`~/.Trash`) | ✓ |
| `browsers` | Web browser caches (Chrome, Firefox, Safari, Edge, Brave, Opera, Vivaldi, Arc, Slack) | ✓ |
| `apps` | Popular app caches (Spotify, Zoom, Teams, Discord, Steam, WhatsApp, Telegram) | ✓ |
| `quicklook` | QuickLook thumbnail cache | ✓ |
| `crashreports` | Crash & diagnostic reports | ✓ |
| `tmp` | System `/tmp` directory | ✓ |
| `mail` | Mail.app cache | – |
| `ios_backups` | iOS/iPadOS backups (MobileSync) ⚠ large & destructive | – |
| `developer` | Xcode/CoreSimulator artefacts, VS Code caches, JetBrains caches (re-generatable) | – |
| `packages` | Package-manager caches: npm, Yarn, pnpm, Gradle, pip, Poetry, Cargo, CocoaPods, Composer, uv, Gem, Bundler, Go modules, Maven, Homebrew (re-downloadable) | – |
| `logs` | Log files, including JetBrains logs | – |

## Custom targets

Extra cleanup targets can be added without touching the script by creating a
JSON file at either:

- `targets.json` next to `clear_caches.py`, or
- `~/.config/clear_caches/targets.json`

Each entry needs a `path`, `label`, and `category` (existing category names
can be reused, or new ones added):

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

Unless `--no-log` is passed, every run writes a JSON summary to
`~/Library/Logs/clear_caches/clear_caches_<timestamp>.json` containing the
timestamp, dry-run/to-trash flags, total entries/bytes reclaimed, and a
per-category breakdown.

## Safety notes

- Some targets (`~/Library/Containers/com.apple.mail/...`,
  `~/Library/Application Support/MobileSync/Backup`, `~/.Trash`) require
  granting **Full Disk Access** to your terminal/IDE in **System Settings →
  Privacy & Security**, otherwise they are skipped with a warning.
- The `ios_backups` category deletes iOS/iPadOS device backups and is not
  enabled by default — double-check before using `--all` or explicitly
  selecting it.
- Several reindex tasks (Spotlight, `mDNSResponder`, font cache, Time Machine
  local snapshots, `purge`) require `sudo` and will simply fail gracefully if
  not run with elevated privileges.
- Prefer `--dry-run` first, especially when using `--all` or custom
  `--categories`.
