import pandas as pd
import markovify
import msgpack
from tqdm import tqdm

def generate_markov_chain(texts, output_file):
    text_model = markovify.Text(texts, state_size=2)
    serialized_model = text_model.to_dict()
    with open(output_file, 'wb') as f:
        f.write(msgpack.packb(serialized_model))

def process_csv(csv_file):
    chunk_size = 100000
    quotes = []

    for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunk_size), desc="Reading CSV in chunks"):
        chunk['quote'] = chunk['quote'].astype(str).fillna('').str.strip('"')
        quotes.extend(chunk['quote'].tolist())
    
    return quotes

def main():
    csv_file = 'quotes.csv'
    quotes = process_csv(csv_file)
    
    # Generate Markov chain for quotes
    generate_markov_chain(quotes, 'quotes_markov_chain.msgpack')

if __name__ == '__main__':
    main()
