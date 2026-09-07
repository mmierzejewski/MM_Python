#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Target:
    path: Path
    label: str
    category: str


# ---------------------------------------------------------------------------
# Targets organised by category
# ---------------------------------------------------------------------------
# "system"      – generic OS-level caches (safe, enabled by default)
# "trash"       – Kosz / Trash (safe, enabled by default)
# "browsers"    – web browser caches (enabled by default)
# "apps"        – popular app caches (Spotify, Zoom, Teams, Discord…)
# "mail"        – Mail.app cache
# "ios_backups" – iOS/iPadOS backups stored by iTunes/Finder (⚠ large, destructive)
# "quicklook"   – QuickLook thumbnail cache
# "crashreports"– crash & diagnostic reports
# "tmp"         – system /tmp directory
# "developer"   – Xcode / CoreSimulator artefacts (large but re-generatable)
# "packages"    – package-manager caches (re-downloadable)
# "logs"        – log files and crash reports
# ---------------------------------------------------------------------------

TARGETS: list[Target] = [
    # --- System caches ------------------------------------------------------
    Target(Path.home() / "Library" / "Caches",
           "macOS User Caches (~/Library/Caches)", "system"),
    Target(Path.home() / ".cache",
           "User Cache (~/.cache)", "system"),

    # --- Kosz / Trash -------------------------------------------------------
    Target(Path.home() / ".Trash",
           "Kosz (Trash) (~/.Trash)", "trash"),

    # --- Developer tools ----------------------------------------------------
    Target(Path.home() / "Library" / "Developer" / "Xcode" / "DerivedData",
           "Xcode DerivedData", "developer"),
    Target(Path.home() / "Library" / "Developer" / "Xcode" / "iOS DeviceSupport",
           "Xcode iOS DeviceSupport", "developer"),
    Target(Path.home() / "Library" / "Developer" / "Xcode" / "watchOS DeviceSupport",
           "Xcode watchOS DeviceSupport", "developer"),
    Target(Path.home() / "Library" / "Developer" / "Xcode" / "visionOS DeviceSupport",
           "Xcode visionOS DeviceSupport", "developer"),
    Target(Path.home() / "Library" / "Developer" / "CoreSimulator" / "Caches",
           "CoreSimulator Caches", "developer"),
    Target(Path.home() / "Library" / "Android" / "sdk" / ".temp",
           "Android SDK temp", "developer"),

    # --- IDEs ---------------------------------------------------------------
    Target(
        Path.home() / "Library" / "Application Support" / "Code" / "CachedExtensionVSIXs",
        "VSCode Cached Extension VSIXs", "developer",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Code" / "CachedData",
        "VSCode Cached Data", "developer",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Code" / "Cache",
        "VSCode Cache", "developer",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Code" / "Code Cache",
        "VSCode Code Cache", "developer",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Code" / "GPUCache",
        "VSCode GPU Cache", "developer",
    ),

    # --- Package managers ---------------------------------------------------
    Target(Path.home() / ".npm" / "_cacache",
           "npm Cache (~/.npm/_cacache)", "packages"),
    Target(Path.home() / ".yarn" / "cache",
           "Yarn Classic Cache (~/.yarn/cache)", "packages"),
    Target(Path.home() / "Library" / "Caches" / "yarn",
           "Yarn Cache (macOS)", "packages"),
    Target(Path.home() / ".pnpm-store",
           "pnpm Store (~/.pnpm-store)", "packages"),
    Target(Path.home() / ".gradle" / "caches",
           "Gradle Caches (~/.gradle/caches)", "packages"),
    Target(Path.home() / "Library" / "Caches" / "pip",
           "pip Cache (macOS)", "packages"),
    Target(Path.home() / ".cache" / "pip",
           "pip Cache (Linux/~/.cache/pip)", "packages"),
    Target(Path.home() / "Library" / "Caches" / "pypoetry",
           "Poetry Cache (macOS)", "packages"),
    Target(Path.home() / ".cache" / "pypoetry",
           "Poetry Cache (Linux)", "packages"),
    Target(Path.home() / ".cargo" / "registry" / "cache",
           "Cargo Registry Cache", "packages"),
    Target(Path.home() / "Library" / "Caches" / "CocoaPods",
           "CocoaPods Cache", "packages"),
    Target(Path.home() / ".cocoapods" / "repos",
           "CocoaPods Repos (~/.cocoapods/repos)", "packages"),
    Target(Path.home() / ".composer" / "cache",
           "Composer Cache (~/.composer/cache)", "packages"),
    Target(Path.home() / ".cache" / "uv",
           "uv Cache (~/.cache/uv)", "packages"),
    Target(Path.home() / ".gem" / "cache",
           "Ruby Gem Cache (~/.gem/cache)", "packages"),
    Target(Path.home() / ".bundle" / "cache",
           "Bundler Cache (~/.bundle/cache)", "packages"),
    Target(Path.home() / "go" / "pkg" / "mod" / "cache",
           "Go Module Cache (~/go/pkg/mod/cache)", "packages"),
    Target(Path.home() / ".m2" / "repository",
           "Maven Local Repository (~/.m2/repository)", "packages"),

    # --- Browsers -----------------------------------------------------------
    Target(Path.home() / "Library" / "Caches" / "Google" / "Chrome",
           "Google Chrome Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "Chromium",
           "Chromium Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "Firefox",
           "Firefox Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "com.apple.Safari",
           "Safari Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "Microsoft Edge",
           "Microsoft Edge Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "BraveSoftware" / "Brave-Browser",
           "Brave Browser Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "com.operasoftware.Opera",
           "Opera Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "Vivaldi",
           "Vivaldi Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "company.thebrowser.Browser",
           "Arc Browser Cache", "browsers"),
    Target(Path.home() / "Library" / "Caches" / "com.tinyspeck.slackmacgap",
           "Slack Cache", "browsers"),

    # --- Applications --------------------------------------------------------
    Target(
        Path.home() / "Library" / "Application Support" / "Spotify" / "PersistentCache",
        "Spotify Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Microsoft" / "Teams" / "Cache",
        "Microsoft Teams Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Microsoft" / "Teams" / "Code Cache",
        "Microsoft Teams Code Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Microsoft" / "Teams" / "GPUCache",
        "Microsoft Teams GPU Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Microsoft" / "Teams"
        / "Service Worker" / "CacheStorage",
        "Microsoft Teams Service Worker Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Microsoft" / "Skype for Desktop" / "Cache",
        "Skype Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Microsoft" / "Skype for Desktop" / "Code Cache",
        "Skype Code Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Microsoft" / "Skype for Desktop" / "GPUCache",
        "Skype GPU Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "discord" / "Cache",
        "Discord Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "discord" / "Code Cache",
        "Discord Code Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Steam" / "appcache",
        "Steam App Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Steam" / "steamapps" / "shadercache",
        "Steam Shader Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "WhatsApp" / "Cache",
        "WhatsApp Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Telegram Desktop" / "tdata" / "emoji",
        "Telegram Emoji Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "GitHub Desktop" / "Cache",
        "GitHub Desktop Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "GitHub Desktop" / "Code Cache",
        "GitHub Desktop Code Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "GitHub Desktop" / "GPUCache",
        "GitHub Desktop GPU Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Bitwarden" / "Cache",
        "Bitwarden Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Bitwarden" / "Code Cache",
        "Bitwarden Code Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Bitwarden" / "GPUCache",
        "Bitwarden GPU Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "balenaEtcher" / "Cache",
        "balenaEtcher Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "balenaEtcher" / "Code Cache",
        "balenaEtcher Code Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "balenaEtcher" / "GPUCache",
        "balenaEtcher GPU Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Google" / "DriveFS" / "cef_cache" / "Cache",
        "Google DriveFS Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Google" / "DriveFS" / "cef_cache" / "Code Cache",
        "Google DriveFS Code Cache", "apps",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Google" / "DriveFS" / "cef_cache" / "component_crx_cache",
        "Google DriveFS Component Cache", "apps",
    ),

    # --- Mail ---------------------------------------------------------------
    Target(
        Path.home() / "Library" / "Containers" / "com.apple.mail"
        / "Data" / "Library" / "Caches",
        "Mail.app Cache", "mail",
    ),

    # --- iOS Backups (⚠ destructive – use with caution) --------------------
    Target(
        Path.home() / "Library" / "Application Support" / "MobileSync" / "Backup",
        "iOS/iPadOS Backups (MobileSync)", "ios_backups",
    ),

    # --- QuickLook ----------------------------------------------------------
    Target(
        Path.home() / "Library" / "Caches" / "com.apple.QuickLookDaemon",
        "QuickLook Thumbnail Cache", "quicklook",
    ),
    Target(
        Path.home() / "Library" / "Application Support" / "Quick Look",
        "QuickLook Application Support Cache", "quicklook",
    ),

    # --- Crash & diagnostic reports -----------------------------------------
    Target(
        Path.home() / "Library" / "Logs" / "DiagnosticReports",
        "User Diagnostic Reports", "crashreports",
    ),
    Target(
        Path("/Library") / "Logs" / "DiagnosticReports",
        "System Diagnostic Reports (/Library/…)", "crashreports",
    ),
    Target(
        Path.home() / "Library" / "Logs" / "CrashReporter",
        "CrashReporter Logs", "crashreports",
    ),

    # --- System /tmp --------------------------------------------------------
    Target(Path("/private/tmp"),
           "System Temporary Files (/tmp)", "tmp"),

    # --- Logs & diagnostics -------------------------------------------------
    Target(Path.home() / "Library" / "Logs",
           "User Logs (~/Library/Logs)", "logs"),

    # --- Homebrew -------------------------------------------------------------
    Target(Path.home() / "Library" / "Caches" / "Homebrew",
           "Homebrew Download Cache", "packages"),

    # --- JetBrains IDEs -------------------------------------------------------
    Target(Path.home() / "Library" / "Caches" / "JetBrains",
           "JetBrains IDE Caches", "developer"),
    Target(Path.home() / "Library" / "Logs" / "JetBrains",
           "JetBrains IDE Logs", "logs"),
]


