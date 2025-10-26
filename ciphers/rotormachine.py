# ciphers/rotormachine.py
# This file implements a simplified Enigma-like rotor machine.

from utils import normalize_text, ALPHABET

# --- Rotor and Reflector Definitions ---

# These are the standard wirings for the historical Enigma I rotors I, II, and III
ROTORS = {
    "I":   {"wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "turnover": "Q"},
    "II":  {"wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "turnover": "E"},
    "III": {"wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "turnover": "V"},
    "IV":  {"wiring": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "turnover": "J"},
    "V":   {"wiring": "VZBRGITYUPSDNHLXAWMJQOFECK", "turnover": "Z"}
}

# Reflector B from the historical Enigma machine
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# --- Main Processing Function ---

def rotor_machine_process(text: str, rotor_names: list[str], initial_positions: str, plugboard_settings: str) -> str:
    """
    Encrypts or decrypts text using the rotor machine simulation. The process is reciprocal.
    
    Args:
        text (str): The text to process.
        rotor_names (list[str]): A list of 3 rotor names (e.g., ["I", "III", "II"]).
        initial_positions (str): A 3-letter string for the starting positions (e.g., "AAA").
        plugboard_settings (str): A string of letter pairs (e.g., "AB CD EF").
        
    Returns:
        str: The processed text.
    """
    normalized_text = normalize_text(text)
    
    # --- Setup Plugboard ---
    plugboard = {}
    if plugboard_settings:
        pairs = plugboard_settings.upper().split()
        for pair in pairs:
            if len(pair) == 2 and pair[0] not in plugboard and pair[1] not in plugboard:
                plugboard[pair[0]] = pair[1]
                plugboard[pair[1]] = pair[0]

    # --- Setup Rotors and Positions ---
    # The rotors are arranged right-to-left physically (rotor_names[2], rotor_names[1], rotor_names[0])
    try:
        rotor_config = [ROTORS[name].copy() for name in rotor_names]
        positions = [ALPHABET.index(p) for p in initial_positions.upper()]
    except (KeyError, IndexError):
        return "Error: Invalid rotor names or initial positions."

    # --- Main Encryption/Decryption Loop ---
    processed_text = ""
    for char in normalized_text:
        
        # 1. Rotor Stepping (mimics physical movement)
        # The rightmost rotor (rotor 2) always steps.
        # "Double-stepping" is handled: If rotor 2 hits its turnover, rotor 1 steps.
        # If rotor 1 hits its turnover *as a result of stepping*, rotor 0 also steps.
        if ALPHABET[positions[1]] == rotor_config[1]['turnover']:
            positions[0] = (positions[0] + 1) % 26
            positions[1] = (positions[1] + 1) % 26
        
        # If the right rotor hits its turnover, the middle rotor steps.
        if ALPHABET[positions[2]] == rotor_config[2]['turnover']:
            positions[1] = (positions[1] + 1) % 26
            
        positions[2] = (positions[2] + 1) % 26

        # 2. Pass through Plugboard (if applicable)
        char = plugboard.get(char, char)
        
        # 3. Forward Pass through Rotors (Right to Left)
        char_index = ALPHABET.index(char)
        
        # Rotor 2 (Right)
        entry_index = (char_index + positions[2]) % 26
        exit_char = rotor_config[2]['wiring'][entry_index]
        char_index = (ALPHABET.index(exit_char) - positions[2] + 26) % 26
        
        # Rotor 1 (Middle)
        entry_index = (char_index + positions[1]) % 26
        exit_char = rotor_config[1]['wiring'][entry_index]
        char_index = (ALPHABET.index(exit_char) - positions[1] + 26) % 26
        
        # Rotor 0 (Left)
        entry_index = (char_index + positions[0]) % 26
        exit_char = rotor_config[0]['wiring'][entry_index]
        char_index = (ALPHABET.index(exit_char) - positions[0] + 26) % 26
        
        # 4. Pass through Reflector
        reflected_char = REFLECTOR_B[char_index]
        char_index = ALPHABET.index(reflected_char)

        # 5. Backward Pass through Rotors (Left to Right)
        # Rotor 0 (Left)
        entry_index = (char_index + positions[0]) % 26
        entry_char = ALPHABET[entry_index]
        exit_index = rotor_config[0]['wiring'].index(entry_char)
        char_index = (exit_index - positions[0] + 26) % 26
        
        # Rotor 1 (Middle)
        entry_index = (char_index + positions[1]) % 26
        entry_char = ALPHABET[entry_index]
        exit_index = rotor_config[1]['wiring'].index(entry_char)
        char_index = (exit_index - positions[1] + 26) % 26
        
        # Rotor 2 (Right)
        entry_index = (char_index + positions[2]) % 26
        entry_char = ALPHABET[entry_index]
        exit_index = rotor_config[2]['wiring'].index(entry_char)
        char_index = (exit_index - positions[2] + 26) % 26

        final_char = ALPHABET[char_index]
        
        # 6. Final Pass through Plugboard
        final_char = plugboard.get(final_char, final_char)
        
        processed_text += final_char
        
    return processed_text