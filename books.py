"""
books.py script
Generate books.json file with books and authors
"""

import json
import random
import sys
from slugify import slugify


def main():
    """ Main entry point """

    print("BEGIN")

    # Generate random number for books and authors
    books_number_limit = 100
    books_number = random.randint(1, books_number_limit)  # (between 1 and 100)
    authors_number_limit = 75
    authors_number = random.randint(1, authors_number_limit)  # (between 1 and 75)

    # Create lists to fill with books and authors
    books = list()
    authors = list()

    # Create authors and fill the list
    for j in range(0, authors_number):
        author = dict()
        author["author_id"] = "author-{}".format(j)
        author["name"] = "Author Name {}".format(j)
        author["slug"] = slugify(author.get("name"))
        authors.append(author)

    # Create books and fill the list
    for i in range(0, books_number):
        book = dict()
        book["book_id"] = "book-{}".format(i)
        book["name"] = "Book Name number {}".format(i)
        book["slug"] = slugify(book.get("name"))
        # writers is the list of authors ids for each book
        writers = list()
        random_int_list = random.sample(range(authors_number), random.randint(1, 3))  # 3 authors maximum per book
        for n in random_int_list:
            random_author_id = authors[n].get("author_id")
            writers.append(random_author_id)
        book["authors"] = writers
        books.append(book)

    # Create a dictionnary to store books and authors
    result_dict = {"books": books,
                   "authors": authors}

    # Fill json file
    with open("books.json", 'w') as books_file:
        json.dump(result_dict, books_file)

    print("END")


if __name__ == "__main__":
    sys.exit(main())
