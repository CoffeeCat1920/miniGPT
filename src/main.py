import os
import re


class SimpleTokenizer:

def Preprocessor(path = "./Jattendrai.txt"): 
    if os.path.exists(path):
        with open(path) as f:
            raw_text = f.read()
        data = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
        result = [item for item in data if item.split()]
        return result
    else:
        return []

def Tokenizer(preprocessed = []):
    words = sorted(set(preprocessed)) 
    vocab = {token:integer for integer, token in enumerate(words)}
    return vocab

def main():
    Tokenizer(Preprocessor())

if __name__ == "__main__":
    main()
