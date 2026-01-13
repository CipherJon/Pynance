"""
Main calculator application.
This module provides a command-line interface for performing various mathematical operations.
"""

import os
from typing import List, Tuple, Callable, Dict, Any
from calculator.operations import (
    add, subtract, multiply, divide, power,
    square_root, percentage, modulo, absolute
)

# Operation definitions: (function, num_args, format_string)
OPERATIONS: Dict[str, Tuple[Callable[..., float], int, str]] = {
    '1': (add, 2, "{0} + {1} = {2}"),
    '2': (subtract, 2, "{0} - {1} = {2}"),
    '3': (multiply, 2, "{0} * {1} = {2}"),
    '4': (divide, 2, "{0} / {1} = {2}"),
    '5': (power, 2, "{0} ^ {1} = {2}"),
    '6': (square_root, 1, "√{0} = {1}"),
    '7': (percentage, 2, "{0} is {2}% of {1}"),
    '8': (modulo, 2, "{0} % {1} = {2}"),
    '9': (absolute, 1, "|{0}| = {1}")
}

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_number(prompt: str) -> float | None:
    """
    Get a valid number from user input.
    
    Args:
        prompt (str): The prompt to display to the user
        
    Returns:
        float | None: The valid number entered by the user, or None if interrupted
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled by user.")
            return None

def display_menu() -> None:
    """Display the calculator menu."""
    print("\nCalculator Menu:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Square Root")
    print("7. Percentage")
    print("8. Modulo")
    print("9. Absolute Value")
    print("h. Show History")
    print("c. Clear Screen")
    print("q. Quit")

def get_operation_inputs(num_args: int) -> List[float] | None:
    """
    Get the required number of inputs for an operation.
    
    Args:
        num_args (int): Number of arguments required for the operation
        
    Returns:
        List[float] | None: List of input numbers, or None if input was cancelled
    """
    inputs = []
    prompts = ["Enter first number: ", "Enter second number: "]
    
    for i in range(num_args):
        num = get_number(prompts[i])
        if num is None:
            return None
        inputs.append(num)
    
    return inputs

def perform_operation(choice: str, history: List[Tuple[str, float]]) -> None:
    """
    Perform the selected mathematical operation.
    
    Args:
        choice (str): The operation choice
        history (List[Tuple[str, float]]): List to store calculation history
    """
    if choice not in OPERATIONS:
        return
        
    try:
        operation, num_args, format_str = OPERATIONS[choice]
        
        # Get inputs
        inputs = get_operation_inputs(num_args)
        if inputs is None:
            return
            
        # Perform operation
        result = operation(*inputs)
        
        # Format and display result
        if num_args == 1:
            print(f"Result: {format_str.format(inputs[0], result)}")
            history.append((format_str.format(inputs[0], result), result))
        else:
            print(f"Result: {format_str.format(inputs[0], inputs[1], result)}")
            history.append((format_str.format(inputs[0], inputs[1], result), result))
            
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def show_history(history: List[Tuple[str, float]]) -> None:
    """
    Display the calculation history.
    
    Args:
        history (List[Tuple[str, float]]): List of calculation history
    """
    if not history:
        print("No calculations in history.")
        return
    
    print("\nCalculation History:")
    for i, (operation, result) in enumerate(history, 1):
        print(f"{i}. {operation}")

def main() -> None:
    """Main calculator function."""
    history: List[Tuple[str, float]] = []
    
    print("Welcome to the Advanced Calculator!")
    print("Type 'h' for help or 'q' to quit.")
    
    while True:
        display_menu()
        choice = input("\nSelect operation: ").lower()
        
        if choice == 'q':
            print("Thank you for using the calculator!")
            break
        elif choice == 'h':
            show_history(history)
        elif choice == 'c':
            clear_screen()
        elif choice in OPERATIONS:
            perform_operation(choice, history)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()