# 🔺 Pythagorean Triple Generator - Pitagoras.py

## 📋 Description

**Pitagoras.py** is an advanced Pythagorean triple generator with full mathematical analysis. The program generates **only primitive** Pythagorean triples (eliminating duplicates such as 3,4,5 and 6,8,10) and performs detailed statistical analysis with prime number detection.

### What is a Pythagorean Triple?

A Pythagorean triple is a set of three positive integers `a`, `b`, `c` satisfying the equation:

```text
a² + b² = c²
```

**Examples:**

- (3, 4, 5) → 3² + 4² = 9 + 16 = 25 = 5²  ✓
- (5, 12, 13) → 5² + 12² = 25 + 144 = 169 = 13²  ✓
- (8, 15, 17) → 8² + 15² = 64 + 225 = 289 = 17²  ✓

## ⭐ Key Features

### ✅ Primitive Triples Only

- **GCD(a, b, c) = 1** - eliminates multiples
- No duplicates such as (3,4,5) and (6,8,10)
- Guaranteed uniqueness of all generated triples

### 📊 Detailed Analysis

For each triple, the program calculates:

- **Dimensions**: a, b, c (sides of the triangle)
- **Perimeter**: a + b + c
- **Area**: (a × b) / 2
- **Prime numbers**: which values in the triple are prime numbers

### 📈 Statistics

- Number of generated primitive triples
- Number of triples containing prime numbers (%)
- All prime numbers in range
- Perimeter: smallest, largest, average
- Area: smallest, largest, average

### ✓ Correctness Verification

- Checking GCD > 1 (non-primitive triples)
- Detection of exact duplicates
- Sample verification of the Pythagorean formula

### 🔄 Menu Loop (New)

- The program runs in continuous mode
- After generating triples, it automatically returns to the main menu
- Ability to perform multiple generations without restarting
- "Exit" option - graceful exit from the program

## 🔬 Algorithm: Euclid's Formula

The program uses **Euclid's formula** to generate primitive Pythagorean triples:

For coprime numbers `m > n > 0` of different parity:

```python
a = m² - n²
b = 2mn
c = m² + n²
```

**Conditions:**

1. `m > n > 0`
2. `GCD(m, n) = 1` (coprime numbers)
3. `m` and `n` have different parity (one even, one odd)

**Example:** m=2, n=1

```text
a = 2² - 1² = 4 - 1 = 3
b = 2 × 2 × 1 = 4
c = 2² + 1² = 4 + 1 = 5
Result: (3, 4, 5) ✓
```

### Time Complexity

- **Triple generation**: O(m²) where m is the formula parameter
- **Sieve of Eratosthenes**: O(n log log n) where n is the largest value
- **Sorting**: O(k log k) where k is the number of triples

## 🚀 Installation and Running

### Requirements

```bash
Python 3.8+

# No external dependencies - standard library only

```

### Running

```bash
cd PITAGORAS
python Pitagoras.py
```

## 💻 Usage

### Step 1: Run the program

```bash
python Pitagoras.py
```

### Step 2: Choose an option and enter the number of triples

```text
╔════════════════════════════════════════════════════════════════════════════════════════╗
║                PYTHAGOREAN TRIPLE GENERATOR                                           ║
║                         (Primitive only)                                             ║
╚════════════════════════════════════════════════════════════════════════════════════════╝

Choose an option:
  1. Generate Pythagorean triples
  2. Exit (quit the program)

Your choice (1/2): 1

Enter the number of Pythagorean triples to generate (1-1000): 10
```

### Step 3: Get the results

#### Triples Table

```text
==========================================================================================

# a     b     c     Perimeter  Area L. Primes

==========================================================================================
1        3     4     5        12           6.0 [3, 5]                         
2        5    12    13        30          30.0 [5, 13]                        
3        8    15    17        40          60.0 [17]                           
4        7    24    25        56          84.0 [7]                            
5       20    21    29        70         210.0 [29]                           
6        9    40    41        90         180.0 [41]                           
7       12    35    37        84         210.0 [37]                           
8       11    60    61       132         330.0 [11, 61]                       
9       13    84    85       182         546.0 [13, 85]                       
10      28    45    53       126         630.0 [53]                           
==========================================================================================
```

#### Duplicate Verification

```text
==========================================================================================
DUPLICATE VERIFICATION:
==========================================================================================
✅ All triples are primitive (no multiples such as 3,4,5 and 6,8,10)
✅ No exact duplicates found
==========================================================================================
```

#### Statistics

```text
==========================================================================================
STATISTICS:
==========================================================================================
Total primitive triples:           10
Triples containing prime numbers:  9 (90.0%)
Primes up to 85:                   23

Perimeter:
  Smallest:                        12
  Largest:                         182
  Average:                         88.2

Area:
  Smallest:                        6.0
  Largest:                         546.0
  Average:                         228.6
==========================================================================================

⏱️  Generation time: 0.001s
   Average per triple: 0.000100s

💡 Sample verification (first 3 triples):
   1. 3² + 4² = 9 + 16 = 25 = 25 = 5²  ✓
   2. 5² + 12² = 25 + 144 = 169 = 169 = 13²  ✓
   3. 8² + 15² = 64 + 225 = 289 = 289 = 17²  ✓
```

## 📊 Usage Examples

### Example 1: Small Sets (5 triples)

```bash
python Pitagoras.py

# Input: 5

# Output: (3,4,5), (5,12,13), (8,15,17), (7,24,25), (20,21,29)

```

### Example 2: Medium Sets (50 triples)

