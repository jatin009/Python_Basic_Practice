from locators.story_locator import Story_Locator

class Story_Parser:

    """
    For parsing each story tag to retrieve the name and link of each story
    """

    def __init__(self, parent):
        self.parent = parent

    @property
    def story_name(self):
        return self.parent.string

    @property
    def story_link(self):
        return self.parent.attrs.get(Story_Locator.LINK_ATTRIBUTE) #href
    
    def __repr__(self):
        return f'<Story {self.story_name}, {self.story_link}>'


class Chrome_Story_Parser:

    def __init__(self, parent):
        self.parent = parent

    @property
    def story_name(self):
        return self.parent.text

    @property
    def story_link(self):
        return self.parent.attrs.get(Story_Locator.LINK_ATTRIBUTE) #href
    
    def __repr__(self):
        return f'<Story {self.story_name}>'
