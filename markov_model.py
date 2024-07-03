import random
from collections import defaultdict, OrderedDict
from dataclasses import dataclass, field
import msgpack
import re

DELIMITER_END = '$'

def each_cons(xs, n):
    return [xs[i:i + n] for i in range(len(xs) - n + 1)]

def normalize_hash(h):
    weights = OrderedDict()
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
    normalized_mapping_chars: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        if not self.mapping_chars:
            self.mapping_chars = defaultdict(int)
            for word in self.custom_words:
                word = '^' + word.lower().replace('\n', DELIMITER_END).replace('.', '')
                for combination in each_cons(word, self.markov_length + 1):
                    self.mapping_chars[combination] += 1
        self.normalized_mapping_chars = {
            prefix: normalize_hash({k: v for k, v in self.mapping_chars.items() if k.startswith(prefix)})
            for prefix in {k[:self.markov_length] for k in self.mapping_chars}
        }

    def select_next_chars(self, previous_chars):
        remainings = self.markov_length + 1 - len(previous_chars)
        choices = self.normalized_mapping_chars.get(previous_chars, {})
        u = random.uniform(0, 1)
        for s in choices:
            if choices[s] >= u:
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
