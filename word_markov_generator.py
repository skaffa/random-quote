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
