from datetime import datetime


def sieve_of_eratosthenes(limit: int) -> list[int]:
    """Generate a list of prime numbers up to a given limit using the Sieve of Eratosthenes."""
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False  # 0 and 1 are not prime numbers.
    for i in range(2, int(limit ** 0.5) + 1):  # Only iterate up to sqrt(limit).
        if primes[i]:
            for j in range(i * i, limit + 1, i):  # Mark multiples of i as non-prime.
                primes[j] = False
    return [x for x, is_prime in enumerate(primes) if is_prime]


def main():
    # User Input
    try:
        limit = int(input("Enter the maximum range (positive integer): "))
        if limit < 2:
            print("The range must be at least 2. Please try again.")
            return
    except ValueError:
        print("Invalid input! Please enter a valid positive integer.")
        return

    # Display Input Range
    formatted_limit = f"{limit:,}"  # Format with thousands separator for readability
    print(f"\nPrime number range to: {formatted_limit}")

    # Start Calculation
    start_time = datetime.now()
    print(f"Calculation started at: {start_time}")

    primes = sieve_of_eratosthenes(limit)

    # Output Prime Count and Percentage
    prime_count = len(primes)
    percentage_primes = (prime_count / limit) * 100
    print(f"\nTotal prime numbers in the range 2 to {formatted_limit}: {prime_count:,}")
    print(f"Percentage of primes in range: {percentage_primes:.2f}%")

    # Timings
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print(f"\nCalculation finished at: {end_time}")
    print(f"Total computation time: {elapsed_time}")


if __name__ == "__main__":
    main()
