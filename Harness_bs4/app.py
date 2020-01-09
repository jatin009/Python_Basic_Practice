from bs4 import BeautifulSoup
from utility import *


class ParsedGameWiseRTP:
    """ A class to take in an HTML analytics page and parse it to find the feature specific RTP """

    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')
        logger.info('Soup object successfully created')

        self.write_str = ""

    def variation(self):
        var_td = [td for td in self.soup.table.find_all('td') if 'Variation ' in td.string]
        if len(var_td):
            self.write_str += var_td[0].string + "\n"

        logger.info('Variation parsed successfully')

    def bet_value(self):
        bet_td = [td for td in self.soup.table.find_all('td') if 'Bet' in td.string]
        self.write_str += "Bet " + bet_td[0].find_next('td').string + "\n"

    def game_wise_rtp(self):
        feature_name_tags = [feature_tag for feature_tag in self.soup.find_all('h2') if 'RTPP' in feature_tag.string]

        logger.debug('Feature wise tables: ' + str(len(feature_name_tags)))

        for feature_tag in feature_name_tags:
            rtp_table = feature_tag.find_next('table')

            for row in rtp_table.find_all('tr'):
                next_to_rtp_tags = [td for td in row.find_all('td') if 'RTPP(%)' in td.string]

            for tag in next_to_rtp_tags:
                rtp_tag = tag.find_next('td')
                self.write_str += feature_tag.string.strip() + "," + rtp_tag.string + "\n"

        logger.info('RTP parsing successfully done')

    def create_harness_summary(self):
        self.variation()
        self.bet_value()
        self.game_wise_rtp()

        try:
            with open("C:/Users/" + getpass.getuser() + "/Desktop/HarnessSummary.csv", 'a') as writer:
                writer.write(self.write_str)
            logger.info('Harness data successfully written to file.')
        except Exception:
            logger.error('Unable to open the HarnessSummary.csv file.')


initialize_logger()
logger = logging.getLogger(__name__)

file_dialog = FileDialog()
game_wise_rtp = ParsedGameWiseRTP(file_dialog.read_html_page())

game_wise_rtp.create_harness_summary()