def browser_profile_targets(cache_root: Path, browser_name: str) -> list[Target]:
    """Chrome/Edge/Brave store their real cache under per-profile folders
    in Application Support, not under Library/Caches."""
    targets: list[Target] = []
    if not cache_root.exists():
        return targets
    subpaths = (
        ("Cache", "Cache"),
        ("Code Cache", "Code Cache"),
        ("GPUCache", "GPU Cache"),
        ("Service Worker/CacheStorage", "Service Worker CacheStorage"),
    )
    for profile_dir in cache_root.iterdir():
        if not profile_dir.is_dir():
            continue
        for rel, label_suffix in subpaths:
            path = profile_dir / Path(*rel.split("/"))
            if path.exists():
                targets.append(
                    Target(path, f"{browser_name} {profile_dir.name} {label_suffix}", "browsers")
                )
    for rel, label_suffix in (
        ("ShaderCache", "Shader Cache"),
        ("GraphiteDawnCache", "Graphite Dawn Cache"),
        ("GrShaderCache", "GrShader Cache"),
        ("GPUPersistentCache/GPUCache", "GPU Persistent Cache"),
    ):
        path = cache_root / Path(*rel.split("/"))
        if path.exists():
            targets.append(Target(path, f"{browser_name} {label_suffix}", "browsers"))
    return targets


