import pandas as pd
import msgpack
import re
import sys
from collections import defaultdict
import random
from dataclasses import dataclass, field

DELIMITER_END = '$'

def each_cons(xs, n):
    return [xs[i:i + n] for i in range(len(xs) - n + 1)]

def normalize_hash(h):
    weights = {}
    total = sum(h.values())
    s = 0
    for c in sorted(h, key=h.get, reverse=True):
        s += h[c]
        weights[c] = float(s) / total
    return weights

@dataclass
class MarkovWordGenerator:
    markov_length: int
    custom_words: list = field(default_factory=list)
    ignore_accents: bool = False
    mapping_chars: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.mapping_chars:
            self.mapping_chars = defaultdict(int)
            for word in self.custom_words:
                word = '^' + word.lower().replace('\n', DELIMITER_END).replace('.', '')
                for combination in each_cons(word, self.markov_length + 1):
                    self.mapping_chars[combination] += 1

    def select_next_chars(self, previous_chars):
        remainings = self.markov_length + 1 - len(previous_chars)
        choices = {s: self.mapping_chars[s] for s in self.mapping_chars if s.startswith(previous_chars)}
        wp = normalize_hash(choices)
        u = random.uniform(0, 1)
        for s in wp:
            if wp[s] >= u:
                return s[-remainings:]
        return DELIMITER_END

    def generate(self, seed=''):
        c = self.select_next_chars(previous_chars='^' + seed)
        if c == DELIMITER_END:
            return seed
        word = seed + c
        c = self.select_next_chars(previous_chars=word[-self.markov_length:])
        while c != DELIMITER_END:
            word += c
            c = self.select_next_chars(previous_chars=word[-self.markov_length:])
        if word[-1] == DELIMITER_END:
            word = word[:-1]
        return word

def process_csv(csv_file):
    chunk_size = 100000
    authors = set()  # Use a set to automatically remove duplicates

    for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
        chunk['author'] = chunk['author'].astype(str).fillna('')
        authors.update(chunk['author'].tolist())

    return list(authors)

def generate_word_model(words, markov_length, output_file):
    generator = MarkovWordGenerator(markov_length, custom_words=words)
    serialized_model = generator.mapping_chars
    with open(output_file, 'wb') as f:
        msgpack.pack(serialized_model, f)

def load_markov_chain(file, markov_length):
    with open(file, 'rb') as f:
        model_dict = msgpack.unpackb(f.read())
        return MarkovWordGenerator(markov_length, mapping_chars=model_dict)

def generate_random_author(model):
    while True:
        generated_name = model.generate()
        potential_names = re.findall(r'\b[A-Z][a-z]{3,9} [A-Z][a-z]{3,9}\b', generated_name.title())
        if potential_names:
            for name in potential_names:
                if is_valid_author_name(name):
                    return name

def is_valid_author_name(name):
    parts = name.split()
    if len(parts) != 2:
        return False
    for part in parts:
        if not (4 <= len(part) <= 9 and part[0].isupper()):
            return False
    return True

def main():
    csv_file = 'quotes.csv'
    authors = process_csv(csv_file)
    
    # Generate Markov chain for authors after removing duplicates
    generate_word_model(authors, 2, 'authors_markov_chain.msgpack')

    author_model = load_markov_chain('authors_markov_chain.msgpack', 2)
    random_author = generate_random_author(author_model)
    
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"Generated Author Name: {random_author}")

if __name__ == '__main__':
    main()
