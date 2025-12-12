#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knight's Tour Problem - Znajdowanie trasy skoczka szachowego.

Problem polega na znalezieniu sekwencji ruchów skoczka, która odwiedza 
każde pole szachownicy dokładnie raz.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import logging
import time
import signal


# Konfiguracja loggingu
log_file = Path(__file__).parent / 'knights_tour.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)

# Type aliases
Board = List[List[int]]

# Stałe
UNVISITED = -1
START_POSITION = 1
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


@dataclass
class SolutionStats:
    """Statystyki rozwiązania."""
    time_elapsed: float = 0.0
    backtracks: int = 0
    max_depth: int = 0
    total_attempts: int = 0
    timeout_occurred: bool = False


@dataclass
class BoardState:
    """Stan planszy do śledzenia najlepszego rozwiązania."""
    board: Board
    moves_count: int


class KnightsTour:
    """Rozwiązuje problem trasy skoczka szachowego."""

    def __init__(self, height: int, width: int, verbose: bool = False):
        """
        Inicjalizuje solver dla podanego rozmiaru planszy.

        Args:
            height: Wysokość planszy
            width: Szerokość planszy
            verbose: Czy wyświetlać szczegółowe logi

        Raises:
            ValueError: Jeśli wymiary są nieprawidłowe
        """
        if not isinstance(height, int) or not isinstance(width, int):
            raise ValueError("Wymiary planszy muszą być liczbami całkowitymi")

        if height < 3 or width < 3:
            raise ValueError("Wymiary planszy muszą być >= 3x3")

        self.height = height
        self.width = width
        self.verbose = verbose
        self.board: Board = [[UNVISITED] * width for _ in range(height)]
        self.best_state = BoardState(
            board=[[UNVISITED] * width for _ in range(height)],
            moves_count=START_POSITION
        )
        self.stats = SolutionStats()
        self.start_time = 0.0
        self.timeout_limit = 300  # 5 minut domyślnie
        
        logging.info(f"Utworzono solver dla planszy {height}x{width}")
        self.stats = SolutionStats()
        self.start_time = 0.0
        self.timeout_limit = 300  # 5 minut domyślnie
        
        logging.info(f"Utworzono solver dla planszy {height}x{width}")

    def is_safe(self, x: int, y: int) -> bool:
        """Sprawdza czy pozycja jest bezpieczna dla skoczka."""
        return (0 <= x < self.height and
                0 <= y < self.width and
                self.board[x][y] == UNVISITED)

    def count_onward_moves(self, x: int, y: int) -> int:
        """
        Liczy liczbę możliwych ruchów z danej pozycji (heurystyka Warnsdorffa).

        Args:
            x, y: Współrzędne pozycji

        Returns:
            Liczba możliwych ruchów
        """
        count = 0
        for dx, dy in KNIGHT_MOVES:
            if self.is_safe(x + dx, y + dy):
                count += 1
        return count

    def get_possible_moves(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        """
        Zwraca możliwe ruchy posortowane według heurystyki Warnsdorffa.

        Args:
            x, y: Aktualna pozycja

        Returns:
            Lista krotek (degree, next_x, next_y)
        """
        possible_moves = []
        for dx, dy in KNIGHT_MOVES:
            next_x, next_y = x + dx, y + dy
            if self.is_safe(next_x, next_y):
                degree = self.count_onward_moves(next_x, next_y)
                possible_moves.append((degree, next_x, next_y))

        return sorted(possible_moves)  # Sortuj według degree (Warnsdorff)

    def update_best_state(self, move_num: int) -> None:
        """Aktualizuje najlepsze znalezione rozwiązanie."""
        if move_num > self.best_state.moves_count:
            self.best_state.moves_count = move_num
            for r in range(self.height):
                self.best_state.board[r] = self.board[r].copy()

            if self.verbose:
                progress = (move_num / (self.height * self.width)) * 100
                print(f"Postęp: {move_num}/{self.height * self.width} ({progress:.1f}%)")

    def solve_recursive(self, x: int, y: int, move_num: int, depth: int = 0) -> bool:
        """
        Rekurencyjna funkcja rozwiązująca problem z backtrackingiem.

        Args:
            x, y: Aktualna pozycja
            move_num: Numer aktualnego ruchu
            depth: Głębokość rekurencji (dla statystyk)

        Returns:
            True jeśli znaleziono kompletne rozwiązanie
        """
        # Sprawdź timeout
        if time.time() - self.start_time > self.timeout_limit:
            self.stats.timeout_occurred = True
            logging.warning(f"Przekroczono limit czasu ({self.timeout_limit}s)")
            raise TimeoutError(f"Przekroczono limit czasu {self.timeout_limit}s")
        
        # Aktualizuj statystyki
        self.stats.max_depth = max(self.stats.max_depth, depth)
        self.stats.total_attempts += 1
        
        # Czy odwiedziliśmy wszystkie pola?
        if move_num == self.height * self.width + 1:
            logging.info("Znaleziono kompletne rozwiązanie!")
            return True

        # Pobierz możliwe ruchy (posortowane według Warnsdorffa)
        for _, next_x, next_y in self.get_possible_moves(x, y):
            # Wykonaj ruch
            self.board[next_x][next_y] = move_num
            self.update_best_state(move_num)

            # Rekurencja
            if self.solve_recursive(next_x, next_y, move_num + 1, depth + 1):
                return True

            # Backtrack
            self.board[next_x][next_y] = UNVISITED
            self.stats.backtracks += 1

        return False

    def solve(self, start_x: int = 0, start_y: int = 0, timeout: int = 300) -> bool:
        """
        Rozwiązuje problem trasy skoczka.

        Args:
            start_x, start_y: Pozycja startowa skoczka
            timeout: Limit czasu w sekundach (domyślnie 300s = 5min)

        Returns:
            True jeśli znaleziono kompletne rozwiązanie
        """
        if not (0 <= start_x < self.height and 0 <= start_y < self.width):
            raise ValueError("Pozycja startowa poza planszą")

        self.timeout_limit = timeout
        self.start_time = time.time()
        
        # Ustaw pozycję startową
        self.board[start_x][start_y] = START_POSITION
        self.update_best_state(START_POSITION)

        print(f"Rozwiązywanie dla planszy {self.height}x{self.width}...")
        logging.info(f"Start rozwiązywania: plansza {self.height}x{self.width}, start=({start_x},{start_y}), timeout={timeout}s")

        # Rozpocznij rozwiązywanie
        try:
            solution_found = self.solve_recursive(start_x, start_y, START_POSITION + 1, depth=0)
        except TimeoutError:
            solution_found = False
        
        self.stats.time_elapsed = time.time() - self.start_time
        logging.info(f"Zakończono po {self.stats.time_elapsed:.2f}s")

        return solution_found

    def print_board(self, board: Optional[List[List[int]]] = None) -> None:
        """Wyświetla planszę."""
        if board is None:
            board = self.best_state.board

        print(f"\nPlansza {self.height}x{self.width}:")
        print("┌" + "─" * (self.width * 3 + 1) + "┐")

        for row in board:
            print("│ " + ' '.join(str(cell).rjust(2) for cell in row) + " │")

        print("└" + "─" * (self.width * 3 + 1) + "┘")

    def print_result(self) -> None:
        """Wyświetla wynik rozwiązania."""
        total_cells = self.height * self.width

        if self.best_state.moves_count == total_cells:
            print("\n✓ Znaleziono kompletne rozwiązanie!")
            logging.info("Znaleziono kompletne rozwiązanie")
        else:
            coverage = (self.best_state.moves_count / total_cells) * 100
            print(f"\n✗ Nie znaleziono kompletnego rozwiązania.")
            print(f"  Najlepszy wynik: {self.best_state.moves_count}/{total_cells} "
                  f"({coverage:.1f}% planszy)")
            logging.info(f"Częściowe rozwiązanie: {self.best_state.moves_count}/{total_cells} ({coverage:.1f}%)")
        
        if self.stats.timeout_occurred:
            print(f"  ⏱️  Przerwano po {self.stats.time_elapsed:.2f}s (timeout)")

        self.print_board()
        self.print_stats()
    
    def print_stats(self) -> None:
        """Wyświetla statystyki rozwiązania."""
        print(f"\n📊 Statystyki:")
        print(f"  Czas wykonania: {self.stats.time_elapsed:.2f}s")
        print(f"  Liczba prób: {self.stats.total_attempts:,}")
        print(f"  Backtracki: {self.stats.backtracks:,}")
        print(f"  Maksymalna głębokość: {self.stats.max_depth}")
        
        if self.stats.total_attempts > 0:
            success_rate = (1 - self.stats.backtracks / self.stats.total_attempts) * 100
            print(f"  Skuteczność: {success_rate:.1f}%")
    
    def export_solution(self, filename: Optional[str] = None) -> None:
        """Eksportuje rozwiązanie do pliku.
        
        Args:
            filename: Nazwa pliku (opcjonalna, domyślnie z timestampem)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Zapisz w katalogu gdzie jest skrypt (Horse/)
            script_dir = Path(__file__).parent
            filename = script_dir / f"knights_tour_{self.height}x{self.width}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Knight's Tour Solution\n")
                f.write(f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Plansza: {self.height}x{self.width}\n")
                f.write(f"="*60 + "\n\n")
                
                # Plansza
                total_cells = self.height * self.width
                if self.best_state.moves_count == total_cells:
                    f.write("✓ KOMPLETNE ROZWIĄZANIE\n\n")
                else:
                    coverage = (self.best_state.moves_count / total_cells) * 100
                    f.write(f"✗ Częściowe rozwiązanie: {self.best_state.moves_count}/{total_cells} ({coverage:.1f}%)\n\n")
                
                # Wizualizacja planszy
                for row in self.best_state.board:
                    f.write(' '.join(str(cell).rjust(3) for cell in row) + '\n')
                
                # Statystyki
                f.write("\n" + "="*60 + "\n")
                f.write("STATYSTYKI:\n")
                f.write(f"Czas wykonania: {self.stats.time_elapsed:.2f}s\n")
                f.write(f"Liczba prób: {self.stats.total_attempts:,}\n")
                f.write(f"Backtracki: {self.stats.backtracks:,}\n")
                f.write(f"Maksymalna głębokość rekurencji: {self.stats.max_depth}\n")
                if self.stats.timeout_occurred:
                    f.write(f"Status: TIMEOUT po {self.timeout_limit}s\n")
            
            print(f"\n✅ Eksportowano do: {filename}")
            logging.info(f"Wyeksportowano rozwiązanie do {filename}")
        except IOError as e:
            print(f"\n❌ Błąd zapisu pliku: {e}")
            logging.error(f"Błąd eksportu: {e}")


def get_board_dimensions():
    """Pobiera i waliduje wymiary planszy od użytkownika."""
    while True:
        try:
            height = int(input("Podaj wysokość planszy (min 3, zalecane max 8): ").strip())
            width = int(input("Podaj szerokość planszy (min 3, zalecane max 8): ").strip())

            if height < 3 or width < 3:
                print("⚠️  Wymiary planszy muszą być >= 3. Spróbuj ponownie.\n")
                continue

            if height > 10 or width > 10:
                print(f"⚠️  Duża plansza {height}x{width} może zająć bardzo dużo czasu!")
                confirm = input("   Kontynuować? (T/N) [N]: ").strip().upper() or "N"
                if confirm != "T":
                    continue

            return height, width

        except ValueError:
            print("❌ Proszę podać liczby całkowite!\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Przerwano przez użytkownika.")
            exit(0)


def main():
    """Główna funkcja programu."""
    print("=== Problem Trasy Skoczka Szachowego ===\n")
    logging.info("Uruchomiono program Knight's Tour")

    height, width = get_board_dimensions()

    print(f"\n{'='*50}")
    try:
        solver = KnightsTour(height, width, verbose=True)
        solver.solve(start_x=0, start_y=0, timeout=300)
        solver.print_result()
        
        # Opcja eksportu
        eksport = input("\nEksportować rozwiązanie do pliku? (T/N) [T]: ").strip().upper() or "T"
        if eksport == "T":
            custom_name = input("Nazwa pliku (Enter = auto): ").strip()
            solver.export_solution(custom_name if custom_name else None)
        
    except ValueError as e:
        print(f"❌ Błąd: {e}")
        logging.error(f"ValueError: {e}")
    except TimeoutError as e:
        print(f"⏱️  {e}")
        logging.error(f"TimeoutError: {e}")
    except Exception as e:
        print(f"❌ Nieoczekiwany błąd: {e}")
        logging.error(f"Nieoczekiwany błąd: {e}", exc_info=True)
    
    print(f"{'='*50}\n")
    logging.info("Zakończono program")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Przerwano przez użytkownika.")
        logging.info("Przerwano przez użytkownika (KeyboardInterrupt)")
    except Exception as e:
        print(f"\n❌ Krytyczny błąd: {e}")
        logging.critical(f"Krytyczny błąd: {e}", exc_info=True)