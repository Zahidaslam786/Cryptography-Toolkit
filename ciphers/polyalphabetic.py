# This file implements the Vigenere, Playfair, and Hill ciphers.

import numpy as np
from utils import normalize_text, ALPHABET, mod_inverse

# --- Vigenere Cipher ---

def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypts text using the Vigenere cipher.
    
    Args:
        plaintext (str): The text to encrypt.
        key (str): The keyword for shifting.
        
    Returns:
        str: The encrypted ciphertext.
    """
    normalized_text = normalize_text(plaintext)
    normalized_key = normalize_text(key)
    ciphertext = ""
    key_index = 0
    for char in normalized_text:
        p_index = ALPHABET.index(char)
        k_index = ALPHABET.index(normalized_key[key_index])
        
        encrypted_index = (p_index + k_index) % 26
        ciphertext += ALPHABET[encrypted_index]
        
        key_index = (key_index + 1) % len(normalized_key)
        
    return ciphertext

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypts text from a Vigenere cipher.
    
    Args:
        ciphertext (str): The text to decrypt.
        key (str): The keyword used for encryption.
        
    Returns:
        str: The decrypted plaintext.
    """
    normalized_text = normalize_text(ciphertext)
    normalized_key = normalize_text(key)
    plaintext = ""
    key_index = 0
    for char in normalized_text:
        c_index = ALPHABET.index(char)
        k_index = ALPHABET.index(normalized_key[key_index])
        
        decrypted_index = (c_index - k_index + 26) % 26
        plaintext += ALPHABET[decrypted_index]
        
        key_index = (key_index + 1) % len(normalized_key)
        
    return plaintext

# --- Playfair Cipher ---

def generate_playfair_matrix(key: str) -> list[list[str]]:
    """
    Generates the 5x5 Playfair key matrix. 'J' is treated as 'I'.
    """
    key = normalize_text(key).replace('J', 'I')
    matrix_chars = []
    
    # Add unique characters from the key
    for char in key:
        if char not in matrix_chars:
            matrix_chars.append(char)
            
    # Add remaining alphabet characters
    for char in ALPHABET:
        if char not in matrix_chars and char != 'J':
            matrix_chars.append(char)
            
    # Construct the 5x5 matrix
    matrix = [matrix_chars[i:i+5] for i in range(0, 25, 5)]
    return matrix

def find_char_coords(matrix: list[list[str]], char: str) -> tuple[int, int]:
    """Finds the (row, col) of a character in the Playfair matrix."""
    for r, row_list in enumerate(matrix):
        if char in row_list:
            return r, row_list.index(char)
    return -1, -1 # Should not happen with valid input

def playfair_process(text: str, key: str, mode: str = 'encrypt') -> str:
    """
    A helper function to handle both encryption and decryption for Playfair.
    """
    matrix = generate_playfair_matrix(key)
    text = normalize_text(text).replace('J', 'I')
    
    # Create digraphs (pairs of letters)
    digraphs = []
    i = 0
    while i < len(text):
        char1 = text[i]
        if i + 1 == len(text) or char1 == text[i+1]:
            digraphs.append(char1 + 'X')
            i += 1
        else:
            digraphs.append(char1 + text[i+1])
            i += 2

    result = ""
    shift = 1 if mode == 'encrypt' else -1
    
    for pair in digraphs:
        r1, c1 = find_char_coords(matrix, pair[0])
        r2, c2 = find_char_coords(matrix, pair[1])
        
        if r1 == r2:  # Same row
            result += matrix[r1][(c1 + shift) % 5]
            result += matrix[r2][(c2 + shift) % 5]
        elif c1 == c2:  # Same column
            result += matrix[(r1 + shift) % 5][c1]
            result += matrix[(r2 + shift) % 5][c2]
        else:  # Rectangle
            result += matrix[r1][c2]
            result += matrix[r2][c1]
            
    return result

# --- Hill Cipher ---

def hill_encrypt(plaintext: str, key_matrix: np.ndarray) -> str:
    """
    Encrypts text using the Hill cipher.
    """
    normalized_text = normalize_text(plaintext)
    n = key_matrix.shape[0]
    
    # Pad plaintext if its length is not a multiple of n
    if len(normalized_text) % n != 0:
        padding_needed = n - (len(normalized_text) % n)
        normalized_text += 'X' * padding_needed

    ciphertext = ""
    for i in range(0, len(normalized_text), n):
        block = normalized_text[i:i+n]
        # Convert block to a vector of numbers
        p_vector = np.array([ALPHABET.index(char) for char in block])
        
        # Matrix multiplication: C = P * K (mod 26)
        c_vector = np.dot(p_vector, key_matrix) % 26
        
        # Convert resulting vector back to characters
        ciphertext += "".join([ALPHABET[num] for num in c_vector])
        
    return ciphertext

def hill_decrypt(ciphertext: str, key_matrix: np.ndarray) -> str:
    """
    Decrypts text from a Hill cipher.
    """
    n = key_matrix.shape[0]
    
    # 1. Calculate the determinant of the key matrix
    det = int(round(np.linalg.det(key_matrix))) % 26

    # 2. Find the modular multiplicative inverse of the determinant
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        return "Error: Key matrix is not invertible modulo 26. Cannot decrypt."

    # 3. Find the inverse of the key matrix (adjugate method)
    adjugate_matrix = np.round(np.linalg.inv(key_matrix) * np.linalg.det(key_matrix)).astype(int)
    inverse_key_matrix = (det_inv * adjugate_matrix) % 26
    
    # Decryption is encryption with the inverse key matrix
    plaintext = hill_encrypt(ciphertext, inverse_key_matrix)
    
    # Remove padding
    return plaintext.rstrip('X')
