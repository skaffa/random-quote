import os
import pickle
import csv
import re  # Import re for regular expressions
from tqdm import tqdm

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def serialize_data_pickle(quotes, authors, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Create a progress bar for the quotes
    with tqdm(total=len(quotes), desc="Serializing Quotes") as pbar:
        # Create a dictionary to store quotes for each tag
        tag_quotes = {}

        for quote in quotes:
            for tag in quote['category']:
                tag = sanitize_filename(tag)  # Sanitize the tag name
                tag_quotes.setdefault(tag, []).append(quote)

            pbar.update(1)

        # Serialize quotes for each tag
        for tag, tag_quote_list in tag_quotes.items():
            tag_path = os.path.join(output_folder, f"{tag}.pkl")
            with open(tag_path, "wb") as tag_file:
                pickle.dump(tag_quote_list, tag_file)

    # Serialize authors
    authors_path = os.path.join(output_folder, "authors.pkl")
    with open(authors_path, "wb") as authors_file:
        pickle.dump(authors, authors_file)

def main():
    quotes = []
    authors = set()

    with open('quotes.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quote = row['quote']
            author = row['author']
            categories = [c.strip() for c in row['category'].split(',')]

            # Add quote to the list
            quotes.append({'quote': quote, 'category': categories})

            # Add author to the set (to avoid duplicates)
            authors.add(author)

    # Convert the set of authors to a list
    authors_list = list(authors)

    # Serialize the data to separate files for each tag and authors using pickle
    serialize_data_pickle(quotes, authors_list, "output_folder")

if __name__ == "__main__":
    main()
