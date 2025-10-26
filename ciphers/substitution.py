
from math import gcd
from utils import normalize_text, ALPHABET, mod_inverse

# --- Caesar Cipher ---

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypts text using the Caesar cipher.
    
    Args:
        plaintext (str): The text to encrypt.
        shift (int): The number of positions to shift letters.
        
    Returns:
        str: The encrypted ciphertext.
    """
    normalized_text = normalize_text(plaintext)
    ciphertext = ""
    for char in normalized_text:
        try:
            index = ALPHABET.index(char)
            shifted_index = (index + shift) % 26
            ciphertext += ALPHABET[shifted_index]
        except ValueError:
            # This case should ideally not be reached due to normalization
            ciphertext += char
    return ciphertext

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """
    Decrypts text from a Caesar cipher.
    
    Args:
        ciphertext (str): The text to decrypt.
        shift (int): The same shift value used for encryption.
        
    Returns:
        str: The decrypted plaintext.
    """
    # Decryption is just encryption with a negative shift.
    return caesar_encrypt(ciphertext, -shift)

# --- Affine Cipher ---

def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    """
    Encrypts text using the Affine cipher: E(x) = (ax + b) mod 26.
    
    Args:
        plaintext (str): The text to encrypt.
        a (int): The multiplicative key (must be coprime with 26).
        b (int): The additive key (the shift).
        
    Returns:
        str: The encrypted ciphertext, or an error message if 'a' is invalid.
    """
    if gcd(a, 26) != 1:
        return "Error: Key 'a' must be coprime with 26."
        
    normalized_text = normalize_text(plaintext)
    ciphertext = ""
    for char in normalized_text:
        try:
            x = ALPHABET.index(char)
            encrypted_index = (a * x + b) % 26
            ciphertext += ALPHABET[encrypted_index]
        except ValueError:
            ciphertext += char
    return ciphertext

def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    """
    Decrypts text from an Affine cipher: D(y) = a_inv * (y - b) mod 26.
    
    Args:
        ciphertext (str): The text to decrypt.
        a (int): The same multiplicative key used for encryption.
        b (int): The same additive key used for encryption.
        
    Returns:
        str: The decrypted plaintext, or an error message if decryption is not possible.
    """
    if gcd(a, 26) != 1:
        return "Error: Key 'a' must be coprime with 26 to be decrypted."
    
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        # This case should be caught by the gcd check above, but it's good practice
        return "Error: Modular inverse does not exist for key 'a'."

    normalized_text = normalize_text(ciphertext)
    plaintext = ""
    for char in normalized_text:
        try:
            y = ALPHABET.index(char)
            # We add 26 to handle potential negative results from (y - b)
            decrypted_index = (a_inv * (y - b + 26)) % 26
            plaintext += ALPHABET[decrypted_index]
        except ValueError:
            plaintext += char
    return plaintext
