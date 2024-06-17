# Key must be 16 bytes
# Deterministic: same input always produces same results
# Stateless: you can do operations in any order, no state is kept. Functional??

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from s1c6 import hamming_distance
"""
Detect AES in ECB mode
In s1c8_input.txt there are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic;
the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

Theory 1: if units of 16 bytes have similar edit distances, this might be evidence of periodicity.
[edit distance x][edit distance x + 1][edit distance x - 2] 
vs
[edit distance x][edit distance x + 18][edit distance x - 74]

Theory 2: I'd expect a lower normalized distance between each byte in a 16 byte sequence (i.e. all bytes 1s have a similar distance, all byte 2s have a similar distance)
Here are edit distances for an encrypted text:
[4 8 16 2 ...][4 7 14 3 ...]
Here are edit distances for an unencrypted text:
[4 8 16 2 ...][16 3 1 28 ...]
This seems harder to test bc the distance between any two bytes will never be very large.


Theory 3: so it actually turns out that we just have to determine whether any of the 16 byte sequences in the output repeats any other set. That is...kind of less interesting.
Index is 132 :) 
"""


def decrypt_c8():
  input_txt = open('s1c8_input.txt', 'r').readlines()
  lines_with_repeats = []
  for (i, line) in enumerate(input_txt):
    # 16 bytes equals 32 hex chars
    print(f'i is {i}, line is {line}')
    sequence_map = {}
    for j in range(0, len(line), 32):
      sequence = line[j:j+32]
      sequence_map[sequence] = sequence_map.get(sequence, 0) + 1
    repeats = 0
    for value in sequence_map.values():
      if value > 1:
        repeats += value
    if repeats > 0:
      lines_with_repeats.append({'index': i, 'repeats': repeats})
  lines_with_repeats.sort(key=lambda item: item['repeats'], reverse=True)
  print(lines_with_repeats)
    

print("hi")
decrypt_c8()

  # turns out we don't need to calculate the standard dev of hamming distances, but if we did, here it is:
  #for (h, input_ln) in enumerate(input_txt):
    ## translate to bytes
    #input_bytes = bytearray.fromhex(input_ln)
    ## get first byte chunk, initialize array
    #first_bytes_chunk = input_bytes[:16]
    #hamming_distances = []
    ## divide the rest into 16 byte chunks, add hamming distances to array
    #for i in range(16, len(input_bytes), 16):
      #bytes_chunk = input_bytes[i:i+16]
      #hamming_distances.append(hamming_distance(first_bytes_chunk, bytes_chunk))
    #mean_hamming_distance = sum(hamming_distances) / len(hamming_distances)
    #squared_distance_from_mean = []
    #for j in hamming_distances:
      #squared_distance_from_mean.append((j - mean_hamming_distance) ** 2)
      #standard_dev = sum(squared_distance_from_mean) / len(squared_distance_from_mean)
    #standard_devs.append({'index': h, 'standard_dev': standard_dev})
  #print('HERE ARE THE DEVS\n')
  #standard_devs.sort(key=lambda item: item['standard_dev'])
  #print(standard_devs)

  ## ok we have our winning index: 155
  #best_index = standard_devs[0]['index']
  #encrypted_bytes_array = bytearray.fromhex(input_txt[best_index])
  ##print(f'encrypted text is {encrypted_bytes_array}')
  ##print(f'length of text is {len(encrypted_bytes_array)}')

  #key = b'YELLOW SUBMARINE'
  #decryptor = Cipher(algorithms.AES128(key), modes.ECB()).decryptor()

  #key = ''
  #for i in range (0,16):
    #bytes_array = []
    #for j in range(i,len(encrypted_bytes_array),16):
      #bytes_array.append(encrypted_bytes_array[j])
    ## ascii
    #for range (0, 128):
      #key_bytes = bytearray()
      #for range(0, 16):
        #key_bytes.append(ord)
  ##output_bytes = decryptor.update(encrypted_text) + decryptor.finalize()
  ##print(''.join([chr(int(byte)) for byte in output_bytes]))