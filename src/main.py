import os
import re

class SimpleTokenizer:
    def __init__(self, path = "./Jattendrai.txt"):
        if os.path.exists(path):
            with open(path) as f:
                raw_text = f.read()
            data = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
            preprocessed = [item for item in data if item.split()]
            words = sorted(set(preprocessed)) 
            words.extend(["<|endoftext|>", "<|unk|>"])
            self.str_to_int = {token:integer for integer, token in enumerate(words)}
            self.int_to_str = {i:s for s,i in self.str_to_int.items()}

    def Encode(self, text):
        tokens = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        tokens = [token.strip() for token in tokens if token.strip()]
        tokens = [
            item if item in self.str_to_int else "<|unk|>" for item in tokens
        ]
        
        ids = [self.str_to_int[token] for token in tokens ]
        return ids

    def Decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
        return text


def main():
    tokenizer = SimpleTokenizer() 
    encoded = tokenizer.Encode("And takopi I will wait for your return")
    print(encoded)
    decoded = tokenizer.Decode(encoded)
    print(decoded)

if __name__ == "__main__":
    main()
