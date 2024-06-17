from secrets import token_bytes
from random import randrange
from s2c10 import cbc_encrypt, ecb_encrypt

# Write a function to generate a random AES key; that's just 16 random bytes.
def generate_random_aes_key():
  return token_bytes(16)

# Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.
# The function should look like:
# encryption_oracle(your-input)
# => [MEANINGLESS JIBBER JABBER]
# Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.
# Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.
def encryption_oracle(input_plaintext):
  print('ENCRYPTION ORACLE:')
  input_bytes = bytearray(input_plaintext, 'utf-8')
  prepend_bytecount = randrange(5, 11)
  append_bytecount = randrange(5, 11)
  input_bytes = token_bytes(prepend_bytecount) + input_bytes + token_bytes(append_bytecount)
  ecb_decider = randrange(2)
  result_bytes = ''
  mode = ''
  iv = generate_random_aes_key()
  if (ecb_decider):
    mode = 'ECB'
    result_bytes = ecb_encrypt(input_bytes, iv)
  else:
    mode = 'CBC'
    result_bytes = cbc_encrypt(input_bytes, iv)
  return (result_bytes, mode)

# Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.
def detect_encryption_mode(result_bytes):
  # try out a range of potential offsets 
  for i in range(5, 12):
    sequence_map = {}
    # put each sequence of 16 bytes in a map, keeping track of duplicates
    for j in range(i, len(result_bytes), 16):
      sequence = f'{result_bytes[j:j+16]}'
      sequence_map[sequence] = sequence_map.get(sequence, 0) + 1
    # after mapping the ciphertext bytes, see if we had any repeating patterns
    repeats = 0
    for value in sequence_map.values():
      if value > 1:
        repeats += value
    if repeats > 0:
      print(f'repeats was {repeats}')
      return "ECB"
  return "CBC"
