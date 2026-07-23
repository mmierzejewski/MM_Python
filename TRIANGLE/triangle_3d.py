"""
Script that draws a triangle in 3D space with arbitrary vertex coordinates
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from typing import List, Tuple
import os


# Tolerance for checking collinearity
COLLINEARITY_TOLERANCE = 1e-10


def calculate_axis_ranges(points: np.ndarray, margin_factor: float = 0.1) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
    """
    Calculates axis ranges for the 3D plot, always including the point (0,0,0)
    
    Args:
        points: array of points to take into account
        margin_factor: margin factor (default 0.1 = 10%)
    
    Returns:
        tuple containing (x_range, y_range, z_range)
    """
    min_xyz = np.min(points, axis=0)
    max_xyz = np.max(points, axis=0)
    
    # Always include zero on each axis
    min_x, min_y, min_z = np.minimum([0, 0, 0], min_xyz)
    max_x, max_y, max_z = np.maximum([0, 0, 0], max_xyz)
    
    # Add margin
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
    Draws a triangle in 3D space
    Checks whether the points form a triangle (not collinear and not identical)
    
    Args:
        A, B, C: lists [x, y, z] representing vertex coordinates
    
    Example:
        >>> draw_triangle_3d([0, 0, 0], [1, 0, 0], [0, 1, 0])
    """
    # Convert to numpy arrays
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)

    # Check whether the points are distinct
    if np.array_equal(A, B) or np.array_equal(A, C) or np.array_equal(B, C):
        print("Error: Two or more vertices have identical coordinates. This is not a triangle.")
        return

    # Check collinearity (vectors AB and AC must be linearly independent)
    AB = B - A
    AC = C - A
    cross = np.cross(AB, AC)
    if np.allclose(cross, [0, 0, 0], atol=COLLINEARITY_TOLERANCE):
        print("Error: The points are collinear. This is not a triangle.")
        return
    
    # Calculate the triangle's area
    area = 0.5 * np.linalg.norm(cross)

    # Side lengths
    AB_len = np.linalg.norm(AB)
    AC_len = np.linalg.norm(AC)
    BC_len = np.linalg.norm(C - B)

    print(f"\nVertex coordinates:")
    print(f"A = ({A[0]:.2f}, {A[1]:.2f}, {A[2]:.2f})")
    print(f"B = ({B[0]:.2f}, {B[1]:.2f}, {B[2]:.2f})")
    print(f"C = ({C[0]:.2f}, {C[1]:.2f}, {C[2]:.2f})")

    print(f"\nTriangle side lengths:")
    print(f"AB = {AB_len:.2f}")
    print(f"AC = {AC_len:.2f}")
    print(f"BC = {BC_len:.2f}")
    
    print(f"\nTriangle area: {area:.2f}")
    
    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw the triangle's edges
    vertices = np.array([A, B, C, A])
    ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
            'b-', linewidth=2, label='Edges')
    
    # Fill the triangle
    triangle = [[A, B, C]]
    poly = Poly3DCollection(triangle, alpha=0.3, facecolor='cyan', 
                           edgecolor='blue', linewidth=2)
    ax.add_collection3d(poly)
    
    # Draw the vertices
    vertices_array = np.array([A, B, C])
    ax.scatter(vertices_array[:, 0], vertices_array[:, 1], 
              vertices_array[:, 2], c='red', s=100, marker='o')
    
    # Label the vertices
    ax.text(A[0], A[1], A[2], f'  A({A[0]:.1f},{A[1]:.1f},{A[2]:.1f})', 
           fontsize=12, color='red')
    ax.text(B[0], B[1], B[2], f'  B({B[0]:.1f},{B[1]:.1f},{B[2]:.1f})', 
           fontsize=12, color='red')
    ax.text(C[0], C[1], C[2], f'  C({C[0]:.1f},{C[1]:.1f},{C[2]:.1f})', 
           fontsize=12, color='red')
    
    # Label the side lengths
    mid_AB = (A + B) / 2
    mid_AC = (A + C) / 2
    mid_BC = (B + C) / 2
    ax.text(mid_AB[0], mid_AB[1], mid_AB[2], f'  {AB_len:.1f}', fontsize=10, color='green')
    ax.text(mid_AC[0], mid_AC[1], mid_AC[2], f'  {AC_len:.1f}', fontsize=10, color='green')
    ax.text(mid_BC[0], mid_BC[1], mid_BC[2], f'  {BC_len:.1f}', fontsize=10, color='green')
    
    # Plot settings
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('Triangle in 3D Space', 
                fontsize=14, fontweight='bold')
    
    # Set axis ranges
    all_points = np.array([A, B, C, [0, 0, 0]])
    x_range, y_range, z_range = calculate_axis_ranges(all_points)
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_zlim(z_range)
    
    # Grid
    ax.grid(True, alpha=0.3)
    
    # Legend
    ax.legend()
    
    plt.tight_layout()
    
    # Save the file in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'triangle_3d.png')
    plt.savefig(output_path)
    print(f"\nPlot saved as {output_path}")
    plt.show()


def get_vertex_coordinates(vertex_name: str) -> List[float]:
    """
    Prompts the user for a vertex's coordinates
    
    Args:
        vertex_name: vertex name (e.g. 'A', 'B', 'C')
    
    Returns:
        list [x, y, z] with the coordinates
    """
    while True:
        try:
            print(f"\nEnter the coordinates for vertex {vertex_name}:")
            x = float(input(f"  X{vertex_name}: "))
            y = float(input(f"  Y{vertex_name}: "))
            z = float(input(f"  Z{vertex_name}: "))
            return [x, y, z]
        except ValueError:
            print("Error! Enter numbers (e.g. 1.5, 2, -3.14)")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted.")
            exit(0)


if __name__ == "__main__":
    print("=" * 60)
    print("Drawing a triangle in 3D space")
    print("=" * 60)
    print("\nThe program will draw a triangle based on the given coordinates")
    print("of three vertices in 3D space (X, Y, Z).")
    
    # Get coordinates from the user
    vertex_a = get_vertex_coordinates('A')
    vertex_b = get_vertex_coordinates('B')
    vertex_c = get_vertex_coordinates('C')
    
    # Draw the triangle
    draw_triangle_3d(vertex_a, vertex_b, vertex_c)
