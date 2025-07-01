import os
import tiktoken
import torch
from torch.utils.data import Dataset, DataLoader

# First Tokenizer with tiktoken
class SimpleTokenizer:
    def __init__(self, path="./Jattendrai.txt", model_name="gpt2"):
        self.encoding = tiktoken.get_encoding(model_name)
        self.token_ids = []

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            self.token_ids = self.encoding.encode(
                raw_text, allowed_special={"<|endoftext|>"}
            )

    def Encode(self, text):
        return self.encoding.encode(text, allowed_special={"<|endoftext|>"})

    def Decode(self, ids):
        return self.encoding.decode(ids)

    def ContextPairs(self, context_size=4):
        pairs = []
        for i in range(1, min(context_size + 1, len(self.token_ids))):
            context = self.token_ids[:i]
            target = self.token_ids[i]
            pairs.append((context, target))
        return pairs


# GPT tokenizer thing
class GPTDatasetV1(Dataset):
    def __init__(self, txt, tokenizer, max_length, stride):
        self.input_ids = []
        self.target_ids = []

        # Tokenize the entire text
        token_ids = tokenizer.encode(txt, allowed_special={"<|endoftext|>"})
        assert len(token_ids) > max_length, "Number of tokenized inputs must at least be equal to max_length+1"

        # Use a sliding window to chunk the book into overlapping sequences of max_length
        for i in range(0, len(token_ids) - max_length, stride):
            input_chunk = token_ids[i:i + max_length]
            target_chunk = token_ids[i + 1: i + max_length + 1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]



# Data loading helper function
def create_dataloader_v1(txt, batch_size=4, max_length=256, stride=128, shuffle=True, drop_last=True, num_workers=0):

    # Initialize the tokenizer
    tokenizer = tiktoken.get_encoding("gpt2")

    # Create dataset
    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)

    # Create dataloader
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,
        num_workers=num_workers
    )

    return dataloader


def main():
    path="./Jattendrai.txt"
    raw_text = ""

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            raw_text = f.read()

    dataloader = create_dataloader_v1(raw_text, batch_size=8, max_length=4, stride=4, shuffle=False)

    data_iter = iter(dataloader)
    inputs, targets = next(data_iter)
    print("Inputs:\n", inputs)
    print("\nTargets:\n", targets)


if __name__ == "__main__":
    main()
