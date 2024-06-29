import csv
import pickle

def serialize_data(quotes, authors):
    with open('quotes.pkl', 'wb') as quotes_file:
        pickle.dump(quotes, quotes_file)

    with open('authors.pkl', 'wb') as authors_file:
        pickle.dump(authors, authors_file)

def main():
    quotes = []
    authors = set()

    with open('your_quotes_dataset.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quote = row['quote']
            author = row['author']
            category = row['category']

            # Add quote to the list
            quotes.append({'quote': quote, 'category': category})

            # Add author to the set (to avoid duplicates)
            authors.add(author)

    # Convert the set of authors to a list
    authors_list = list(authors)

    # Serialize the data to files
    serialize_data(quotes, authors_list)

if __name__ == "__main__":
    main()
