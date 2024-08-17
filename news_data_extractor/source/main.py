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
            'apnews': {'text_search_url': 'https://apnews.com/search?q=', 'enabled': True, 'captcha': False},
            'aljazeera': {'text_search_url': 'https://www.aljazeera.com/search/', 'enabled': True, 'captcha': False},
            'reuters': {'text_search_url': 'https://www.reuters.com/site-search/?query=', 'enabled': False,
                        'captcha': True},
            'latimes': {'text_search_url': 'https://www.latimes.com/search?q=', 'enabled': False, 'captcha': True},
            'gothamist': {'text_search_url': 'https://gothamist.com/search?q=', 'enabled': True, 'captcha': False},
            'yahoo': {'text_search_url': 'https://news.search.yahoo.com/search;?p=', 'enabled': True, 'captcha': False},
        }
        if only_active:
            filtered_sources = {}
            for source in sources_config:
                if sources_config[source]['enabled']:
                    filtered_sources[source] = sources_config[source]
            return filtered_sources
        else:
            return sources_config

    def _search_news(self):
        for source in list(self.source_parameters.keys()):
            search_url = self.source_parameters[source]['text_search_url']
            search_text = self.search_parameters['text_phrase']
            # TODO: Add other filtering directly in search
            search_category = self.search_parameters['news_category']
            search_months = self.search_parameters['max_months']
            search_full_url = f"{search_url}{search_text}"
            try:
                # Headers for a typical HTTP request
                request_headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/115.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                }

                response = requests.get(search_full_url, headers=request_headers)
                response_status = response.status_code
                response_html = response.text

            except:
                response_status = 500
                response_html = None

            # TODO: Add elapsed time to request
            logging.info(f"[Request] {source} | {response_status}")
            self.source_parameters[source]['search_results'] = {'status_code': response_status,
                                                                'html': response_html}

    def extraction_manager(self):
        self.source_parameters = self._get_sources(only_active=True)
        logging.info(f'Obtained {len(list(self.source_parameters.keys()))} sources to process.')
        self._search_news()


if __name__ == '__main__':
    bot_class = NewsDataExtractor()
    bot_class.extraction_manager()
