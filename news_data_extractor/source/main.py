import time

import requests
from bs4 import BeautifulSoup
import logging
import re
import datetime

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
        self.ignore_urls_with_text = ['/staff/']
        self.extracted_data = []

    def _get_sources(self, only_active=False):
        sources_config = {
            'apnews': {'text_search_url': 'https://apnews.com/search?q=', 'domain': 'https://apnews.com',
                       'enabled': True, 'captcha': False,
                       'listing_steps': [{'type': 'div', 'loc': {'class': 'PageList-items-item'}}],
                       'extraction_steps': [
                           {'column_name': 'title', 'type': 'h1', 'loc': {'class': 'Page-headline'}},
                           {'column_name': 'description', 'type': 'div',
                            'loc': {'class': 'RichTextStoryBody RichTextBody'}},
                           {'column_name': 'full_text', 'type': 'div',
                            'loc': {'class': 'RichTextStoryBody RichTextBody'}},
                           {'column_name': 'date', 'type': 'bsp-timestamp', 'loc': {}},
                           {'column_name': 'picture_url', 'type': 'img', 'loc': {'class': 'Image', 'alt': 'Image'}},
                           {'column_name': 'picture_caption', 'type': 'figcaption', 'loc': {'class': 'Figure-caption'}},
                           {'column_name': 'authors', 'type': 'div', 'loc': {'class': 'Page-authors'}},

                       ],
                       },

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
                              {'type': 'div', 'loc': {'class': 'v-card gothamist-card mod-horizontal'}}],
                          'extraction_steps': [
                              {'column_name': 'title', 'type': 'h1', 'loc': {'class': 'mt-4 mb-3 h2'}},
                              {'column_name': 'description', 'type': 'div',
                               'loc': {'class': 'streamfield-paragraph rte-text'}},
                              {'column_name': 'full_text', 'type': 'div',
                               'loc': {'class': 'streamfield-paragraph rte-text'}},
                              {'column_name': 'date', 'type': 'div', 'loc': {'class': 'date-published'}},
                              {'column_name': 'picture_url', 'type': 'img',
                               'loc': {'class': 'image native-image prime-img-class'}},
                              {'column_name': 'picture_caption', 'type': 'figcaption', 'loc': {
                                  'class': 'flexible-link null image-with-caption-credit-link image-with-caption-credit-link'}},
                              {'column_name': 'authors', 'type': 'a',
                               'loc': {'class': 'flexible-link internal v-byline-author-name v-byline-author-name'}},

                          ],
                          },

            'yahoo': {'text_search_url': 'https://news.search.yahoo.com/search;?p=',
                      'domain': 'https://news.search.yahoo.com', 'enabled': True, 'captcha': False,
                      'listing_steps': [{'type': 'div', 'loc': {'class': 'dd NewsArticle'}}],
                      'extraction_steps': [
                          {'column_name': 'title', 'type': 'div', 'loc': {'class': 'caas-title-wrapper'}},
                          {'column_name': 'description', 'type': 'div',
                           'loc': {'class': 'caas-body'}},
                          {'column_name': 'full_text', 'type': 'div',
                           'loc': {'class': 'caas-body'}},
                          {'column_name': 'date', 'type': 'div', 'loc': {'class': 'caas-attr-time-style'}},
                          {'column_name': 'picture_url', 'type': 'img', 'loc': {'class': 'caas-img'}},
                          {'column_name': 'picture_caption', 'type': 'figcaption',
                           'loc': {'class': 'caption-collapse'}},
                          {'column_name': 'authors', 'type': 'span', 'loc': {'class': 'caas-author-byline-collapse'}},

                      ],
                      },
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
                valid_urls = []
                for url in news_url_found:
                    if source in url:
                        ignore_flag = False
                        for text in self.ignore_urls_with_text:
                            if text in url:
                                ignore_flag = True
                        if ignore_flag:
                            pass
                        else:
                            valid_urls.append(url)

                self.source_parameters[source]['listing_results'] = valid_urls

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

    def _parse_each_news(self):
        for source in list(self.source_parameters.keys()):
            self.source_parameters[source]['collected_data'] = []
            for news_article in self.source_parameters[source]['news_to_collect_data']:
                article_status = news_article['status_code']
                url = news_article['url']
                search_html = news_article['html']
                if article_status == 200 and search_html is not None:
                    generated_row = {'url': url, 'source': source}
                    soup = BeautifulSoup(search_html, 'html.parser')
                    # TODO: Add tolerance to accept not only class
                    for step_dict in self.source_parameters[source]['extraction_steps']:
                        column_name = step_dict['column_name']
                        object_type = step_dict['type']
                        object_param = step_dict['loc']
                        result = None

                        element = soup.find(f'{object_type}', object_param)
                        if element is None:
                            try:
                                element = soup.find(class_=lambda x: x and x.startswith(object_param['class']))
                            except:
                                pass
                        if element is None:
                            try:
                                element = soup.find(id_=lambda x: x and x.startswith(object_param['id']))
                            except:
                                pass

                        if element is not None:
                            if column_name == "title":
                                result = element.text
                            elif column_name == "description":
                                result = element.findNext('p').text

                            elif column_name == "full_text":
                                full_text = ""
                                all_p = element.find_all('p')
                                if len(all_p) != 0:
                                    for p in all_p:
                                        if full_text == "":
                                            full_text = f"{p.text}"
                                        else:
                                            full_text = f"{full_text}\n{p.text}"
                                else:
                                    full_text = element.text
                                result = full_text
                                # TODO: Remove this 50 char limitation
                                result = result[:50]

                            elif column_name == "date":
                                try:
                                    try:
                                        result = str(element['datetime'])
                                        if len(result) == 0:
                                            result = str(element.text)
                                    except:
                                        result = str(element['data-timestamp'])
                                except:
                                    result = str(element.text)

                            elif column_name == "picture_url":
                                result = str(element['src'])

                            else:
                                result = str(element.text)
                            generated_row[column_name] = result
                        else:
                            generated_row[column_name] = result
                    self.source_parameters[source]['collected_data'].append(generated_row)

            print(self.source_parameters[source]['collected_data'])
            if len(self.source_parameters[source]['collected_data']) != 0:
                self.extracted_data = self.extracted_data + self.source_parameters[source]['collected_data']

    def _normalize_all_data(self):
        def clean_text(text):
            """
            Normalize text by removing extra spaces, HTML tags, and unwanted characters.

            Parameters:
            text (str): The text to be cleaned.

            Returns:
            str: Cleaned text.
            """
            if not isinstance(text, str):
                return text
            # Remove HTML tags
            text = BeautifulSoup(text, "html.parser").get_text()
            # Remove unwanted characters
            text = re.sub(r'\s+', ' ', text).strip()
            return text

        def parse_date(date_str):
            """
            Parse different date formats and convert them to datetime format.

            Parameters:
            date_str (str): The date string to be parsed.

            Returns:
            datetime: The parsed datetime object or None if parsing fails.
            """
            try:
                # Case where date is a timestamp in milliseconds
                if date_str.isdigit():
                    return datetime.datetime.fromtimestamp(int(date_str) / 1000)

                # Case where date is a standard formatted date string
                formats = [
                    "%B %d, %Y at %I:%M %p",  # e.g., August 17, 2024 at 6:23 PM
                    "%Y-%m-%d",  # e.g., 2024-08-17
                    "%A, %B %d, %Y, %I:%M %p",  # e.g., Saturday, August 17, 2024, 6:47 PM
                    "%b %d, %Y",  # e.g., Aug 8, 2024
                    "%B %d, %Y",  # e.g., August 17, 2024
                    "%b %d, %YModified %b %d, %Y"  # e.g., Published Jul 18, 2024Modified Jul 19, 2024
                ]

                for fmt in formats:
                    try:
                        return datetime.datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue

                # Handle "Published" and "Modified" dates with keywords
                if "Published" in date_str or "Modified" in date_str:
                    cleaned_str = re.sub(r"(Published|Modified)\s*", "", date_str)
                    return parse_date(cleaned_str)

            except Exception as e:
                return None  # Handle errors gracefully

        formatted_rows = []
        for row in self.extracted_data:
            if row['title'] is not None:
                print(row)
                print(str(row['date']))
                if '·' in str(row['date']):
                    row['date'] = str(row['date']).split('·')[0].strip()
                elif 'Published' in str(row['date']):
                    row['date'] = str(row['date']).split('Published')[1].strip()
                    if 'Modified' in str(row['date']):
                        row['date'] = str(row['date']).split('Modified')[0].strip()
                to_remove = ['SAT,', 'MON,', 'WED,', 'THU,', 'FRI', 'TUE,', 'SUN,']
                for value_to_remove in to_remove:
                    if value_to_remove in str(row['date']).upper():
                        row['date'] = str(row['date']).split(f"{str(row['date']).split(',')[0]},")[1].strip()
                print(str(row['date']))
                formatted_date = parse_date(str(row['date']))
                print(formatted_date)

    def extraction_manager(self):
        self.source_parameters = self._get_sources(only_active=True)
        logging.info(f'Obtained {len(list(self.source_parameters.keys()))} sources to process.')
        self._search_news()
        self._get_news_listing()
        self._get_news_html()
        self._parse_each_news()
        self._normalize_all_data()


if __name__ == '__main__':
    bot_class = NewsDataExtractor()
    bot_class.extraction_manager()
