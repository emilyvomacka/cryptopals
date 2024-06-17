



def add_cms_padding(string, padding_bytes_quantity):
  hex_padding_bytes = bytearray.fromhex('04') * padding_bytes_quantity
  string = string.encode() + (hex_padding_bytes)
  print(f'returning: %b', string)
  return string

assert add_cms_padding("YELLOW SUBMARINE", 4) == b'YELLOW SUBMARINE\x04\x04\x04\x04'
 
