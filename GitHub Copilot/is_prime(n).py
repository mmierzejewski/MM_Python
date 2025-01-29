def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def count_primes(start, end):
    prime_count = 0
    for num in range(start, end + 1):
        if is_prime(num):
            prime_count += 1
    return prime_count

# Example usage
start = 1
end = 1000000
print(f"Number of prime numbers between {start} and {end}: {count_primes(start, end)}")