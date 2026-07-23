# Torrent Downloader

A simple Python script for downloading torrents from a magnet link or a `.torrent` file.

## Requirements

- Python 3.14.5
- `aria2` 1.37+
- `aria2p` library 0.12.1

Installation:

```bash
brew install aria2
python3.14 -m venv ~/.venv
~/.venv/bin/python -m pip install -r requirements.txt
```

## Usage

Magnet link:

```bash
python torrent_downloader.py "magnet:?xt=urn:btih:..."
```

`.torrent` file:

```bash
python torrent_downloader.py /path/to/file.torrent
```

Text file with multiple entries:

```bash
python torrent_downloader.py --batch-file list.txt
```

Interactive mode:

```bash
python torrent_downloader.py --interactive
```

Run without arguments:

```bash
python torrent_downloader.py
```

The script will then ask for the destination directory and for a magnet link or path to a `.torrent` file, similar to how `YT-DLP` asks for a directory and URLs.
By default it only asks for these two items.

Additional options:

- `--listen-port 6881` - BitTorrent client listen port
- `--listen-port-end 6891` - end of the BitTorrent and DHT port range
- `--rpc-port 0` - aria2 RPC port exposed on host interfaces; defaults to a random free port
- `--listen-address 0.0.0.0` - RPC listen scope: `0.0.0.0` or `localhost`
- `--local-only` - shortcut for `--listen-address localhost`
- `--public-rpc` - shortcut for `--listen-address 0.0.0.0`
- `--timeout 120` - maximum time to wait for metadata
- `--seed` - keeps the client in seeding mode after the download finishes
- `--allow-overwrite` - allows overwriting an existing destination file when there's no `*.aria2` file
- `--interactive` - forces prompts for the source and additional options in the terminal
- `--batch-file list.txt` - reads multiple sources from a text file, one per line
- `--log-file ./torrent.log` - writes logs to the specified file

Example `list.txt` file:

```text

# comments are ignored

magnet:?xt=urn:btih:...
/path/to/archive.torrent
```

## Notes

The script does not bypass any protections and should only be used to download content you have the rights to.

The script runs `aria2c` in RPC mode on a host port and shuts it down once the work is finished.
RPC is protected with a random `rpc-secret`, but the port remains exposed on host interfaces.
BitTorrent and DHT ports use the `6881-6891` range by default, which can be changed via `--listen-port` and `--listen-port-end`.
If you want to restrict RPC to this machine only, use `--local-only`.
If you want to explicitly expose RPC on host interfaces, use `--public-rpc`.
The `--local-only` and `--public-rpc` flags cannot be combined in a single run.
The `--listen-address` option only controls RPC exposure: `localhost` restricts RPC to this machine, while `0.0.0.0` exposes RPC on host interfaces. `aria2c` does not offer an equivalent option for binding IPv4 BitTorrent to a specific address.
If you don't provide `--rpc-port`, the script automatically picks a random free RPC port on the host. An explicitly provided `--rpc-port` causes a hard failure on conflict.
In interactive mode, the script also asks whether it should overwrite existing destination files.

While running, the script writes logs to the `torrent_downloader.log` file in the current directory, unless you provide a different path via `--log-file`.
