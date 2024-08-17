import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[logging.FileHandler("my_log.log", mode='w'),
                              logging.StreamHandler()])


class NewsDataExtractor:
    def __init__(self, search_parameters: dict = None):
        if search_parameters is None:
            search_parameters = {'text_phrase': "Cure to cancer", 'news_category': str, 'max_months': int}
        self.search_parameters = search_parameters
        self.source_parameters = {}

    def _get_sources(self, only_active=False):
        sources_config = {
            'apnews': {'search_url': 'https://apnews.com/search?q=', 'enabled': True, 'captcha': False},
            'aljazeera': {'search_url': 'https://www.aljazeera.com/search/', 'enabled': True, 'captcha': False},
            'reuters': {'search_url': 'https://www.reuters.com/site-search/?query=', 'enabled': False, 'captcha': True},
            'latimes': {'search_url': 'https://www.latimes.com/search?q=', 'enabled': False, 'captcha': True},
            'gothamist': {'search_url': 'https://gothamist.com/search?q=', 'enabled': True, 'captcha': False},
            'yahoo': {'search_url': 'https://news.search.yahoo.com/search;?p=', 'enabled': True, 'captcha': False},
        }
        if only_active:
            filtered_sources = {}
            for source in sources_config:
                if sources_config[source]['enabled']:
                    filtered_sources[source] = sources_config[source]
            return filtered_sources
        else:
            return sources_config

    def _initialize_requests(self):
        for source in list(self.source_parameters.keys()):
            search_url = self.source_parameters[source]['search_url']
            search_text = self.search_parameters['text_phrase']
            search_category = self.search_parameters['news_category']
            search_months = self.search_parameters['max_months']

    def extraction_manager(self):
        self.source_parameters = self._get_sources(only_active=True)
        logging.info(f'Obtained {len(list(self.source_parameters.keys()))} sources to process.')


if __name__ == '__main__':
    bot_class = NewsDataExtractor()
    bot_class.extraction_manager()
