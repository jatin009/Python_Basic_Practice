import re
from locators.contents_locator import BooksContentsLocator

import logger


class BooksParser:

    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent):
        self.parent = parent
        self.log_inducer = logger.get_logger(__name__)

    def __repr__(self):
        return f'<Book {self.name}, {self.rating} star ({self.price})>'

    @property
    def price(self):
        locator = BooksContentsLocator.PRICE
        expression = "[0-9]*\.[0-9]*"
        matches = re.search(expression, self.parent.select_one(locator).string)
        self.log_inducer.debug("RegEx match for price: "+matches[0])
        return float(matches[0])

    @property
    def rating(self):
        locator = BooksContentsLocator.RATING
        rating_words = self.parent.select_one(locator).attrs['class'][1]
        self.log_inducer.debug("Ratings in words: " + rating_words)
        return BooksParser.RATINGS[rating_words]

    @property
    def name(self):
        locator = BooksContentsLocator.NAME
        book_name = self.parent.select_one(locator).attrs['title']
        self.log_inducer.debug("Ratings in words: " + book_name)
        return book_name