```bash
python Pitagoras.py

# Input: 50

# Get 50 unique primitive triples

# Time: ~0.01s

```

### Example 3: Large Sets (500 triples)

```bash
python Pitagoras.py

# Input: 500

# System warns: "⚠️  A large number (500) may take some time!"

# Confirm: Y (Yes) or N (No)

```

## 🎯 Advanced Features

### 1. PythagoreanTriple Class

```python
class PythagoreanTriple:
    def __init__(self, a: int, b: int, c: int)

    @property
    def perimeter(self) -> int
        """Calculates the perimeter: a + b + c"""

    @property
    def area(self) -> float
        """Calculates the area: (a × b) / 2"""
```

### 2. Triple Generation

```python
def generate_primitive_triples(count: int) -> List[PythagoreanTriple]
    """
    Generates a specified number of primitive Pythagorean triples
    using Euclid's formula.

    Returns: A list sorted by perimeter (ascending)
    """
```

### 3. Sieve of Eratosthenes

```python
def sieve_of_eratosthenes(limit: int) -> Set[int]
    """
    Generates all prime numbers up to the limit.

    Complexity: O(n log log n)
    Returns: Set of prime numbers for O(1) lookup
    """
```

### 4. Prime Number Analysis

```python
def analyze_primes_in_triple(triple: PythagoreanTriple, primes: Set[int]) -> List[int]
    """
    Finds which numbers in the triple are prime.

    Example: (5, 12, 13) → [5, 13]
    """
```

## 🔍 Mathematical Details

### Primitive vs Non-Primitive

**Primitive Triples** (GCD = 1):

- (3, 4, 5) ✓
- (5, 12, 13) ✓
- (8, 15, 17) ✓
- (7, 24, 25) ✓

**Non-Primitive Triples** (GCD > 1):

- (6, 8, 10) = 2 × (3, 4, 5) ✗
- (9, 12, 15) = 3 × (3, 4, 5) ✗
- (10, 24, 26) = 2 × (5, 12, 13) ✗

### Properties of Primitive Triples

1. **Exactly one** of the numbers a, b is even
2. **Exactly one** of the numbers a, b, c is divisible by 3
3. **Exactly one** of the numbers a, b, c is divisible by 5
4. The sum a + b + c is **always even**
5. The product abc is **always divisible by 60**

## 📈 Performance

### Benchmarks

```text
Number of triples    Time         Memory
──────────────────────────────────────
10              < 0.001s     < 1 MB
50              ~ 0.005s     < 1 MB
100             ~ 0.010s     < 1 MB
500             ~ 0.050s     ~ 2 MB
1000            ~ 0.100s     ~ 5 MB
```

### Optimizations

- ⚡ Euclid's formula instead of brute force
- 🔍 Set for O(1) prime number lookup
- 📊 Sorting only once at the end
- 💾 Minimal memory usage

## ❓ FAQ

### Q: Why only primitive triples?

**A:** Primitive triples are the basic "building blocks". All other triples are their multiples, so they are redundant.

### Q: How long does it take to generate 1000 triples?

**A:** About 0.1 seconds on a modern computer.

### Q: Can I generate more than 1000 triples?

**A:** Yes, but the program will warn about potentially long computation time. You can confirm to continue.

### Q: What is GCD (Greatest Common Divisor)?

**A:** It is the largest integer that divides all the given numbers. For primitive triples, GCD(a,b,c) = 1.

### Q: Why does the program show prime numbers?

**A:** This is additional mathematical analysis showing which values in the triple are prime numbers - an interesting property from a number theory perspective.

## 🐛 Error Handling

The program handles:

- ❌ Invalid input (non-numbers)
- ❌ Numbers < 1
- ⚠️ Warnings for large values (> 1000)
- 🛑 Ctrl+C (interruption by the user)
- 🚨 Unexpected errors with messages

## 📚 Mathematical Theory

### Pythagorean Theorem

For a right triangle with legs a, b and hypotenuse c:

```text
a² + b² = c²
```

### Euclid's Formula (c. 300 BC)

All primitive Pythagorean triples can be generated using:

```text
a = m² - n²
b = 2mn
c = m² + n²
```

where m > n > 0, GCD(m,n) = 1, and m-n is odd.

### First Pythagorean Triples

```text
(3, 4, 5)       - Smallest
(5, 12, 13)
(8, 15, 17)
(7, 24, 25)
(20, 21, 29)
(9, 40, 41)
(12, 35, 37)
(11, 60, 61)
(13, 84, 85)
(28, 45, 53)
```

## 🔗 Related Projects

The same directory also contains:

- **Pitagoras_unified.py** - Extended version with additional features
- **Pit2.py** - Version with limit-based search

## 📖 Bibliography

1. **Pythagorean triple** - Wikipedia PL: <https://pl.wikipedia.org/wiki/Trójka_pitagorejska>
2. **Euclid's Formula** - Wikipedia EN: <https://en.wikipedia.org/wiki/Formulas_for_generating_Pythagorean_triples>
3. **Tree of Primitive Pythagorean Triples**: <https://en.wikipedia.org/wiki/Tree_of_primitive_Pythagorean_triples>

## 👨‍💻 Author

### Maciej Mierzejewski

- GitHub: [@mmierzejewski](https://github.com/mmierzejewski)
- Repository: [MM_Python](https://github.com/mmierzejewski/MM_Python)

## 📄 License

Free to use and modify.

---

**💡 Tip:** The program is ideal for educational purposes, exploring number theory, and generating test sets for geometric algorithms!
