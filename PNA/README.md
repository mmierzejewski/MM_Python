# 🔢 Prime Number Generator - PNA.py

## 📋 Description

**PNA.py** (Prime Numbers Analyzer) is an efficient prime number generator using the **Sieve of Eratosthenes**. The program finds all prime numbers within a given range with performance timing and detailed statistics. It includes an optimization for very large ranges in the form of a **segmented sieve**.

### What Is a Prime Number?

A **prime number** is a natural number greater than 1 that has exactly two divisors: 1 and itself.

**Examples:**

- ✅ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...
- ❌ 1 (has only one divisor)
- ❌ 4 = 2 × 2 (has more than two divisors)
- ❌ 6 = 2 × 3 (has more than two divisors)

## ⭐ Key Features

### 🎯 Three Operation Modes

#### Mode 1: Primes up to a Limit

Find all prime numbers from 2 to a given limit n.

#### Mode 2: First n Primes

Find exactly the first n prime numbers (e.g., the first 100, 1000, 10000 primes).

- **Automatic estimation**: Uses the mathematical approximation n * (ln(n) + ln(ln(n)))
- **Smart expansion**: Automatically increases the limit if needed
- **Optimization**: Uses an efficient sieve for large n

#### Mode 3: Check a Prime Number (New)

Check whether a given number is prime.

- **Fast verification**: O(√n) algorithm
- **Optimization**: Only checks odd divisors
- **Divisor display**: If the number is not prime, the program shows its proper divisors (excluding 1 and the number itself)
- **Timing**: Detailed performance timing for the check

### 🚀 Two Generation Methods

#### 1. Standard Sieve of Eratosthenes

- **Range**: Up to ~100 million
- **Memory**: O(n) - ~100 MB for 100 million
- **Speed**: Very fast for small and medium ranges
- **Usage**: Automatic for ranges < 10 million

#### 2. Segmented Sieve (Advanced)

- **Range**: Above 1 billion
- **Memory**: O(√n) - memory savings!
- **Speed**: Optimal for very large ranges
- **Usage**: Recommended/automatic for ranges > 1 billion

### 📊 Detailed Statistics

- **Range**: From-to
- **Number found**: How many primes
- **Density**: Percentage of primes in the range
- **Smallest/Largest**: Extreme values
- **Generation time**: Performance timing

### 💾 Export to File

- Automatic saving to the PNA/ directory
- Format: `primes_up_to_{limit}_{timestamp}.txt`
- Content: Header + prime numbers (10 per line)
- Offered for sets > 100 numbers

### 🔄 Menu Loop

- The program runs in continuous mode
- Automatic return to the main menu after computations
- Ability to perform multiple operations without restarting
- Option 4: "Exit" - a clean way to quit the program

### ⚡ Performance Optimizations

- Progress bar for large ranges (> 1M)
- Warnings about time/memory for large limits
- Automatic suggestion of the segmented sieve
- Time formatting (μs, ms, s, m)

## 🔬 Algorithm: Sieve of Eratosthenes

### How It Works

The **Sieve of Eratosthenes** (3rd century BC) is one of the oldest and most efficient algorithms for finding prime numbers.

#### Algorithm Steps

1. Create a list of numbers from 2 to n
2. Start with the first number (2)
3. Mark all multiples of this number as composite
4. Move to the next unmarked number
5. Repeat steps 3-4 until √n

#### Visualization (for n=30)

```text
Start: 2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30

Step 1 (2): 2  3  ✗  5  ✗  7  ✗  9  ✗  11 ✗  13 ✗  15 ✗  17 ✗  19 ✗  21 ✗  23 ✗  25 ✗  27 ✗  29 ✗

Step 2 (3): 2  3  ✗  5  ✗  7  ✗  ✗  ✗  11 ✗  13 ✗  ✗  ✗  17 ✗  19 ✗  ✗  ✗  23 ✗  ✗  ✗  ✗  ✗  29 ✗

Step 3 (5): 2  3  ✗  5  ✗  7  ✗  ✗  ✗  11 ✗  13 ✗  ✗  ✗  17 ✗  19 ✗  ✗  ✗  23 ✗  ✗  ✗  ✗  ✗  29 ✗

Result: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
```

### Time Complexity

- **Standard sieve**: O(n log log n)
- **Segmented sieve**: O(n log log n) with O(√n) memory

## 🚀 Installation and Running

### Requirements

```bash
Python 3.10+

# No external dependencies - standard library only

```

### Running

```bash
cd PNA
python PNA.py
```

## 💻 How to Use

### Step 1: Run the program

```bash
python PNA.py
```

### Step 2: Choose the operation mode

