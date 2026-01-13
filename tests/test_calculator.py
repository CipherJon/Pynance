"""
Test suite for the calculator operations.
This module contains unit tests for all calculator operations.
"""

import pytest
import math
from calculator.operations import (
    add, subtract, multiply, divide, power,
    square_root, percentage, modulo, absolute
)

# Test basic arithmetic operations
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(2.5, 3.5) == 6.0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 0) == 0
    assert subtract(3.5, 2.5) == 1.0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0
    assert multiply(2.5, 2) == 5.0

def test_divide():
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    assert divide(0, 5) == 0
    with pytest.raises(ValueError):
        divide(5, 0)

# Test advanced operations
def test_power():
    assert power(2, 3) == 8
    assert power(2, 0) == 1
    assert power(2, -1) == 0.5
    assert power(0, 0) == 1

def test_square_root():
    assert square_root(4) == 2
    assert square_root(0) == 0
    assert square_root(2) == 2 ** 0.5
    with pytest.raises(ValueError):
        square_root(-1)

def test_percentage():
    assert percentage(50, 100) == 50
    assert percentage(0, 100) == 0
    assert percentage(100, 100) == 100
    with pytest.raises(ValueError):
        percentage(50, 0)

def test_modulo():
    assert modulo(5, 2) == 1
    assert modulo(10, 5) == 0
    assert modulo(7, 3) == 1
    with pytest.raises(ValueError):
        modulo(5, 0)

def test_absolute():
    assert absolute(5) == 5
    assert absolute(-5) == 5
    assert absolute(0) == 0
    assert absolute(-2.5) == 2.5

# Test edge cases and error handling
def test_edge_cases():
    # Test very large numbers
    assert add(1e308, 1e308) == 2e308
    assert multiply(1e308, 0) == 0
    
    # Test very small numbers
    assert add(1e-308, 1e-308) == 2e-308
    assert multiply(1e-308, 0) == 0
    
    # Test NaN handling
    with pytest.raises(ValueError, match="Cannot perform addition with NaN values"):
        add(float('nan'), 1)
    with pytest.raises(ValueError, match="Cannot perform addition with NaN values"):
        add(1, float('nan'))
    
    # Test Infinity handling
    assert math.isinf(add(float('inf'), 1))
    assert math.isinf(add(1, float('inf')))
    assert math.isinf(add(float('inf'), float('inf'))) 