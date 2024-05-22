
from base64 import b64encode
import string
# S1E1: hex to base64

def hex_to_base64(hex_string):
  # First, convert hex to bytes
  bytes_from_hex = bytes.fromhex(hex_string)
  # Then, convert bytes to b64
  base64_from_bytes = b64encode(bytes_from_hex).decode()
  return base64_from_bytes

#     # Convert hex string into binary
#     binary_string = bytes.fromhex(hex_string)
#     print(f'BINARY STRING {binary_string}')
#     strip = binary_string[2:]

#     # Split the binary string into six-bit chunks
#     len_binary_string = len(strip)
#     six_bit_list = []
#     for i in range(6, len_binary_string, 6):
#       six_bit_list.append(strip[i-6:i])
#     print(f'SIX BIT LIST: {six_bit_list}')
#     base64string = ''

#     # Translate each chunk into b64
#     for bit_chunk in six_bit_list:
#       print(f'BIT CHUNK IS {bit_chunk}')
#       i = int(bit_chunk, 2)
#       print(f'int is {i}')
#       char = binary_to_b64_map[i]
#       base64string += char
#     print(base64string)

   
assert hex_to_base64('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d') == 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'


