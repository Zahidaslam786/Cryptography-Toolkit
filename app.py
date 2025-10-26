
# # app.py
# # This is the main file for the Streamlit web application.

# import streamlit as st
# import numpy as np
# import base64 # <-- IMPORT FOR KEY VALIDATION

# # Import all the utility and cipher functions from our other files
# from utils import normalize_text, string_to_matrix, mod_inverse, gcd
# from ciphers import substitution, polyalphabetic, transposition, rotormachine
# from ciphers import des
# from ciphers import aes  # <-- ADDED IMPORT FOR AES

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Classical Cryptography Toolkit",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- Main Title ---
# st.title("Cryptography Toolkit")
# st.markdown("An interactive web app for exploring classical and modern encryption algorithms.")

# # --- Sidebar for Controls ---
# st.sidebar.title("Cipher Controls")
# st.sidebar.markdown("Select an algorithm and configure its parameters.")

# # A dictionary to organize the ciphers by category for the selectbox
# ALGORITHMS = {
#     "Classical Ciphers (Substitution)": [
#         "Caesar Cipher",
#         "Affine Cipher"
#     ],
#     "Classical Ciphers (Polyalphabetic)": [
#         "Vigenere Cipher",
#         "Playfair Cipher",
#         "Hill Cipher"
#     ],
#     "Classical Ciphers (Transposition)": [
#         "Rail Fence Cipher",
#         "Row Transposition Cipher"
#     ],
#     "Mechanical Ciphers": [
#         "Rotor Machine (Enigma-like)"
#     ],
#     "Modern Block Ciphers": [
#         "DES (Data Encryption Standard)",
#         "AES (Advanced Encryption Standard)"  # <-- NEWLY ADDED
#     ]
# }

# # Sidebar widgets for selection
# cipher_category = st.sidebar.selectbox("Cipher Category", list(ALGORITHMS.keys()))
# cipher_name = st.sidebar.selectbox("Algorithm", ALGORITHMS[cipher_category])
# mode = st.sidebar.radio("Mode", ("Encrypt", "Decrypt"), horizontal=True)

# # --- Main Content Area ---
# col1, col2 = st.columns(2, gap="medium")

# # Input/Output text areas
# if mode == "Encrypt":
#     col1.subheader("Plaintext")
#     input_text = col1.text_area("Enter text to encrypt...", height=250, label_visibility="collapsed")
#     col2.subheader("Ciphertext")
#     output_area = col2.empty()
# else:
#     col1.subheader("Ciphertext")
#     input_text = col1.text_area("Enter text to decrypt...", height=250, label_visibility="collapsed")
#     col2.subheader("Plaintext")
#     output_area = col2.empty()

# # --- Dynamic Key Inputs & Explanation Area ---
# st.subheader("🔑 Key Configuration & Cipher Details")

# key_inputs = {}
# explanation_area = st.expander(f"About the {cipher_name}", expanded=True)

# # This block dynamically creates the correct UI for each cipher's key
# try:
#     if cipher_name == "Caesar Cipher":
#         explanation_area.markdown("""
#         The Caesar cipher is one of the simplest and most widely known encryption techniques. It is a type of substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet.
#         - **Formula:** `E(x) = (x + n) mod 26`
#         """)
#         key_inputs['shift'] = st.number_input("Shift (Key)", min_value=1, max_value=25, value=3)

#     elif cipher_name == "Affine Cipher":
#         explanation_area.markdown("""
#         The Affine cipher is a type of monoalphabetic substitution cipher, where each letter is mapped to its numeric equivalent, encrypted using a simple mathematical function, and converted back to a letter.
#         - **Formula:** `E(x) = (ax + b) mod 26`
#         - **Constraint:** `a` must be coprime to 26 for the cipher to be decryptable.
#         """)
#         k1, k2 = st.columns(2)
#         key_inputs['a'] = k1.number_input("Key 'a'", min_value=1, value=5, help="Must be coprime to 26 (e.g., 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25).")
#         key_inputs['b'] = k2.number_input("Key 'b' (shift)", min_value=0, max_value=25, value=7)
#         if gcd(key_inputs['a'], 26) != 1:
#             st.error(f"The selected value for 'a' ({key_inputs['a']}) is not coprime to 26. Decryption will not be possible.")

#     elif cipher_name == "Vigenere Cipher":
#         explanation_area.markdown("""
#         The Vigenere cipher is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers based on the letters of a keyword. It is a form of polyalphabetic substitution.
#         - **Formula:** `E(Pi) = (Pi + Ki) mod 26`
#         """)
#         key_inputs['key'] = st.text_input("Keyword", value="KEY")
#         if not (key_inputs['key'] and key_inputs['key'].isalpha()):
#             st.error("Keyword must only contain alphabetic characters.")

