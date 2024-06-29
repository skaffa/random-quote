import pandas as pd
import msgpack
import markovify
from tqdm import tqdm

def process_csv(csv_file):
    chunk_size = 100000
    authors = []

    for chunk in tqdm(pd.read_csv(csv_file, chunksize=chunk_size), desc="Reading CSV in chunks"):
        chunk['author'] = chunk['author'].astype(str).fillna('')
        authors.extend(chunk['author'].tolist())
    
    return authors

def generate_word_model(authors, output_file):
    text = ' '.join(authors)
    model = markovify.Text(text, state_size=2)
    model_dict = model.to_dict()
    with open(output_file, 'wb') as f:
        msgpack.pack(model_dict, f)

def main():
    csv_file = 'quotes.csv'
    authors = process_csv(csv_file)
    
    # Generate and save Markov chain model for authors
    generate_word_model(authors, 'authors_markov_chain.msgpack')

if __name__ == '__main__':
    main()
