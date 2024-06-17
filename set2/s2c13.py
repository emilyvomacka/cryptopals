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
  print(f'output is {output_dict}')

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
  print(f'profile string is {input}, len {len(input)}')
  return ecb_encrypt(input, key)

profile_ciphertext = create_encoded_profile('foo@bar.com')
print(f'encrypted profile: {profile_ciphertext}')
# Decrypt the encoded user profile and parse it.
decrypted_profile = ecb_decrypt(profile_ciphertext, key)
print(f'decrypted profile: {decrypted_profile}')

# Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile.
def make_admin_profile():
  # first get the encoding of "admin" in byte position 0-4 of a 16 byte block
  first_output = create_encoded_profile('12345678901234567890123456admin\v\v\v\v\v\v\v\v\v\v\v')
  admin_block = first_output[32:48]
  print(f'admin block: {admin_block}')

  print(f'admin block decrypted: {ecb_decrypt(first_output[32:], key)}')

  profile = bytearray(create_encoded_profile('tilapia@fishy'))
  print(f'length before editing is {len(profile)}')
  print(f'decryption which should be role=user: {ecb_decrypt(profile, key)}')
  edited_profile = profile[:32] + admin_block 
  print(f'encrypted edited profile is {edited_profile}')
  print(f'we expect this block to be admin: {edited_profile[32:37]}')
  print(f'length after editing is {len(edited_profile)}')
  for i in range(len(edited_profile)):
    if edited_profile[i] != profile[i]:
      print(f'byte {i} has been changed')

  print(f'decryped profile first two blocks: {ecb_decrypt(edited_profile[:32], key)}')
  print(f'decryped profile: {ecb_decrypt(edited_profile, key)}')


make_admin_profile()