#     elif cipher_name == "Playfair Cipher":
#         explanation_area.markdown("""
#         The Playfair cipher was the first practical digraph substitution cipher. The scheme encrypts pairs of letters (digraphs), instead of single letters. This makes it significantly harder to break than simple substitution ciphers.
#         - **Key:** A 5x5 matrix is constructed from a keyword.
#         - **Rules:** Letters in the same row are shifted right; letters in the same column are shifted down; otherwise, they form a rectangle, and the letters at the opposite corners are taken.
#         """)
#         key_inputs['key'] = st.text_input("Keyword", value="PLAYFAIR")
#         if not (key_inputs['key'] and key_inputs['key'].isalpha()):
#             st.error("Keyword must only contain alphabetic characters.")
#         else:
#             explanation_area.markdown("#### Key Matrix")
#             matrix = polyalphabetic.generate_playfair_matrix(key_inputs['key'])
#             explanation_area.table(matrix)

#     elif cipher_name == "Hill Cipher":
#         explanation_area.markdown("""
#         The Hill cipher is a polygraphic substitution cipher based on linear algebra. Each block of `n` letters is treated as a vector and encrypted by multiplying it by an `n x n` matrix, modulo 26.
#         - **Formula:** `C = K * P (mod 26)`
#         - **Constraint:** The key matrix must be invertible modulo 26 for decryption to be possible.
#         """)
#         key_inputs['n'] = st.radio("Matrix Size", (2, 3), horizontal=True, index=0)
#         default_key = "5 8 17 3" if key_inputs['n'] == 2 else "17 17 5 21 18 21 2 2 19"
#         key_inputs['key_str'] = st.text_area("Key Matrix (space-separated numbers)", value=default_key, height=50)
        
#         try:
#             key_matrix = string_to_matrix(key_inputs['key_str'], key_inputs['n'])
#             key_inputs['key_matrix'] = key_matrix
#             explanation_area.markdown("#### Parsed Key Matrix")
#             explanation_area.table(key_matrix)
#             # Check for invertibility
#             det = int(round(np.linalg.det(key_matrix))) % 26
#             if mod_inverse(det, 26) is None:
#                 st.error("This key matrix is not invertible modulo 26. Decryption will fail.")
#         except Exception as e:
#             st.error(f"Invalid matrix format for a {key_inputs['n']}x{key_inputs['n']} matrix. Please enter {key_inputs['n']**2} numbers.")

#     elif cipher_name == "Rail Fence Cipher":
#         explanation_area.markdown("""
#         The rail fence cipher is a form of transposition cipher that gets its name from the way in which it is encoded. The plaintext is written downwards and diagonally on successive "rails" of an imaginary fence, then read off in rows.
#         - **Key:** The number of rails.
#         """)
#         key_inputs['rails'] = st.number_input("Number of Rails (Key)", min_value=2, value=3)

#     elif cipher_name == "Row Transposition Cipher":
#         explanation_area.markdown("""
#         The row transposition cipher is a transposition cipher that involves writing the plaintext out in a grid and then reordering the columns based on the alphabetical order of a keyword.
#         - **Key:** A keyword that determines the column order.
#         """)
#         key_inputs['key'] = st.text_input("Keyword", value="ZEBRAS")
#         if not (key_inputs['key'] and key_inputs['key'].isalpha()):
#             st.error("Keyword must only contain alphabetic characters.")

#     elif cipher_name == "Rotor Machine (Enigma-like)":
#         explanation_area.markdown("""
#         This is a simulation of an electro-mechanical rotor cipher machine like the Enigma. Each keypress rotates one or more rotors, changing the substitution alphabet for every single letter. The signal goes through the rotors, bounces off a reflector, and goes back through the rotors in reverse.
#         - **Key:** The choice and order of rotors, their initial positions, and plugboard settings.
#         """)
#         r1, r2, r3 = st.columns(3)
#         rotor_choices = list(rotormachine.ROTORS.keys())
#         key_inputs['rotor_names'] = [
#             r1.selectbox("Rotor 1 (Left)", rotor_choices, index=0),
#             r2.selectbox("Rotor 2 (Middle)", rotor_choices, index=1),
#             r3.selectbox("Rotor 3 (Right)", rotor_choices, index=2)
#         ]
#         key_inputs['initial_positions'] = st.text_input("Rotor Initial Positions (3 letters)", value="AAA", max_chars=3)
#         key_inputs['plugboard_settings'] = st.text_input("Plugboard Pairs (e.g., 'AB CD EF')", value="", help="Space-separated pairs of letters.")
        
