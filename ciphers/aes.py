# This file implements AES using the professional pycryptodome library.
# This ensures security and correctness. We will use GCM mode for AEAD.

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json

# AES GCM mode provides both confidentiality and integrity (authentication).
# We need to store/send the ciphertext, the tag, and the nonce.
# We will use Base64 encoding to make them into a single, printable string.

def aes_encrypt(plaintext: str, key_bytes: bytes) -> str:
    """
    Encrypts text using AES-GCM mode.
    
    Args:
        plaintext (str): The text to encrypt.
        key_bytes (bytes): The encryption key (must be 16, 24, or 32 bytes).
        
    Returns:
        str: A Base64 encoded string containing the nonce, tag, and ciphertext.
    """
    try:
        # Convert plaintext to bytes
        data = plaintext.encode('utf-8')
        
        # Create a new AES cipher object in GCM mode
        cipher = AES.new(key_bytes, AES.MODE_GCM)
        
        # Encrypt the data
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # We need to store nonce, tag, and ciphertext to be able to decrypt.
        # We'll pack them into a JSON object and then Base64 encode it.
        json_fields = {
            'nonce': base64.b64encode(cipher.nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
        }
        
        # Encode the JSON object to Base64
        encrypted_data = base64.b64encode(json.dumps(json_fields).encode('utf-8'))
        
        return encrypted_data.decode('utf-8')
        
    except Exception as e:
        return f"Encryption Error: {e}"

def aes_decrypt(base64_data: str, key_bytes: bytes) -> str:
    """
    Decrypts a Base64 encoded AES-GCM string.
    
    Args:
        base64_data (str): The Base64 encoded string from aes_encrypt.
        key_bytes (bytes): The same key used for encryption.
        
    Returns:
        str: The decrypted plaintext or an error message.
    """
    try:
        # Decode the Base64 data to get the JSON string
        json_data = base64.b64decode(base64_data).decode('utf-8')
        
        # Parse the JSON object
        fields = json.loads(json_data)
        
        # Decode each part from Base64
        nonce = base64.b64decode(fields['nonce'])
        tag = base64.b64decode(fields['tag'])
        ciphertext = base64.b64decode(fields['ciphertext'])
        
        # Create the AES cipher object with the same key and nonce
        cipher = AES.new(key_bytes, AES.MODE_GCM, nonce=nonce)
        
        # Decrypt and verify the data (GCM automatically checks the tag)
        decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        
        # Decode bytes back to a string
        return decrypted_bytes.decode('utf-8')
        
    except (ValueError, KeyError, json.JSONDecodeError):
        return "Decryption Error: Invalid data or key. (Authentication failed)"
    except Exception as e:
        return f"Decryption Error: {e}"