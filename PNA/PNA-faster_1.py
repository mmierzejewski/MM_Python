from datetime import datetime
from typing import List


def generate_primes(limit: int) -> List[int]:
    """Generate a list of prime numbers up to a given limit using an optimized Sieve of Eratosthenes."""
    if limit < 2:
        return []

    # Initialize a list to track prime status, only for odd numbers
    primes = [True] * ((limit // 2) + 1)
    primes[0] = False  # 1 is not a prime number

    # Handle the number 2 separately
    prime_list = [2]

    # Iterate over odd numbers only
    for i in range(3, limit + 1, 2):
        if primes[i // 2]:
            prime_list.append(i)
            for j in range(i * i, limit + 1, 2 * i):
                primes[j // 2] = False

    return prime_list


def display_time_taken(key: str, start: datetime, stop: datetime) -> None:
    """Print the time duration for a specific process."""
    duration = stop - start
    print(f"{key} started at: {start}")
    print(f"{key} ended at: {stop}")
    print(f"{key} duration: {duration}\n")


def main():
    # Set limit value directly (no user interaction)
    limit = 1000000  # Change this value as needed
    
    # Validate the limit
    if limit < 2:
        print("The range must be at least 2.")
        return

    # Format Range Value
    formatted_limit = f"{limit:,}"
    print(f"Prime number range: {formatted_limit}")

    # Start Prime Calculation
    overall_start = datetime.now()

    # Step 1: Prime Number Calculation
    step_start = datetime.now()
    primes = generate_primes(limit)
    prime_count = len(primes)
    step_end = datetime.now()
    display_time_taken("Prime number generation", step_start, step_end)

    # Step 2: Highest Prime Calculation
    step_start = datetime.now()
    highest_prime = primes[-1] if primes else None
    step_end = datetime.now()
    display_time_taken("Highest prime determination", step_start, step_end)

    # Print Results
    print(f"Total primes in the range 2 to {formatted_limit}: {prime_count:,}")
    if highest_prime:
        print(f"The highest prime in the range is: {highest_prime:,}")
    else:
        print("No primes found in this range.")

    # Overall Timing
    overall_end = datetime.now()
    display_time_taken("Overall computation", overall_start, overall_end)


if __name__ == "__main__":
    main()