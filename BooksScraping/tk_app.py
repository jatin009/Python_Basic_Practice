import tkinter
from app import requests, BooksPage

idx_page = 0


def go_to_page(is_next=True):
    global idx_page
    idx_page = idx_page+1 if is_next else idx_page-1

    books_str = "############## Page "+str(idx_page)+" ###############\n"
    page_content = requests.get('http://books.toscrape.com/catalogue/page-' + str(idx_page) + '.html').content
    page = BooksPage(page_content)
    for b in page.books_list():
        books_str += repr(b) + "\n"
    output_.delete(1.0, tkinter.END)
    output_.insert(tkinter.END, books_str)


def sort_(comp):
    books_str = "############## Page "+str(idx_page)+" ###############\n"

    page_content = requests.get('http://books.toscrape.com/catalogue/page-' + str(idx_page) + '.html').content
    page = BooksPage(page_content)
    books = sorted(page.books_list(), key=lambda x: x.rating if comp.lower() == 'rating' else x.price)
    for b in books:
        books_str += repr(b) + "\n"
    output_.delete(1.0, tkinter.END)
    output_.insert(tkinter.END, books_str)


window = tkinter.Tk()
window.title("Books Scraping")
window.geometry("1000x700")

# Row 1 elements
tkinter.Button(window, text='Rating', fg='black', bg='lightgrey', command=lambda: sort_('rating')).grid(column=0, row=0)
tkinter.Button(window, text='Price', fg='black', bg='lightgrey', command=lambda: sort_('price')).grid(column=1, row=0)

# Row 2 Text element
output_ = tkinter.Text(window, height=30, width=120)
output_.grid(columnspan=2)

# Row 3 next-prev buttons
prev_btn = tkinter.Button(window, text='Prev Page', fg='black', bg='lightgrey', command=lambda: go_to_page(is_next=False)).grid(column=0, row=2)
next_btn = tkinter.Button(window, text='Next Page', fg='black', bg='lightgrey', command=lambda: go_to_page(is_next=True)).grid(column=1, row=2)

window.mainloop()
