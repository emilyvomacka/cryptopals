
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64decode, b64encode

def subtract_cms_padding(bytestring):
  equality = bytestring[-1:] == b"\x04"
  while bytestring[-1:] == b'\x04':
    bytestring = bytestring[:-1]
  return bytestring

def add_cms_padding(plaintext_bytes):
  padding_len = 16 - (len(plaintext_bytes) % 16)
  if padding_len != 0:
    padding_bytes = bytearray.fromhex('04') * padding_len
    return plaintext_bytes + padding_bytes

def xor_two_bytearrays(bytes_1, bytes_2):
  output = bytearray()
  for position in range(0,len(bytes_1)):
    output.append(bytes_1[position] ^ bytes_2[position])
  return output

def ecb_encrypt(plaintext_bytes, key):
  encryptor = Cipher(algorithms.AES128(key), modes.ECB()).encryptor()
  plaintext_bytes = add_cms_padding(plaintext_bytes)
  output_bytes = encryptor.update(plaintext_bytes) + encryptor.finalize()
  return output_bytes

def ecb_decrypt(ciphertext_bytes):
  key = b'YELLOW SUBMARINE'
  decryptor = Cipher(algorithms.AES128(key), modes.ECB()).decryptor()
  output_bytes = decryptor.update(ciphertext_bytes) + decryptor.finalize()
  return subtract_cms_padding(output_bytes).decode('utf-8')

def cbc_encrypt(plaintext_bytes, key_bytes):
  # Get an encryptor
  encryptor = Cipher(algorithms.AES128(key_bytes), modes.ECB()).encryptor()
  result = bytearray()
  plaintext_bytes = add_cms_padding(plaintext_bytes)

  # xor the first block of plaintext against the initialization vector
  iv = bytes(16)
  xored_first_plaintext = xor_two_bytearrays(plaintext_bytes[:16], iv)

  # encrypt the first block of plaintext
  ciphertext = encryptor.update(xored_first_plaintext)
  result = result + ciphertext

  for i in range(16, len(plaintext_bytes), 16):
    # xor each block of plaintext with the previous ciphertext block
    xored_current_plaintext = xor_two_bytearrays(plaintext_bytes[i:i+16], ciphertext)
    # encrypt each xored plaintext block
    ciphertext = encryptor.update(xored_current_plaintext)
    result = result + ciphertext
  return result + encryptor.finalize()

def cbc_decrypt(ciphertext_bytes):
  # Get an decryptor 
  key = b'YELLOW SUBMARINE'
  decryptor = Cipher(algorithms.AES128(key), modes.ECB()).decryptor()
  result = b''

  previous_block = bytes(16)

  for i in range(0, len(ciphertext_bytes), 16):
    encrypted_text = ciphertext_bytes[i:i+16]
    decrypted_text = decryptor.update(encrypted_text)
    xored_text = xor_two_bytearrays(decrypted_text, previous_block)
    previous_block = encrypted_text
    result += xored_text
  return subtract_cms_padding(result).decode('utf-8')

input_txt = open('c10_input.txt', 'r').read()
input_bytes = b64decode(input_txt)
cbc_decrypt(input_bytes)

message = b'here is a plaintext it is very long extremely long plaintext'

ciphermessage = cbc_encrypt(message, b'YELLOW SUBMARINE')
decrypt_message = cbc_decrypt(ciphermessage)
if decrypt_message == message.decode('utf-8'):
  print('cbc encrypt and decrypt work')
else: 
  print(decrypt_message)

ciphermessage = ecb_encrypt(message, b'YELLOW SUBMARINE')
decrypt_message = ecb_decrypt(ciphermessage)
if decrypt_message == message.decode('utf-8'):
  print('ecb encrypt and decrypt work')
else:
  print(decrypt_message)