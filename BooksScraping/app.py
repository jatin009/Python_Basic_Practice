import requests

from pages.books_page import BooksPage
from menu import menu

import logger

log_inducer = logger.get_logger(__name__)
log_inducer.info("Ready to read website content")

content = requests.get('http://books.toscrape.com/').content
page = BooksPage(content)


def main_menu():
    option = input("Enter 'a' for page-1 content, 'b' for all pages, 'q' to quit: ").strip().lower()

    idx = 2
    while option != 'q':

        if option == 'a':
            menu(page.books_list(), log_inducer)

        elif option == 'b':
            if idx <= 50:
                page_content = requests.get('http://books.toscrape.com/catalogue/page-' + str(idx) + '.html').content
                current_page = BooksPage(page_content)
                for b in current_page.books_list():
                    print(b)
                idx += 1

        else:
            print("Enter valid option.")

        option = input("Enter 'a' for page-1 content, 'b' for all pages, 'q' to quit: ").strip().lower()


# main_menu()
