#!/usr/bin/env python3
"""Prosty downloader torrentow oparty o libtorrent."""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

try:
    import libtorrent as lt
except ImportError:  # pragma: no cover - zalezne od srodowiska
    lt = None


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


def ensure_libtorrent() -> None:
    if lt is not None:
        return

    logging.error("Brak biblioteki libtorrent")
    print(
        "Brak biblioteki 'libtorrent'. Zainstaluj zaleznosci: pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)


def create_session(listen_port: int) -> lt.session:
    session = lt.session()
    session.listen_on(listen_port, listen_port + 10)
    settings = {
        "alert_mask": lt.alert.category_t.error_notification
        | lt.alert.category_t.storage_notification
        | lt.alert.category_t.status_notification,
        "enable_dht": True,
        "enable_lsd": True,
        "enable_upnp": True,
        "enable_natpmp": True,
    }
    session.apply_settings(settings)
    session.start_dht()
    logging.info("Utworzono sesje BitTorrent na porcie %d", listen_port)
    return session


def add_torrent(session: lt.session, source: str, output_dir: Path) -> lt.torrent_handle:
    params = {"save_path": str(output_dir)}

    if source.startswith("magnet:"):
        logging.info("Dodawanie magnet linku")
        return lt.add_magnet_uri(session, source, params)

    torrent_path = Path(source).expanduser().resolve()
    if not torrent_path.is_file():
        logging.error("Nie znaleziono pliku torrent: %s", torrent_path)
        print(f"Nie znaleziono pliku torrent: {torrent_path}", file=sys.stderr)
        raise SystemExit(1)

    logging.info("Dodawanie pliku torrent: %s", torrent_path)
    torrent_info = lt.torrent_info(str(torrent_path))
    params["ti"] = torrent_info
    return session.add_torrent(params)


def wait_for_metadata(handle: lt.torrent_handle, timeout: int) -> None:
    started = time.monotonic()
    while not handle.status().has_metadata:
        if time.monotonic() - started > timeout:
            logging.error("Przekroczono czas oczekiwania na metadane torrentu")
            print("Przekroczono czas oczekiwania na metadane torrentu.", file=sys.stderr)
            raise SystemExit(1)
        print("Oczekiwanie na metadane...", end="\r", flush=True)
        time.sleep(1)
    logging.info("Pobrano metadane torrentu")
    print("Metadane pobrane." + " " * 20)


def format_size(size_bytes: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size_bytes} B"


def print_progress(handle: lt.torrent_handle) -> str:
    status = handle.status()
    progress = status.progress * 100
    download_rate = status.download_rate / 1000
    upload_rate = status.upload_rate / 1000
    peers = status.num_peers
    total_done = format_size(status.total_done)
    total_wanted = format_size(status.total_wanted)

    line = (
        f"{progress:6.2f}% | {total_done}/{total_wanted} | "
        f"DL {download_rate:8.1f} kB/s | UL {upload_rate:8.1f} kB/s | peers {peers:3d}"
    )
    print(line, end="\r", flush=True)
    return line


def download(handle: lt.torrent_handle, seed: bool) -> None:
    last_logged_second = -1
    while not handle.status().is_seeding:
        line = print_progress(handle)
        elapsed_second = int(time.monotonic())
        if elapsed_second != last_logged_second:
            logging.info("Postep: %s", line)
            last_logged_second = elapsed_second
        time.sleep(1)

    final_line = print_progress(handle)
    logging.info("Pobieranie zakonczone: %s", final_line)
    print("\nPobieranie zakonczone.")

    if not seed:
        return

    logging.info("Tryb seedowania aktywny")
    print("Tryb seedowania aktywny. Zatrzymaj program Ctrl+C.")
    try:
        while True:
            print_progress(handle)
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Zatrzymano seedowanie przez uzytkownika")
        print("\nZatrzymano seedowanie.")


def run_download(session: lt.session, source: str, output_dir: Path, timeout: int, seed: bool) -> None:
    logging.info("Rozpoczecie obslugi zrodla: %s", source)
    handle = add_torrent(session, source, output_dir)
    wait_for_metadata(handle, timeout)

    name = handle.status().name or "nieznany torrent"
    logging.info("Start pobierania: %s", name)
    print(f"Start pobierania: {name}")
    print(f"Katalog docelowy: {output_dir}")
    download(handle, seed)


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

    ensure_libtorrent()

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Katalog docelowy: %s", output_dir)

    session = create_session(args.listen_port)

    try:
        for index, source in enumerate(sources, start=1):
            if len(sources) > 1:
                print(f"\n[{index}/{len(sources)}] Zrodlo: {source}")
            run_download(session, source, output_dir, args.timeout, args.seed)
    except KeyboardInterrupt:
        logging.info("Przerwano pobieranie przez uzytkownika")
        print("\nPrzerwano pobieranie.")
        raise SystemExit(130)
    except Exception:
        logging.exception("Nieoczekiwany blad podczas pobierania")
        raise


if __name__ == "__main__":
    main()