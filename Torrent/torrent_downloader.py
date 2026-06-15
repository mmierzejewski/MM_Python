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
except ImportError as e:  # pragma: no cover - zalezne od srodowiska
    print(f"Brak wymaganego pakietu: {e.name}", file=sys.stderr)
    print("\nZainstaluj zaleznosci:", file=sys.stderr)
    print("   pip install -r requirements.txt", file=sys.stderr)
    print("   lub", file=sys.stderr)
    print("   pip install aria2p", file=sys.stderr)
    sys.exit(1)


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
        default=".",
        help="Katalog docelowy dla pobieranych danych (domyslnie: biezacy katalog)",
    )
    parser.add_argument(
        "--listen-port",
        type=int,
        default=6881,
        help="Port nasluchu BitTorrent (domyslnie: 6881)",
    )
    parser.add_argument(
        "--listen-port-end",
        type=int,
        default=6891,
        help="Koniec zakresu portow BitTorrent i DHT (domyslnie: 6891)",
    )
    parser.add_argument(
        "--rpc-port",
        type=int,
        default=0,
        help="Port RPC aria2 dostepny na interfejsach hosta (domyslnie: losowy wolny port)",
    )
    parser.add_argument(
        "--listen-address",
        choices=("localhost", "127.0.0.1", "0.0.0.0"),
        default="0.0.0.0",
        help="Zakres nasluchu RPC: localhost albo 0.0.0.0 (domyslnie: 0.0.0.0)",
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Skrot dla --listen-address localhost.",
    )
    parser.add_argument(
        "--public-rpc",
        action="store_true",
        help="Skrot dla --listen-address 0.0.0.0.",
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
        "--allow-overwrite",
        action="store_true",
        help="Pozwala nadpisac istniejacy plik docelowy, gdy aria2 blokuje ponowne pobranie.",
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


def get_output_directory(default_output: str = ".") -> str:
    current_dir = Path.cwd().resolve()
    default_path = (current_dir / default_output).resolve()

    print(f"Katalog wyjsciowy [domyslnie: {default_path}]:")
    try:
        user_input = input("   (wcisnij Enter, aby uzyc domyslnego katalogu): ").strip()
    except EOFError:
        print()
        return str(default_path)

    if not user_input:
        return str(default_path)

    output_path = Path(user_input).expanduser().resolve()
    if not output_path.exists():
        print(f"Katalog nie istnieje: {output_path}")
        if not prompt_bool("Utworzyc katalog?", default=False):
            print(f"Uzywam domyslnego katalogu: {default_path}")
            return str(default_path)

    return str(output_path)


def collect_interactive_sources() -> tuple[str | None, str | None]:
    print("Podaj magnet linki albo sciezki do plikow .torrent.")
    print("Wprowadzaj po jednym wpisie w linii; pusta linia konczy.")

    entries: list[str] = []
    entry_count = 0

    while True:
        entry_count += 1
        try:
            source = input(f"   Zrodlo #{entry_count}: ").strip()
        except EOFError:
            print()
            if entries:
                break
            print("   Wprowadz przynajmniej jedno zrodlo")
            raise SystemExit(2)
        if not source:
            if entries:
                break
            print("   Wprowadz przynajmniej jedno zrodlo")
            entry_count -= 1
            continue
        entries.append(source)
        if len(entries) == 1:
            print("   (wcisnij Enter, aby zakonczyc lub podaj kolejne zrodlo)")

    if len(entries) == 1:
        return entries[0], None

    batch_file = Path(tempfile.NamedTemporaryFile(prefix="torrent-batch-", suffix=".txt", delete=False).name)
    batch_file.write_text("\n".join(entries) + "\n", encoding="utf-8")
    return None, str(batch_file)


def interactive_args(args: argparse.Namespace, full_interactive: bool = True) -> argparse.Namespace:
    print("Tryb interaktywny torrent downloader")
    logging.info("Uruchomiono tryb interaktywny")

    if args.output == ".":
        args.output = get_output_directory(args.output)

    if not args.source and not args.batch_file:
        args.source, args.batch_file = collect_interactive_sources()

    if not args.allow_overwrite:
        args.allow_overwrite = prompt_bool(
            "Czy nadpisac istniejace pliki docelowe, jesli aria2 zablokuje wznowienie?",
            default=False,
        )

    if full_interactive and args.listen_port == 6881:
        port = input("Port nasluchu [6881]: ").strip()
        if port:
            args.listen_port = int(port)

    if full_interactive and args.timeout == 120:
        timeout = input("Timeout metadanych w sekundach [120]: ").strip()
        if timeout:
            args.timeout = int(timeout)

    if full_interactive and not args.seed:
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
    if shutil.which("aria2c"):
        return

    logging.error("Brak programu aria2c")
    print(
        "Brak programu 'aria2c'. Zainstaluj zaleznosci: brew install aria2",
        file=sys.stderr,
    )
    raise SystemExit(1)


def find_free_port(bind_host: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind((bind_host, 0))
        probe.listen(1)
        return int(probe.getsockname()[1])


def can_bind_tcp_port(bind_host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        try:
            probe.bind((bind_host, port))
        except OSError:
            return False
        return True


def resolve_rpc_port(requested_port: int, listen_address: str, explicit_port: bool) -> int:
    bind_host = "127.0.0.1" if listen_address in {"localhost", "127.0.0.1"} else "0.0.0.0"

    if requested_port <= 0:
        random_port = find_free_port(bind_host)
        logging.info("Wybrano losowy wolny port RPC: %d", random_port)
        print(f"Wybrano losowy wolny port RPC: {random_port}", file=sys.stderr)
        return random_port

    if can_bind_tcp_port(bind_host, requested_port):
        return requested_port

    if explicit_port:
        print(
            f"Port RPC {requested_port} jest juz zajety. Wybierz inny przez --rpc-port.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    fallback_port = find_free_port(bind_host)
    logging.warning(
        "Domyslny port RPC %d jest zajety; uzywam wolnego portu %d",
        requested_port,
        fallback_port,
    )
    print(
        f"Port RPC {requested_port} jest zajety. Uzywam wolnego portu: {fallback_port}",
        file=sys.stderr,
    )
    return fallback_port

class Aria2Runtime:
    def __init__(
        self,
        listen_port: int,
        listen_port_end: int,
        rpc_port: int,
        listen_address: str,
        output_dir: Path,
    ) -> None:
        self.listen_port = listen_port
        self.listen_port_end = listen_port_end
        self.rpc_port = rpc_port
        self.listen_address = listen_address
        self.output_dir = output_dir
        self.rpc_secret = secrets.token_hex(16)
        self.runtime_dir = tempfile.TemporaryDirectory(prefix="torrent-downloader-aria2-")
        self.client: aria2p.Client | None = None
        self.api: aria2p.API | None = None

    def start(self) -> aria2p.API:
        aria2c_path = shutil.which("aria2c")
        if aria2c_path is None:
            ensure_aria2()

        rpc_listen_all = self.listen_address == "0.0.0.0"

        command = [
            aria2c_path or "aria2c",
            "--daemon=true",
            "--enable-rpc=true",
            f"--rpc-listen-all={'true' if rpc_listen_all else 'false'}",
            f"--rpc-listen-port={self.rpc_port}",
            f"--rpc-secret={self.rpc_secret}",
            f"--dir={self.output_dir}",
            f"--listen-port={self.listen_port}-{self.listen_port_end}",
            f"--dht-listen-port={self.listen_port}-{self.listen_port_end}",
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
                    print(
                        f"Nie udalo sie uruchomic aria2 RPC na porcie {self.rpc_port}.",
                        file=sys.stderr,
                    )
                    raise SystemExit(1)
                time.sleep(0.2)

        logging.info("Uruchomiono aria2 RPC na porcie %d", self.rpc_port)
        print(f"RPC aria2 nasluchuje na {self.listen_address}:{self.rpc_port}")
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


def add_download(
    api: aria2p.API,
    source: str,
    output_dir: Path,
    seed: bool,
    allow_overwrite: bool,
) -> aria2p.Download:
    options = {
        "dir": str(output_dir),
        "bt-save-metadata": "true",
    }
    if seed:
        options["seed-ratio"] = "0.0"
    else:
        options["seed-time"] = "0"
    if allow_overwrite:
        options["allow-overwrite"] = "true"

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
    if "control file(*.aria2) does not exist" in error_message:
        error_message = (
            error_message
            + " Uzyj --allow-overwrite albo usun istniejacy plik przed ponownym pobraniem."
        )
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


def run_download(
    api: aria2p.API,
    source: str,
    output_dir: Path,
    timeout: int,
    seed: bool,
    allow_overwrite: bool,
) -> None:
    logging.info("Rozpoczecie obslugi zrodla: %s", source)
    download_item = add_download(api, source, output_dir, seed, allow_overwrite)
    download_item = wait_for_metadata(download_item, timeout)

    name = download_item.name or "nieznany torrent"
    logging.info("Start pobierania: %s", name)
    print(f"Start pobierania: {name}")
    print(f"Katalog docelowy: {output_dir}")
    download(download_item, seed)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    explicit_rpc_port = any(
        argument == "--rpc-port" or argument.startswith("--rpc-port=")
        for argument in sys.argv[1:]
    )

    if args.local_only and args.public_rpc:
        print("Nie mozna uzyc jednoczesnie --local-only i --public-rpc.", file=sys.stderr)
        raise SystemExit(2)

    if args.local_only:
        args.listen_address = "localhost"
    if args.public_rpc:
        args.listen_address = "0.0.0.0"

    if args.listen_port_end < args.listen_port:
        print("--listen-port-end musi byc wiekszy lub rowny --listen-port.", file=sys.stderr)
        raise SystemExit(2)

    log_path = setup_logging(args.log_file)
    logging.info("Plik logu: %s", log_path)

    auto_interactive = not args.source and not args.batch_file

    if args.interactive or auto_interactive:
        try:
            args = interactive_args(args, full_interactive=args.interactive)
        except KeyboardInterrupt:
            logging.info("Przerwano tryb interaktywny przez uzytkownika")
            print("\nPrzerwano.")
            raise SystemExit(130)
        except ValueError as error:
            logging.exception("Bledna wartosc w trybie interaktywnym")
            print(f"Bledna wartosc w trybie interaktywnym: {error}", file=sys.stderr)
            raise SystemExit(2) from error

    sources = resolve_sources(args)

    ensure_aria2()

    args.rpc_port = resolve_rpc_port(args.rpc_port, args.listen_address, explicit_rpc_port)

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Katalog docelowy: %s", output_dir)

    runtime = Aria2Runtime(
        args.listen_port,
        args.listen_port_end,
        args.rpc_port,
        args.listen_address,
        output_dir,
    )
    api = runtime.start()

    try:
        for index, source in enumerate(sources, start=1):
            if len(sources) > 1:
                print(f"\n[{index}/{len(sources)}] Zrodlo: {source}")
            run_download(api, source, output_dir, args.timeout, args.seed, args.allow_overwrite)
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