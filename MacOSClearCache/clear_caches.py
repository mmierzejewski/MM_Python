#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import plistlib
import re
import shutil
import signal
import stat
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
    remove_self: bool = False


# ---------------------------------------------------------------------------
# Targets organised by category
# ---------------------------------------------------------------------------
# Enabled by default: system, browsers, apps, quicklook, crashreports.
#
# "system"      – generic OS-level caches
# "trash"       – Trash (~/.Trash)
# "browsers"    – web browser caches
# "apps"        – popular app caches (Slack, Spotify, Teams, Discord…)
# "mail"        – Mail.app cache
# "ios_backups" – iOS/iPadOS backups stored by iTunes/Finder (⚠ large, destructive)
# "quicklook"   – QuickLook thumbnail cache
# "crashreports"– crash & diagnostic reports
# "developer"   – Xcode / CoreSimulator artefacts (large but re-generatable)
# "packages"    – package-manager caches (re-downloadable)
# "logs"        – JetBrains IDE logs
# "stale"       – leftovers: old JetBrains IDE settings, broken symlinks in bin dirs
# "maintenance" – Homebrew cleanup/autoremove commands
# ---------------------------------------------------------------------------

TARGETS: list[Target] = [
    # --- System caches ------------------------------------------------------
    Target(Path.home() / "Library" / "Caches",
           "macOS User Caches (~/Library/Caches)", "system"),
    Target(Path.home() / ".cache",
           "User Cache (~/.cache)", "system"),

    # --- Trash ---------------------------------------------------------------
    Target(Path.home() / ".Trash",
           "Trash (~/.Trash)", "trash"),

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
           "pip Cache (~/.cache/pip)", "packages"),
    Target(Path.home() / "Library" / "Caches" / "pypoetry",
           "Poetry Cache (macOS)", "packages"),
    Target(Path.home() / ".cache" / "pypoetry",
           "Poetry Cache (~/.cache/pypoetry)", "packages"),
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

    # --- Applications --------------------------------------------------------
    Target(Path.home() / "Library" / "Caches" / "com.tinyspeck.slackmacgap",
           "Slack Cache", "apps"),
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

    # --- Homebrew -------------------------------------------------------------
    Target(Path.home() / "Library" / "Caches" / "Homebrew",
           "Homebrew Download Cache", "packages"),

    # --- JetBrains IDEs -------------------------------------------------------
    Target(Path.home() / "Library" / "Caches" / "JetBrains",
           "JetBrains IDE Caches", "developer"),
    Target(Path.home() / "Library" / "Logs" / "JetBrains",
           "JetBrains IDE Logs", "logs"),

    # --- Updater downloads & tool caches --------------------------------------
    Target(
        Path.home() / "Library" / "Application Support" / "Foxit Software" / "Continuous" / "updater",
        "Foxit Updater Downloads", "apps",
    ),
    Target(Path.home() / "Library" / "Application Support" / "virtualenv",
           "virtualenv Seed/Wheel Cache", "packages"),
]


# ---------------------------------------------------------------------------
# Stale leftovers (removed as whole items, not emptied)
# ---------------------------------------------------------------------------

JETBRAINS_CONFIG_RE = re.compile(r"^([A-Za-z]+)(\d{4}(?:\.\d+)+)$")
BROKEN_SYMLINK_DIRS = (Path("/opt/homebrew/bin"),)


def stale_jetbrains_config_dirs(root: Path | None = None) -> list[Path]:
    """Return per-version JetBrains settings dirs (e.g. PyCharm2025.2) except
    the newest version of each product."""
    root = root or Path.home() / "Library" / "Application Support" / "JetBrains"
    groups: dict[str, list[tuple[tuple[int, ...], Path]]] = {}
    try:
        entries = list(root.iterdir())
    except OSError:
        return []
    for entry in entries:
        match = JETBRAINS_CONFIG_RE.match(entry.name)
        if not match or not entry.is_dir() or entry.is_symlink():
            continue
        version = tuple(int(part) for part in match.group(2).split("."))
        groups.setdefault(match.group(1).lower(), []).append((version, entry))
    stale: list[Path] = []
    for versions in groups.values():
        versions.sort()
        stale.extend(path for _, path in versions[:-1])
    return sorted(stale)


def broken_symlinks(directories: tuple[Path, ...] = BROKEN_SYMLINK_DIRS) -> list[Path]:
    found: list[Path] = []
    for directory in directories:
        try:
            entries = list(directory.iterdir())
        except OSError:
            continue
        found.extend(e for e in entries if e.is_symlink() and not e.exists())
    return sorted(found)


