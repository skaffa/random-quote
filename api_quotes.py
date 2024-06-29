import markovify
import msgpack

def load_markov_chain(file):
    with open(file, 'rb') as f:
        model_dict = msgpack.unpackb(f.read())
        return markovify.Text.from_dict(model_dict)

def generate_random_quote(model):
    random_quote = model.make_sentence()
    if not random_quote:
        return "Could not generate a quote at this time."
    return random_quote

def main():
    model_file = 'quotes_markov_chain.msgpack'
    quotes_model = load_markov_chain(model_file)
    random_quote = generate_random_quote(quotes_model)
    print(f"Random Quote: {random_quote}")

if __name__ == '__main__':
    main()