for _root, _name in (
    (Path.home() / "Library" / "Application Support" / "Google" / "Chrome", "Chrome"),
    (Path.home() / "Library" / "Application Support" / "Microsoft Edge", "Edge"),
    (Path.home() / "Library" / "Application Support" / "BraveSoftware" / "Brave-Browser", "Brave"),
):
    TARGETS.extend(browser_profile_targets(_root, _name))


def load_external_targets() -> list[Target]:
    """Load extra targets from an optional user-editable JSON config, so new
    paths can be added without touching this file."""
    candidates = [
        Path(__file__).resolve().parent / "targets.json",
        Path.home() / ".config" / "clear_caches" / "targets.json",
    ]
    extra: list[Target] = []
    for config_path in candidates:
        if not config_path.exists():
            continue
        try:
            entries = json.loads(config_path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            print(f"  [info] Could not read {config_path}: {exc}")
            continue
        for entry in entries:
            try:
                extra.append(
                    Target(Path(entry["path"]).expanduser(), entry["label"], entry["category"])
                )
            except KeyError as exc:
                print(f"  [info] Skipping malformed entry in {config_path}: missing {exc}")
    return extra


TARGETS.extend(load_external_targets())

CATEGORY_LABELS: dict[str, str] = {
    "system":       "System Caches",
    "trash":        "Kosz (Trash)",
    "browsers":     "Browser Caches",
    "apps":         "Application Caches",
    "mail":         "Mail Cache",
    "ios_backups":  "iOS/iPadOS Backups ⚠",
    "quicklook":    "QuickLook Cache",
    "crashreports": "Crash & Diagnostic Reports",
    "tmp":          "System /tmp",
    "developer":    "Developer Tools",
    "packages":     "Package Managers",
    "logs":         "Logs & Diagnostics",
}

DEFAULT_CATEGORIES = {"system", "browsers", "apps", "quicklook", "crashreports"}
ALL_CATEGORIES = set(CATEGORY_LABELS)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def format_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f}{unit}" if unit != "B" else f"{int(size)}B"
        size /= 1024
    return f"{size_bytes}B"  # unreachable; satisfies type-checkers


