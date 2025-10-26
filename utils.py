# # utils.py
# # This file contains helper functions used by various ciphers.
# import numpy as np

# # A constant for the English alphabet
# ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# def normalize_text(text: str) -> str:
#     """
#     Removes all non-alphabetic characters from the string
#     and converts it to uppercase.
    
#     Args:
#         text (str): The input string.
    
#     Returns:
#         str: The normalized, uppercase alphabetic string.
#     """
#     return "".join(filter(str.isalpha, text.upper()))

# def egcd(a, b):
#     """
#     Extended Euclidean Algorithm to find the greatest common divisor (gcd)
#     and coefficients for Bezout's identity.
    
#     Args:
#         a (int): First integer.
#         b (int): Second integer.
        
#     Returns:
#         tuple: (gcd, x, y) such that a*x + b*y = gcd
#     """
#     if a == 0:
#         return (b, 0, 1)
#     else:
#         g, y, x = egcd(b % a, a)
#         return (g, x - (b // a) * y, y)

# def mod_inverse(a, m):
#     """
#     Finds the modular multiplicative inverse of a under modulo m.
#     Required for Affine and Hill cipher decryption.
    
#     Args:
#         a (int): The number to find the inverse of.
#         m (int): The modulus.
        
#     Returns:
#         int or None: The modular inverse, or None if it doesn't exist.
#     """
#     g, x, y = egcd(a, m)
#     if g != 1:
#         # Modular inverse does not exist
#         return None
#     else:
#         return x % m

# def string_to_matrix(text: str, n: int) -> np.ndarray:
#     """
#     Converts a string of space-separated numbers into a NumPy n x n matrix.
#     Used for the Hill Cipher key.
    
#     Args:
#         text (str): A string of numbers separated by spaces.
#         n (int): The dimension of the matrix (e.g., 2 for 2x2).
    
#     Returns:
#         np.ndarray: The resulting n x n NumPy matrix.
    
#     Raises:
#         ValueError: If the number of elements doesn't form an n x n matrix.
#     """
#     numbers = list(map(int, text.split()))
#     if len(numbers) != n * n:
#         raise ValueError(f"Cannot form a {n}x{n} matrix with {len(numbers)} elements.")
    
#     matrix = np.array(numbers).reshape((n, n))
#     return matrix



# utils.py
# This file contains shared helper functions for various ciphers.

import numpy as np
from math import gcd  # <-- THIS IS THE NEWLY ADDED IMPORT

# Alphabet constant used by multiple ciphers
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def normalize_text(text: str) -> str:
    """
    Removes all non-alphabetic characters from a string and converts it to uppercase.
    
    Args:
        text (str): The input string.
        
    Returns:
        str: The normalized, uppercase alphabetic string.
    """
    return ''.join(filter(str.isalpha, text)).upper()

def egcd(a, b):
    """
    Extended Euclidean Algorithm.
    Returns the greatest common divisor and the coefficients of Bezout's identity.
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    """
    Finds the modular multiplicative inverse of a under modulo m.
    
    Args:
        a (int): The number to find the inverse of.
        m (int): The modulus.
        
    Returns:
        int or None: The modular inverse, or None if it does not exist.
    """
    g, x, y = egcd(a, m)
    if g != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

def string_to_matrix(text: str, n: int) -> np.ndarray:
    """
    Converts a string of space-separated numbers into a NumPy n x n matrix.
    
    Args:
        text (str): The string of numbers.
        n (int): The dimension of the matrix (e.g., 2 for 2x2).
        
    Returns:
        np.ndarray: The resulting n x n matrix.
    """
    numbers = list(map(int, text.split()))
    if len(numbers) != n * n:
        raise ValueError(f"Invalid number of elements for a {n}x{n} matrix.")
    return np.array(numbers).reshape((n, n))

def matrix_to_string(matrix: np.ndarray) -> str:
    """
    Converts a NumPy matrix back to a space-separated string.
    
    Args:
        matrix (np.ndarray): The input matrix.
        
    Returns:
        str: The string representation of the matrix elements.
    """
    return ' '.join(map(str, matrix.flatten()))
