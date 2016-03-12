
import sys
import json
import logging
import numpy as np

from alchemy import Alchemy
from oxford import Oxford
from IPython import embed


class Extractor:

    def __init__(self, json_file):
        self.alchemy_options = ['main', 'sentiment', 'emotion']  # ['emotion', 'sentiment', 'main']
        self.data = self.json_file_to_obj(json_file)
        self.alchemy = Alchemy()
        self.oxford = Oxford()
        logging.info("Ready to extract")

    def json_file_to_obj(self, json_file):
        try:
            # preprocess
            json_data = self.json_file_to_string(json_file)

            # load
            obj = json.loads(json_data)
            return obj
        except SyntaxError:
            logging.error("JSON input has invalid format! Bye.")
            sys.exit(0)

        return None

    def json_file_to_string(self, file_name):
        with open(file_name) as json_file:
            data = "".join([line.strip() for line in json_file])
            return data

    def extract(self):
        if self.data is None:
            raise Exception('No data to extract')

        result_obj = {
            "articles": [],
        }

        for idx, payload in enumerate(self.data):
            logging.info("(" + str(idx + 1) + "/" + str(len(self.data)) + ") Extracting: " + payload['article_link'])

            # get content and real url using Alchemy API
            article = {}
            text, url = self.extract_alchemy_text(payload['article_link'])

            # assign calues to the article object
            article['title'] = payload['link_name']
            article['text'] = text
            article['real_url'] = url
            article['image_link'] = payload['image_link']
            article['alchemy'] = self.extract_alchemy_data(text)
            article['oxford'] = self.extract_oxford_vision_data(payload['image_link'])
            article['targets'] = {}

            # store targets
            reactions = ['angry', 'haha', 'likes', 'love', 'sad']
            for r in reactions:
                article['targets'][r] = payload[r]

            result_obj['articles'].append(article)

            break

        return result_obj

    def extract_alchemy_text(self, url):
        resutl = self.alchemy.run(url, target='text')
        return resutl['text'], resutl['url']

    def extract_alchemy_data(self, text):
        alchemy_result = self.alchemy.run(text, target='combined', options=self.alchemy_options)

        return self.convert_to_alchemy_template(alchemy_result)

    def convert_to_alchemy_template(self, combined):
        obj = {}
        for n in ['keywords', 'taxonomy', 'concepts', 'entities', 'docEmotions', 'docSentiment']:
            if n in combined:
                obj[n] = combined[n]

        return obj

    def extract_oxford_vision_data(self, url):
        return self.oxford.run(url, target='emotion')

    def emotions_to_x_array(self, articles=None):
        """
        returns X array NxM with emotion values,
        N = number of articles, M = 5 ordered emotions ['anger','disgust','fear','joy','sadness']
        """
        # dictionary of aticles extracted from the IBM json
        if articles is None:
            articles = self.extract()

        articles = articles['articles']

        x = np.zeros([len(articles), 5])
        for i in xrange(len(articles)):
            emotions = articles[i]['alchemy']['emotions']
            for (j, e) in enumerate(['joy', 'fear', 'disgust', 'sadness', 'anger']):
                x[i, j] = emotions[e]

        return x

if __name__ == "__main__":
    logging.basicConfig(format="\033[95m\r%(asctime)s - %(levelname)s - %(message)s\033[0m", level=logging.INFO)
    logging.root.setLevel(logging.DEBUG)

    json_file = '../data_gathering/bbc_data_10_articles.json'
    e = Extractor(json_file)
    b = e.extract()
    c = b['articles'][0]
    embed()

    X = e.emotions_to_x_array(b)
