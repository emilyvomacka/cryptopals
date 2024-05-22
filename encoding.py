c = 'a'
print(c)
c_int = ord(c)
print(c_int)
c_hex = hex(c_int)
print(c_hex)
c_hex_without_prefix = "%02x" % c_int
print(c_hex_without_prefix)

abc_bytes = bytearray.fromhex('616263373839')
print(f'abc bytes: {abc_bytes}')
abc_str = ''.join([chr(int(byte)) for byte in abc_bytes])
print(f'abc string: {abc_str}')
print(f'abc_str.encode(): {abc_str.encode()}')