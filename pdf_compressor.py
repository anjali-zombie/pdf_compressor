import heapq
from collections import Counter
import os
from PyPDF2 import PdfReader

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = Counter(text)
    heap = [HuffmanNode(char, f) for char, f in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_huffman_codes(root):
    codes = {}
    def generate_codes(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")
    generate_codes(root, "")
    return codes

def huffman_encode(text, codes):
    return ''.join(codes[char] for char in text)

def huffman_decode(encoded_text, root):
    decoded_text = []
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = root
    return ''.join(decoded_text)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def save_compressed_data(encoded_text, codes, output_path):
    with open(output_path, "wb") as file:
        file.write(encoded_text.encode())
    print(f"Compressed file saved as {output_path}")

def compress_pdf(pdf_path, output_path):
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Original text length: {len(text)} characters")
    
    print("Building Huffman Tree...")
    root = build_huffman_tree(text)
    
    print("Generating Huffman Codes...")
    codes = generate_huffman_codes(root)
    
    print("Compressing text...")
    encoded_text = huffman_encode(text, codes)
    print(f"Compressed text length: {len(encoded_text)} bits")
    
    print("Saving compressed data...")
    save_compressed_data(encoded_text, codes, output_path)
    print("Compression complete.")

def decompress_file(encoded_path, root):
    print("Reading compressed data...")
    with open(encoded_path, "rb") as file:
        encoded_text = file.read().decode()
    
    print("Decompressing text...")
    text = huffman_decode(encoded_text, root)
    print("Decompression complete.")
    return text

if __name__ == "__main__":
    input_pdf = "syspro.pdf"  
    output_file = "compressed.txt"
    decompress_output = "decompress.txt"
    text = extract_text_from_pdf(input_pdf)
    root = build_huffman_tree(text)

    compress_pdf(input_pdf, output_file)

    decompress_text = decompress_file(output_file, root)
    with open(decompress_output,"w") as file:
        file.write(decompress_text)

