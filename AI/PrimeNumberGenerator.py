import math  # For square root calculation

# List to store the prime numbers
prime_numbers = [2]


def is_prime(number: int) -> bool:
    """Check if a number is a prime number."""
    if number < 2:
        return False
    for divisor in prime_numbers:
        if divisor > math.isqrt(number):  # Only check divisors up to √number
            break
        if number % divisor == 0:
            return False
    return True


def calculate_primes(limit: int) -> None:
    """Populate the list of prime numbers up to a given limit."""
    global prime_numbers
    # Avoid recomputing primes already calculated
    last_checked = prime_numbers[-1] if prime_numbers else 1
    for num in range(last_checked + 1, limit):
        if is_prime(num):
            prime_numbers.append(num)


def main():
    """Main function to get user input and display results."""
    try:
        limit = int(input("Enter the range limit: "))
        if limit < 2:
            print("The range must be 2 or higher.")
            return

        calculate_primes(limit)
        print("Prime numbers:", prime_numbers)
        print(f"Count of prime numbers up to {limit}: {len(prime_numbers)}")

    except ValueError:
        print("Please enter a valid number.")


if __name__ == "__main__":
    main()