"""
Basic mathematical operations for the calculator.
This module provides various mathematical operations including basic arithmetic,
power, square root, percentage, modulo, and absolute value calculations.
"""

import math

def add(a: float, b: float) -> float:
    """
    Add two numbers.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Sum of a and b
        
    Raises:
        ValueError: If either input is NaN
    """
    if math.isnan(a) or math.isnan(b):
        raise ValueError("Cannot perform addition with NaN values")
    return a + b

def subtract(a: float, b: float) -> float:
    """
    Subtract second number from first number.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Difference between a and b
    """
    return a - b

def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Product of a and b
    """
    return a * b

def divide(a: float, b: float) -> float:
    """
    Divide first number by second number.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Quotient of a and b
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a: float, b: float) -> float:
    """
    Calculate a raised to the power of b.
    
    Args:
        a (float): Base number
        b (float): Exponent
        
    Returns:
        float: a raised to the power of b
    """
    return a ** b

def square_root(a: float) -> float:
    """
    Calculate the square root of a number.
    
    Args:
        a (float): Number to calculate square root of
        
    Returns:
        float: Square root of a
        
    Raises:
        ValueError: If a is negative
    """
    if a < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return a ** 0.5

def percentage(a: float, b: float) -> float:
    """
    Calculate what percentage a is of b.
    
    Args:
        a (float): Number to calculate percentage of
        b (float): Total value
        
    Returns:
        float: Percentage value
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot calculate percentage with zero total")
    return (a / b) * 100

def modulo(a: float, b: float) -> float:
    """
    Calculate the remainder of division of a by b.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: Remainder of a divided by b
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot calculate modulo with zero divisor")
    return a % b

def absolute(a: float) -> float:
    """
    Calculate the absolute value of a number.
    
    Args:
        a (float): Number to calculate absolute value of
        
    Returns:
        float: Absolute value of a
    """
    return abs(a)