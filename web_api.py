"""
JSON Web API
  /books : get books with their authors
  /books?author=Author Name : filter books by author name
  /books?title=Book Title : filter books by book title
  /authors : get authors with books they written
"""

import json
import sys
from flask import Flask, request, jsonify
from tools import get_author_id, get_books_from_author_id, get_book_from_title
app = Flask(__name__)

# Get data from json file
try:
    with open("books.json") as f:
        data = json.load(f)
except FileNotFoundError as err:
    print("books.json not found")
    print("{}".format(err))
    sys.exit(1)
AUTHORS_LIST = data.get("authors")
BOOKS_LIST = data.get("books")


@app.route("/books")
def books():
    """ Endpoint /books """
    # Get URL parameters
    book_title = request.args.get("title")
    author_name = request.args.get("author")

    # If all parameters are there, we choose to print warning message
    if book_title and author_name:
        return "Cannot filter by author and book title together"

    # Create HTML
    if not book_title and not author_name:
        # Default return : all books
        resp = BOOKS_LIST
    elif book_title and not author_name:
        # return book for a given book title
        book = get_book_from_title(book_title, BOOKS_LIST)
        resp = book
    else:
        # return for a given author name
        # Search author id of author author_name
        filter_author_id = get_author_id(author_name, AUTHORS_LIST)
        resp = get_books_from_author_id(filter_author_id, BOOKS_LIST)

    return jsonify(resp)


@app.route("/authors")
def authors():
    """ Endpoint /authors """
    # return all authors with books they written
    resp = list()
    for author in AUTHORS_LIST:
        # Get written books by author
        books_author_list = get_books_from_author_id(author.get("author_id"), BOOKS_LIST)
        author['books'] = books_author_list
        resp.append(author)
    return jsonify(resp)


@app.route("/")
def main():
    """ main entry point / """
    return "<a href='/books'>Books</a><br/><a href='/authors'>Authors</a>"
