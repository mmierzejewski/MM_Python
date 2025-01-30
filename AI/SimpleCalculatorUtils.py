def add(x, y):
    """Add two numbers"""
    return x + y


def subtract(x, y):
    """Subtract two numbers"""
    return x - y


def multiply(x, y):
    """Multiply two numbers"""
    return x * y


def divide(x, y):
    """Divide two numbers"""
    try:
        return x / y
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."


def calculator():
    print("Simple Calculator")
    print("Select an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    # Get user input
    choice = input("Enter the number for your choice (1/2/3/4): ")

    if choice in ("1", "2", "3", "4"):
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
        except ValueError:
            print("Invalid input! Please enter numbers only.")
            return

        if choice == "1":
            print(f"The result of addition is: {add(num1, num2)}")
        elif choice == "2":
            print(f"The result of subtraction is: {subtract(num1, num2)}")
        elif choice == "3":
            print(f"The result of multiplication is: {multiply(num1, num2)}")
        elif choice == "4":
            print(f"The result of division is: {divide(num1, num2)}")
    else:
        print("Invalid choice! Please select a valid operation.")


if __name__ == "__main__":
    calculator()