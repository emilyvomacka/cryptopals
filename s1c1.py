
import string
# S1C1: hex to base64

def hex_to_base64(hex_string):
  # First, convert hex to bytes
  bytes_from_hex = bytes.fromhex(hex_string)
  bin_string = ''.join(["{:08b}".format(b) for b in bytes_from_hex])

  # Pad so the string is divisible by 6
  padding_bytes = 0
  if len(bin_string) % 6 != 0:
    bin_string += "0" * 6 - (len(bin_string) % 6)
  
  # Convert bytes to b64
  b64_string = ''
  b64_table = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
  for i in range (0, len(bin_string), 6):
    found_int = int(bin_string[i:i+6], base=2)
    found_letter = b64_table[found_int]
    b64_string += b64_table[(int(bin_string[i:i+6], base=2))]
  return b64_string

assert hex_to_base64('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d') == 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
