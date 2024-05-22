from base64 import b64decode

def ascii_to_bytes(string):
  return bytearray([ord(c) for c in string])

def hamming_distance(str1_bytes, str2_bytes):
  assert len(str1_bytes) == len(str2_bytes), 'bytestrings are different lengths'
  result = [(str1_bytes[i] ^ str2_bytes[i]) for i in range(len(str1_bytes))]
  result_bytes = [bin(i)[2:] for i in result]
  binary_string = ''.join(result_bytes)
  return sum([int(i) for i in binary_string])
  
assert hamming_distance(ascii_to_bytes("this is a test"), ascii_to_bytes("wokka wokka!!!")) == 37

def chunk(input_bytes, chunk_size_bytes):
  return [input_bytes[i:i + chunk_size_bytes] in range (0,len(input_bytes) - chunk_size_bytes, chunk_size_bytes)]

def find_low_ham_key_lengths(input_str):
  # first let's get the input str in binary
  input_bytes = b64decode(input_str)
  key_range = range(2,40)
  hamming_distances = []
  # for each key range, get the hamming distance between the first and second chunk
  for key_length in key_range: 
    hamming_distances.append((key_length, find_normalized_ham(input_bytes, key_length)))
  hamming_distances.sort(key=lambda item: item[1])
  print(f'sorted hamming distances are: {hamming_distances}')
  return hamming_distances


# let's get the first three hamming distances and average them 
def find_normalized_ham(input_bytes, key_length):
  chunk_1 = input_bytes[:key_length] 
  hams = [hamming_distance(chunk_1, input_bytes[key_length:2*key_length]), 
          hamming_distance(chunk_1, input_bytes[2*key_length:3*key_length]), 
          hamming_distance(chunk_1, input_bytes[3*key_length:4*key_length])] 
  average_ham = sum(hams) / len(hams) 
  normalized = average_ham / key_length
  return normalized

# This splits the binary-encoded text into equal chunks of a given size, so we can try out keys of different lengths against the input.
def split_chunks(input_bin, chunk_size):
  """Split an iterable into chunks of a specified size"""
  number_of_chunks = len(input_bin) // chunk_size
  # print(f'chunk_size is {chunk_size}, len of input_bin is {len(input_bin)}, number of chunks is {number_of_chunks}')
  result = []
  for i in range(0, number_of_chunks):
    index = i * chunk_size
    result.append(bytearray(input_bin[index:index + chunk_size]))
  return result

def find_best_key_and_score(key_length, input_bytes):
  # splits the input into key-sized chunks
  split_input = split_chunks(input_bytes, key_length)
  key = ''
  scores_per_index = []
  for i in range(0, key_length):
    # for each byte in key_length, make a block comprised of that byte in each chunk.
    transposed_chunks = bytearray([chunk[i] for chunk in split_input])
    key_letter = ''
    common_letters = 'etaoin shrdlu'
    highest_common_letter_count = 0
    ascii = [chr(x) for x in range(128)]
    for ascii_char in ascii:
      xor_bytes = bytearray()
      for position in range(0, len(transposed_chunks)):
        xor_bytes.append(transposed_chunks[position] ^ ord(ascii_char))
      xor_result_string = ''.join([chr(i) for i in xor_bytes])
      common_letter_count = sum([xor_result_string.count(letter) for letter in common_letters])
      if (common_letter_count > highest_common_letter_count):
        highest_common_letter_count = common_letter_count
        key_letter = ascii_char
    key = key + key_letter
    scores_per_index.append(highest_common_letter_count)
  return {'key': key, 'score': sum(scores_per_index)}

def decrypt_input(input_bytes, key_str):
  key_byte_array = bytearray([ord(c) for c in key_str])
  key_length = len(key_str)
  xor_result_bytes = bytearray()
  for i, input_byte in enumerate(input_bytes):
    xor_result_bytes.append(input_byte ^ key_byte_array[i % key_length])
  xor_result_str = ''.join([chr(int(byte)) for byte in xor_result_bytes])
  return xor_result_str

def vigenere():
  input_txt = open('set1/s1c6_input.txt', 'r').read()
  key_rank = find_low_ham_key_lengths(input_txt)
  results_for_top_key_lengths = []
  input_bytes = b64decode(input_txt)
  for i in range(0,3):
    results_for_top_key_lengths.append(find_best_key_and_score(key_rank[i][0], input_bytes))
  results_for_top_key_lengths.sort(key=lambda item: item['score'], reverse=True)
  print(decrypt_input(input_bytes, results_for_top_key_lengths[0]['key']))

vigenere()
