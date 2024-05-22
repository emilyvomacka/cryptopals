# Key must be 16 bytes
# Deterministic: same input always produces same results
# Stateless: you can do operations in any order, no state is kept. Functional??

"""
Detect AES in ECB mode
In s1c8_input.txt there are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic;
the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

"""

from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decrypt_c8():
  input_txt = open('s1c8_input.txt', 'r').read()
  key = b'YELLOW SUBMARINE'
  decryptor = Cipher(algorithms.AES128(key), modes.ECB()).decryptor()


print("hi")
decrypt_c8()