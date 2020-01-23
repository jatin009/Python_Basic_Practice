from bs4 import BeautifulSoup

from parsers.story_parser import Story_Parser
from parsers.story_parser import Chrome_Story_Parser
from locators.story_locator import Story_Locator

class Story_Page:

    """
    Parses the story page using BeautifulSoup object
    """

    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    def get_stories_beginning_with(self, begins_with='A'):
        return [Story_Parser(e) for e in self.soup.select(Story_Locator.NAME+f'[href^={begins_with}]')]

    def get_all_stories(self):
        return [Story_Parser(e) for e in self.soup.select(Story_Locator.NAME)]


class Chrome_Story_Page:
    

    def __init__(self, browser):
        self.browser = browser

    def get_stories_beginning_with(self, begins_with='A'):
        return [Chrome_Story_Parser(e) for e in self.browser.find_elements_by_css_selector(Story_Locator.NAME+f'[href^={begins_with}]')]

    def get_all_stories(self):
        return [Chrome_Story_Parser(e) for e in self.browser.find_elements_by_css_selector(Story_Locator.NAME)]
