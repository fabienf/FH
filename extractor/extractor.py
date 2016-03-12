
import sys
import json
import numpy as np

from alchemy import Alchemy
from IPython import embed


class Extractor:

    def __init__(self, json_file):
        self.data = self.json_file_to_obj(json_file)
        print "Ready to extract"

    def json_file_to_obj(self, json_file):
        try:
            # preprocess
            json_data = self.json_file_to_string(json_file)

            # load
            obj = json.loads(json_data)
            return obj
        except SyntaxError:
            print("JSON input has invalid format! Bye.")
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
            "articles": []
        }

        for payload in self.data:
            article = {}
            article['original_text'] = payload['text']
            article['image_url'] = payload['image_url']
            article['alchemy'] = self.extract_alchemy(payload)
            article['targets'] = {}

            # store targets
            reactions = ['angry', 'haha', 'like', 'love', 'sad']
            for r in reactions:
                article['targets'][r] = payload[r]

            result_obj['articles'].append(article)

        return result_obj

    def extract_alchemy(self, payload):
        a = Alchemy(payload['text'])
        alchemy_result = a.run('combined')

        return self.convert_to_alchemy_template(alchemy_result)

    def convert_to_alchemy_template(self, combined):
        return {
            'keywords': combined['keywords'],
            'sentiment': combined['docSentiment'],
            'taxonomy': combined['taxonomy'],
            'concepts': combined['concepts'],
            'emotions': combined['docEmotions']
        }

    def emotions_to_X_array(self):
        """
        returns X array NxM with emotion values, 
        N = number of articles, M = 5 ordered emotions ['anger','disgust','fear','joy','sadness'] 
        """
        # dictionary of aticles extracted from the IBM json 
        articles = self.extract()
        articles = articles['articles']

        X = np.zeros([len(articles),5])
        for i in xrange(len(articles)):
            emotions = articles[i]['alchemy']['emotions']
            for (j,e) in enumerate(['anger','disgust','fear','joy','sadness']):
                X[i,j] = emotions[e]

        return X

if __name__ == "__main__":
    json_file = '../data_gathering/bbc_data/bbc_raw_with_links.json'
    e = Extractor(json_file)
    b = e.extract()
    c = b['articles'][0]
    embed()

    X = e.emotions_to_X_array()

