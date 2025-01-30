def generate_fibonacci_upto(n):
    """
    Generate Fibonacci sequence up to a given number `n`.
    """
    if n < 0:
        return "Invalid input! Please enter a non-negative number."

    fib_prev, fib_curr = 0, 1
    results = []

    while fib_prev <= n:
        results.append(fib_prev)
        fib_prev, fib_curr = fib_curr, fib_prev + fib_curr

    return results


def get_nth_fibonacci(n):
    """
    Get the n-th Fibonacci number.
    """
    if n <= 0:
        return "Invalid input! Please enter a positive integer."

    fib_prev, fib_curr = 0, 1
    for _ in range(2, n):
        fib_prev, fib_curr = fib_curr, fib_prev + fib_curr

    return fib_curr if n > 1 else 0


def generate_first_n_fibonacci(n):
    """
    Generate the first `n` Fibonacci numbers starting from 0.
    """
    if n <= 0:
        return "Invalid input! Please enter a positive integer."

    fib_prev, fib_curr = 0, 1
    results = [0] if n >= 1 else []

    for _ in range(1, n):
        results.append(fib_curr)
        fib_prev, fib_curr = fib_curr, fib_prev + fib_curr

    return results


def main():
    try:
        print("Choose an option:")
        print("1. Generate Fibonacci numbers up to a value")
        print("2. Get the n-th Fibonacci number")
        print("3. Generate the first n Fibonacci numbers starting from 0")
        choice = int(input("Your choice (1, 2 or 3): "))

        if choice == 1:
            n = int(input("Enter the maximum value for the Fibonacci sequence: "))
            fib_sequence = generate_fibonacci_upto(n)
            print(f"Fibonacci numbers up to {n}: {fib_sequence}")
        elif choice == 2:
            n = int(input("Enter the position (n) of the Fibonacci number: "))
            nth_fib = get_nth_fibonacci(n)
            print(f"The {n}-th Fibonacci number is: {nth_fib}")
        elif choice == 3:
            n = int(input("Enter the number of Fibonacci numbers to generate: "))
            first_n_fib = generate_first_n_fibonacci(n)
            print(f"The first {n} Fibonacci numbers are: {first_n_fib}")
        else:
            print("Invalid choice! Please select 1, 2, or 3.")
    except ValueError:
        print("Invalid input! Please enter a valid number.")


if __name__ == "__main__":
    main()