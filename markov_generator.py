# markov_generator.py

import random
from collections import defaultdict

class MarkovWordGenerator:
    def __init__(self, markov_length=2, word_list=None):
        if word_list is None:
            word_list = []
        self.markov_length = markov_length
        self.word_list = word_list
        self.markov_chain = self.build_markov_chain(word_list)

    def build_markov_chain(self, word_list):
        markov_chain = defaultdict(list)
        for word in word_list:
            padded_word = f"{' ' * self.markov_length}{word}{' ' * self.markov_length}"
            for i in range(len(word) + self.markov_length):
                key = padded_word[i:i + self.markov_length]
                next_char = padded_word[i + self.markov_length]
                markov_chain[key].append(next_char)
        return markov_chain

    def generate_word(self, max_length=10):
        current_sequence = ' ' * self.markov_length
        generated_word = ''
        while len(generated_word) < max_length:
            next_chars = self.markov_chain.get(current_sequence, [])
            if not next_chars:
                break
            next_char = random.choice(next_chars)
            if next_char == ' ':
                break
            generated_word += next_char
            current_sequence = current_sequence[1:] + next_char
        return generated_word.strip()

    def word_exists(self, word):
        return word in self.word_list