def path_size(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    total = 0
    for item in path.rglob("*"):
        try:
            if item.is_file():
                total += item.stat().st_size
        except OSError:
            continue
    return total


def sizes_in_parallel(paths: list[Path]) -> dict[Path, int]:
    """Compute path_size for many top-level paths concurrently (I/O bound)."""
    if not paths:
        return {}
    with ThreadPoolExecutor(max_workers=min(16, len(paths))) as pool:
        results = pool.map(path_size, paths)
    return dict(zip(paths, results))


def move_to_trash(item: Path) -> None:
    trash_dir = Path.home() / ".Trash"
    trash_dir.mkdir(exist_ok=True)
    destination = trash_dir / item.name
    if destination.exists():
        destination = trash_dir / f"{item.name}.{int(time.time())}"
    shutil.move(str(item), str(destination))


def clear_directory(
    path: Path,
    dry_run: bool,
    older_than_days: float | None = None,
    to_trash: bool = False,
) -> tuple[list[str], int, int]:
    """Returns (output_lines, removed_entries, reclaimed_bytes)."""
    if not path.exists():
        return [], 0, 0

    removed_entries = 0
    reclaimed_bytes = 0
    lines: list[str] = []

    try:
        children = list(path.iterdir())
    except PermissionError as exc:
        lines.append(f"  Warning – no permission to read {path}: {exc}")
        lines.append(
            "  Tip: grant Full Disk Access to Terminal in System Settings → Privacy & Security."
        )
        return lines, 0, 0

    cutoff = time.time() - older_than_days * 86400 if older_than_days is not None else None

    for item in children:
        if cutoff is not None:
            try:
                if item.stat().st_mtime > cutoff:
                    lines.append(f"  [skipped-age] too recent: {item}")
                    continue
            except OSError:
                pass

        item_size = path_size(item)
        removed_entries += 1
        reclaimed_bytes += item_size

        if dry_run:
            verb = "would move to Trash" if to_trash else "would remove"
            lines.append(f"  [dry-run] {verb}: {item}")
            continue

        try:
            if to_trash:
                move_to_trash(item)
                lines.append(f"  Moved to Trash: {item}")
            else:
                if item.is_dir() and not item.is_symlink():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                lines.append(f"  Removed: {item}")
        except OSError as exc:
            lines.append(f"  Warning – could not remove {item}: {exc}")
            removed_entries -= 1
            reclaimed_bytes -= item_size

    return lines, removed_entries, reclaimed_bytes


def resolve_targets(targets: list[Target]) -> list[Target]:
    """Drop targets whose path is a subdirectory of another active target.

    Prevents double-counting and double-deletion when, for example, both
    ~/Library/Caches (system) and ~/Library/Caches/pip (packages) are active.
    """
    paths = {t.path for t in targets}
    result = []
    skipped = []
    for target in targets:
        if any(target.path != p and target.path.is_relative_to(p) for p in paths):
            skipped.append(target.label)
        else:
            result.append(target)
    if skipped:
        print(
            "  [info] Skipped (already covered by a parent target): "
            + ", ".join(skipped)
        )
    return result


def confirm(total_size: int, to_trash: bool) -> bool:
    print(f"\nEstimated space to reclaim: {format_size(total_size)}")
    action = "move the listed items to Trash" if to_trash else "permanently delete the listed items"
    reply = input(f"This will {action}. Continue? [y/N]: ")
    return reply.strip().lower() in {"y", "yes"}


def confirm_category(category_label: str) -> bool:
    reply = input(f"Clean [{category_label}]? [y/N]: ")
    return reply.strip().lower() in {"y", "yes"}


def send_notification(title: str, message: str) -> None:
    script = f'display notification "{message}" with title "{title}"'
    try:
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        pass


LOG_DIR = Path.home() / "Library" / "Logs" / "clear_caches"


def write_log(summary: dict) -> Path | None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_path = LOG_DIR / f"clear_caches_{datetime.now():%Y%m%d_%H%M%S}.json"
        log_path.write_text(json.dumps(summary, indent=2))
        return log_path
    except OSError as exc:
        print(f"  [info] Could not write log: {exc}")
        return None


LAUNCH_AGENT_LABEL = "com.mmierzejewski.clearcaches"
LAUNCH_AGENT_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LAUNCH_AGENT_LABEL}.plist"