#     elif cipher_name == "DES (Data Encryption Standard)":
#         explanation_area.markdown("""
#         DES is a symmetric-key block cipher published in 1977. It operates on 64-bit blocks of data using a 56-bit key (provided as 64 bits with 8 parity bits). It uses a complex 16-round Feistel network.
#         - **Block Size:** 64 bits (8 ASCII characters)
#         - **Key Size:** 56 bits (Entered as 8 ASCII characters)
#         - **Rounds:** 16
#         - **Security Warning:** DES is no longer secure. This implementation is for educational purposes only.
#         """)
#         key_inputs['key'] = st.text_input("Key (MUST be 8 characters)", value="mysecret", max_chars=8)
#         if len(key_inputs['key']) != 8:
#             st.error("Key must be exactly 8 characters long.")
#         else:
#             try:
#                 # Show the "working" part - the 16 round keys
#                 key_bits = des.text_to_bits(key_inputs['key'])
#                 _, hex_keys = des.des_process("", key_inputs['key'], 'encrypt') # Get keys
                
#                 with explanation_area.expander("Show 16 Generated Round Keys (48-bit each)"):
#                     keys_data = [{"Round": i+1, "Round Key (Hex)": hex_keys[i]} for i in range(16)]
#                     st.dataframe(keys_data, use_container_width=True)
#                 key_inputs['key_for_des'] = key_inputs['key'] # Pass the valid key
#             except Exception as e:
#                 st.error(f"Error generating keys: {e}")

#     # --- NEW BLOCK FOR AES ---
#     elif cipher_name == "AES (Advanced Encryption Standard)":
#         explanation_area.markdown("""
#         AES is the modern, secure standard for symmetric encryption. It is a block cipher that operates on 128-bit blocks of data (16 bytes) using a "State" matrix. It performs multiple rounds of substitution and permutation.
#         - **Block Size:** 128 bits (16 bytes)
#         - **Key Sizes:** 128, 192, or 256 bits (16, 24, or 32 characters)
#         - **Mode:** Using AES-GCM (Galois/Counter Mode) for authenticated encryption.
#         - **Secure:** This is the modern, recommended standard.
#         """)
        
#         # Key Size Selection
#         key_size_options = {
#             "128-bit (16 chars)": 16,
#             "192-bit (24 chars)": 24,
#             "256-bit (32 chars)": 32
#         }
#         selected_size_label = st.radio("Select Key Size", list(key_size_options.keys()), horizontal=True)
#         key_len = key_size_options[selected_size_label]
        
#         # Key Input
#         key_inputs['key'] = st.text_input(f"Key (MUST be {key_len} characters)", value="a" * key_len, max_chars=key_len)
        
#         # Key Validation
#         if len(key_inputs['key']) != key_len:
#             st.error(f"Key must be exactly {key_len} characters long.")
#         else:
#             # Convert key to bytes for the cipher
#             key_inputs['key_bytes'] = key_inputs['key'].encode('utf-8')
        
#         # --- AES Visualizer ---
#         explanation_area.subheader("How an AES Round Works (Visualized)")
#         explanation_area.markdown("AES repeats these 4 steps in multiple 'rounds' (10, 12, or 14 times).")
        
#         tab1, tab2, tab3, tab4 = explanation_area.tabs(["1. SubBytes", "2. ShiftRows", "3. MixColumns", "4. AddRoundKey"])
        
#         with tab1:
#             st.markdown("""
#             **SubBytes (Substitution)**
#             Each of the 16 bytes in the 4x4 'State' matrix is replaced with a different byte using a lookup table called the **Rijndael S-box**.
            
#             This is the main non-linear step that provides confusion and makes the cipher difficult to break.
            
#             `Byte[i, j] = S_Box(Byte[i, j])`
#             """)
#             st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/AES-SubBytes.svg/300px-AES-SubBytes.svg.png", caption="SubBytes: Each byte is substituted.")

#         with tab2:
#             st.markdown("""
#             **ShiftRows (Permutation)**
#             The bytes in each row of the 'State' matrix are shifted cyclically to the left.
            
#             - **Row 0:** No shift.
#             - **Row 1:** Shifted left by 1.
#             - **Row 2:** Shifted left by 2.
#             - **Row 3:** Shifted left by 3.
            
#             This step provides diffusion by mixing data within rows.
#             """)
#             st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/AES-ShiftRows.svg/300px-AES-ShiftRows.svg.png", caption="ShiftRows: Rows are shifted left.")

#         with tab3:
#             st.markdown("""
#             **MixColumns (Diffusion)**
#             Each of the 4 columns is transformed by multiplying it with a special matrix in the finite field $GF(2^8)$.
            
#             This is the most complex step and provides significant diffusion, mixing the data within each column.
#             """)
#             st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/AES-MixColumns.svg/300px-AES-MixColumns.svg.png", caption="MixColumns: Columns are mixed.")

