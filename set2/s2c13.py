from secrets import token_bytes
from s2c10 import add_cms_padding, subtract_cms_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Write a k=v parsing routine, as if for a structured cookie. The routine should take:

# foo=bar&baz=qux&zap=zazzle
# ... and produce:

# {
#   foo: 'bar',
#   baz: 'qux',
#   zap: 'zazzle'
# }
# (you know, the object; I don't care if you convert it to JSON).
def key_value_parse(input_string):
  input_list = input_string.split("&")
  output_dict = {}
  for item in input_list:
    split = item.split("=")
    output_dict[split[0]] = split[1]

key_value_parse("foo=bar&baz=qux&zap=zazzle")

# Now write a function that encodes a user profile in that format, given an email address. You should have something like:
# profile_for("foo@bar.com")
# ... and it should produce:

# {
#   email: 'foo@bar.com',
#   uid: 10,
#   role: 'user'
# }
# ... encoded as:

# email=foo@bar.com&uid=10&role=user
# Your "profile_for" function should not allow encoding metacharacters (& and =). Eat them, quote them, whatever you want to do, but don't let people set their email address to "foo@bar.com&role=admin".
def profile_for(input_email: str):
  if "&" in input_email or "=" in input_email:
    raise ValueError("invalid input chars in email")
  profile_list = (('email', input_email), ('uid', '10'), ('role', 'user'))
  return '&'.join(key + '=' + val for (key, val) in profile_list)

print(profile_for('somebody@email.com'))

# Now, two more easy functions. Generate a random AES key, then:
key = token_bytes(16)

def ecb_encrypt(plaintext: bytes, key: bytes):
  encryptor = Cipher(algorithms.AES128(key), modes.ECB()).encryptor()
  plaintext = add_cms_padding(plaintext)
  output_bytes = encryptor.update(plaintext) + encryptor.finalize()
  return output_bytes

def ecb_decrypt(ciphertext: bytes, key: bytes):
  decryptor = Cipher(algorithms.AES128(key), modes.ECB()).decryptor()
  output = decryptor.update(ciphertext) + decryptor.finalize()
  print(output)
  return subtract_cms_padding(output).decode('utf-8')

assert ecb_decrypt(ecb_encrypt(b'somebody@email.com', key), key) == 'somebody@email.com'

# Encrypt the encoded user profile under the key; "provide" that to the "attacker".
def create_encoded_profile(email):
  input = bytes(profile_for(email), 'utf-8')
  return ecb_encrypt(input, key)

profile_ciphertext = create_encoded_profile('foo@bar.com')
# Decrypt the encoded user profile and parse it.
decrypted_profile = ecb_decrypt(profile_ciphertext, key)

# Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile.
def make_admin_profile():
  # first get the encoding of "admin" in byte position 0-4 of a 16 byte block
  first_output = create_encoded_profile('12345678901234567890123456admin\v\v\v\v\v\v\v\v\v\v\v')
  admin_block = first_output[32:48]


  profile = bytearray(create_encoded_profile('tilapia@fishy'))
  edited_profile = profile[:32] + admin_block 

  return ecb_decrypt(edited_profile, key)


print(make_admin_profile())