```text
╔══════════════════════════════════════════════════════╗
║        PRIME NUMBER GENERATOR                         ║
║            (Sieve of Eratosthenes)                    ║
╚══════════════════════════════════════════════════════╝

Choose the operation mode:
  1. Find all primes up to a given limit
  2. Find the first n primes
  3. Check whether a number is prime
  4. Exit (quit the program)

Your choice (1/2/3/4): 1

Enter the range (integer >= 2): 100
```

### Step 3: Get the results

#### Small Ranges (< 10M)

```text
🔍 Searching for primes up to 100...

⏱️  Generation time: 0.145 ms

============================================================
📊 PRIME NUMBER STATISTICS
============================================================
Range:               2 to 100
Primes:              25
Density:             25.0000%
Smallest:            2
Largest:             97
All numbers:         2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
============================================================
```

#### Medium Ranges (10M - 1B)

```text
⚠️  Large range (50,000,000) may require significant time and memory!
   Estimated memory: ~48 MB
   Continue? (Y/N) [N]: Y

🔍 Searching for primes up to 50,000,000...
Progress: 100.0% (checking 7,071)

⏱️  Generation time: 2.847 s

============================================================
📊 PRIME NUMBER STATISTICS
============================================================
Range:               2 to 50,000,000
Primes:              3,001,134
Density:             6.0023%
Smallest:            2
Largest:             49,999,991
============================================================

💾 Save the primes to a file? (Y/N) [Y]: Y
✅ Primes saved to: /Users/.../PNA/primes_up_to_50000000_20251212_143052.txt
```

#### Very Large Ranges (> 1B) - Segmented Sieve

```text
⚠️  VERY LARGE range (2,000,000,000)!
   Standard sieve: ~1907 MB (~1.9 GB)
   Segmented sieve: ~43 MB (recommended!)

   💡 The segmented sieve uses significantly less memory for large ranges
   Use the segmented sieve? (Y/N) [Y]: Y

🔍 Searching for primes up to 2,000,000,000...
   Using segmented sieve (memory optimization)
Phase 1/2: Finding base primes up to 44,721...
Phase 2/2: Processing 1,955 segments of size 1,000,000...
Progress: 100.0% (processed up to 2,000,000,000)

⏱️  Generation time: 2m 15.34s

============================================================
📊 PRIME NUMBER STATISTICS
============================================================
Range:               2 to 2,000,000,000
Primes:              98,222,287
Density:             4.9111%
Smallest:            2
Largest:             1,999,999,973
============================================================

💾 Save the primes to a file? (Y/N) [Y]: Y
✅ Primes saved to: /Users/.../PNA/primes_up_to_2000000000_20251212_144523.txt
```

## 📊 Usage Examples

### Example 1: First n Primes (NEW!)

```bash
python PNA.py

# Choice: 2 (First n primes)

# Input: 100

# Output: The first 100 primes

# Largest: 541

# Time: < 5 ms

# Sample output

============================================================
📊 PRIME NUMBER STATISTICS
============================================================
Mode:                First 100 primes
Found:               100
Smallest:            2
Largest:             541
First 10:            2, 3, 5, 7, 11, 13, 17, 19, 23, 29
Last 10:             467, 479, 487, 491, 499, 503, 509, 521, 523, 541
============================================================
```

### Example 2: Small Ranges (Limit Mode)

```bash
python PNA.py

# Choice: 1 (Limit)

# Input: 1000

# Output: 168 primes (16.8%)

# Time: < 1 ms

```

### Example 3: Medium Ranges (Limit Mode)

```bash
python PNA.py

# Choice: 1 (Limit)

# Input: 10000000 (10 million)

# Output: 664,579 primes (6.6%)

# Time: ~0.5s

# Memory: ~10 MB

```

### Example 4: Large Ranges (Limit Mode)

```bash
python PNA.py

# Choice: 1 (Limit)

# Input: 100000000 (100 million)

# Output: 5,761,455 primes (5.76%)

# Time: ~5s

# Memory: ~100 MB

```

### Example 5: Very Large Ranges (Segmented Sieve)

```bash
python PNA.py

# Choice: 1 (Limit)

# Input: 1000000000 (1 billion)

# Method: Segmented sieve (automatic)

# Output: 50,847,534 primes (5.08%)

# Time: ~1 minute

# Memory: ~32 MB (instead of ~950 MB!)

```

### Example 6: First 1 Million Primes

```bash
python PNA.py

# Choice: 2 (First n)

# Input: 1000000

# Output: The first 1,000,000 primes

# Largest: 15,485,863

# T

### Example 7a: Checking a Prime Number (NEW!)

```bash

python PNA.py

# Choice: 3 (Check whether a number is prime)

# Input: 17

# Output

============================================================
✅ 17 IS a prime number
============================================================
⏱️  Check time: 2.15 μs

