import string
from set2 import find_xor_combination
# S1E3: Single-byte XOR cipher
# The hex encoded string:

# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# ... has been XOR'd against a single character. Find the key, decrypt the message.

# You can do this by hand. But don't: write code to do it for you.

# How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.

def which_char_has_this_string_been_xored_against(input_string_hex):
  best_result = ''
  best_space_count = 0
  best_char = ''
  for ascii_char in string.ascii_letters:
    # make your ASCII to hex string 
    ascii_string_hex = ascii_char_to_hex_string(ascii_char, (len(input_string_hex) // 2)) 
    result_string = find_xor_combination(input_string_hex, ascii_string_hex)
    # now encode the hex to utf-8
    space_count = 0
    for c in [result_string[i:i+2] for i in range(0, len(result_string), 2)]:
      # get each 2 hex units to char
      char = chr(int(c, 16))
      if char == ' ':
        space_count += 1
    if space_count > best_space_count:
      best_result = result_string
      best_char = ascii_char
  return best_char

def ascii_char_to_hex_string(ascii_char, result_string_len):
  hex_code = hex(ord(ascii_char))
  return result_string_len * hex_code[2:]

assert (which_char_has_this_string_been_xored_against ('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')) == 'X'