#         with tab4:
#             st.markdown("""
#             **AddRoundKey (XOR)**
#             The 'State' matrix is combined with the 'Round Key' for the current round using a simple bitwise XOR.
            
#             The Round Keys are generated from the main encryption key using the **AES Key Schedule**.
            
#             `State = State XOR RoundKey`
#             """)
#             st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/AES-AddRoundKey.svg/300px-AES-AddRoundKey.svg.png", caption="AddRoundKey: State is XORed with the Round Key.")

# except Exception as e:
#     st.error(f"An unexpected UI error occurred: {e}")
#     st.exception(e) # Show full error for debugging

# # --- Process Button and Output ---
# if st.button(f" {mode} Text", use_container_width=True, type="primary"):
#     if not input_text:
#         st.warning("Please enter some text to process.")
#     else:
#         output_text = ""
#         try:
#             # Call the correct function based on user selections
#             if mode == "Encrypt":
#                 if cipher_name == "Caesar Cipher":
#                     output_text = substitution.caesar_encrypt(input_text, key_inputs['shift'])
#                 elif cipher_name == "Affine Cipher":
#                     output_text = substitution.affine_encrypt(input_text, key_inputs['a'], key_inputs['b'])
#                 elif cipher_name == "Vigenere Cipher":
#                     output_text = polyalphabetic.vigenere_encrypt(input_text, key_inputs['key'])
#                 elif cipher_name == "Playfair Cipher":
#                     output_text = polyalphabetic.playfair_process(input_text, key_inputs['key'], 'encrypt')
#                 elif cipher_name == "Hill Cipher":
#                     output_text = polyalphabetic.hill_encrypt(input_text, key_inputs['key_matrix'])
#                 elif cipher_name == "Rail Fence Cipher":
#                     output_text = transposition.rail_fence_encrypt(input_text, key_inputs['rails'])
#                 elif cipher_name == "Row Transposition Cipher":
#                     output_text = transposition.row_transposition_encrypt(input_text, key_inputs['key'])
#                 elif cipher_name == "Rotor Machine (Enigma-like)":
#                     output_text = rotormachine.rotor_machine_process(input_text, key_inputs['rotor_names'], key_inputs['initial_positions'], key_inputs['plugboard_settings'])
#                 elif cipher_name == "DES (Data Encryption Standard)":
#                     if 'key_for_des' in key_inputs:
#                         output_text, _ = des.des_process(input_text, key_inputs['key_for_des'], mode='encrypt')
#                     else:
#                         output_text = "Error: Key is not 8 characters."
#                 # --- NEW CALL FOR AES ---
#                 elif cipher_name == "AES (Advanced Encryption Standard)":
#                     if 'key_bytes' in key_inputs:
#                         output_text = aes.aes_encrypt(input_text, key_inputs['key_bytes'])
#                     else:
#                         output_text = "Error: Key is not the correct length."
            
#             else: # Decrypt
#                 if cipher_name == "Caesar Cipher":
#                     output_text = substitution.caesar_decrypt(input_text, key_inputs['shift'])
#                 elif cipher_name == "Affine Cipher":
#                     output_text = substitution.affine_decrypt(input_text, key_inputs['a'], key_inputs['b'])
#                 elif cipher_name == "Vigenere Cipher":
#                     output_text = polyalphabetic.vigenere_decrypt(input_text, key_inputs['key'])
#                 elif cipher_name == "Playfair Cipher":
#                     output_text = polyalphabetic.playfair_process(input_text, key_inputs['key'], 'decrypt')
#                 elif cipher_name == "Hill Cipher":
#                     output_text = polyalphabetic.hill_decrypt(input_text, key_inputs['key_matrix'])
#                 elif cipher_name == "Rail Fence Cipher":
#                     output_text = transposition.rail_fence_decrypt(input_text, key_inputs['rails'])
#                 elif cipher_name == "Row Transposition Cipher":
#                     output_text = transposition.row_transposition_decrypt(input_text, key_inputs['key'])
#                 elif cipher_name == "Rotor Machine (Enigma-like)":
#                     output_text = rotormachine.rotor_machine_process(input_text, key_inputs['rotor_names'], key_inputs['initial_positions'], key_inputs['plugboard_settings'])
#                 elif cipher_name == "DES (Data Encryption Standard)":
#                     if 'key_for_des' in key_inputs:
#                         output_text, _ = des.des_process(input_text, key_inputs['key_for_des'], mode='decrypt')
#                     else:
#                         output_text = "Error: Key is not 8 characters."
#                 # --- NEW CALL FOR AES ---
#                 elif cipher_name == "AES (Advanced Encryption Standard)":
#                     if 'key_bytes' in key_inputs:
#                         output_text = aes.aes_decrypt(input_text, key_inputs['key_bytes'])
#                     else:
#                         output_text = "Error: Key is not the correct length."
            
