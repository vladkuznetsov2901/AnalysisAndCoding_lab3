import ast
import heapq
import math


class ShannonFanoNode:
    def __init__(self, symbol=None, frequency=None, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency


def build_tree(symbols, frequencies):
    heap = []

    for symbol, frequency in zip(symbols, frequencies):
        node = ShannonFanoNode(symbol=symbol, frequency=frequency)
        heapq.heappush(heap, node)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        parent = ShannonFanoNode(
            symbol=None,
            frequency=node1.frequency + node2.frequency,
            left=node1,
            right=node2
        )

        heapq.heappush(heap, parent)

    return heap[0]


def encode_text(text):
    symbols = list(set(text))
    frequencies = [text.count(symbol) for symbol in symbols]

    tree = build_tree(symbols, frequencies)
    codes = {}

    def traverse(node, code=''):
        if node.symbol:
            codes[node.symbol] = code
        else:
            traverse(node.left, code + '0')
            traverse(node.right, code + '1')

    traverse(tree)
    encoded_text = ''.join(codes[symbol] for symbol in text)

    return encoded_text, codes


def decode_text(encoded_text, codes):
    inverted_codes = {v: k for k, v in codes.items()}
    decoded_text = ''
    current_code = ''

    for bit in encoded_text:
        current_code += bit
        if current_code in inverted_codes:
            decoded_text += inverted_codes[current_code]
            current_code = ''

    return decoded_text, codes


def lz77_encode(text):
    window_size = 7
    encoded_text = ""
    i = 0

    while i < len(text):
        match = ''
        length = 0
        offset = 0

        for j in range(1, min(window_size, i) + 1):
            if text[i:i + j] in text[max(0, i - window_size):i]:
                offset = i - text.rfind(text[i:i + j], 0, i)
                length = j

        if length > 0:
            next_char = text[i + length] if i + length < len(text) else ''
            match = f"<{offset},{length},{next_char}>"
            i += length + 1
        else:
            match = f"<0,0,{text[i]}>"
            i += 1

        encoded_text += match

    return encoded_text


def lz77_decode(encoded_text):
    decoded_text = ''
    i = 0

    while i < len(encoded_text):
        if encoded_text[i] != '<':
            decoded_text += encoded_text[i]
            i += 1
        else:
            end_index = encoded_text.find(">", i)
            if end_index == -1:
                break
            comma_index1 = encoded_text.find(",", i)
            comma_index2 = encoded_text.find(",", comma_index1 + 1, end_index)
            offset = int(encoded_text[i + 1:comma_index1])
            length_str = encoded_text[comma_index1 + 1:comma_index2]
            length = int(''.join(filter(str.isdigit, length_str)))
            next_char = encoded_text[comma_index2 + 1:end_index]

            start_pos = len(decoded_text) - offset

            for j in range(length):
                if start_pos + j < len(decoded_text):
                    decoded_text += decoded_text[start_pos + j]

            decoded_text += next_char
            i = end_index + 1

    return decoded_text


with open("RGB_svg.bmp", 'rb') as file:
    original_text = file.read()

choice = int(input("1 - Encode, 2 - Decode: "))

if choice == 1:
    encoded_text, codes = encode_text(original_text.decode('latin-1'))

    encoded_lz77 = lz77_encode(encoded_text)

    with open("shannon_fano_encoded.txt", 'w', encoding='latin-1') as file:
        file.write(encoded_text)
        file.write("\n")
        file.write(str(codes))

    with open("lz77_encoded.txt", 'w', encoding='latin-1') as file:
        file.write(str(encoded_lz77))

    with open("lz77_encoded.txt", 'r', encoding='latin-1') as file:
        encoded_lz77 = file.read()
else:
    with open("lz77_encoded.txt", "r", encoding='latin-1') as f:
        encoded_lz77 = f.read()
    with open("shannon_fano_encoded.txt", 'r', encoding='latin-1') as file:
        content = file.readlines()
        codes = ast.literal_eval(content[1].strip())

    output_lz77 = str(encoded_lz77).replace('<', '', )
    output_lz77 = str(output_lz77).replace('>', '', )
    output_lz77 = str(output_lz77).replace(',', '', )

    decoded_lz77 = lz77_decode(encoded_lz77)
    decoded_text, codes = decode_text(decoded_lz77, codes)

    with open("code_lz77.txt", 'w', encoding='latin-1') as file:
        file.write(output_lz77)

    with open("decoded_lz77.txt", 'w', encoding='latin-1') as file:
        file.write(decoded_lz77)

    with open("output.bmp", 'wb') as file:
        file.write(decoded_text.encode('latin-1'))

print("Done")
