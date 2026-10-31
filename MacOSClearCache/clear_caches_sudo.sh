#!/bin/sh
# Runs the root-only cleanup (broken symlinks in /usr/local/bin) with sudo.
# Extra arguments are passed through, e.g.: ./clear_caches_sudo.sh --dry-run
# Set PYTHON to override the interpreter used when dist/clear_caches is absent.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"

# The wrapper always targets the "stale" category; category options would conflict.
for arg in "$@"; do
    case "$arg" in
        --all|--categories|--categories=*|--exclude|--exclude=*)
            echo "Error: $arg is not supported; this wrapper only cleans the 'stale' category." >&2
            exit 2
            ;;
    esac
done

BIN="$DIR/dist/clear_caches"
if [ -x "$BIN" ]; then
    # Skip a binary built before the latest source change to avoid running stale code.
    if [ -z "$(find "$DIR/clear_caches.py" -newer "$BIN" 2>/dev/null)" ]; then
        exec sudo "$BIN" --categories stale --no-kill-apps "$@"
    fi
    echo "Warning: $BIN is older than clear_caches.py; using Python instead." >&2
    echo "         Rebuild with: python3 -m PyInstaller --clean clear_caches.spec" >&2
fi

# Resolve the interpreter before sudo, which may reset PATH and drop the active venv.
PYTHON="${PYTHON:-$(command -v python3 || true)}"
if [ -z "$PYTHON" ] || [ ! -x "$PYTHON" ]; then
    echo "Error: python3 not found; set PYTHON or build dist/clear_caches." >&2
    exit 1
fi
if ! "$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
    echo "Error: $PYTHON is older than Python 3.10." >&2
    exit 1
fi

exec sudo "$PYTHON" "$DIR/clear_caches.py" --categories stale --no-kill-apps "$@"