```text

### Example 7b: Checking a Non-Prime Number with Divisors (NEW!)

```bash

python PNA.py

# Choice: 3 (Check whether a number is prime)

# Input: 24

# Output

============================================================
❌ 24 is NOT a prime number

📋 Divisors of 24 (excluding 1 and 24):
   2, 3, 4, 6, 8, 12
   Number of proper divisors: 6
============================================================
⏱️  Check time: 3.42 μs

```text

### Example 8: The get_divisors() Function (NEW!)

```python

def get_divisors(n: int) -> list[int]:
    """
    Finds all divisors of the given number.

    Algorithm:

    - Iterates from 1 to √n
    - For each divisor i, adds both i and n/i
    - Avoids duplicates for perfect squares
    - Returns a sorted list of divisors

    Complexity: O(√n)

    Examples:

    - is_prime(2) → True (the smallest prime)
    - is_prime(17) → True
    - is_prime(97) → True
    - is_prime(100) → False (100 = 2 × 50)
    - is_prime(1) → False (not a prime number)
    """

```text

### 2. First n Primes

# Input: 97

# Output

============================================================
✅ 97 IS a prime number
============================================================
⏱️  Check time: 3.81 μs

# Example - composite number

# Input: 100

# Output

============================================================
❌ 100 is NOT a prime number
============================================================
⏱️  Check time: 2.15 μs
```Time: ~1.5s

```3. Segmented Sieve
```python

def generate_primes_segmented(limit: int, verbose: bool = False) -> list[int]
    """
    Generates prime numbers for very large ranges.

    Advantages:

    - Memory: O(√n) instead of O(n)
    - For 1 billion: ~32 MB instead of ~950 MB
    - Progress bar for tracking progress

    Algorithm:

    1. Find base primes up to √n
    2. Process the range in segments (default 1M)
    3. In each segment, mark multiples
    """

```text

### 4. Standard Sieve

```python

def generate_primes(limit: int, verbose: bool = False) -> list[int]
    """
    Classic Sieve of Eratosthenes.

    Advantages:

    - Very fast for ranges < 100M
    - Simple and proven
    - Progress bar for ranges > 1M

    Complexity: O(n log log n)
    """

```text

### 5. Time Formatting

```python

def format_duration(duration) -> str
    """
    Automatic time formatting:

    - μs (microseconds): < 1ms
    - ms (milliseconds): < 1s
    - s (seconds): < 60s
    - m (minutes) + s: ≥ 60s
    """

```text

### 6 Classic Sieve of Eratosthenes.

    Advantages:
    - Very fast for ranges < 100M
    - Simple and proven
    - Progress bar for ranges > 1M

    Complexity: O(n log log n)
    """
```

### 4. Time Formatting

```python
def format_duration(duration) -> str
    """
    Automatic time formatting:
    - μs (microseconds): < 1ms
    - ms (milliseconds): < 1s
    - s (seconds): < 60s
    - m (minutes) + s: ≥ 60s
    """
```

### 5. Saving to a File

```python
def save_primes_to_file(primes: list[int], limit: int, filename: Optional[str] = None)
    """
    Saves the prime numbers to a text file.

    File format:
    - Header with metadata (range, count, date)
    - Primes: 10 per line, comma-separated
    - UTF-8 encoding
    """
```

## 📈 Performance

### Benchmarks (Apple M1/Intel i5)

| Range | Primes | Time | Memory | Method |
| --- | --- | --- | --- | --- |
| 1,000 | 168 | < 1 ms | < 1 MB | Standard |
| 10,000 | 1,229 | < 5 ms | < 1 MB | Standard |
| 100,000 | 9,592 | ~20 ms | ~1 MB | Standard |
| 1,000,000 | 78,498 | ~50 ms | ~5 MB | Standard |
| 10,000,000 | 664,579 | ~500 ms | ~10 MB | Standard |
| 100,000,000 | 5,761,455 | ~5s | ~100 MB | Standard |
| 1,000,000,000 | 50,847,534 | ~60s | ~32 MB | **Segmented** |
| 2,000,000,000 | 98,222,287 | ~135s | ~44 MB | **Segmented** |

### Prime Number Density

According to the **Prime Number Theorem**:

```text
π(n) ≈ n / ln(n)
```

Density decreases as n increases:

- **n = 100**: 25% primes
- **n = 1,000**: 16.8%
- **n = 10,000**: 12.3%
- **n = 100,000**: 9.6%
- **n = 1,000,000**: 7.8%
- **n = 10,000,000**: 6.6%
- **n = 100,000,000**: 5.8%
- **n = 1,000,000,000**: 5.1%

## 🔍 Technical Details

### Memory Optimizations

#### Standard Sieve

