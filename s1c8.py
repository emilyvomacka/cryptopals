# Key must be 16 bytes
# Deterministic: same input always produces same results
# Stateless: you can do operations in any order, no state is kept. Functional??

def decrypt_c8():
  input_txt = open('set1/s1c8_input.txt', 'r').read()
  key = b'YELLOW SUBMARINE'
  decryptor = Cipher(algorithms.AES128(key), modes.ECB()).decryptor()