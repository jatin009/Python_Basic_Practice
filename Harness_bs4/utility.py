from tkinter import filedialog
from tkinter import *
import logging
import getpass


class FileDialog:
    """ A file dialog class to open a file """

    def __init__(self):
        self.root = Tk()
        # We do not want to display the tkinter window
        self.root.withdraw()
        logger.info('Tkinter window created and hidden')

    @staticmethod
    def read_html_page():
        filename = filedialog.askopenfilename(initialdir="C:/Users/" + getpass.getuser() + "/Desktop",
                                              title="Select file", filetypes=(("html files", "*.html"),))
        logger.debug('HTML file selected to open: ' + filename)

        try:
            with open(filename, "r") as reader:
                page = reader.read()
            logger.info('File read successfully')
        except Exception:
            logger.error('Unable to open the file')
        else:
            return page


def initialize_logger():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.DEBUG,
        filename='logs.txt'
    )


logger = logging.getLogger(__name__)
