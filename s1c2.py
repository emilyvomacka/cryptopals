
# S1E2: fixed xor
def find_xor_combination(string_1, string_2):
  bytes_from_hex_1, bytes_from_hex_2 = bytes.fromhex(string_1), bytes.fromhex(string_2)

  output = bytearray()

  for position in range(0,len(bytes_from_hex_1)):
    output.append(bytes_from_hex_1[position] ^ bytes_from_hex_2[position])
  # why can't we just: output = bytes_from_hex_1 ^ bytes_from_hex_2

  # print(output) # will print as if in utf8 
  return output.hex()


assert find_xor_combination('1c0111001f010100061a024b53535009181c','686974207468652062756c6c277320657965') == '746865206b696420646f6e277420706c6179'