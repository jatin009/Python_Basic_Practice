from bs4 import BeautifulSoup
from locators.books_locator import BooksLocator
from parsers.books_parser import BooksParser

import logger


class BooksPage:
    def __init__(self, page):
        self.log_inducer = logger.get_logger(__name__)
        self.soup = BeautifulSoup(page, 'html.parser')
        self.log_inducer.info("BeautifulSoup object initialized")

    def books_list(self):
        locator = BooksLocator.BOOKS
        books = self.soup.select(locator)
        self.log_inducer.debug("Books parsed with given locator: "+str(len(books)))
        # instantiating Books Parser on each book to find the contents
        return [BooksParser(e) for e in books]
