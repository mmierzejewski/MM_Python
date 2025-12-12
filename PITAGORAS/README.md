# 🔺 Pythagorean Triples Generator

Collection of scripts for generating and analyzing Pythagorean triples (a² + b² = c²).

## 📁 Files

### `Pitagoras_unified.py` ⭐ **RECOMMENDED**
**Unified, optimized script combining features from all versions.**

#### Features:
- ✅ **Primitive triples only** - eliminates duplicates (no 3,4,5 and 6,8,10)
- 📊 Input by **count** (number of triples to generate)
- 📋 Complete output table with:
  - Triangle dimensions (a, b, c)
  - Perimeter (obwód)
  - Area (powierzchnia)
  - Prime number detection
- 🔢 Sorted by perimeter (smallest first)
- 📈 Statistical analysis
- ⚡ Fast Euclid's formula algorithm
- ✓ Duplicate verification

#### Usage:
```bash
python Pitagoras_unified.py
# Enter number of triples: 10
```

#### Output Example:
```
#        a     b     c  Perimeter         Area Primes
1        3     4     5         12          6.0 [3, 5]
2        5    12    13         30         30.0 [5, 13]
3        8    15    17         40         60.0 [17]
...
```

---

### `Pit2.py`
Original script with prime analysis.

#### Features:
- Finds triples where c < limit
- Prime number detection
- Detailed statistics

#### Usage:
```bash
python Pit2.py
# Enter limit: 100
```

---

### `Pitagoras.py`
Original script with two algorithms.

#### Features:
- Brute force method (slow)
- Euclid's formula (fast)
- Includes multiples (3,4,5 AND 6,8,10)

#### Usage:
```bash
python Pitagoras.py
# Enter limit: 100
```

---

## 📚 What are Pythagorean Triples?

A **Pythagorean triple** is a set of three positive integers a, b, c such that:

```
a² + b² = c²
```

Examples:
- (3, 4, 5) → 3² + 4² = 9 + 16 = 25 = 5²
- (5, 12, 13) → 5² + 12² = 25 + 144 = 169 = 13²
- (8, 15, 17) → 8² + 15² = 64 + 225 = 289 = 17²

### Primitive vs Non-Primitive

**Primitive triples**: gcd(a, b, c) = 1
- (3, 4, 5) ✓ Primitive
- (5, 12, 13) ✓ Primitive

**Non-primitive triples**: Multiples of primitive triples
- (6, 8, 10) = 2 × (3, 4, 5) ✗ Non-primitive
- (9, 12, 15) = 3 × (3, 4, 5) ✗ Non-primitive

## 🔬 Algorithm: Euclid's Formula

To generate **primitive** Pythagorean triples:

For any two coprime integers m > n > 0 with different parity:

```
a = m² - n²
b = 2mn
c = m² + n²
```

**Example**: m=2, n=1
- a = 2² - 1² = 4 - 1 = 3
- b = 2 × 2 × 1 = 4
- c = 2² + 1² = 4 + 1 = 5
- Result: (3, 4, 5) ✓

## 📊 Comparison

| Feature | Pitagoras_unified.py | Pit2.py | Pitagoras.py |
|---------|---------------------|---------|--------------|
| Input method | Count | Limit | Limit |
| Primitive only | ✅ | ✅ | ❌ |
| Perimeter | ✅ | ❌ | ❌ |
| Area | ✅ | ❌ | ❌ |
| Prime detection | ✅ | ✅ | ❌ |
| Sorted output | ✅ Perimeter | ✅ Perimeter | ✅ c value |
| Duplicate check | ✅ | ❌ | ❌ |
| Statistics | ✅ Detailed | ✅ Basic | ✅ Basic |

## 🎯 Recommendations

**Use `Pitagoras_unified.py` for:**
- Getting exact number of unique triples
- Detailed analysis with perimeter and area
- Eliminating duplicate multiples
- Prime number analysis
- Professional output formatting

**Use `Pit2.py` for:**
- Finding all triples up to a limit
- Quick prime analysis

**Use `Pitagoras.py` for:**
- Learning purposes
- Comparing algorithms
- Including multiples

## 💡 Examples

### Generate 5 primitive triples:
```bash
python Pitagoras_unified.py
# Input: 5
# Output: (3,4,5), (5,12,13), (8,15,17), (7,24,25), (20,21,29)
```

### Generate 100 triples:
```bash
python Pitagoras_unified.py
# Input: 100
# Gets exactly 100 unique primitive triples sorted by perimeter
```

## 📖 References

- [Pythagorean Triple - Wikipedia](https://en.wikipedia.org/wiki/Pythagorean_triple)
- [Euclid's Formula](https://en.wikipedia.org/wiki/Formulas_for_generating_Pythagorean_triples#Euclid's_formula)
- [Tree of Primitive Pythagorean Triples](https://en.wikipedia.org/wiki/Tree_of_primitive_Pythagorean_triples)

## 🔧 Requirements

```bash
# Python 3.8+
# No external dependencies - uses only standard library
```
