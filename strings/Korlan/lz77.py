class LZ77Coder:
    """
    A class to perform LZ77 encoding and decoding.
    """
    def __init__(self, window_size, lookahead_buffer_size):
        self.window_size = window_size
        self.lookahead_buffer_size = lookahead_buffer_size

    def encode(self, data):
        """
        Encodes the input data using the LZ77 algorithm.
        Returns a list of (offset, length, next_char) tuples.
        """
        # TODO: Implement this method.
        # The encoding loop and sliding window logic go here.
        
        encoded_data = []
        window = ""
        pos = 0
        
        while pos < len(data):
            lookahead = data[pos:pos+self.lookahead_buffer_size]
            
            offset, length, char = self._find_longest_match(window, lookahead)
            
            encoded_data.append((offset, length, char))
            
            move = length + 1 if length > 0 else 1
            window += data[pos:pos+move]
            window = window[-self.window_size:]
            pos += move
        
        return encoded_data

    def decode(self, encoded_data):
        """
        Decodes the LZ77 encoded data.
        Returns the original string.
        """
        # TODO: Implement this method.
        # Reconstruct the string from the tokens.
        
        decoded = []
        window = ""
        
        for offset, length, char in encoded_data:
            if offset == 0 and length == 0: # No match, just add the character
                decoded.append(char)
                window += char
            else:   # Get the matched string from the window
                start = len(window) - offset
                matched_string = window[start:start+length]
                decoded.append(matched_string)
                decoded.append(char)
                window += matched_string + char
            
            window = window[-self.window_size:]
        
        return ''.join(decoded)
    
    def _find_longest_match(self, window, lookahead):
        """
        Finds the longest match of lookahead prefix in the window.
        Returns (offset, length, next_char) tuple.
        """
        best_offset = 0
        best_length = 0
        best_char = lookahead[0] if lookahead else ''
        
        # Try all possible match lengths from maximum down to 1
        for length in range(min(len(lookahead), self.lookahead_buffer_size), 0, -1):
            pattern = lookahead[:length]
            # Search backwards from the end of window 
            offset = window.rfind(pattern)
            
            if offset != -1:
                best_offset = len(window) - offset
                best_length = length
                best_char = lookahead[length] if length < len(lookahead) else ''
                break
        
        return (best_offset, best_length, best_char)
    

def main_lz77():
    """Main function for testing the LZ77Coder class."""
    text_to_compress = "aabacaadaaaba"
    window_size = 10
    lookahead_buffer_size = 5
    
    lz77_coder = LZ77Coder(window_size, lookahead_buffer_size)
    
    # Encoding and Decoding
    encoded_tokens = lz77_coder.encode(text_to_compress)
    decoded_text = lz77_coder.decode(encoded_tokens)

    # Verification
    assert text_to_compress == decoded_text, "Decoding failed!"
    print("LZ77 Encoding/Decoding works correctly! ✅")
    
    # Compression analysis (approximate)
    original_size = len(text_to_compress)
    compressed_size_approx = len(encoded_tokens) * 3  # For a rough character-based comparison
    compression_rate = (1 - compressed_size_approx / original_size) * 100
    
    print(f"\nOriginal Size (chars): {original_size}")
    print(f"Approx Compressed Size (chars): {compressed_size_approx}")
    print(f"Approx Compression Rate: {compression_rate:.2f}%")

if __name__ == '__main__':
    main_lz77()