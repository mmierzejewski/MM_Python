from datetime import datetime
from typing import List


def generate_primes(limit: int) -> List[int]:
    """Generate a list of prime numbers up to a given limit using the Sieve of Eratosthenes."""
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False  # 0 and 1 are not prime numbers
    for i in range(2, int(limit ** 0.5) + 1):  # Only iterate up to sqrt(limit)
        if primes[i]:
            for j in range(i * i, limit + 1, i):  # Mark multiples of i as non-prime
                primes[j] = False
    return [x for x, is_prime in enumerate(primes) if is_prime]


def save_to_file(numbers: List[int], filename: str) -> None:
    """Save a list of numbers to a text file."""
    try:
        with open(filename, "w") as file:
            for number in numbers:
                file.write(f"{number}\n")
        print(f"Numbers successfully saved to {filename}.")
    except Exception as e:
        print(f"An error occurred while saving to {filename}: {e}")


def display_time_taken(key: str, start: datetime, stop: datetime) -> None:
    """Print the time duration for a specific process."""
    duration = stop - start
    print(f"{key} started at: {start}")
    print(f"{key} ended at: {stop}")
    print(f"{key} duration: {duration}\n")


def main():
    # Input Handling
    try:
        limit = int(input("Enter the range (a positive integer >= 2): "))
        if limit < 2:
            print("The range must be at least 2. Please try again.")
            return
    except ValueError:
        print("Invalid input! Please enter a valid positive integer.")
        return

    # Format Range Value
    formatted_limit = f"{limit:,}"
    print(f"\nPrime number range: {formatted_limit}")

    # Start Prime Calculation
    overall_start = datetime.now()

    # Step 1: Prime Number Calculation
    step_start = datetime.now()
    primes = generate_primes(limit)
    prime_count = len(primes)
    step_end = datetime.now()
    display_time_taken("Prime number generation", step_start, step_end)

    # Step 2: Choose Whether to Save to File
    user_choice = input("Would you like to save the prime numbers to primes.txt? (yes/no): ").strip().lower()
    if user_choice in ("yes", "y"):
        step_start = datetime.now()
        save_to_file(primes, "primes.txt")
        step_end = datetime.now()
        display_time_taken("Saving primes to file", step_start, step_end)
    else:
        print("Skipping file save.")

    # Step 3: Highest Prime Calculation
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