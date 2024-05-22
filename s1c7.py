from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decrypt_ECB():
  input_txt = open('set1/s1c7_input.txt', 'r').read()
  key = b'YELLOW SUBMARINE'
  decryptor = Cipher(algorithms.AES128(key), modes.ECB()).decryptor()
  ciphertext = b64decode(input_txt)
  output_bytes = decryptor.update(ciphertext) + decryptor.finalize()
  print(''.join([chr(int(byte)) for byte in output_bytes]))

decrypt_ECB()

