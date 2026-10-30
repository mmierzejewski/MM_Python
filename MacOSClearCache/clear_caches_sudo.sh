#!/bin/sh
# Runs the root-only cleanup (broken symlinks in /usr/local/bin) with sudo.
# Extra arguments are passed through, e.g.: ./clear_caches_sudo.sh --dry-run
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
exec sudo "$DIR/dist/clear_caches" --categories stale --no-kill-apps "$@"