def install_schedule(time_str: str) -> None:
    hour, _, minute = time_str.partition(":")
    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>{LAUNCH_AGENT_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{Path(__file__).resolve()}</string>
        <string>--yes</string>
        <string>--no-reindex</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>{int(hour)}</integer>
        <key>Minute</key><integer>{int(minute or 0)}</integer>
    </dict>
    <key>StandardOutPath</key><string>{LOG_DIR}/launchd.log</string>
    <key>StandardErrorPath</key><string>{LOG_DIR}/launchd.err.log</string>
</dict>
</plist>
"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LAUNCH_AGENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAUNCH_AGENT_PATH.write_text(plist)
    subprocess.run(["launchctl", "load", "-w", str(LAUNCH_AGENT_PATH)], capture_output=True)
    print(f"Zaplanowano codzienne uruchamianie o {hour}:{minute or '00'} -> {LAUNCH_AGENT_PATH}")


def uninstall_schedule() -> None:
    subprocess.run(["launchctl", "unload", str(LAUNCH_AGENT_PATH)], capture_output=True)
    if LAUNCH_AGENT_PATH.exists():
        LAUNCH_AGENT_PATH.unlink()
    print(f"Usunięto harmonogram: {LAUNCH_AGENT_PATH}")


# ---------------------------------------------------------------------------
# Reindexing
# ---------------------------------------------------------------------------

@dataclass
class ReindexTask:
    label: str
    cmd: list[str]
    note: str = ""


REINDEX_TASKS: list[ReindexTask] = [
    ReindexTask(
        label="Spotlight – disable index (flush)",
        cmd=["mdutil", "-i", "off", "/"],
        note="Requires sudo",
    ),
    ReindexTask(
        label="Spotlight – enable & rebuild index",
        cmd=["mdutil", "-i", "on", "/"],
        note="Requires sudo",
    ),
    ReindexTask(
        label="Launch Services – rebuild app database",
        cmd=[
            "/System/Library/Frameworks/CoreServices.framework"
            "/Frameworks/LaunchServices.framework/Support/lsregister",
            "-kill", "-r",
            "-domain", "local",
            "-domain", "system",
            "-domain", "user",
        ],
    ),
    ReindexTask(
        label="DNS cache – flush",
        cmd=["dscacheutil", "-flushcache"],
    ),
    ReindexTask(
        label="mDNSResponder – restart",
        cmd=["killall", "-HUP", "mDNSResponder"],
        note="Requires sudo",
    ),
    ReindexTask(
        label="Font cache – rebuild (atsutil)",
        cmd=["atsutil", "databases", "-remove"],
        note="Requires sudo; fonts reload on next login",
    ),
    ReindexTask(
        label="QuickLook cache – reset",
        cmd=["qlmanage", "-r", "cache"],
    ),
    ReindexTask(
        label="Dock – relaunch (icon cache refresh)",
        cmd=["killall", "Dock"],
    ),
    ReindexTask(
        label="Finder – relaunch",
        cmd=["killall", "Finder"],
    ),
]


def run_reindex(dry_run: bool) -> None:
    print("\n[Reindexing & Service Restart]")
    for task in REINDEX_TASKS:
        note = f"  ({task.note})" if task.note else ""
        if dry_run:
            print(f"  [dry-run] would run: {' '.join(task.cmd)}{note}")
            continue
        print(f"  ▶ {task.label}{note} … ", end="", flush=True)
        try:
            result = subprocess.run(
                task.cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                print("OK")
            else:
                err = result.stderr.strip().splitlines()[0] if result.stderr.strip() else "non-zero exit"
                print(f"Warning – {err}")
        except FileNotFoundError:
            print("Skipped (command not found)")
        except subprocess.TimeoutExpired:
            print("Warning – timed out")
        except OSError as exc:
            print(f"Warning – {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Clear cache files, temporary files, and Trash on macOS/Linux.\n\n"
            "Categories:\n"
            + "\n".join(
                f"  {k:12s} – {v}" for k, v in CATEGORY_LABELS.items()
            )
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without deleting anything.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Enable all categories, including destructive ones.",
    )
    parser.add_argument(
        "--categories",
        metavar="CAT",
        nargs="+",
        choices=sorted(ALL_CATEGORIES),
        default=None,
        help=(
            "Space-separated list of categories to clean "
            f"(default: {', '.join(sorted(DEFAULT_CATEGORIES))}). "
            f"Choices: {', '.join(sorted(ALL_CATEGORIES))}."
        ),
    )
    parser.add_argument(
        "--exclude",
        metavar="CAT",
        nargs="+",
        choices=sorted(ALL_CATEGORIES),
        default=None,
        help="Space-separated list of categories to exclude from cleaning.",
    )
    parser.add_argument(
        "--no-reindex",
        action="store_true",
        help="Keep the default behavior of skipping reindexing and service restarts.",
    )
    parser.add_argument(
        "--reindex",
        action="store_true",
        help="Run reindexing and service restarts after cleaning.",
    )
    parser.add_argument(
        "--older-than",
        metavar="DAYS",
        type=float,
        default=None,
        help="Only remove items last modified more than DAYS days ago.",
    )
    parser.add_argument(
        "--to-trash",
        action="store_true",
        help="Move items to ~/.Trash instead of deleting them permanently.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Ask for confirmation before cleaning each category.",
    )
    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Do not write a JSON summary log to ~/Library/Logs/clear_caches/.",
    )
    parser.add_argument(
        "--no-notify",
        action="store_true",
        help="Do not send a macOS notification when done.",
    )
    parser.add_argument(
        "--install-schedule",
        metavar="HH:MM",
        default=None,
        help="Install a launchd agent to run this script daily at HH:MM.",
    )
    parser.add_argument(
        "--uninstall-schedule",
        action="store_true",
        help="Remove the previously installed launchd agent.",
    )
    args = parser.parse_args()

    if args.install_schedule:
        install_schedule(args.install_schedule)
        return 0
    if args.uninstall_schedule:
        uninstall_schedule()
        return 0

    if args.all:
        active_categories = ALL_CATEGORIES
    elif args.categories:
        active_categories = set(args.categories)
    else:
        active_categories = DEFAULT_CATEGORIES

    if args.exclude:
        active_categories -= set(args.exclude)

    if args.to_trash and "trash" in active_categories:
        parser.error("--to-trash cannot be combined with the trash category")

    active_targets = [t for t in TARGETS if t.category in active_categories]
    active_targets = resolve_targets(active_targets)

    # Group by category once to avoid repeated filtering
    cats_to_targets: dict[str, list[Target]] = {}
    for t in active_targets:
        cats_to_targets.setdefault(t.category, []).append(t)

    # Compute and cache sizes up-front in parallel (avoids double disk scan)
    size_cache: dict[Path, int] = sizes_in_parallel([t.path for t in active_targets])

    # Print plan grouped by category
    for cat in sorted(active_categories):
        cat_targets = cats_to_targets.get(cat, [])
        if not cat_targets:
            continue
        print(f"\n[{CATEGORY_LABELS[cat]}]")
        for t in cat_targets:
            exists = "✓" if t.path.exists() else "–"
            print(f"  {exists} {t.label}  ({format_size(size_cache[t.path])})")

    total_size = sum(size_cache.values())

    if not args.dry_run and not args.yes and not confirm(total_size, args.to_trash):
        print("Cancelled.")
        return 1

    disk_before = shutil.disk_usage(Path.home()).free if not args.dry_run else None

    print()
    grand_entries = 0
    grand_bytes = 0
    category_summary: dict[str, dict[str, int]] = {}

    for cat in sorted(active_categories):
        cat_targets = cats_to_targets.get(cat, [])
        if not cat_targets:
            continue
        if args.interactive and not confirm_category(CATEGORY_LABELS[cat]):
            print(f"  [skipped by user] {CATEGORY_LABELS[cat]}")
            continue
        cat_block: list[str] = []
        cat_entries = 0
        cat_bytes = 0
        for t in cat_targets:
            lines, entries, size_bytes = clear_directory(
                t.path, args.dry_run, older_than_days=args.older_than, to_trash=args.to_trash
            )
            grand_entries += entries
            grand_bytes += size_bytes
            cat_entries += entries
            cat_bytes += size_bytes
            verb = "would remove" if args.dry_run else "removed"
            if lines or entries:
                cat_block.extend(lines)
                if entries:
                    cat_block.append(
                        f"  {t.label}: {verb} {entries} item(s), {format_size(size_bytes)}"
                    )
        if cat_block:
            print(f"[{CATEGORY_LABELS[cat]}]")
            print("\n".join(cat_block))
            print()
        if cat_entries:
            category_summary[cat] = {"entries": cat_entries, "bytes": cat_bytes}

    verb = "Would reclaim" if args.dry_run else "Reclaimed"
    print(
        f"Done. {verb} ~{format_size(grand_bytes)} across {grand_entries} item(s)."
    )

    if disk_before is not None:
        disk_after = shutil.disk_usage(Path.home()).free
        print(f"Free disk space: {format_size(disk_before)} -> {format_size(disk_after)} "
              f"(+{format_size(disk_after - disk_before)})")

    if args.reindex and not args.no_reindex:
        run_reindex(args.dry_run)

    if not args.no_log:
        log_path = write_log({
            "timestamp": datetime.now().isoformat(),
            "dry_run": args.dry_run,
            "to_trash": args.to_trash,
            "total_entries": grand_entries,
            "total_bytes": grand_bytes,
            "categories": category_summary,
        })
        if log_path:
            print(f"Log zapisany: {log_path}")

    if not args.dry_run and not args.no_notify:
        send_notification("Clear Caches", f"Zwolniono {format_size(grand_bytes)} ({grand_entries} elementów).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