```python
is_prime = [True] * (limit + 1)  # O(n) memory

# For 1 billion: ~950 MB

```

#### Segmented Sieve

```python
result = generate_primes(sqrt_limit)  # O(√n) memory for the base
segment = [True] * segment_size        # Only 1M elements at a time

# For 1 billion: ~32 MB (30x savings!)

```

### Progress Bar

For ranges > 1,000,000:

```text
Progress: 45.3% (checking 3,207)
```

For the segmented sieve:

```text
Phase 1/2: Finding base primes up to 44,721...
Phase 2/2: Processing 1,955 segments of size 1,000,000...
Progress: 67.8% (processed up to 678,000,000)
```

## 🐛 Error Handling

The program handles:

- ❌ **Invalid input**: Non-numbers, numbers < 2
- ⚠️ **Warnings**: Large ranges (> 10M) with memory estimation
- 💡 **Suggestions**: Automatic recommendation of the segmented sieve
- 🚨 **MemoryError**: Catching memory errors with suggestions
- 🛑 **Ctrl+C**: Safe interruption, 2 or 3?

**A:**

- **Mode 1** finds all primes up to the limit (e.g., up to 100 will find 25 primes).
- **Mode 2** finds exactly the first n primes (e.g., the first 100 numbers, i.e. 2, 3, 5... up to 541).
- **Mode 3** checks whether a single number is prime (e.g., whether 97 is prime → YES

### Error Handling Examples

#### Range too large (standard sieve)

```text
❌ Memory error: Not enough memory to create sieve for 5,000,000,000

💡 Suggestions:
   • Try a smaller range
   • Use the segmented sieve option for large ranges
   • Close other applications to free up memory
```

#### Invalid input

```text
Enter the range (integer >= 2): abc
❌ Invalid input! Please enter a valid positive integer.
```

## ❓ FAQ

### Q: What is the difference between mode 1 and 2?

**A:** Mode 1 finds all primes up to the limit (e.g., up to 100). Mode 2 finds exactly the first n primes (e.g., the first 100 numbers, i.e. 2, 3, 5... up to 541).

### Q: How does the program estimate the limit for the first n numbers?

**A:** It uses the mathematical approximation n × (ln(n) + ln(ln(n))) × 1.3, and then automatically expands the limit if needed.

### Q: What is the maximum range value?

**A:** Theoretically there is no limit thanks to the segmented sieve. In practice, computation time is the constraint (e.g., 10 billion would take ~20 minutes).

### Q: Is 1 a prime number?

**A:** No! A prime number must have exactly two divisors. 1 has only one divisor (itself).

### Q: Why does the density of primes decrease?

**A:** According to the Prime Number Theorem, primes become rarer as n grows, with a density of ~1/ln(n).

### Q: What is a segmented sieve?

**A:** It's an optimization of the Sieve of Eratosthenes that processes the range in small segments instead of all at once, saving memory.

### Q: Can I save the results for small ranges?

**A:** The save option appears automatically for ranges with > 100 primes.

### Q: How does the progress bar work?

**A:** It's displayed automatically for ranges > 1,000,000, showing the percentage of completion and the number currently being checked.

## 📚 Mathematical Theory

### Prime Number Theorem

For large n, the number of primes ≤ n is approximately:

```text
π(n) ≈ n / ln(n)
```

where π(n) is the prime-counting function.

### The First Primes

```text
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97...
```

### Fun Facts

- **2** is the only even prime number
- Every natural number > 1 has a unique prime factorization
- Between n and 2n there always exists at least one prime (Bertrand's Postulate)
- The largest known prime number (2024): 2^82,589,933 - 1 (over 24 million digits!)

### The Riemann Hypothesis

Related to the distribution of primes, one of the **Millennium Prize Problems** with a $1,000,000 reward!

## 🔗 Related Projects

Also available in the same directory:

- **PNA2a.py** - An improved version with additional features

## 📖 Bibliography

1. **Sieve of Eratosthenes** - Wikipedia PL: <https://pl.wikipedia.org/wiki/Sito_Eratostenesa>
2. **Prime numbers** - Wikipedia PL: <https://pl.wikipedia.org/wiki/Liczba_pierwsza>
3. **Prime Number Theorem**: <https://en.wikipedia.org/wiki/Prime_number_theorem>
4. **Segmented Sieve**: <https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Segmented_sieve>

## 👨‍💻 Author

### Maciej Mierzejewski

- GitHub: [@mmierzejewski](https://github.com/mmierzejewski)
- Repository: [MM_Python](https://github.com/mmierzejewski/MM_Python)

## 📄 License

Free to use and modify.

---

**💡 Tip:** This program is ideal for educational purposes, experimenting with number theory, and generating large sets of prime numbers for cryptographic testing!
