"""
Tools for Web API scripts
"""


def get_author_id(author_name, authors_list):
    """ Get author id from author author_name """
    # search author id of author_name
    for author in authors_list:
        if author_name == author.get("name"):
            filter_author_id = author.get("author_id")
            return filter_author_id


def get_books_from_author_id(author_id, books_list):
    """ Get books written by author author_id """
    result_books = list()
    for book in books_list:
        if author_id in book.get("authors"):
            result_books.append(book)
    return result_books


def get_book_from_title(book_title, books_list):
    """ Get book from book title """
    for book in books_list:
        if book_title == book.get("name"):
            return book
