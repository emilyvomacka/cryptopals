
# One of the 60-character strings in this file has been encrypted by single-character XOR.
# Find it.
# (Your code from #3 should help.)
def find_single_char_xor_encrypted_string():
  common_letters = 'etaoin shrdlu'
  ascii = [chr(x) for x in range(128)]
  file = open('set1/s1c4_input.txt', 'r')
  highest_common_letter_count = 0
  encoded_string = ''
  for line_hex in file:
    for ascii_char in ascii:
      line_bytes = bytearray.fromhex(line_hex)  
      xor_result = [byte ^ ord(ascii_char) for byte in line_bytes]
      xor_result_string = ''.join([chr(i) for i in xor_result])
      common_letter_count = sum([xor_result_string.count(letter) for letter in common_letters])
      if (common_letter_count > highest_common_letter_count):
        print(f'SET 4 FOUND NEW HIGHEST SCORING STRING {xor_result_string}')
        highest_common_letter_count = common_letter_count
        encoded_string = xor_result_string
  return encoded_string

find_single_char_xor_encrypted_string()
