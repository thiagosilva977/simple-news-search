from robocorp.tasks import task
from news_data_extractor.source.main import NewsDataExtractor
import json

@task
def minimal_task():
    message = "Hello"
    message = message + " World!"
    print('hello word')

@task
def search_news():
    search_parameters = {'text_phrase': "Olympic Paris", 'news_category': None, 'max_months': 2}
    bot_class = NewsDataExtractor(search_parameters=search_parameters)
    step_1 = bot_class._search_news()
    json_object = json.dumps(step_1)
    with open('/output/step_1.json', 'w') as outfile:
        json.dump(json_object, outfile)