#             output_area.text_area("Result", value=output_text, height=250, label_visibility="collapsed", disabled=True)

#         except Exception as e:
#             st.error(f"An error occurred during processing: {e}")
#             st.exception(e) # Show full error for debugging
# else:
#     output_area.text_area("Result", value="Click the button to see the result.", height=250, label_visibility="collapsed", disabled=True)


# app.py
# This is the main file for the Streamlit web application.
# FIXED: Removed external st.image() calls that were breaking the app.

import streamlit as st
import numpy as np
import base64 # <-- IMPORT FOR KEY VALIDATION

# Import all the utility and cipher functions from our other files
from utils import normalize_text, string_to_matrix, mod_inverse, gcd
from ciphers import substitution, polyalphabetic, transposition, rotormachine
from ciphers import des
from ciphers import aes  # <-- IMPORT FOR AES

# --- Page Configuration ---
st.set_page_config(
    page_title="Classical Cryptography Toolkit",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Title ---
st.title("Cryptography Toolkit")
st.markdown("An interactive web app for exploring classical and modern encryption algorithms.")

# --- Sidebar for Controls ---
st.sidebar.title("Cipher Controls")
st.sidebar.markdown("Select an algorithm and configure its parameters.")

# A dictionary to organize the ciphers by category for the selectbox
ALGORITHMS = {
    "Classical Ciphers (Substitution)": [
        "Caesar Cipher",
        "Affine Cipher"
    ],
    "Classical Ciphers (Polyalphabetic)": [
        "Vigenere Cipher",
        "Playfair Cipher",
        "Hill Cipher"
    ],
    "Classical Ciphers (Transposition)": [
        "Rail Fence Cipher",
        "Row Transposition Cipher"
    ],
    "Mechanical Ciphers": [
        "Rotor Machine (Enigma-like)"
    ],
    "Modern Block Ciphers": [
        "DES (Data Encryption Standard)",
        "AES (Advanced Encryption Standard)"
    ]
}

# Sidebar widgets for selection
cipher_category = st.sidebar.selectbox("Cipher Category", list(ALGORITHMS.keys()))
cipher_name = st.sidebar.selectbox("Algorithm", ALGORITHMS[cipher_category])
mode = st.sidebar.radio("Mode", ("Encrypt", "Decrypt"), horizontal=True)

# --- Main Content Area ---
col1, col2 = st.columns(2, gap="medium")

# Input/Output text areas
if mode == "Encrypt":
    col1.subheader("Plaintext")
    input_text = col1.text_area("Enter text to encrypt...", height=250, label_visibility="collapsed")
    col2.subheader("Ciphertext")
    output_area = col2.empty()
else:
    col1.subheader("Ciphertext")
    input_text = col1.text_area("Enter text to decrypt...", height=250, label_visibility="collapsed")
    col2.subheader("Plaintext")
    output_area = col2.empty()

# --- Dynamic Key Inputs & Explanation Area ---
st.subheader("🔑 Key Configuration & Cipher Details")

key_inputs = {}
explanation_area = st.expander(f"About the {cipher_name}", expanded=True)

# This block dynamically creates the correct UI for each cipher's key
try:
    if cipher_name == "Caesar Cipher":
        explanation_area.markdown("""
        The Caesar cipher is one of the simplest and most widely known encryption techniques. It is a type of substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet.
        - **Formula:** `E(x) = (x + n) mod 26`
        """)
        key_inputs['shift'] = st.number_input("Shift (Key)", min_value=1, max_value=25, value=3)

    elif cipher_name == "Affine Cipher":
        explanation_area.markdown("""
        The Affine cipher is a type of monoalphabetic substitution cipher, where each letter is mapped to its numeric equivalent, encrypted using a simple mathematical function, and converted back to a letter.
        - **Formula:** `E(x) = (ax + b) mod 26`
        - **Constraint:** `a` must be coprime to 26 for the cipher to be decryptable.
        """)
        k1, k2 = st.columns(2)
        key_inputs['a'] = k1.number_input("Key 'a'", min_value=1, value=5, help="Must be coprime to 26 (e.g., 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25).")
        key_inputs['b'] = k2.number_input("Key 'b' (shift)", min_value=0, max_value=25, value=7)
        if gcd(key_inputs['a'], 26) != 1:
            st.error(f"The selected value for 'a' ({key_inputs['a']}) is not coprime to 26. Decryption will not be possible.")

    elif cipher_name == "Vigenere Cipher":
        explanation_area.markdown("""
        The Vigenere cipher is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers based on the letters of a keyword. It is a form of polyalphabetic substitution.
        - **Formula:** `E(Pi) = (Pi + Ki) mod 26`
        """)
        key_inputs['key'] = st.text_input("Keyword", value="KEY")
        if not (key_inputs['key'] and key_inputs['key'].isalpha()):
            st.error("Keyword must only contain alphabetic characters.")

    elif cipher_name == "Playfair Cipher":
        explanation_area.markdown("""
        The Playfair cipher was the first practical digraph substitution cipher. The scheme encrypts pairs of letters (digraphs), instead of single letters. This makes it significantly harder to break than simple substitution ciphers.
        - **Key:** A 5x5 matrix is constructed from a keyword.
        - **Rules:** Letters in the same row are shifted right; letters in the same column are shifted down; otherwise, they form a rectangle, and the letters at the opposite corners are taken.
        """)
        key_inputs['key'] = st.text_input("Keyword", value="PLAYFAIR")
        if not (key_inputs['key'] and key_inputs['key'].isalpha()):
            st.error("Keyword must only contain alphabetic characters.")
        else:
            explanation_area.markdown("#### Key Matrix")
            matrix = polyalphabetic.generate_playfair_matrix(key_inputs['key'])
            explanation_area.table(matrix)

    elif cipher_name == "Hill Cipher":
        explanation_area.markdown("""
        The Hill cipher is a polygraphic substitution cipher based on linear algebra. Each block of `n` letters is treated as a vector and encrypted by multiplying it by an `n x n` matrix, modulo 26.
        - **Formula:** `C = K * P (mod 26)`
        - **Constraint:** The key matrix must be invertible modulo 26 for decryption to be possible.
        """)
        key_inputs['n'] = st.radio("Matrix Size", (2, 3), horizontal=True, index=0)
        default_key = "5 8 17 3" if key_inputs['n'] == 2 else "17 17 5 21 18 21 2 2 19"
        key_inputs['key_str'] = st.text_area("Key Matrix (space-separated numbers)", value=default_key, height=50)
        
        try:
            key_matrix = string_to_matrix(key_inputs['key_str'], key_inputs['n'])
            key_inputs['key_matrix'] = key_matrix
            explanation_area.markdown("#### Parsed Key Matrix")
            explanation_area.table(key_matrix)
            # Check for invertibility
            det = int(round(np.linalg.det(key_matrix))) % 26
            if mod_inverse(det, 26) is None:
                st.error("This key matrix is not invertible modulo 26. Decryption will fail.")
        except Exception as e:
            st.error(f"Invalid matrix format for a {key_inputs['n']}x{key_inputs['n']} matrix. Please enter {key_inputs['n']**2} numbers.")

    elif cipher_name == "Rail Fence Cipher":
        explanation_area.markdown("""
        The rail fence cipher is a form of transposition cipher that gets its name from the way in which it is encoded. The plaintext is written downwards and diagonally on successive "rails" of an imaginary fence, then read off in rows.
        - **Key:** The number of rails.
        """)
        key_inputs['rails'] = st.number_input("Number of Rails (Key)", min_value=2, value=3)

    elif cipher_name == "Row Transposition Cipher":
        explanation_area.markdown("""
        The row transposition cipher is a transposition cipher that involves writing the plaintext out in a grid and then reordering the columns based on the alphabetical order of a keyword.
        - **Key:** A keyword that determines the column order.
        """)
        key_inputs['key'] = st.text_input("Keyword", value="ZEBRAS")
        if not (key_inputs['key'] and key_inputs['key'].isalpha()):
            st.error("Keyword must only contain alphabetic characters.")

    elif cipher_name == "Rotor Machine (Enigma-like)":
        explanation_area.markdown("""
        This is a simulation of an electro-mechanical rotor cipher machine like the Enigma. Each keypress rotates one or more rotors, changing the substitution alphabet for every single letter. The signal goes through the rotors, bounces off a reflector, and goes back through the rotors in reverse.
        - **Key:** The choice and order of rotors, their initial positions, and plugboard settings.
        """)
        r1, r2, r3 = st.columns(3)
        rotor_choices = list(rotormachine.ROTORS.keys())
        key_inputs['rotor_names'] = [
            r1.selectbox("Rotor 1 (Left)", rotor_choices, index=0),
            r2.selectbox("Rotor 2 (Middle)", rotor_choices, index=1),
            r3.selectbox("Rotor 3 (Right)", rotor_choices, index=2)
        ]
        key_inputs['initial_positions'] = st.text_input("Rotor Initial Positions (3 letters)", value="AAA", max_chars=3)
        key_inputs['plugboard_settings'] = st.text_input("Plugboard Pairs (e.g., 'AB CD EF')", value="", help="Space-separated pairs of letters.")
        
    elif cipher_name == "DES (Data Encryption Standard)":
        explanation_area.markdown("""
        DES is a symmetric-key block cipher published in 1977. It operates on 64-bit blocks of data using a 56-bit key (provided as 64 bits with 8 parity bits). It uses a complex 16-round Feistel network.
        - **Block Size:** 64 bits (8 ASCII characters)
        - **Key Size:** 56 bits (Entered as 8 ASCII characters)
        - **Rounds:** 16
        - ** Security Warning:** DES is no longer secure. This implementation is for educational purposes only.
        """)
        key_inputs['key'] = st.text_input("Key (MUST be 8 characters)", value="mysecret", max_chars=8)
        if len(key_inputs['key']) != 8:
            st.error("Key must be exactly 8 characters long.")
        else:
            try:
                # Show the "working" part - the 16 round keys
                key_bits = des.text_to_bits(key_inputs['key'])
                _, hex_keys = des.des_process("", key_inputs['key'], 'encrypt') # Get keys
                
                with explanation_area.expander("Show 16 Generated Round Keys (48-bit each)"):
                    keys_data = [{"Round": i+1, "Round Key (Hex)": hex_keys[i]} for i in range(16)]
                    st.dataframe(keys_data, use_container_width=True)
                key_inputs['key_for_des'] = key_inputs['key'] # Pass the valid key
            except Exception as e:
                st.error(f"Error generating keys: {e}")

    # --- UPDATED AES BLOCK ---
    elif cipher_name == "AES (Advanced Encryption Standard)":
        explanation_area.markdown("""
        AES is the modern, secure standard for symmetric encryption. It is a block cipher that operates on 128-bit blocks of data (16 bytes) using a "State" matrix. It performs multiple rounds of substitution and permutation.
        - **Block Size:** 128 bits (16 bytes)
        - **Key Sizes:** 128, 192, or 256 bits (16, 24, or 32 characters)
        - **Mode:** Using AES-GCM (Galois/Counter Mode) for authenticated encryption.
        - ** Secure:** This is the modern, recommended standard.
        """)
        
        # Key Size Selection
        key_size_options = {
            "128-bit (16 chars)": 16,
            "192-bit (24 chars)": 24,
            "256-bit (32 chars)": 32
        }
        selected_size_label = st.radio("Select Key Size", list(key_size_options.keys()), horizontal=True)
        key_len = key_size_options[selected_size_label]
        
        # Key Input
        key_inputs['key'] = st.text_input(f"Key (MUST be {key_len} characters)", value="a" * key_len, max_chars=key_len)
        
        # Key Validation
        if len(key_inputs['key']) != key_len:
            st.error(f"Key must be exactly {key_len} characters long.")
        else:
            # Convert key to bytes for the cipher
            key_inputs['key_bytes'] = key_inputs['key'].encode('utf-8')
        
        # --- AES Visualizer (Text Only) ---
        explanation_area.subheader("How an AES Round Works (Visualized)")
        explanation_area.markdown("AES repeats these 4 steps in multiple 'rounds' (10, 12, or 14 times).")
        
        tab1, tab2, tab3, tab4 = explanation_area.tabs(["1. SubBytes", "2. ShiftRows", "3. MixColumns", "4. AddRoundKey"])
        
        with tab1:
            st.markdown("""
            **SubBytes (Substitution)**
            Each of the 16 bytes in the 4x4 'State' matrix is replaced with a different byte using a lookup table called the **Rijndael S-box**.
            
            This is the main non-linear step that provides confusion and makes the cipher difficult to break.
            
            `Byte[i, j] = S_Box(Byte[i, j])`
            """)
            # st.image(...) REMOVED TO PREVENT ERROR

        with tab2:
            st.markdown("""
            **ShiftRows (Permutation)**
            The bytes in each row of the 'State' matrix are shifted cyclically to the left.
            
            - **Row 0:** No shift.
            - **Row 1:** Shifted left by 1.
            - **Row 2:** Shifted left by 2.
            - **Row 3:** Shifted left by 3.
            
            This step provides diffusion by mixing data within rows.
            """)
            # st.image(...) REMOVED TO PREVENT ERROR

        with tab3:
            st.markdown("""
            **MixColumns (Diffusion)**
            Each of the 4 columns is transformed by multiplying it with a special matrix in the finite field $GF(2^8)$.
            
            This is the most complex step and provides significant diffusion, mixing the data within each column.
            """)
            # st.image(...) REMOVED TO PREVENT ERROR

        with tab4:
            st.markdown("""
            **AddRoundKey (XOR)**
            The 'State' matrix is combined with the 'Round Key' for the current round using a simple bitwise XOR.
            
            The Round Keys are generated from the main encryption key using the **AES Key Schedule**.
            
            `State = State XOR RoundKey`
            """)
            # st.image(...) REMOVED TO PREVENT ERROR

except Exception as e:
    st.error(f"An unexpected UI error occurred: {e}")
    st.exception(e) # Show full error for debugging

# --- Process Button and Output ---
if st.button(f" {mode} Text", use_container_width=True, type="primary"):
    if not input_text:
        st.warning("Please enter some text to process.")
    else:
        output_text = ""
        try:
            # Call the correct function based on user selections
            if mode == "Encrypt":
                if cipher_name == "Caesar Cipher":
                    output_text = substitution.caesar_encrypt(input_text, key_inputs['shift'])
                elif cipher_name == "Affine Cipher":
                    output_text = substitution.affine_encrypt(input_text, key_inputs['a'], key_inputs['b'])
                elif cipher_name == "Vigenere Cipher":
                    output_text = polyalphabetic.vigenere_encrypt(input_text, key_inputs['key'])
                elif cipher_name == "Playfair Cipher":
                    output_text = polyalphabetic.playfair_process(input_text, key_inputs['key'], 'encrypt')
                elif cipher_name == "Hill Cipher":
                    output_text = polyalphabetic.hill_encrypt(input_text, key_inputs['key_matrix'])
                elif cipher_name == "Rail Fence Cipher":
                    output_text = transposition.rail_fence_encrypt(input_text, key_inputs['rails'])
                elif cipher_name == "Row Transposition Cipher":
                    output_text = transposition.row_transposition_encrypt(input_text, key_inputs['key'])
                elif cipher_name == "Rotor Machine (Enigma-like)":
                    output_text = rotormachine.rotor_machine_process(input_text, key_inputs['rotor_names'], key_inputs['initial_positions'], key_inputs['plugboard_settings'])
                elif cipher_name == "DES (Data Encryption Standard)":
                    if 'key_for_des' in key_inputs:
                        output_text, _ = des.des_process(input_text, key_inputs['key_for_des'], mode='encrypt')
                    else:
                        output_text = "Error: Key is not 8 characters."
                # --- NEW CALL FOR AES ---
                elif cipher_name == "AES (Advanced Encryption Standard)":
                    if 'key_bytes' in key_inputs:
                        output_text = aes.aes_encrypt(input_text, key_inputs['key_bytes'])
                    else:
                        output_text = "Error: Key is not the correct length."
            
            else: # Decrypt
                if cipher_name == "Caesar Cipher":
                    output_text = substitution.caesar_decrypt(input_text, key_inputs['shift'])
                elif cipher_name == "Affine Cipher":
                    output_text = substitution.affine_decrypt(input_text, key_inputs['a'], key_inputs['b'])
                elif cipher_name == "Vigenere Cipher":
                    output_text = polyalphabetic.vigenere_decrypt(input_text, key_inputs['key'])
                elif cipher_name == "Playfair Cipher":
                    output_text = polyalphabetic.playfair_process(input_text, key_inputs['key'], 'decrypt')
                elif cipher_name == "Hill Cipher":
                    output_text = polyalphabetic.hill_decrypt(input_text, key_inputs['key_matrix'])
                elif cipher_name == "Rail Fence Cipher":
                    output_text = transposition.rail_fence_decrypt(input_text, key_inputs['rails'])
                elif cipher_name == "Row Transposition Cipher":
                    output_text = transposition.row_transposition_decrypt(input_text, key_inputs['key'])
                elif cipher_name == "Rotor Machine (Enigma-like)":
                    output_text = rotormachine.rotor_machine_process(input_text, key_inputs['rotor_names'], key_inputs['initial_positions'], key_inputs['plugboard_settings'])
                elif cipher_name == "DES (Data Encryption Standard)":
                    if 'key_for_des' in key_inputs:
                        output_text, _ = des.des_process(input_text, key_inputs['key_for_des'], mode='decrypt')
                    else:
                        output_text = "Error: Key is not 8 characters."
                # --- NEW CALL FOR AES ---
                elif cipher_name == "AES (Advanced Encryption Standard)":
                    if 'key_bytes' in key_inputs:
                        output_text = aes.aes_decrypt(input_text, key_inputs['key_bytes'])
                    else:
                        output_text = "Error: Key is not the correct length."
            
            output_area.text_area("Result", value=output_text, height=250, label_visibility="collapsed", disabled=True)

        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
            st.exception(e) # Show full error for debugging
else:
    output_area.text_area("Result", value="Click the button to see the result.", height=250, label_visibility="collapsed", disabled=True)

