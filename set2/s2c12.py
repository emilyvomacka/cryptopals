from base64 import b64decode
from s2c10 import ecb_encrypt
from s2c11 import encryption_oracle, detect_encryption_mode
from secrets import token_bytes

# Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable).
unknown_key = token_bytes(16)

# Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string:
# Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
# aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
# dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
# YnkK

# What you have now is a function that produces:
# AES-128-ECB(your-string || unknown-string, random-key)
def ecb_oracle_encrypt_unknown_string(input):
  plaintext_bytes = append_to_input_string(input)
  return ecb_encrypt(plaintext_bytes, unknown_key)

def append_to_input_string(input):
  string_to_decode = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
  dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
  return bytearray(input, 'utf-8') + b64decode(string_to_decode)

# It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function!
def ecb_decrypt_unknown_string(ciphertext):
  # Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway.
  block_size, padding_len = determine_block_size(ciphertext)
  # Detect that the function is using ECB. You already know, but do this step anyways.
  cipher_mode = detect_encryption_mode(ciphertext)
  assert cipher_mode == 'ECB'
  plaintext = ''
  no_append_len = len(ecb_oracle_encrypt_unknown_string(''))
  print(f'no append len is {no_append_len}')
  for i in range(0, no_append_len, block_size): 
    input_block = "A" * (block_size - 1)
    temp_input_block = plaintext[-(i - 1):] if i > 0 else input_block
    for j in range(0, block_size):
      # Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position.
      output_block = ecb_oracle_encrypt_unknown_string(input_block)[i:i+block_size]
      # Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation.
      for k in range(0, 256):
        temp_char = chr(k)
        output = ecb_oracle_encrypt_unknown_string(temp_input_block + temp_char)
        temp_output_block = output[i - block_size:i] if i > 0 else output[0:block_size] 
        if temp_output_block == output_block:
          plaintext += temp_char
          temp_input_block = temp_input_block[1:] + temp_char
          # decrement input block to expose one more char of the plaintext for the next iteration
          input_block = input_block[1:]
          break

  print(f'plaintext: {plaintext}')
  print(f'len plaintext == {len(plaintext)}, len no_append string = {no_append_len}')

def determine_block_size(ciphertext):
  padding_len = 0
  # Lengthen the string until a new block of ciphertext is produced, to determine padding and block size
  initial_output_len = len(ecb_oracle_encrypt_unknown_string(''))
  for i in range(1, len(ciphertext)):
    input = "A" * i
    output_len = len(ecb_oracle_encrypt_unknown_string(input))
    if output_len != initial_output_len:
      padding_len = i
      block_size = output_len - initial_output_len
      return (block_size, padding_len)

def main():
  input_txt = open('c11_input_twocities.txt', 'r').read()
  ciphertext = ecb_oracle_encrypt_unknown_string(input_txt)
  ecb_decrypt_unknown_string(ciphertext)

main()