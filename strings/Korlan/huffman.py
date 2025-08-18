import heapq
from collections import defaultdict

class Node:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol  # Only used for leaf nodes
        self.freq = freq      # Frequency of the symbol (or sum of children's frequencies)
        self.left = left
        self.right = right
        
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoder:
    """
    A class to perform Huffman encoding and decoding for any array of immutable objects.
    """
    
    def __init__(self):
        self.huffman_tree = None    # Root of the Huffman tree
        self.huffman_codes = {}     # Maps symbols to their Huffman codes 
        
    def _build_frequency_table(self, data):
        """
        Builds a frequency table for the immutable objects in the input data array.
        """
        frequency_table = defaultdict(int)
        for item in data:
            frequency_table[item] += 1
        return frequency_table

    def _build_huffman_tree(self, frequency_table):
        """
        Builds a Huffman tree from the frequency table using a min-heap.
        """
        pq = []
        for symbol, freq in frequency_table.items():
            heapq.heappush(pq, Node(symbol=symbol, freq=freq))

        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            parent = Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(pq, parent)

        self.huffman_tree = heapq.heappop(pq) if pq else None
        

    def _build_huffman_codes(self, node, current_code=""):
        """
        Recursively builds the Huffman codes dictionary by traversing the corrected tree structure.
        """
        if node is None:
            return
        
        if node.left is None and node.right is None:
            self.huffman_codes[node.symbol] = current_code
            return
        
        # Traverse left (add '0') and right (add '1')
        self._build_huffman_codes(node.left, current_code + "0")
        self._build_huffman_codes(node.right, current_code + "1")   
    
    def encode(self, data):
        """
        Encodes the input data array.
        Returns a tuple: (encoded_string, huffman_tree)
        """
        # Build frequency table, tree, and codes
        freq_table = self._build_frequency_table(data)
        self._build_huffman_tree(freq_table)
        self._build_huffman_codes(self.huffman_tree)
        
        # Generate encoded string
        encoded_str = ''.join(self.huffman_codes[item] for item in data)
        return (encoded_str, self.huffman_tree)

    def decode(self, encoded_data, huffman_tree):
        """
        Decodes the binary string using the provided Huffman tree.
        Returns the original array of immutable objects.
        """
        current_node = huffman_tree
        decoded_data = []
        for bit in encoded_data:
            current_node = current_node.left if bit == '0' else current_node.right
            if current_node.left is None and current_node.right is None:
                decoded_data.append(current_node.symbol)
                current_node = huffman_tree

        return decoded_data
    
def main_huffman():
    """
    Main function for testing the HuffmanCoder class with a string and a list of tuples.
    """
    print("--- Testing Huffman with a simple string ---")
    text_to_compress = "this is a simple example of huffman encoding"
    
    huffman_coder = HuffmanCoder()
    encoded_text, huffman_tree = huffman_coder.encode(list(text_to_compress))
    decoded_text_list = huffman_coder.decode(encoded_text, huffman_tree)
    decoded_text = "".join(decoded_text_list)
    
    assert text_to_compress == decoded_text, "Decoding failed for string!"
    print(f"Original Text: '{text_to_compress}'")
    print(f"Decoded Text:  '{decoded_text}'")
    print("Huffman Encoding/Decoding works correctly for strings! ✅")

    original_size_bits = len(text_to_compress) * 8
    compressed_size_bits = len(encoded_text)
    compression_rate = (1 - compressed_size_bits / original_size_bits) * 100
    
    print(f"\nOriginal Size (bits): {original_size_bits}")
    print(f"Compressed Size (bits): {compressed_size_bits}")
    print(f"Compression Rate: {compression_rate:.2f}%")

    print("\n" + "="*50 + "\n")

    print("--- Testing Huffman with a list of tuples (simulating LZ77 tokens) ---")
    
    # Example data representing LZ77 tokens
    lz77_tokens = [
        (0, 0, 't'), (0, 0, 'h'), (0, 0, 'i'), (0, 0, 's'), (0, 0, ' '),
        (0, 0, 'i'), (0, 0, 's'), (0, 0, ' '), (0, 0, 'a'), (0, 0, ' '),
        (0, 0, 's'), (0, 0, 'i'), (0, 0, 'm'), (0, 0, 'p'), (0, 0, 'l'),
        (0, 0, 'e'), (0, 0, ' '), (0, 0, 'e'), (0, 0, 'x'), (0, 0, 'a'),
        (0, 0, 'm'), (0, 0, 'p'), (0, 0, 'l'), (0, 0, 'e')
    ]
    
    huffman_coder_tokens = HuffmanCoder()
    encoded_tokens, huffman_tree_tokens = huffman_coder_tokens.encode(lz77_tokens)
    decoded_tokens = huffman_coder_tokens.decode(encoded_tokens, huffman_tree_tokens)
    
    assert lz77_tokens == decoded_tokens, "Decoding failed for tuples!"
    print("Huffman Encoding/Decoding works correctly for a list of tuples! ✅")

    print(f"\nOriginal number of tokens: {len(lz77_tokens)}")
    print(f"Encoded size (bits): {len(encoded_tokens)}")
    print("Note: The compression rate here is an approximation, as the original size "
          "in bits depends on the bit representation of each token (offset, length, char).")

if __name__ == '__main__':
    main_huffman()
    