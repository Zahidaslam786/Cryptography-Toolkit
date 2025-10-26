# A from-scratch implementation of the DES algorithm for educational purposes.
# This code operates on 8-character (64-bit) ASCII blocks.

# --- DES Constants (Permutation Tables) ---

# Initial Permutation (IP)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation (IP Inverse)
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

# Key Permutation (PC-1)
PC_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Key Permutation (PC-2)
PC_2 = [14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]

# Left Circular Shift schedule for key generation
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Expansion (E-box)
E_BOX = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

# S-Boxes (Substitution Boxes)
S_BOXES = [
    # S-1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S-2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S-3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S-4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S-5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S-6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S-7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S-8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]

# Permutation (P-box)
P_BOX = [16, 7, 20, 21,
         29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2, 8, 24, 14,
         32, 27, 3, 9,
         19, 13, 30, 6,
         22, 11, 4, 25]

# --- Helper Functions ---

def permute(bits, table):
    """Apply a permutation table to a list of bits."""
    return [bits[i - 1] for i in table]

def text_to_bits(text):
    """Convert an ASCII string to a list of bits."""
    bits = []
    for char in text:
        bin_val = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in bin_val])
    return bits

def bits_to_text(bits):
    """Convert a list of bits back to an ASCII string."""
    text = ""
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if not byte_bits:
            continue
        byte_str = "".join(map(str, byte_bits))
        try:
            text += chr(int(byte_str, 2))
        except ValueError:
            text += '?' # Handle potential padding error
    return text

def xor(bits_a, bits_b):
    """XOR two lists of bits."""
    return [a ^ b for a, b in zip(bits_a, bits_b)]

def left_circular_shift(bits, n):
    """Perform a left circular shift on a list of bits."""
    return bits[n:] + bits[:n]

# --- Core DES Functions ---

def generate_round_keys(key_bits):
    """Generate the 16 48-bit round keys from the 64-bit key."""
    # Apply PC-1 to get 56 bits
    key_56 = permute(key_bits, PC_1)
    
    # Split into C (left) and D (right)
    C = key_56[:28]
    D = key_56[28:]
    
    round_keys = []
    for i in range(16):
        # Apply circular shift based on the schedule
        C = left_circular_shift(C, SHIFT_SCHEDULE[i])
        D = left_circular_shift(D, SHIFT_SCHEDULE[i])
        
        # Combine C and D
        CD = C + D
        
        # Apply PC-2 to get 48-bit round key
        round_key = permute(CD, PC_2)
        round_keys.append(round_key)
        
    return round_keys

def f_function(right_half, round_key):
    """The Feistel function (f)."""
    # 1. Expand 32 bits to 48 bits using E-box
    expanded_bits = permute(right_half, E_BOX)
    
    # 2. XOR with the round key
    xored_bits = xor(expanded_bits, round_key)
    
    # 3. S-box substitution
    s_box_output = []
    for i in range(8):
        # Get 6-bit block
        block = xored_bits[i*6 : (i+1)*6]
        
        # Calculate row (bits 1 and 6)
        row = (block[0] << 1) + block[5]
        # Calculate col (bits 2-5)
        col = (block[1] << 3) + (block[2] << 2) + (block[3] << 1) + block[4]
        
        # Get 4-bit value from S-box
        val = S_BOXES[i][row][col]
        # Convert to 4 bits
        bin_val = bin(val)[2:].zfill(4)
        s_box_output.extend([int(b) for b in bin_val])
        
    # 4. Permutation (P-box)
    final_32_bits = permute(s_box_output, P_BOX)
    return final_32_bits

def des_process(input_text, key_text, mode='encrypt'):
    """
    The main function to encrypt or decrypt a string using DES.
    Pads text with spaces to fit 8-character (64-bit) blocks.
    """
    
    # --- Input Validation and Preparation ---
    if len(key_text) != 8:
        return "Error: Key must be exactly 8 ASCII characters long (64 bits).", []
    
    try:
        key_bits = text_to_bits(key_text)
    except Exception as e:
        return f"Error processing key. Ensure it is 8 ASCII characters. {e}", []

    # Pad the input text with spaces to be a multiple of 8 characters
    if mode == 'encrypt':
        padding_len = (8 - len(input_text) % 8) % 8
        input_text += ' ' * padding_len
    
    try:
        input_bits = text_to_bits(input_text)
    except Exception as e:
        return f"Error processing input text. Ensure it is ASCII. {e}", []

    if len(input_bits) % 64 != 0:
        return "Error: Padded text is not a multiple of 64 bits.", []
        
    # --- Key Generation ---
    round_keys = generate_round_keys(key_bits)
    
    # For decryption, the round keys are used in reverse order
    if mode == 'decrypt':
        round_keys.reverse()
    
    # --- Main Process (Block by Block) ---
    output_bits = []
    
    for i in range(0, len(input_bits), 64):
        # Get 64-bit block
        block = input_bits[i:i+64]
        
        # 1. Initial Permutation (IP)
        block = permute(block, IP)
        
        # 2. Split into Left and Right halves (32 bits each)
        L = block[:32]
        R = block[32:]
        
        # 3. 16 Rounds of Feistel Network
        for j in range(16):
            L_prev = L
            R_prev = R
            
            # Apply f-function
            f_result = f_function(R_prev, round_keys[j])
            
            # Li = Ri-1
            L = R_prev
            # Ri = Li-1 XOR f(Ri-1, Ki)
            R = xor(L_prev, f_result)
            
        # 4. Final Swap (R16, L16)
        block = R + L
        
        # 5. Final Permutation (FP)
        final_block = permute(block, FP)
        output_bits.extend(final_block)
        
    # --- Final Conversion ---
    output_text = bits_to_text(output_bits)
    
    # For decryption, remove the space padding
    if mode == 'decrypt':
        output_text = output_text.rstrip(' ')

    # Also prepare round keys for display
    hex_keys = []
    for key in generate_round_keys(key_bits): # Get original order for display
        key_str = "".join(map(str, key))
        hex_keys.append(f'{int(key_str, 2):012x}') # 48 bits = 12 hex chars

    return output_text, hex_keys