def stale_targets() -> list[Target]:
    targets = [
        Target(path, f"Old JetBrains settings ({path.name})", "stale", remove_self=True)
        for path in stale_jetbrains_config_dirs()
    ]
    targets.extend(
        Target(path, f"Broken symlink ({path} -> {os.readlink(path)})", "stale", remove_self=True)
        for path in broken_symlinks()
    )
    return targets


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
    try:
        profile_dirs = list(cache_root.iterdir())
    except OSError as exc:
        print(f"  [info] Could not scan browser profiles in {cache_root}: {exc}")
        return targets

    for profile_dir in profile_dirs:
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


APPLICATION_SUPPORT_CACHE_NAMES = {
    "Cache",
    "Caches",
    "Code Cache",
    "GPUCache",
    "DawnCache",
    "DawnGraphiteCache",
    "DawnWebGPUCache",
    "GraphiteDawnCache",
    "GrShaderCache",
    "ShaderCache",
    "ScriptCache",
    "crx_cache",
}
# Persistent stores that may hold user data (offline content, PWA storage).
NON_CACHE_DATA_DIRS = {
    "blob_storage", "content_cache", "thumbnails_cache", "indexeddb", "local storage",
    "service worker",
}
# Large or private top-level Application Support folders that never contain
# regenerable caches; skipping them keeps the discovery scan fast.
SKIPPED_APPLICATION_SUPPORT_ROOTS = {"MobileSync", "CloudDocs", "FileProvider", "CallHistoryDB", "Knowledge"}


BROWSER_SUPPORT_ROOTS = (
    ("Google", "Chrome"),
    ("Microsoft Edge",),
    ("BraveSoftware", "Brave-Browser"),
    ("Chromium",),
)


def application_support_cache_targets(
    root: Path | None = None,
    known_paths: set[Path] | None = None,
) -> list[Target]:
    """Discover conventional, regenerable app caches under Application Support."""
    root = root or Path.home() / "Library" / "Application Support"
    targets: list[Target] = []
    if known_paths is None:
        known_paths = {target.path for target in TARGETS}
    else:
        known_paths = set(known_paths)
    scan_errors: list[OSError] = []

    for current, directories, _ in os.walk(root, topdown=True, onerror=scan_errors.append):
        current_path = Path(current)
        depth = len(current_path.relative_to(root).parts)
        if depth >= 6:
            directories.clear()
            continue
        for name in tuple(directories):
            lowered_name = name.lower()
            if depth == 0 and name in SKIPPED_APPLICATION_SUPPORT_ROOTS:
                directories.remove(name)
                continue
            if name.startswith(".") or lowered_name in NON_CACHE_DATA_DIRS:
                directories.remove(name)
                continue

            candidate = current_path / name
            is_cache = name in APPLICATION_SUPPORT_CACHE_NAMES or (
                lowered_name == "cache" and current_path.name == "Shared Dictionary"
            )
            if not is_cache:
                continue

            directories.remove(name)
            relative = candidate.relative_to(root)
            if relative.parts[0].startswith("com.apple.") or candidate in known_paths:
                continue

            if any(relative.parts[:len(prefix)] == prefix for prefix in BROWSER_SUPPORT_ROOTS):
                category = "browsers"
            elif relative.parts[0] == "Code":
                category = "developer"
            else:
                category = "apps"

            targets.append(
                Target(candidate, f"Discovered cache ({relative.as_posix()})", category)
            )
            known_paths.add(candidate)

    if scan_errors:
        print(f"  [info] Could not inspect {len(scan_errors)} Application Support directories")
    return targets


def sandboxed_app_cache_targets(
    root: Path | None = None,
    known_paths: set[Path] | None = None,
) -> list[Target]:
    """Discover canonical Caches folders in third-party app containers."""
    root = root or Path.home() / "Library" / "Containers"
    targets: list[Target] = []
    if known_paths is None:
        known_paths = {target.path for target in TARGETS}
    else:
        known_paths = set(known_paths)
    try:
        containers = list(root.iterdir())
    except OSError as exc:
        print(f"  [info] Could not scan app containers in {root}: {exc}")
        return targets

    for container in containers:
        if container.name.startswith("com.apple.") or "." not in container.name:
            continue
        cache_path = container / "Data" / "Library" / "Caches"
        if cache_path.is_dir() and cache_path not in known_paths:
            targets.append(
                Target(cache_path, f"Sandbox cache ({container.name})", "apps")
            )
            known_paths.add(cache_path)
    return targets


