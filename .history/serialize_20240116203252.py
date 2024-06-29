import os
import pickle
import csv
from tqdm import tqdm  # Import tqdm for the progress bar

def serialize_data_pickle(quotes, authors, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Create a progress bar for the quotes
    with tqdm(total=len(quotes), desc="Serializing Quotes") as pbar:
        for category in set(quote['category'] for quote in quotes):
            category_quotes = [quote for quote in quotes if category in quote['category']]
            
            category_path = os.path.join(output_folder, f"{category}.pkl")
            with open(category_path, "wb") as category_file:
                pickle.dump(category_quotes, category_file)

            pbar.update(len(category_quotes))

    # Serialize authors
    authors_path = os.path.join(output_folder, "authors.pkl")
    with open(authors_path, "wb") as authors_file:
        pickle.dump(authors, authors_file)

def load_category_data_pickle(output_folder, category):
    category_path = os.path.join(output_folder, f"{category}.pkl")
    with open(category_path, "rb") as category_file:
        data = pickle.load(category_file)
    return data

def load_authors_pickle(output_folder):
    authors_path = os.path.join(output_folder, "authors.pkl")
    with open(authors_path, "rb") as authors_file:
        authors_data = pickle.load(authors_file)
    return authors_data

def main():
    quotes = []
    authors = set()

    with open('quotes.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quote = row['quote']
            author = row['author']
            category = [c.strip() for c in row['category'].split(',')]

            # Add quote to the list
            quotes.append({'quote': quote, 'category': category})

            # Add author to the set (to avoid duplicates)
            authors.add(author)

    # Convert the set of authors to a list
    authors_list = list(authors)

    # Serialize the data to separate files for each category and authors using pickle
    serialize_data_pickle(quotes, authors_list, "output_folder")

if __name__ == "__main__":
    main()
