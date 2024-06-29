import msgpack
import csv

def serialize_data_msgpack(quotes, authors):
    with open("quotes.msgpack", "wb") as quotes_file:
        packed_quotes = msgpack.packb(quotes, use_bin_type=True)
        quotes_file.write(packed_quotes)

    with open("authors.msgpack", "wb") as authors_file:
        packed_authors = msgpack.packb(authors, use_bin_type=True)
        authors_file.write(packed_authors)

def load_data_msgpack():
    with open("quotes.msgpack", "rb") as quotes_file:
        packed_quotes = quotes_file.read()
        quotes = msgpack.unpackb(packed_quotes, raw=False, use_list=False)

    with open("authors.msgpack", "rb") as authors_file:
        packed_authors = authors_file.read()
        authors = msgpack.unpackb(packed_authors, raw=False, use_list=False)

    return quotes, authors

def main():
    quotes = []
    authors = set()

    with open('quotes.csv', newline='', encoding='utf-8') as csvfile:
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

    # Serialize the data to files using MessagePack
    serialize_data_msgpack(quotes, authors_list)

if __name__ == "__main__":
    main()