def application_directory() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def load_external_targets() -> list[Target]:
    """Load extra targets from an optional user-editable JSON config, so new
    paths can be added without touching this file."""
    candidates = [
        application_directory() / "targets.json",
        Path.home() / ".config" / "clear_caches" / "targets.json",
    ]
    extra: list[Target] = []
    for config_path in candidates:
        if not config_path.exists():
            continue
        try:
            entries = json.loads(config_path.read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            print(f"  [info] Could not read {config_path}: {exc}")
            continue
        if not isinstance(entries, list):
            print(f"  [info] Skipping malformed config {config_path}: expected a JSON list")
            continue
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                print(f"  [info] Skipping malformed entry {index} in {config_path}: expected an object")
                continue

            path_value = entry.get("path")
            label = entry.get("label")
            category = entry.get("category")
            if not isinstance(path_value, str) or not path_value.strip():
                print(f"  [info] Skipping malformed entry {index} in {config_path}: invalid path")
                continue
            if not isinstance(label, str) or not label.strip():
                print(f"  [info] Skipping malformed entry {index} in {config_path}: invalid label")
                continue
            if not isinstance(category, str) or category not in ALL_CATEGORIES:
                print(f"  [info] Skipping malformed entry {index} in {config_path}: invalid category")
                continue

            try:
                path = Path(path_value).expanduser()
                if not path.is_absolute():
                    raise ValueError("path must be absolute")
                path = path.resolve()
                home = Path.home().resolve()
            except (OSError, RuntimeError, ValueError) as exc:
                print(f"  [info] Skipping malformed entry {index} in {config_path}: {exc}")
                continue

            if home.is_relative_to(path):
                print(
                    f"  [info] Skipping unsafe entry {index} in {config_path}: "
                    "path is the home directory or one of its parents"
                )
                continue
            if path.exists() and not path.is_dir():
                print(f"  [info] Skipping malformed entry {index} in {config_path}: not a directory")
                continue

            extra.append(Target(path, label.strip(), category))
    return extra


def get_all_targets() -> list[Target]:
    """Collect all targets: static targets, browser profiles, Application Support,
    sandboxed app containers, and user-defined targets from config files."""
    targets = list(TARGETS)
    for root, name in (
        (Path.home() / "Library" / "Application Support" / "Google" / "Chrome", "Chrome"),
        (Path.home() / "Library" / "Application Support" / "Microsoft Edge", "Edge"),
        (Path.home() / "Library" / "Application Support" / "BraveSoftware" / "Brave-Browser", "Brave"),
    ):
        targets.extend(browser_profile_targets(root, name))

    known = {t.path for t in targets}
    targets.extend(application_support_cache_targets(known_paths=known))
    known = {t.path for t in targets}
    targets.extend(sandboxed_app_cache_targets(known_paths=known))
    targets.extend(stale_targets())
    targets.extend(load_external_targets())
    return targets

CATEGORY_LABELS: dict[str, str] = {
    "system":       "System Caches",
    "trash":        "Trash",
    "browsers":     "Browser Caches",
    "apps":         "Application Caches",
    "mail":         "Mail Cache",
    "ios_backups":  "iOS/iPadOS Backups ⚠",
    "quicklook":    "QuickLook Cache",
    "crashreports": "Crash & Diagnostic Reports",
    "developer":    "Developer Tools",
    "packages":     "Package Managers",
    "logs":         "JetBrains IDE Logs",
    "stale":        "Stale Leftovers (old IDE settings, broken symlinks)",
    "maintenance":  "Homebrew Maintenance (cleanup, autoremove)",
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


@dataclass
class TreeScan:
    size: int = 0
    is_old: bool = True
    errors: int = 0


def scan_tree(path: Path, cutoff: float | None = None) -> TreeScan:
    """Walk a tree once without following symlinks, summing regular-file sizes
    and checking whether every entry is older than ``cutoff``.

    Any entry that cannot be inspected makes the tree count as "not old", so
    age-filtered runs never remove something whose age is unknown.
    """
    result = TreeScan()
    pending = [path]
    while pending:
        current = pending.pop()
        try:
            metadata = current.lstat()
        except OSError:
            result.errors += 1
            result.is_old = False
            continue
        if cutoff is not None and metadata.st_mtime > cutoff:
            result.is_old = False
        if stat.S_ISREG(metadata.st_mode):
            result.size += metadata.st_size
        elif stat.S_ISDIR(metadata.st_mode):
            try:
                with os.scandir(current) as children:
                    pending.extend(Path(child.path) for child in children)
            except OSError:
                result.errors += 1
                result.is_old = False
    return result


def path_size(path: Path) -> int:
    if not os.path.lexists(path):
        return 0
    return scan_tree(path).size


def age_cutoff(older_than_days: float | None) -> float | None:
    return time.time() - older_than_days * 86400 if older_than_days is not None else None


@dataclass
class PlannedItem:
    path: Path
    size: int
    eligible: bool


@dataclass
class TargetPlan:
    target: Target
    items: list[PlannedItem]
    warnings: list[str]
    scan_errors: int = 0

    @property
    def size(self) -> int:
        return sum(item.size for item in self.items if item.eligible)


def plan_item(path: Path, cutoff: float | None) -> tuple[PlannedItem, int]:
    scan = scan_tree(path, cutoff)
    return PlannedItem(path, scan.size, cutoff is None or scan.is_old), scan.errors


def list_children(path: Path) -> tuple[list[Path], list[str]]:
    try:
        return list(path.iterdir()), []
    except (FileNotFoundError, NotADirectoryError):
        return [], []
    except PermissionError as exc:
        return [], [
            f"  Warning – no permission to read {path}: {exc}",
            "  Tip: grant Full Disk Access to Terminal in System Settings → Privacy & Security.",
        ]
    except OSError as exc:
        return [], [f"  Warning – could not read {path}: {exc}"]


def plan_target(target: Target, cutoff: float | None) -> TargetPlan:
    """Scan a target once and record each removable item with its size and
    age eligibility."""
    plan = TargetPlan(target, [], [])
    if target.remove_self:
        candidates = [target.path] if os.path.lexists(target.path) else []
    else:
        candidates, plan.warnings = list_children(target.path)
    for candidate in candidates:
        item, errors = plan_item(candidate, cutoff)
        plan.items.append(item)
        plan.scan_errors += errors
    return plan


def plan_targets_in_parallel(targets: list[Target], cutoff: float | None) -> dict[Path, TargetPlan]:
    """Plan many targets concurrently (I/O bound)."""
    if not targets:
        return {}
    with ThreadPoolExecutor(max_workers=min(16, len(targets))) as pool:
        plans = list(pool.map(lambda target: plan_target(target, cutoff), targets))
    return {plan.target.path: plan for plan in plans}


def refresh_plan(plan: TargetPlan, cutoff: float | None) -> None:
    """Add children created since planning (e.g. by apps that were just closed)."""
    if plan.target.remove_self:
        return
    known = {item.path for item in plan.items}
    children, _ = list_children(plan.target.path)
    for child in children:
        if child not in known:
            item, errors = plan_item(child, cutoff)
            plan.items.append(item)
            plan.scan_errors += errors


def move_to_trash(item: Path) -> None:
    trash_dir = Path.home() / ".Trash"
    trash_dir.mkdir(exist_ok=True)
    destination = trash_dir / item.name
    if os.path.lexists(destination):
        timestamp = time.time_ns()
        suffix = 0
        while True:
            candidate = trash_dir / f"{item.name}.{timestamp}.{suffix}"
            if not os.path.lexists(candidate):
                destination = candidate
                break
            suffix += 1
    shutil.move(str(item), str(destination))


def remove_item(path: Path, to_trash: bool) -> str:
    if to_trash:
        move_to_trash(path)
        return f"  Moved to Trash: {path}"
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()
    return f"  Removed: {path}"


def execute_plan(
    plan: TargetPlan,
    dry_run: bool,
    to_trash: bool = False,
) -> tuple[list[str], int, int]:
    """Returns (output_lines, removed_entries, reclaimed_bytes)."""
    lines = list(plan.warnings)
    removed_entries = 0
    reclaimed_bytes = 0
    for item in plan.items:
        if not item.eligible:
            lines.append(f"  [skipped-age] recent or age unavailable: {item.path}")
            continue
        if dry_run:
            verb = "would move to Trash" if to_trash else "would remove"
            lines.append(f"  [dry-run] {verb}: {item.path}")
        else:
            if not os.path.lexists(item.path):
                continue
            try:
                lines.append(remove_item(item.path, to_trash))
            except OSError as exc:
                lines.append(f"  Warning – could not remove {item.path}: {exc}")
                continue
        removed_entries += 1
        reclaimed_bytes += item.size
    return lines, removed_entries, reclaimed_bytes


def clear_directory(
    path: Path,
    dry_run: bool,
    older_than_days: float | None = None,
    to_trash: bool = False,
) -> tuple[list[str], int, int]:
    """Empty a directory. Returns (output_lines, removed_entries, reclaimed_bytes)."""
    plan = plan_target(Target(path, str(path), ""), age_cutoff(older_than_days))
    return execute_plan(plan, dry_run, to_trash)


def remove_path(
    path: Path,
    dry_run: bool,
    older_than_days: float | None = None,
    to_trash: bool = False,
) -> tuple[list[str], int, int]:
    """Remove the item itself (dir, file, or broken symlink).
    Returns (output_lines, removed_entries, reclaimed_bytes)."""
    plan = plan_target(Target(path, str(path), "", remove_self=True), age_cutoff(older_than_days))
    return execute_plan(plan, dry_run, to_trash)


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


def confirm(total_size: int, to_trash: bool, apps_count: int = 0) -> bool:
    if to_trash:
        print(f"\nEstimated size to move to Trash: {format_size(total_size)}")
    else:
        print(f"\nEstimated space to reclaim: {format_size(total_size)}")
    action = "move the listed items to Trash" if to_trash else "permanently delete the listed items"
    if apps_count > 0:
        warning = f"This will force-quit {apps_count} running application(s) and {action}."
    else:
        warning = f"This will {action}."
    reply = input(f"{warning} Continue? [y/N]: ")
    return reply.strip().lower() in {"y", "yes"}


def confirm_category(category_label: str) -> bool:
    reply = input(f"Clean [{category_label}]? [y/N]: ")
    return reply.strip().lower() in {"y", "yes"}


def applescript_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def send_notification(title: str, message: str) -> None:
    script = (
        f"display notification {applescript_string(message)} "
        f"with title {applescript_string(title)}"
    )
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


def schedule_program_arguments() -> list[str]:
    arguments = [sys.executable]
    if not getattr(sys, "frozen", False):
        arguments.append(str(Path(__file__).resolve()))
    arguments.extend(["--yes", "--no-reindex", "--no-kill-apps"])
    return arguments


def parse_schedule_time(time_str: str) -> tuple[int, int]:
    """Parse and validate schedule time string in HH:MM format."""
    parts = time_str.strip().split(":")
    if len(parts) != 2 or not (parts[0].isdigit() and parts[1].isdigit()):
        raise ValueError(
            f"Invalid time format '{time_str}'. Expected HH:MM (e.g. 03:00 or 14:30)."
        )
    hour, minute = int(parts[0]), int(parts[1])
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(
            f"Time out of range '{time_str}'. Hour must be 0-23 and minute 0-59."
        )
    return hour, minute


def install_schedule(time_str: str) -> None:
    try:
        hour, minute = parse_schedule_time(time_str)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    plist = {
        "Label": LAUNCH_AGENT_LABEL,
        "ProgramArguments": schedule_program_arguments(),
        "StartCalendarInterval": {
            "Hour": hour,
            "Minute": minute,
        },
        "StandardOutPath": str(LOG_DIR / "launchd.log"),
        "StandardErrorPath": str(LOG_DIR / "launchd.err.log"),
    }
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LAUNCH_AGENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Unload any previous version first so reinstalling picks up the new plist.
    run_launchctl("bootout", f"{launchd_domain()}/{LAUNCH_AGENT_LABEL}")
    LAUNCH_AGENT_PATH.write_bytes(plistlib.dumps(plist, fmt=plistlib.FMT_XML, sort_keys=False))
    result = run_launchctl("bootstrap", launchd_domain(), str(LAUNCH_AGENT_PATH))
    if result.returncode != 0:
        print(
            f"Error: launchctl bootstrap failed: {launchctl_error(result)}",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Scheduled daily run at {hour:02d}:{minute:02d} -> {LAUNCH_AGENT_PATH}")


def uninstall_schedule() -> None:
    result = run_launchctl("bootout", f"{launchd_domain()}/{LAUNCH_AGENT_LABEL}")
    if result.returncode != 0 and LAUNCH_AGENT_PATH.exists():
        print(f"  [info] launchctl bootout: {launchctl_error(result)}")
    if LAUNCH_AGENT_PATH.exists():
        LAUNCH_AGENT_PATH.unlink()
    print(f"Removed schedule: {LAUNCH_AGENT_PATH}")


def launchd_domain() -> str:
    return f"gui/{os.getuid()}"


def run_launchctl(*arguments: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["launchctl", *arguments], capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(["launchctl", *arguments], 1, "", str(exc))


def launchctl_error(result: subprocess.CompletedProcess[str]) -> str:
    output = (result.stderr or result.stdout or "").strip()
    return output.splitlines()[0] if output else f"exit code {result.returncode}"


# ---------------------------------------------------------------------------
# Root detection
# ---------------------------------------------------------------------------

def is_root_user() -> bool:
    """Return True if running with root privileges (UID 0)."""
    return hasattr(os, "geteuid") and os.geteuid() == 0


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
        label="Launch Services – rebuild app database",
        cmd=[
            "/System/Library/Frameworks/CoreServices.framework"
            "/Frameworks/LaunchServices.framework/Support/lsregister",
            "-r",
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


# ---------------------------------------------------------------------------
# Homebrew maintenance
# ---------------------------------------------------------------------------

@dataclass
class MaintenanceTask:
    label: str
    cmd: list[str]
    dry_run_cmd: list[str]


def maintenance_tasks() -> list[MaintenanceTask]:
    brew = shutil.which("brew") or next(
        (p for p in ("/opt/homebrew/bin/brew", "/usr/local/bin/brew") if Path(p).exists()), None
    )
    if not brew:
        return []
    return [
        MaintenanceTask(
            "Homebrew – remove unused dependencies (autoremove)",
            [brew, "autoremove"],
            [brew, "autoremove", "--dry-run"],
        ),
        MaintenanceTask(
            "Homebrew – remove old versions & all downloads (cleanup --prune=all -s)",
            [brew, "cleanup", "--prune=all", "-s"],
            [brew, "cleanup", "--prune=all", "-s", "-n"],
        ),
    ]


def run_maintenance(tasks: list[MaintenanceTask], dry_run: bool) -> None:
    print(f"\n[{CATEGORY_LABELS['maintenance']}]")
    if not tasks:
        print("  Skipped (Homebrew not found)")
        return
    for task in tasks:
        cmd = task.dry_run_cmd if dry_run else task.cmd
        prefix = "[dry-run] " if dry_run else ""
        print(f"  ▶ {prefix}{task.label} … ", end="", flush=True)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"Warning – {exc}")
            continue
        print("OK" if result.returncode == 0 else "Warning – non-zero exit")
        output = (result.stdout + result.stderr).strip().splitlines()
        for line in output[-5:]:
            print(f"      {line}")


# ---------------------------------------------------------------------------
# Running Applications Management
# ---------------------------------------------------------------------------

@dataclass
class RunningApp:
    name: str
    pid: int
    bundle_id: str = ""
    bundle_path: str = ""
    app_type: str = ""


PROTECTED_BUNDLE_IDS: set[str] = {
    # System desktop services & WindowServer
    "com.apple.finder",
    "com.apple.dock",
    "com.apple.loginwindow",
    "com.apple.WindowManager",
    "com.apple.systemuiserver",
    "com.apple.controlcenter",
    "com.apple.notificationcenterui",
    "com.apple.CoreServicesUIAgent",
    "com.apple.talagent",
    "com.apple.Spotlight",
    # Terminal emulators (never terminate the user's terminal window)
    "com.apple.Terminal",
    "com.googlecode.iterm2",
    "org.alacritty",
    "net.kovidgoyal.kitty",
    "dev.warp.Warp-Stable",
    "com.mitchellh.ghostty",
    "co.zeit.hyper",
}

PROTECTED_APP_NAMES: set[str] = {
    "Finder",
    "Dock",
    "loginwindow",
    "WindowManager",
    "SystemUIServer",
    "ControlCenter",
    "Centrum sterowania",
    "NotificationCenter",
    "Spotlight",
    "Terminal",
    "iTerm2",
    "iTerm",
    "Alacritty",
    "kitty",
    "Warp",
    "Ghostty",
    "Hyper",
    "launchd",
    "kernel_task",
    "WindowServer",
}

TARGET_BUNDLE_PREFIXES: tuple[str, ...] = (
    "com.google.Chrome",
    "org.mozilla.firefox",
    "com.apple.Safari",
    "com.microsoft.edgemac",
    "com.brave.Browser",
    "com.operasoftware.Opera",
    "com.vivaldi.Vivaldi",
    "company.thebrowser.Browser",
    "com.tinyspeck.slackmacgap",
    "com.spotify.client",
    "com.microsoft.teams",
    "com.microsoft.teams2",
    "com.skype.skype",
    "com.hnc.discord",
    "com.valvesoftware.steam",
    "net.whatsapp.WhatsApp",
    "ru.keepcoder.Telegram",
    "com.github.GitHubClient",
    "com.bitwarden.desktop",
    "io.balena.etcher",
    "com.google.drivefs",
    "com.microsoft.OneDrive",
    "com.apple.mail",
    "com.apple.dt.Xcode",
)

TARGET_APP_NAMES: set[str] = {
    "google chrome",
    "firefox",
    "safari",
    "microsoft edge",
    "brave browser",
    "opera",
    "vivaldi",
    "arc",
    "slack",
    "spotify",
    "microsoft teams",
    "teams",
    "skype",
    "discord",
    "steam",
    "whatsapp",
    "telegram",
    "github desktop",
    "bitwarden",
    "balenaetcher",
    "google drive",
    "onedrive",
    "mail",
    "xcode",
}


def get_protected_pids() -> set[int]:
    """Identify PIDs that must never be terminated (self, parents, host IDE)."""
    pids = {os.getpid(), os.getppid()}
    vscode_pid = os.environ.get("VSCODE_PID")
    if vscode_pid and vscode_pid.isdigit():
        pids.add(int(vscode_pid))

    curr = os.getppid()
    while curr > 1:
        try:
            res = subprocess.run(
                ["ps", "-o", "ppid=", "-p", str(curr)],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if res.returncode == 0 and res.stdout.strip().isdigit():
                curr = int(res.stdout.strip())
                pids.add(curr)
            else:
                break
        except Exception:
            break
    return pids


def get_running_applications() -> list[RunningApp]:
    """Discover running user and target applications to close before cache cleanup."""
    protected_pids = get_protected_pids()
    host_term = os.environ.get("TERM_PROGRAM", "").lower()
    apps: list[RunningApp] = []
    seen_pids: set[int] = set()

    try:
        res = subprocess.run(
            ["/usr/bin/lsappinfo", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if res.returncode == 0:
            blocks = re.split(r"(?=^\s*\d+\)\s+\")", res.stdout, flags=re.MULTILINE)
            for block in blocks:
                m_name = re.search(r"^\s*\d+\)\s+\"([^\"]+)\"", block, re.MULTILINE)
                m_pid = re.search(r"\bpid\s*=\s*(\d+)", block)
                if not (m_name and m_pid):
                    continue
                pid = int(m_pid.group(1))
                if pid in seen_pids or pid in protected_pids:
                    continue

                m_bundle = re.search(r"bundleID=\"([^\"]+)\"", block)
                m_type = re.search(r"type=\"([^\"]+)\"", block)
                m_path = re.search(r"bundle path=\"([^\"]+)\"", block)

                name = m_name.group(1)
                bundle_id = m_bundle.group(1) if m_bundle else ""
                app_type = m_type.group(1) if m_type else ""
                bundle_path = m_path.group(1) if m_path else ""

                if bundle_id in PROTECTED_BUNDLE_IDS or name in PROTECTED_APP_NAMES:
                    continue

                lower_name = name.lower()
                lower_bundle = bundle_id.lower()
                if "vscode" in host_term or "code" in host_term or os.environ.get("VSCODE_PID"):
                    if "code" in lower_name or "vscode" in lower_bundle:
                        continue

                matches_target = (
                    lower_name in TARGET_APP_NAMES
                    or any(bundle_id.startswith(p) for p in TARGET_BUNDLE_PREFIXES)
                )

                if matches_target:
                    seen_pids.add(pid)
                    apps.append(
                        RunningApp(
                            name=name,
                            pid=pid,
                            bundle_id=bundle_id,
                            bundle_path=bundle_path,
                            app_type=app_type,
                        )
                    )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        print(f"  [info] Could not query running applications via lsappinfo: {exc}")

    return apps


def still_running_apps(apps: list[RunningApp]) -> list[RunningApp]:
    """Keep only apps whose PID still belongs to the same application.

    This narrows, but cannot close, the window in which a PID reused after
    confirmation could be signalled, because the check and kill are separate."""
    if not apps:
        return []
    current = {(app.pid, app.name, app.bundle_id) for app in get_running_applications()}
    return [app for app in apps if (app.pid, app.name, app.bundle_id) in current]


def close_running_applications(
    apps: list[RunningApp],
    dry_run: bool = False,
) -> list[str]:
    """Force close running applications so cache files can be safely and completely deleted."""
    if not apps:
        return []

    lines: list[str] = []
    print(f"\n[Force-Closing Applications ({len(apps)})]")

    if dry_run:
        for app in apps:
            line = f"  [dry-run] would force quit: {app.name} (PID {app.pid})"
            print(line)
            lines.append(line)
        return lines

    # Step 1: Send SIGTERM for quick graceful flush
    for app in apps:
        try:
            os.kill(app.pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass

    # Wait briefly up to 0.5s
    time.sleep(0.5)

    # Step 2: Force kill (SIGKILL) any processes still running
    closed_count = 0
    for app in apps:
        print(f"  ▶ {app.name} (PID {app.pid}) … ", end="", flush=True)
        still_running = True
        try:
            os.kill(app.pid, 0)
        except ProcessLookupError:
            still_running = False
        except PermissionError:
            still_running = True

        if still_running:
            try:
                os.kill(app.pid, signal.SIGKILL)
                print("Force Quit (SIGKILL)")
                lines.append(f"  Force-closed: {app.name} (PID {app.pid})")
                closed_count += 1
            except ProcessLookupError:
                print("OK")
                lines.append(f"  Closed: {app.name} (PID {app.pid})")
                closed_count += 1
            except PermissionError as exc:
                print(f"Warning – permission denied: {exc}")
                lines.append(f"  Warning – could not close {app.name}: {exc}")
        else:
            print("OK")
            lines.append(f"  Closed: {app.name} (PID {app.pid})")
            closed_count += 1

    print(f"Finished closing applications ({closed_count}/{len(apps)}).\n")
    return lines


def non_negative_days(value: str) -> float:
    try:
        days = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid number of days: {value!r}") from None
    if not math.isfinite(days) or days < 0:
        raise argparse.ArgumentTypeError(f"number of days must be a non-negative number: {value!r}")
    return days


def format_signed_size(size_bytes: int) -> str:
    sign = "-" if size_bytes < 0 else "+"
    return f"{sign}{format_size(abs(size_bytes))}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Clear cache files, logs, and Trash on macOS.\n\n"
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
    cat_group = parser.add_mutually_exclusive_group()
    cat_group.add_argument(
        "--all",
        action="store_true",
        help="Enable all categories, including destructive ones.",
    )
    cat_group.add_argument(
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
    reindex_group = parser.add_mutually_exclusive_group()
    reindex_group.add_argument(
        "--no-reindex",
        action="store_true",
        default=False,
        help="Keep the default behavior of skipping reindexing and service restarts.",
    )
    reindex_group.add_argument(
        "--reindex",
        action="store_true",
        default=False,
        help="Run reindexing and service restarts after cleaning.",
    )
    parser.add_argument(
        "--older-than",
        metavar="DAYS",
        type=non_negative_days,
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
        "--no-kill-apps",
        action="store_true",
        help="Do not force-quit running applications before cleaning caches.",
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

    # Everything cleaned lives in the current user's home; root would target the wrong
    # home and leave root-owned files behind.
    if is_root_user():
        parser.error("do not run as root or with sudo; run as the logged-in user")

    if args.install_schedule:
        install_schedule(args.install_schedule)
        return 0
    if args.uninstall_schedule:
        uninstall_schedule()
        return 0

    if args.all:
        active_categories = set(ALL_CATEGORIES)
    elif args.categories:
        active_categories = set(args.categories)
    else:
        active_categories = set(DEFAULT_CATEGORIES)

    if args.exclude:
        active_categories -= set(args.exclude)

    if args.to_trash and "trash" in active_categories:
        parser.error("--to-trash cannot be combined with the trash category")

    active_targets = [t for t in get_all_targets() if t.category in active_categories]
    active_targets = resolve_targets(active_targets)

    # Group by category once to avoid repeated filtering
    cats_to_targets: dict[str, list[Target]] = {}
    for t in active_targets:
        cats_to_targets.setdefault(t.category, []).append(t)

    # Scan every target once; the plan is reused for cleaning, so sizes and
    # age checks are not recomputed.
    cutoff = age_cutoff(args.older_than)
    plans = plan_targets_in_parallel(active_targets, cutoff)
    apps_to_close = get_running_applications() if not args.no_kill_apps else []

    # Print plan grouped by category
    for cat in sorted(active_categories):
        cat_targets = cats_to_targets.get(cat, [])
        if not cat_targets:
            continue
        print(f"\n[{CATEGORY_LABELS[cat]}]")
        for t in cat_targets:
            plan = plans[t.path]
            exists = "✓" if os.path.lexists(t.path) else "–"
            note = f", {plan.scan_errors} unreadable item(s)" if plan.scan_errors else ""
            print(f"  {exists} {t.label}  ({format_size(plan.size)}{note})")

    brew_tasks = maintenance_tasks() if "maintenance" in active_categories else []
    if brew_tasks:
        print(f"\n[{CATEGORY_LABELS['maintenance']}]")
        for task in brew_tasks:
            print(f"  ▶ {task.label}")

    if apps_to_close:
        print(f"\n[Running Applications to Force-Quit ({len(apps_to_close)})]")
        for app in apps_to_close:
            print(f"  ▶ {app.name} (PID: {app.pid})")

    total_size = sum(plan.size for plan in plans.values())

    if not args.dry_run and not args.yes and not confirm(total_size, args.to_trash, apps_count=len(apps_to_close)):
        print("Cancelled.")
        return 1

    if apps_to_close:
        if not args.dry_run:
            apps_to_close = still_running_apps(apps_to_close)
        close_running_applications(apps_to_close, dry_run=args.dry_run)

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
            plan = plans[t.path]
            if not args.dry_run:
                refresh_plan(plan, cutoff)
            lines, entries, size_bytes = execute_plan(plan, args.dry_run, to_trash=args.to_trash)
            grand_entries += entries
            grand_bytes += size_bytes
            cat_entries += entries
            cat_bytes += size_bytes
            if args.to_trash:
                verb = "would move to Trash" if args.dry_run else "moved to Trash"
            else:
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

    if args.to_trash:
        verb = "Would move to Trash" if args.dry_run else "Moved to Trash"
    else:
        verb = "Would reclaim" if args.dry_run else "Reclaimed"
    print(
        f"Done. {verb} ~{format_size(grand_bytes)} across {grand_entries} item(s)."
    )

    if "maintenance" in active_categories and not (
        args.interactive and not confirm_category(CATEGORY_LABELS["maintenance"])
    ):
        run_maintenance(brew_tasks, args.dry_run)

    if disk_before is not None:
        disk_after = shutil.disk_usage(Path.home()).free
        print(f"Free disk space: {format_size(disk_before)} -> {format_size(disk_after)} "
              f"({format_signed_size(disk_after - disk_before)})")

    if args.reindex:
        run_reindex(args.dry_run)

    if not args.no_log:
        log_path = write_log({
            "timestamp": datetime.now().isoformat(),
            "dry_run": args.dry_run,
            "to_trash": args.to_trash,
            "closed_apps": [a.name for a in apps_to_close] if not args.dry_run else [],
            "total_entries": grand_entries,
            "total_bytes": grand_bytes,
            "categories": category_summary,
        })
        if log_path:
            print(f"Log written: {log_path}")

    if not args.dry_run and not args.no_notify:
        action = "Moved to Trash" if args.to_trash else "Reclaimed"
        send_notification(
            "Clear Caches", f"{action} {format_size(grand_bytes)} ({grand_entries} items)."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
