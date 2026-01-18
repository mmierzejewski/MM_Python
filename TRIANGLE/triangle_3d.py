"""
Skrypt rysujący trójkąt w przestrzeni 3D z dowolnymi współrzędnymi wierzchołków
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def draw_triangle_3d(A, B, C):
    """
    Rysuje trójkąt w przestrzeni 3D
    Sprawdza czy punkty tworzą trójkąt (nie są współliniowe i nie są identyczne)
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
    if np.allclose(cross, [0, 0, 0]):
        print("Błąd: Punkty są współliniowe. To nie jest trójkąt.")
        return

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
    
    # Ustawianie zakresów osi tak, by punkt (0,0,0) był zawsze widoczny w tym samym miejscu
    all_points = np.array([A, B, C, [0, 0, 0]])
    min_xyz = np.min(all_points, axis=0)
    max_xyz = np.max(all_points, axis=0)
    # Zawsze obejmij zero na każdej osi
    min_x = min(0, min_xyz[0])
    min_y = min(0, min_xyz[1])
    min_z = min(0, min_xyz[2])
    max_x = max(0, max_xyz[0])
    max_y = max(0, max_xyz[1])
    max_z = max(0, max_xyz[2])
    # Dodaj margines
    margin_x = (max_x - min_x) * 0.1 if max_x != min_x else 1
    margin_y = (max_y - min_y) * 0.1 if max_y != min_y else 1
    margin_z = (max_z - min_z) * 0.1 if max_z != min_z else 1
    ax.set_xlim([min_x - margin_x, max_x + margin_x])
    ax.set_ylim([min_y - margin_y, max_y + margin_y])
    ax.set_zlim([min_z - margin_z, max_z + margin_z])
    
    # Siatka
    ax.grid(True, alpha=0.3)
    
    # Legenda
    ax.legend()
    
    plt.tight_layout()
    plt.show()


def get_vertex_coordinates(vertex_name):
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
