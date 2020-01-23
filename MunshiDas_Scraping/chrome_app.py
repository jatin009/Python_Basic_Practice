from selenium import webdriver

from pages.story_page import Chrome_Story_Page

chrome = webdriver.Chrome(executable_path='C:\chromedriver_win32\chromedriver.exe')
chrome.get('http://www.hindikahani.hindi-kavita.com/HK-MunshiPremchand.php')

story_page = Chrome_Story_Page(chrome)

for story in story_page.get_stories_beginning_with():
    print(story)
