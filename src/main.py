import re

class TextTokenizer:
    def __init__(self, filepath):
        # Read the file
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Tokenize (split on punctuation and whitespace)
        tokens = re.split(r'([,.?_!"()\']|--|\s)', content)

        # Filter out empty or whitespace tokens
        self.tokens = [token for token in tokens if token.strip()]

        # Build vocabulary (sorted, unique)
        self.all_words = sorted(set(self.tokens))
        self.all_words.extend(["<|endofline|>", "<|unk|>"])

        # Create vocab maps: token -> ID and ID -> token
        self.vocab = {token: idx for idx, token in enumerate(self.all_words)}
        self.reverse_vocab = {idx: token for token, idx in self.vocab.items()}

    def encode(self, text):
        """Convert text to list of token IDs."""
        tokens = re.split(r'([,.?_!"()\']|--|\s)', text)
        tokens = [token for token in tokens if token.strip()]
        return [self.vocab[token] if token in self.vocab else "<|unk|>" for token in tokens]

    def decode(self, ids):
        tokens = [self.reverse_vocab[i] for i in ids if i in self.reverse_vocab]
        spaced_text = ''
        for i, token in enumerate(tokens):
            if token in ".,!?;:'\"()":
                spaced_text += token  # no space before punctuation
            elif i > 0 and tokens[i - 1] not in ".,!?;:'\"()":
                spaced_text += ' ' + token
            else:
                spaced_text += token
        return spaced_text

def main():
    tokenizer = TextTokenizer("Jattendrai.txt")

    # Encode a line
    input_text = "I will like for flowers. <|endoftext|> In the great garden of love"
    encoded = tokenizer.encode(input_text)
    print("Original Text: ", input_text)
    print("Encoded IDs:   ", encoded)

    # Decode back
    decoded = tokenizer.decode(encoded)
    print("Decoded Text:  ", decoded)

if __name__ == "__main__":
    main()
