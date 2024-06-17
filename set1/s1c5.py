# Here is the opening stanza of an important work of the English language:

# Burning 'em, if you ain't quick and nimble
# I go crazy when I hear a cymbal
# Encrypt it, under the key "ICE", using repeating-key XOR.

# In repeating-key XOR, you'll sequentially apply each byte of the key; the first byte of plaintext will be XOR'd against I, the next C, the next E, then I again for the 4th byte, and so on.

# It should come out to:

# 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
# a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

def ice_encrypt(input_string_ascii):
  key_index = 0
  keys = ['I', 'C', 'E']
  input_byte_array = bytearray([ord(c) for c in input_string_ascii])
  xor_result_bytes = bytearray()
  for input_byte in input_byte_array:
    result_byte = input_byte ^ ord(keys[key_index % 3])
    xor_result_bytes.append(input_byte ^ ord(keys[key_index % 3]))
    key_index += 1
  # this also works: return ''.join(["%02x" % ord(chr(x)) for x in xor_result_bytes])
  return xor_result_bytes.hex()

input = "Burning \'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
result = ice_encrypt(input)

assert result == "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
