import time

import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[logging.FileHandler("my_log.log", mode='w'),
                              logging.StreamHandler()])


class NewsDataExtractor:
    def __init__(self, search_parameters: dict = None):
        if search_parameters is None:
            search_parameters = {'text_phrase': "Olympic Paris", 'news_category': str, 'max_months': int}
        self.search_parameters = search_parameters
        self.source_parameters = {}

    def _get_sources(self, only_active=False):
        sources_config = {
            'apnews': {'text_search_url': 'https://apnews.com/search?q=', 'domain': 'https://apnews.com',
                       'enabled': True, 'captcha': False,
                       'listing_steps': [{'type': 'div', 'loc': {'class': 'PageList-items-item'}}], },

            'aljazeera': {'text_search_url': 'https://www.aljazeera.com/search/', 'domain': 'https://www.aljazeera.com',
                          'enabled': True, 'captcha': False,
                          'listing_steps': [{'type': 'article', 'loc': {
                              'class': 'gc u-clickable-card gc--type-customsearch#result gc--list gc--with-image'}}], },

            'reuters': {'text_search_url': 'https://www.reuters.com/site-search/?query=',
                        'domain': 'https://www.reuters.com', 'enabled': False,
                        'captcha': True},

            'latimes': {'text_search_url': 'https://www.latimes.com/search?q=', 'domain': 'https://www.latimes.com',
                        'enabled': False, 'captcha': True},

            'gothamist': {'text_search_url': 'https://gothamist.com/search?q=', 'domain': 'https://gothamist.com',
                          'enabled': True, 'captcha': False,
                          'listing_steps': [
                              {'type': 'div', 'loc': {'class': 'v-card gothamist-card mod-horizontal'}}], },

            'yahoo': {'text_search_url': 'https://news.search.yahoo.com/search;?p=',
                      'domain': 'https://news.search.yahoo.com', 'enabled': True, 'captcha': False,
                      'listing_steps': [{'type': 'div', 'loc': {'class': 'dd NewsArticle'}}], },
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
                response = requests.get(search_full_url)
                response_status = response.status_code
                response_html = response.text

            except:
                response_status = 500
                response_html = None

            # TODO: Add elapsed time to request
            logging.info(f"[Request] {source} | {response_status}")
            self.source_parameters[source]['search_results'] = {'status_code': response_status,
                                                                'html': response_html}

    def _get_news_listing(self):
        for source in list(self.source_parameters.keys()):
            search_status = self.source_parameters[source]['search_results']['status_code']
            search_html = self.source_parameters[source]['search_results']['html']
            news_url_found = []
            if search_status == 200:
                # TODO: Add tolerance to accept not only class
                listing_object_class_name = self.source_parameters[source]['listing_steps'][0]['loc']['class']
                listing_object_type = self.source_parameters[source]['listing_steps'][0]['type']
                listing_object_properties = self.source_parameters[source]['listing_steps'][0]['loc']
                source_domain = self.source_parameters[source]['domain']
                soup = BeautifulSoup(search_html, 'html.parser')
                elements = soup.find_all(class_=lambda x: x and x.startswith(listing_object_class_name))
                if len(elements) == 0:
                    elements = soup.find_all(f"{listing_object_type}", listing_object_properties)
                if len(elements) != 0:
                    for element in elements:
                        http_urls = [a['href'] for a in element.find_all('a', href=True) if
                                     a['href'].startswith('https')]
                        if isinstance(http_urls, list):
                            if len(http_urls) != 0:
                                news_url_found = news_url_found + http_urls
                            else:
                                # Another way to get urls, not that safe but works.
                                a_list = element.find_all('a', href=True)
                                for a in a_list:
                                    if str(a['href'])[0] == '/':
                                        divider = ""
                                    else:
                                        divider = "/"
                                    news_url_found.append(f"{source_domain}/{divider}{a['href']}")

            logging.info(f"[Listings] {source} Found {list(set(news_url_found))} news.")
            if news_url_found != 0:
                news_url_found = list(set(news_url_found))
                self.source_parameters[source]['listing_results'] = news_url_found

    def _get_news_html(self):
        for source in list(self.source_parameters.keys()):
            listing_results = self.source_parameters[source]['listing_results']
            if 'news_collect_data' not in list(self.source_parameters[source].keys()):
                self.source_parameters[source]['news_to_collect_data'] = []
            if len(listing_results) != 0:
                # TODO: REMOVE THIS LIMITATION
                listing_results = listing_results[:2]
                for listing_url in listing_results:
                    try:
                        print(listing_url)
                        response = requests.get(listing_url)
                        response_status = response.status_code
                        response_html = response.text

                    except:
                        response_status = 500
                        response_html = None

                    # TODO: Add elapsed time to request
                    logging.info(f"[Request NEWS] {source} | {response_status}")
                    self.source_parameters[source]['news_to_collect_data'].append({
                        'url': listing_url,
                        'status_code': response_status,
                        'html': response_html})

    def extraction_manager(self):
        self.source_parameters = self._get_sources(only_active=True)
        logging.info(f'Obtained {len(list(self.source_parameters.keys()))} sources to process.')
        self._search_news()
        self._get_news_listing()
        self._get_news_html()


if __name__ == '__main__':
    bot_class = NewsDataExtractor()
    bot_class.extraction_manager()
