from huffman import HuffmanCoder
from lz77 import LZ77Coder

class CombinedCompressor:
    """
    A class that combines LZ77 and Huffman encoding.
    """
    def __init__(self, window_size, lookahead_buffer_size):
        self.lz77_coder = LZ77Coder(window_size, lookahead_buffer_size)
        self.huffman_coder = HuffmanCoder()

    def compress(self, data):
        """
        Compresses data first with LZ77, then with Huffman.
        Returns a tuple: (huffman_encoded_data, huffman_tree)
        """
        # Step 1: LZ77 Encoding produces a list of (offset, length, next_char) tuples.
        lz77_tokens = self.lz77_coder.encode(data)
        
        # Step 2: Huffman Encoding
        encoded_data, huffman_tree = self.huffman_coder.encode(lz77_tokens)
        
        return encoded_data, huffman_tree

    def decompress(self, encoded_data, huffman_tree):
        """
        Decompresses data first with Huffman, then with LZ77.
        """
        # Step 1: Huffman Decoding
        # This returns the original list of LZ77 tokens.
        lz77_tokens = self.huffman_coder.decode(encoded_data, huffman_tree)

        # Step 2: LZ77 Decoding
        # The list of tokens is now passed directly to the LZ77 decoder.
        original_data = self.lz77_coder.decode(lz77_tokens)
        
        return original_data

def main_combined():
    """Main function for testing the CombinedCompressor."""
    text_to_compress = "the quick brown fox jumps over the lazy dog " * 50
    window_size = 50
    lookahead_buffer_size = 20

    combined_compressor = CombinedCompressor(window_size, lookahead_buffer_size)

    # 1. Compress
    print(f"Original Text (first 50 chars): '{text_to_compress[:50]}...'")
    compressed_data, huffman_tree = combined_compressor.compress(text_to_compress)
    print("Combined Compression successful.")

    # 2. Decompress
    decompressed_data = combined_compressor.decompress(compressed_data, huffman_tree)
    
    # print("Decompressed Data: \n", decompressed_data)
    # print("Text to compress: \n", text_to_compress)

    # 3. Verification
    assert text_to_compress == decompressed_data, "Decompression failed!"
    print("Combined Compression/Decompression works correctly! ✅")

    # 4. Compression analysis
    original_size_bits = len(text_to_compress) * 8
    compressed_size_bits = len(compressed_data)
    compression_rate = (1 - compressed_size_bits / original_size_bits) * 100

    print(f"\nOriginal Size (bits): {original_size_bits}")
    print(f"Combined Compressed Size (bits): {compressed_size_bits}")
    print(f"Combined Compression Rate: {compression_rate:.2f}%")

if __name__ == '__main__':
    main_combined()