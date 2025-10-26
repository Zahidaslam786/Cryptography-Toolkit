# This file implements the Rail Fence and Row Transposition ciphers.

from utils import normalize_text

# --- Rail Fence Cipher ---

def rail_fence_encrypt(plaintext: str, rails: int) -> str:
    """
    Encrypts text using the Rail Fence cipher.
    The text is written in a zig-zag pattern across a number of "rails".
    

    Args:
        plaintext (str): The text to encrypt.
        rails (int): The number of rails to use.

    Returns:
        str: The encrypted ciphertext.
    """
    if rails <= 1:
        return plaintext

    normalized_text = normalize_text(plaintext)
    fence = [[] for _ in range(rails)]
    current_rail = 0
    direction = 1  # 1 for down, -1 for up

    for char in normalized_text:
        fence[current_rail].append(char)
        current_rail += direction
        if current_rail == 0 or current_rail == rails - 1:
            direction *= -1
    
    # Join the characters from each rail
    ciphertext = "".join(["".join(rail) for rail in fence])
    return ciphertext

def rail_fence_decrypt(ciphertext: str, rails: int) -> str:
    """
    Decrypts text from a Rail Fence cipher.

    Args:
        ciphertext (str): The text to decrypt.
        rails (int): The number of rails used for encryption.

    Returns:
        str: The decrypted plaintext.
    """
    if rails <= 1:
        return ciphertext

    normalized_text = normalize_text(ciphertext)
    text_len = len(normalized_text)
    
    # Create the fence with placeholders to determine rail lengths
    fence = [[] for _ in range(rails)]
    rail_lengths = [0] * rails
    current_rail = 0
    direction = 1

    for _ in range(text_len):
        rail_lengths[current_rail] += 1
        current_rail += direction
        if current_rail == 0 or current_rail == rails - 1:
            direction *= -1

    # Populate the fence with the actual ciphertext
    text_index = 0
    for i in range(rails):
        fence[i] = list(normalized_text[text_index : text_index + rail_lengths[i]])
        text_index += rail_lengths[i]

    # Read the fence in zig-zag order to get the plaintext
    plaintext = ""
    current_rail = 0
    direction = 1
    for _ in range(text_len):
        plaintext += fence[current_rail].pop(0)
        current_rail += direction
        if current_rail == 0 or current_rail == rails - 1:
            direction *= -1
            
    return plaintext

# --- Row Transposition Cipher ---

def row_transposition_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypts text using the Row (Columnar) Transposition cipher.

    Args:
        plaintext (str): The text to encrypt.
        key (str): The keyword to determine column order.

    Returns:
        str: The encrypted ciphertext.
    """
    normalized_text = normalize_text(plaintext)
    normalized_key = normalize_text(key)

    # Determine column order from the key
    key_order = sorted([(char, i) for i, char in enumerate(normalized_key)])
    col_order = [i for char, i in key_order]

    num_cols = len(normalized_key)
    num_rows = -(-len(normalized_text) // num_cols)  # Ceiling division

    # Pad the text if necessary
    padded_text = normalized_text.ljust(num_rows * num_cols, 'X')
    
    # Create the grid
    grid = [list(padded_text[i:i+num_cols]) for i in range(0, len(padded_text), num_cols)]

    # Read off columns in the specified order
    ciphertext = ""
    for col_index in col_order:
        for row in range(num_rows):
            ciphertext += grid[row][col_index]

    return ciphertext

def row_transposition_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypts text from a Row (Columnar) Transposition cipher.

    Args:
        ciphertext (str): The text to decrypt.
        key (str): The keyword used for encryption.

    Returns:
        str: The decrypted plaintext.
    """
    normalized_text = normalize_text(ciphertext)
    normalized_key = normalize_text(key)

    # Determine column order
    key_order = sorted([(char, i) for i, char in enumerate(normalized_key)])
    col_order = [i for char, i in key_order]

    num_cols = len(normalized_key)
    num_rows = -(-len(normalized_text) // num_cols)
    num_full_cols = len(normalized_text) % num_cols or num_cols

    # Create an empty grid
    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]

    # Reconstruct the columns
    text_index = 0
    for i, col_index in enumerate(col_order):
        col_len = num_rows if i < num_full_cols else num_rows - 1
        for row in range(col_len):
            grid[row][col_index] = normalized_text[text_index]
            text_index += 1
            
    # Read row by row to get plaintext
    plaintext = "".join(["".join(row) for row in grid])
    
    # It's possible for padding 'X' characters to be part of the original message.
    # A perfect decryption would require knowing the original message length.
    # For this implementation, we will assume padding is not part of the message.
    return plaintext.rstrip('X')
