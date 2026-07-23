# 📐 3D Triangle

**Advanced triangle visualizer in 3D space** with full geometric validation.

## 🎯 Description

The program uses the Matplotlib library for professional visualization of a triangle in three-dimensional space. It interactively collects coordinates (X, Y, Z) for three vertices and creates a detailed 3D visualization with full geometric analysis.

## ✨ Features

- ✅ **Geometric validation** - checks whether the points are not identical and not collinear
- 📏 **Side length calculation** - automatic display of all dimensions
- 📐 **Surface area calculation** - using the cross product
- 🎨 **Professional visualization**:
  - Filled triangle with transparency
  - Marked vertices (red dots)
  - Labeled side lengths (green labels)
  - Automatic scale adjustment with a 10% margin
  - Point (0,0,0) always visible as a reference
- 💾 **PNG export** - automatic plot saving in the script's directory
- 📊 **Detailed statistics** - coordinates, side lengths, surface area
- 🛡️ **Full error handling** - input validation and exception handling
- 🔢 **Type hints** - full type annotations for better code readability
- 📈 **Interactive plot** - ability to rotate and zoom in `plt.show()` mode

## 🛠️ Requirements

- Python 3.10+
- matplotlib >= 3.5.0
- numpy >= 1.21.0

## Installing Dependencies

```bash
pip install -r requirements.txt
```

## Running

```bash
python triangle_3d.py
```

The program will ask you to enter the X, Y, Z coordinates for each of the three vertices (A, B, C).

## Usage Example

```text
============================================================
Drawing a triangle in 3D space
============================================================

The program will draw a triangle based on the given coordinates
of three vertices in 3D space (X, Y, Z).

Enter the coordinates for vertex A:
  XA: 0
  YA: 0
  ZA: 0

Enter the coordinates for vertex B:
  XB: 3
  YB: 0
  ZB: 0

Enter the coordinates for vertex C:
  XC: 0
  YC: 4
  ZC: 0
```

**The program will display:**

```text
Vertex coordinates:
A = (0.00, 0.00, 0.00)
B = (3.00, 0.00, 0.00)
C = (0.00, 4.00, 0.00)

Triangle side lengths:
AB = 3.00
AC = 4.00
BC = 5.00

Triangle area: 6.00

Plot saved as /home/mmierzejewski/GitHub/MM_Python/TRIANGLE/triangle_3d.png
```

## 🔧 Functionality

### Geometric Validation

- ✅ Check whether the points are not identical
- ✅ Check for collinearity (cross product with an explicit tolerance)
- ⚠️ Error messages for invalid configurations

### Calculations

- 📏 Lengths of all three sides (Euclidean norm)
- 📐 Triangle surface area (½ |AB × AC|)
- 📊 Automatic result formatting (2 decimal places)

### Visualization

- 🎨 Triangle filled with cyan color at alpha=0.3
- 🔴 Red vertex markers (size 100)
- 🏷️ Coordinate labels at each vertex
- 🟢 Green length labels at the midpoints of the sides
- 📏 Automatic axis ranges including (0,0,0) and all vertices
- ⚙️ Grid with alpha=0.3 for better spatial orientation

### Export and Display

- 💾 Automatic save to `triangle_3d.png` in the script's directory
- 🖥️ Interactive matplotlib window (rotate, zoom, pan)
- 📍 Full path to the saved file in the message

## 🏗️ Code Architecture

### Helper Functions

**`calculate_axis_ranges(points, margin_factor=0.1)`**

- Calculates axis ranges for the 3D plot
- Always includes the point (0,0,0)
- Adds a 10% margin (configurable)
- Returns a tuple with the ranges for X, Y, Z

**`draw_triangle_3d(A, B, C)`**

- Main drawing function
- Full input validation
- Geometric calculations
- Plot creation and configuration
- Export and display

**`get_vertex_coordinates(vertex_name)`**

- Interactive coordinate collection
- ValueError handling (invalid format)
- KeyboardInterrupt handling (Ctrl+C)
- Retry loop on errors

## 🔍 Technical Details

- **Type hints**: Full type annotations (`List[float]`, `Tuple`, `np.ndarray`)
- **Collinearity tolerance**: `1e-10` (explicitly defined constant)
- **Image format**: PNG with matplotlib's default DPI
- **Coordinate system**: Standard right-handed (X-right, Y-forward, Z-up)

## 💡 Usage Examples

### 3-4-5 Right Triangle

```text
A: (0, 0, 0)
B: (3, 0, 0)
C: (0, 4, 0)
Result: Area = 6.00
```

### Equilateral Triangle

```text
A: (0, 0, 0)
B: (1, 0, 0)
C: (0.5, 0.866, 0)
Result: Area ≈ 0.43
```

### Triangle in Full 3D Space

```text
A: (1, 2, 3)
B: (4, 5, 6)
C: (7, 1, 2)
```

## ⚠️ Error Handling

**Identical vertices:**

```text
Error: Two or more vertices have identical coordinates. This is not a triangle.
```

**Collinear points:**

```text
Error: The points are collinear. This is not a triangle.
```

**Invalid data format:**

```text
Error! Enter numbers (e.g. 1.5, 2, -3.14)
```

## 🚀 Future Improvements (TODO)

- [ ] Calculate angles between sides
- [ ] Classify triangle type (right, isosceles, equilateral)
- [ ] Command-line arguments for non-interactive mode
- [ ] Export to multiple formats (SVG, PDF)
- [ ] Batch processing from a CSV file
- [ ] Rotation animations

---

**Author**: [@mmierzejewski](https://github.com/mmierzejewski)  
**Project**: [MM_Python/TRIANGLE](https://github.com/mmierzejewski/MM_Python/tree/developer/TRIANGLE)
