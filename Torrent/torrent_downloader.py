#!/usr/bin/env python3
"""Prosty downloader torrentow oparty o aria2."""

from __future__ import annotations

import argparse
import logging
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    import aria2p
except ImportError:  # pragma: no cover - zalezne od srodowiska
    aria2p = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pobieranie torrentow z magnet linku lub pliku .torrent.",
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="Magnet link lub sciezka do pliku .torrent",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="downloads",
        help="Katalog docelowy dla pobieranych danych (domyslnie: downloads)",
    )
    parser.add_argument(
        "--listen-port",
        type=int,
        default=6881,
        help="Port nasluchu BitTorrent (domyslnie: 6881)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Maksymalny czas oczekiwania na metadane w sekundach (domyslnie: 120)",
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Po zakonczeniu pobierania pozostaw klient w trybie seedowania.",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Uruchom prosty tryb interaktywny do podania zrodla i opcji.",
    )
    parser.add_argument(
        "-f",
        "--batch-file",
        help="Plik tekstowy z lista magnet linkow lub sciezek do plikow .torrent.",
    )
    parser.add_argument(
        "--log-file",
        default="torrent_downloader.log",
        help="Sciezka do pliku logowania (domyslnie: torrent_downloader.log)",
    )
    return parser


def setup_logging(log_file: str) -> Path:
    log_path = Path(log_file).expanduser().resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
        ],
        force=True,
    )
    logging.info("Uruchomienie skryptu torrent downloader")
    return log_path


def prompt_bool(message: str, default: bool = False) -> bool:
    suffix = "[T/n]" if default else "[t/N]"
    answer = input(f"{message} {suffix}: ").strip().lower()
    if not answer:
        return default
    return answer in {"t", "tak", "y", "yes"}


def interactive_args(args: argparse.Namespace) -> argparse.Namespace:
    print("Tryb interaktywny torrent downloader")
    logging.info("Uruchomiono tryb interaktywny")

    if not args.source and not args.batch_file:
        source = input("Podaj magnet link, plik .torrent albo sciezke do listy: ").strip()
        if source.endswith(".txt") and Path(source).expanduser().exists():
            args.batch_file = source
        else:
            args.source = source

    if args.output == "downloads":
        output = input("Katalog docelowy [downloads]: ").strip()
        if output:
            args.output = output

    if args.listen_port == 6881:
        port = input("Port nasluchu [6881]: ").strip()
        if port:
            args.listen_port = int(port)

    if args.timeout == 120:
        timeout = input("Timeout metadanych w sekundach [120]: ").strip()
        if timeout:
            args.timeout = int(timeout)

    if not args.seed:
        args.seed = prompt_bool("Czy pozostawic seedowanie po pobraniu?", default=False)

    return args


def resolve_sources(args: argparse.Namespace) -> list[str]:
    sources: list[str] = []

    if args.source:
        sources.append(args.source)

    if args.batch_file:
        batch_path = Path(args.batch_file).expanduser().resolve()
        if not batch_path.is_file():
            logging.error("Nie znaleziono pliku z lista: %s", batch_path)
            print(f"Nie znaleziono pliku z lista: {batch_path}", file=sys.stderr)
            raise SystemExit(1)

        lines = batch_path.read_text(encoding="utf-8").splitlines()
        batch_sources = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        sources.extend(batch_sources)

    unique_sources: list[str] = []
    seen: set[str] = set()
    for source in sources:
        if source in seen:
            continue
        seen.add(source)
        unique_sources.append(source)

    if not unique_sources:
        logging.error("Nie podano zadnego zrodla do pobierania")
        print("Musisz podac source, --interactive lub --batch-file.", file=sys.stderr)
        raise SystemExit(2)

    logging.info("Przygotowano %d unikalnych zrodel", len(unique_sources))
    return unique_sources


