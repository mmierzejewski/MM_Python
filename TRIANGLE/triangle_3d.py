"""
Skrypt rysujący trójkąt prostokątny o bokach 3, 4, 5 w przestrzeni 3D
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def draw_triangle_3d():
    """
    Rysuje trójkąt prostokątny o bokach 3, 4, 5 w przestrzeni 3D
    """
    # Definicja wierzchołków trójkąta (3-4-5 to trójkąt prostokątny)
    # Wierzchołek A w początku układu współrzędnych
    A = np.array([0, 0, 0])
    # Wierzchołek B na osi X w odległości 3
    B = np.array([3, 0, 0])
    # Wierzchołek C na osi Y w odległości 4
    C = np.array([0, 4, 0])
    
    # Sprawdzenie długości boków
    AB = np.linalg.norm(B - A)
    AC = np.linalg.norm(C - A)
    BC = np.linalg.norm(C - B)
    
    print(f"Długości boków trójkąta:")
    print(f"AB = {AB:.2f}")
    print(f"AC = {AC:.2f}")
    print(f"BC = {BC:.2f}")
    
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
    ax.text(A[0], A[1], A[2], '  A(0,0,0)', fontsize=12, color='red')
    ax.text(B[0], B[1], B[2], '  B(3,0,0)', fontsize=12, color='red')
    ax.text(C[0], C[1], C[2], '  C(0,4,0)', fontsize=12, color='red')
    
    # Oznaczenie długości boków
    mid_AB = (A + B) / 2
    mid_AC = (A + C) / 2
    mid_BC = (B + C) / 2
    
    ax.text(mid_AB[0], mid_AB[1], mid_AB[2], f'  {AB:.1f}', 
           fontsize=10, color='green')
    ax.text(mid_AC[0], mid_AC[1], mid_AC[2], f'  {AC:.1f}', 
           fontsize=10, color='green')
    ax.text(mid_BC[0], mid_BC[1], mid_BC[2], f'  {BC:.1f}', 
           fontsize=10, color='green')
    
    # Ustawienia wykresu
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('Trójkąt prostokątny 3-4-5 w przestrzeni 3D', 
                fontsize=14, fontweight='bold')
    
    # Ustawienie równych skal na osiach
    max_range = 5
    ax.set_xlim([-1, max_range])
    ax.set_ylim([-1, max_range])
    ax.set_zlim([-1, max_range])
    
    # Siatka
    ax.grid(True, alpha=0.3)
    
    # Legenda
    ax.legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Rysowanie trójkąta prostokątnego o bokach 3, 4, 5 w przestrzeni 3D...")
    draw_triangle_3d()
