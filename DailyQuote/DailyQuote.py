import requests
import random
from random import shuffle
from bs4 import BeautifulSoup

import tkinter as tk

page_id = random.randint(1, 10)

page = requests.get(f'http://quotes.toscrape.com/page/{page_id}/').content
soup = BeautifulSoup(page, 'html.parser')

all_quotes = soup.select('div.quote')
shuffle(all_quotes)

today_quote = all_quotes[0].select_one('span.text').string

root = tk.Tk()
root.title("Your Daily Quote")

tk.Label(root, text=today_quote, font=("Helvetica", 15), wraplength=700).pack()

root.mainloop()
