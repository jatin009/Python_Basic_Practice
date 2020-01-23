import requests
# import string

from pages.story_page import Story_Page

# getting html content of the stories by Upanyas Samrat Munshi Das Premchand ji
page = requests.get('http://www.hindikahani.hindi-kavita.com/HK-MunshiPremchand.php')
story_page = Story_Page(page.content)

# printing example stories for user starting with 'A'
for story in story_page.get_stories_beginning_with():
    print (story)

# gen = ( x for x in string.ascii_lowercase )

begins_with = input("Enter the character/string your story starts with, default is 'A', 'X' to print all stories, else 'q' to quit: ").title()
while begins_with != 'q':

    if begins_with == 'X':
        for story in story_page.get_all_stories():
            print (story)
    else:
        for story in story_page.get_stories_beginning_with(begins_with):
            print (story)

    begins_with = input("Enter the character/string your story starts with, default is 'A', 'X' to print all stories, else 'q' to quit: ").title()
