import csv
import pickle
from tqdm import tqdm

def serialize_data(quotes, authors):
    with open('quotes.pkl', 'wb') as quotes_file:
        pickle.dump(quotes, quotes_file)

    with open('authors.pkl', 'wb') as authors_file:
        pickle.dump(authors, authors_file)

def main():
    quotes = []
    authors = set()

    with open('quotes.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        total_rows = sum(1 for row in reader)
        csvfile.seek(0)  # Reset file pointer for iteration
        progress_bar = tqdm(total=total_rows, desc="Processing", unit="row")

        for row in reader:
            quote = row['quote']
            author = row['author']
            category = row['category']

            # Add quote to the list
            quotes.append({'quote': quote, 'category': category})

            # Add author to the set (to avoid duplicates)
            authors.add(author)

            # Update the progress bar
            progress_bar.update(1)

        progress_bar.close()

    # Convert the set of authors to a list
    authors_list = list(authors)

    # Serialize the data to files
    serialize_data(quotes, authors_list)

if __name__ == "__main__":
    main()
