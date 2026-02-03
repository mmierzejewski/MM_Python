"""
Skrypt rysujący trójkąt w przestrzeni 3D z dowolnymi współrzędnymi wierzchołków
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from typing import List, Tuple
import os


# Tolerancja dla sprawdzania współliniowości
COLLINEARITY_TOLERANCE = 1e-10


def calculate_axis_ranges(points: np.ndarray, margin_factor: float = 0.1) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
    """
    Oblicza zakresy osi dla wykresu 3D, zawsze zawierając punkt (0,0,0)
    
    Args:
        points: tablica punktów do uwzględnienia
        margin_factor: współczynnik marginesu (domyślnie 0.1 = 10%)
    
    Returns:
        tuple zawierający (x_range, y_range, z_range)
    """
    min_xyz = np.min(points, axis=0)
    max_xyz = np.max(points, axis=0)
    
    # Zawsze obejmij zero na każdej osi
    min_x, min_y, min_z = np.minimum([0, 0, 0], min_xyz)
    max_x, max_y, max_z = np.maximum([0, 0, 0], max_xyz)
    
    # Dodaj margines
    margin_x = (max_x - min_x) * margin_factor if max_x != min_x else 1
    margin_y = (max_y - min_y) * margin_factor if max_y != min_y else 1
    margin_z = (max_z - min_z) * margin_factor if max_z != min_z else 1
    
    return (
        (min_x - margin_x, max_x + margin_x),
        (min_y - margin_y, max_y + margin_y),
        (min_z - margin_z, max_z + margin_z)
    )


def draw_triangle_3d(A: List[float], B: List[float], C: List[float]) -> None:
    """
    Rysuje trójkąt w przestrzeni 3D
    Sprawdza czy punkty tworzą trójkąt (nie są współliniowe i nie są identyczne)
    
    Args:
        A, B, C: listy [x, y, z] reprezentujące współrzędne wierzchołków
    
    Example:
        >>> draw_triangle_3d([0, 0, 0], [1, 0, 0], [0, 1, 0])
    """
    # Konwersja do numpy arrays
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)

    # Sprawdzenie czy punkty są różne
    if np.array_equal(A, B) or np.array_equal(A, C) or np.array_equal(B, C):
        print("Błąd: Dwa lub więcej wierzchołków mają identyczne współrzędne. To nie jest trójkąt.")
        return

    # Sprawdzenie współliniowości (wektory AB i AC muszą być liniowo niezależne)
    AB = B - A
    AC = C - A
    cross = np.cross(AB, AC)
    if np.allclose(cross, [0, 0, 0], atol=COLLINEARITY_TOLERANCE):
        print("Błąd: Punkty są współliniowe. To nie jest trójkąt.")
        return
    
    # Obliczenie pola trójkąta
    area = 0.5 * np.linalg.norm(cross)

    # Długości boków
    AB_len = np.linalg.norm(AB)
    AC_len = np.linalg.norm(AC)
    BC_len = np.linalg.norm(C - B)

    print(f"\nWspółrzędne wierzchołków:")
    print(f"A = ({A[0]:.2f}, {A[1]:.2f}, {A[2]:.2f})")
    print(f"B = ({B[0]:.2f}, {B[1]:.2f}, {B[2]:.2f})")
    print(f"C = ({C[0]:.2f}, {C[1]:.2f}, {C[2]:.2f})")

    print(f"\nDługości boków trójkąta:")
    print(f"AB = {AB_len:.2f}")
    print(f"AC = {AC_len:.2f}")
    print(f"BC = {BC_len:.2f}")
    
    print(f"\nPole trójkąta: {area:.2f}")
    
    # Utworzenie wykresu 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Rysowanie krawędzi trójkąta
    vertices = np.array([A, B, C, A])
    ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
            'b-', linewidth=2, label='Krawędzie')
    
    # Wypełnienie trójkąta
    triangle = [[A, B, C]]
    poly = Poly3DCollection(triangle, alpha=0.3, facecolor='cyan', 
                           edgecolor='blue', linewidth=2)
    ax.add_collection3d(poly)
    
    # Rysowanie wierzchołków
    vertices_array = np.array([A, B, C])
    ax.scatter(vertices_array[:, 0], vertices_array[:, 1], 
              vertices_array[:, 2], c='red', s=100, marker='o')
    
    # Oznaczenie wierzchołków
    ax.text(A[0], A[1], A[2], f'  A({A[0]:.1f},{A[1]:.1f},{A[2]:.1f})', 
           fontsize=12, color='red')
    ax.text(B[0], B[1], B[2], f'  B({B[0]:.1f},{B[1]:.1f},{B[2]:.1f})', 
           fontsize=12, color='red')
    ax.text(C[0], C[1], C[2], f'  C({C[0]:.1f},{C[1]:.1f},{C[2]:.1f})', 
           fontsize=12, color='red')
    
    # Oznaczenie długości boków
    mid_AB = (A + B) / 2
    mid_AC = (A + C) / 2
    mid_BC = (B + C) / 2
    ax.text(mid_AB[0], mid_AB[1], mid_AB[2], f'  {AB_len:.1f}', fontsize=10, color='green')
    ax.text(mid_AC[0], mid_AC[1], mid_AC[2], f'  {AC_len:.1f}', fontsize=10, color='green')
    ax.text(mid_BC[0], mid_BC[1], mid_BC[2], f'  {BC_len:.1f}', fontsize=10, color='green')
    
    # Ustawienia wykresu
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('Trójkąt w przestrzeni 3D', 
                fontsize=14, fontweight='bold')
    
    # Ustawianie zakresów osi
    all_points = np.array([A, B, C, [0, 0, 0]])
    x_range, y_range, z_range = calculate_axis_ranges(all_points)
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_zlim(z_range)
    
    # Siatka
    ax.grid(True, alpha=0.3)
    
    # Legenda
    ax.legend()
    
    plt.tight_layout()
    
    # Zapisz plik w tym samym katalogu co skrypt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'triangle_3d.png')
    plt.savefig(output_path)
    print(f"\nWykres zapisany jako {output_path}")
    plt.show()


def get_vertex_coordinates(vertex_name: str) -> List[float]:
    """
    Pobiera współrzędne wierzchołka od użytkownika
    
    Args:
        vertex_name: nazwa wierzchołka (np. 'A', 'B', 'C')
    
    Returns:
        lista [x, y, z] ze współrzędnymi
    """
    while True:
        try:
            print(f"\nPodaj współrzędne wierzchołka {vertex_name}:")
            x = float(input(f"  X{vertex_name}: "))
            y = float(input(f"  Y{vertex_name}: "))
            z = float(input(f"  Z{vertex_name}: "))
            return [x, y, z]
        except ValueError:
            print("Błąd! Podaj liczby (np. 1.5, 2, -3.14)")
        except KeyboardInterrupt:
            print("\n\nPrzerwano działanie programu.")
            exit(0)


if __name__ == "__main__":
    print("=" * 60)
    print("Rysowanie trójkąta w przestrzeni 3D")
    print("=" * 60)
    print("\nProgram narysuje trójkąt na podstawie podanych współrzędnych")
    print("trzech wierzchołków w przestrzeni 3D (X, Y, Z).")
    
    # Pobieranie współrzędnych od użytkownika
    vertex_a = get_vertex_coordinates('A')
    vertex_b = get_vertex_coordinates('B')
    vertex_c = get_vertex_coordinates('C')
    
    # Rysowanie trójkąta
    draw_triangle_3d(vertex_a, vertex_b, vertex_c)
