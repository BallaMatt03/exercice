"""
Scraping script
Get books from web page https://www.babelio.com/decouvrir.php
(approximately 45 books)
"""

import sys
import json
import uuid
import urllib.request
import lxml.html
from slugify import slugify

URL = 'https://www.babelio.com/decouvrir.php'
AUTHORS_LIST = list()
BOOKS_LIST = list()


def get_author_id(author_name):
    """ Get author id from author author_name in AUTHORS_LIST list """
    for author in AUTHORS_LIST:
        if author_name == author.get("name"):
            author_id = author.get("author_id")
            return author_id


def main():
    """ Main entry point """

    print("BEGIN")

    books_dict = dict()

    # Get data from HTML response
    response = urllib.request.urlopen(URL)
    html = response.read()
    html_element = lxml.html.document_fromstring(html)
    # list_livre_con div class contains books
    div_elements_list_livre = html_element.xpath('//div[@class="list_livre_con"]')
    for div_list_livre in div_elements_list_livre:
        for div_livre in div_list_livre.getchildren():
            book = div_livre.getchildren()
            # we consider there is multiple authors per book on the web page
            # so we are using list for authors
            # (even if this is false when we are testing on babelio.com)
            authors_list = list()
            authors_list.append(book[1].getchildren()[0].text)  # author name (multiple names)
            title = book[0].getchildren()[1].text  # book title
            books_dict[title] = authors_list

    my_books_list = list(set(books_dict.keys()))  # remove duplicate books if needed

    # Create authors and books lists (like in books.py)
    for my_book in my_books_list:
        book_title = my_book  # my_book is book title

        # Initialize writers (authors list of the current book)
        writers = list()

        # Add authors for the book
        for author_name in books_dict[book_title]:

            # Author already registered in AUTHORS_LIST ?
            author_id = get_author_id(author_name)
            if author_id:
                # Yes, author already exists
                writers.append(author_id)
            else:
                # No, new author
                # Create author and add it to AUTHORS_LIST
                author = dict()
                author["name"] = author_name
                author["slug"] = slugify(author.get("name"))

                # Create author id
                author["author_id"] = "{}-{}".format(author.get("slug"), str(uuid.uuid4()))
                AUTHORS_LIST.append(author)

                # Add author_id to the list of book's authors
                writers.append(author.get("author_id"))

        # Create book and add it to BOOKS_LIST
        book = dict()
        book["name"] = book_title
        book["slug"] = slugify(book.get("name"))

        # Create book id
        book["book_id"] = "{}-{}".format(book.get("slug"), str(uuid.uuid4()))

        # Add writers to book's authors
        book["authors"] = writers
        BOOKS_LIST.append(book)

    # Create a dictionnary to store books and authors
    result_dict = {"books": BOOKS_LIST,
                   "authors": AUTHORS_LIST}

    # Fill json file
    with open("books.json", 'w') as books_file:
        json.dump(result_dict, books_file)

    print("END")


if __name__ == '__main__':
    sys.exit(main())