def ensure_aria2() -> None:
    if aria2p is not None and shutil.which("aria2c"):
        return

    logging.error("Brak zaleznosci aria2/aria2p")
    print(
        "Brak zaleznosci 'aria2c' lub biblioteki 'aria2p'. Zainstaluj zaleznosci: brew install aria2 && pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        probe.listen(1)
        return int(probe.getsockname()[1])


class Aria2Runtime:
    def __init__(self, listen_port: int, output_dir: Path) -> None:
        self.listen_port = listen_port
        self.output_dir = output_dir
        self.rpc_port = find_free_port()
        self.rpc_secret = secrets.token_hex(16)
        self.runtime_dir = tempfile.TemporaryDirectory(prefix="torrent-downloader-aria2-")
        self.client: aria2p.Client | None = None
        self.api: aria2p.API | None = None

    def start(self) -> aria2p.API:
        aria2c_path = shutil.which("aria2c")
        if aria2c_path is None or aria2p is None:
            ensure_aria2()

        command = [
            aria2c_path or "aria2c",
            "--daemon=true",
            "--enable-rpc=true",
            "--rpc-listen-all=false",
            f"--rpc-listen-port={self.rpc_port}",
            f"--rpc-secret={self.rpc_secret}",
            f"--dir={self.output_dir}",
            f"--listen-port={self.listen_port}-{self.listen_port + 10}",
            f"--dht-listen-port={self.listen_port}-{self.listen_port + 10}",
            f"--stop-with-process={os.getpid()}",
            "--max-concurrent-downloads=1",
            "--summary-interval=0",
            "--console-log-level=warn",
            "--bt-save-metadata=true",
            "--no-conf=true",
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)

        self.client = aria2p.Client(host="http://localhost", port=self.rpc_port, secret=self.rpc_secret)
        self.api = aria2p.API(self.client)

        deadline = time.monotonic() + 10
        while True:
            try:
                self.client.get_version()
                break
            except Exception:
                if time.monotonic() >= deadline:
                    logging.exception("Nie udalo sie uruchomic aria2 RPC")
                    print("Nie udalo sie uruchomic aria2 RPC.", file=sys.stderr)
                    raise SystemExit(1)
                time.sleep(0.2)

        logging.info("Uruchomiono aria2 RPC na porcie %d", self.rpc_port)
        return self.api

    def close(self) -> None:
        if self.client is not None:
            shutdown = getattr(self.client, "shutdown", None)
            if shutdown is not None:
                try:
                    shutdown()
                except Exception:
                    logging.debug("Nie udalo sie zamknac aria2 RPC", exc_info=True)
        self.runtime_dir.cleanup()


def add_download(api: aria2p.API, source: str, output_dir: Path, seed: bool) -> aria2p.Download:
    options = {
        "dir": str(output_dir),
        "bt-save-metadata": "true",
    }
    if seed:
        options["seed-ratio"] = "0.0"
    else:
        options["seed-time"] = "0"

    if source.startswith("magnet:"):
        logging.info("Dodawanie magnet linku")
        return api.add_magnet(source, options=options)

    torrent_path = Path(source).expanduser().resolve()
    if not torrent_path.is_file():
        logging.error("Nie znaleziono pliku torrent: %s", torrent_path)
        print(f"Nie znaleziono pliku torrent: {torrent_path}", file=sys.stderr)
        raise SystemExit(1)

    logging.info("Dodawanie pliku torrent: %s", torrent_path)
    return api.add_torrent(str(torrent_path), options=options)


def fail_download(download: aria2p.Download, message: str) -> None:
    error_message = getattr(download, "error_message", "") or download.status
    logging.error("%s: %s", message, error_message)
    print(f"{message}: {error_message}", file=sys.stderr)
    raise SystemExit(1)


def wait_for_metadata(download: aria2p.Download, timeout: int) -> aria2p.Download:
    started = time.monotonic()
    current = download
    while current.is_metadata:
        current.update()
        if current.followed_by:
            current = current.followed_by[0]
            current.update()
            logging.info("Pobrano metadane torrentu")
            print("Metadane pobrane." + " " * 20)
            return current
        if current.has_failed or current.is_removed:
            fail_download(current, "Nie udalo sie pobrac metadanych torrentu")
        if time.monotonic() - started > timeout:
            current.remove(force=True, files=False)
            logging.error("Przekroczono czas oczekiwania na metadane torrentu")
            print("Przekroczono czas oczekiwania na metadane torrentu.", file=sys.stderr)
            raise SystemExit(1)
        print("Oczekiwanie na metadane...", end="\r", flush=True)
        time.sleep(1)
    return current


def format_size(size_bytes: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size_bytes} B"


def print_progress(download: aria2p.Download) -> str:
    progress = download.progress
    download_rate = download.download_speed / 1000
    upload_rate = download.upload_speed / 1000
    peers = download.connections
    total_done = format_size(download.completed_length)
    total_wanted = format_size(download.total_length)

    line = (
        f"{progress:6.2f}% | {total_done}/{total_wanted} | "
        f"DL {download_rate:8.1f} kB/s | UL {upload_rate:8.1f} kB/s | peers {peers:3d}"
    )
    print(line, end="\r", flush=True)
    return line


def download(download_item: aria2p.Download, seed: bool) -> None:
    last_logged_second = -1
    while True:
        download_item.update()
        if download_item.has_failed or download_item.is_removed:
            fail_download(download_item, "Pobieranie nie powiodlo sie")

        if seed and download_item.seeder:
            logging.info("Tryb seedowania aktywny")
            print("\nTryb seedowania aktywny. Zatrzymaj program Ctrl+C.")
            try:
                while True:
                    download_item.update()
                    if download_item.has_failed or download_item.is_removed:
                        fail_download(download_item, "Seedowanie zostalo przerwane")
                    line = print_progress(download_item)
                    elapsed_second = int(time.monotonic())
                    if elapsed_second != last_logged_second:
                        logging.info("Seedowanie: %s", line)
                        last_logged_second = elapsed_second
                    time.sleep(5)
            except KeyboardInterrupt:
                logging.info("Zatrzymano seedowanie przez uzytkownika")
                print("\nZatrzymano seedowanie.")
                return

        line = print_progress(download_item)
        elapsed_second = int(time.monotonic())
        if elapsed_second != last_logged_second:
            logging.info("Postep: %s", line)
            last_logged_second = elapsed_second
        if download_item.is_complete:
            break
        time.sleep(1)

    final_line = print_progress(download_item)
    logging.info("Pobieranie zakonczone: %s", final_line)
    print("\nPobieranie zakonczone.")


def run_download(api: aria2p.API, source: str, output_dir: Path, timeout: int, seed: bool) -> None:
    logging.info("Rozpoczecie obslugi zrodla: %s", source)
    download_item = add_download(api, source, output_dir, seed)
    download_item = wait_for_metadata(download_item, timeout)

    name = download_item.name or "nieznany torrent"
    logging.info("Start pobierania: %s", name)
    print(f"Start pobierania: {name}")
    print(f"Katalog docelowy: {output_dir}")
    download(download_item, seed)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    log_path = setup_logging(args.log_file)
    logging.info("Plik logu: %s", log_path)

    if args.interactive:
        try:
            args = interactive_args(args)
        except ValueError as error:
            logging.exception("Bledna wartosc w trybie interaktywnym")
            print(f"Bledna wartosc w trybie interaktywnym: {error}", file=sys.stderr)
            raise SystemExit(2) from error

    sources = resolve_sources(args)

    ensure_aria2()

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Katalog docelowy: %s", output_dir)

    runtime = Aria2Runtime(args.listen_port, output_dir)
    api = runtime.start()

    try:
        for index, source in enumerate(sources, start=1):
            if len(sources) > 1:
                print(f"\n[{index}/{len(sources)}] Zrodlo: {source}")
            run_download(api, source, output_dir, args.timeout, args.seed)
    except KeyboardInterrupt:
        logging.info("Przerwano pobieranie przez uzytkownika")
        print("\nPrzerwano pobieranie.")
        raise SystemExit(130)
    except Exception:
        logging.exception("Nieoczekiwany blad podczas pobierania")
        raise
    finally:
        runtime.close()


if __name__ == "__main__":
    main()