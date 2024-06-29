import markovify
import msgpack
import re
import sys

def load_markov_chain(file):
    with open(file, 'rb') as f:
        model_dict = msgpack.unpackb(f.read())
        return markovify.Text.from_dict(model_dict)

def generate_random_author(model):
    while True:
        random_output = model.make_short_sentence(max_chars=150)  # Adjust max_chars for varying sentence lengths
        if random_output:
            potential_names = re.findall(r'\b[A-Z][a-z]* [A-Z][a-z]*\b', random_output)
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
    model_file = 'authors_markov_chain.msgpack'
    author_model = load_markov_chain(model_file)
    random_author = generate_random_author(author_model)
    
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"Generated Author Name: {random_author}")

if __name__ == '__main__':
    main()
