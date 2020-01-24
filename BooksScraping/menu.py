
USER_CHOICE = """
- 'b' to look 5-star books
- 'c' to look at the cheapest books
- 'n' to just get the next available book on the catalogue
- 'r' to print price range
- 'q' to exit
"""


def get_books_generator(all_books):
    return (x for x in all_books)


def menu(all_books, log_inducer):

    option = input(USER_CHOICE).strip().lower()
    books_generator = get_books_generator(all_books)

    while option != 'q':

        books_list = []

        log_inducer.info(f"Choice {option} entered")

        if option == 'b':
            books_list = [b for b in all_books if b.rating == 5]

        elif option == 'c':
            books_list = sorted(all_books, key=lambda b: b.price)[:5]

        elif option == 'r':
            min_price = min([b.price for b in all_books])
            max_price = max([b.price for b in all_books])
            print(f"Price range is {min_price}-{max_price}")

        elif option == 'n':
            print(next(books_generator))

        else:
            print("Please enter valid option.")

        for book in books_list:
            print(book)

        option = input(USER_CHOICE).strip().lower()
