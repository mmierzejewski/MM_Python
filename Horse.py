#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knight's Tour Problem - Znajdowanie trasy skoczka szachowego.

Problem polega na znalezieniu sekwencji ruchów skoczka, która odwiedza 
każde pole szachownicy dokładnie raz.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass


# Stałe
UNVISITED = -1
START_POSITION = 1
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


@dataclass
class BoardState:
    """Stan planszy do śledzenia najlepszego rozwiązania."""
    board: List[List[int]]
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
        self.board = [[UNVISITED] * width for _ in range(height)]
        self.best_state = BoardState(
            board=[[UNVISITED] * width for _ in range(height)],
            moves_count=START_POSITION
        )

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

    def solve_recursive(self, x: int, y: int, move_num: int) -> bool:
        """
        Rekurencyjna funkcja rozwiązująca problem z backtrackingiem.

        Args:
            x, y: Aktualna pozycja
            move_num: Numer aktualnego ruchu

        Returns:
            True jeśli znaleziono kompletne rozwiązanie
        """
        # Czy odwiedziliśmy wszystkie pola?
        if move_num == self.height * self.width + 1:
            return True

        # Pobierz możliwe ruchy (posortowane według Warnsdorffa)
        for _, next_x, next_y in self.get_possible_moves(x, y):
            # Wykonaj ruch
            self.board[next_x][next_y] = move_num
            self.update_best_state(move_num)

            # Rekurencja
            if self.solve_recursive(next_x, next_y, move_num + 1):
                return True

            # Backtrack
            self.board[next_x][next_y] = UNVISITED

        return False

    def solve(self, start_x: int = 0, start_y: int = 0) -> bool:
        """
        Rozwiązuje problem trasy skoczka.

        Args:
            start_x, start_y: Pozycja startowa skoczka

        Returns:
            True jeśli znaleziono kompletne rozwiązanie
        """
        if not (0 <= start_x < self.height and 0 <= start_y < self.width):
            raise ValueError("Pozycja startowa poza planszą")

        # Ustaw pozycję startową
        self.board[start_x][start_y] = START_POSITION
        self.update_best_state(START_POSITION)

        print(f"Rozwiązywanie dla planszy {self.height}x{self.width}...")

        # Rozpocznij rozwiązywanie
        solution_found = self.solve_recursive(start_x, start_y, START_POSITION + 1)

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
        else:
            coverage = (self.best_state.moves_count / total_cells) * 100
            print(f"\n✗ Nie znaleziono kompletnego rozwiązania.")
            print(f"  Najlepszy wynik: {self.best_state.moves_count}/{total_cells} "
                  f"({coverage:.1f}% planszy)")

        self.print_board()


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
                confirm = input("   Kontynuować? (tak/nie): ").strip().lower()
                if confirm not in ['tak', 't', 'yes', 'y']:
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

    height, width = get_board_dimensions()

    print(f"\n{'='*50}")
    try:
        solver = KnightsTour(height, width, verbose=True)
        solver.solve(start_x=0, start_y=0)
        solver.print_result()
    except ValueError as e:
        print(f"❌ Błąd: {e}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()