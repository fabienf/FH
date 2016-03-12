
import sys
import json

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
            article['alchemy'] = self.extract_alchemy(payload)

            result_obj['articles'].append(article)

        return result_obj

    def extract_alchemy(self, payload):
        a = Alchemy(payload['text'])
        alchemy_result = a.run('combined')

        return self.convert_to_alchemy_template(alchemy_result)

    def convert_to_alchemy_template(self, combined):
        return {
            'keywords': combined['keywords'],
            'sentiment': None,
            'taxonomy': combined['taxonomy'],
            'concepts': combined['concepts'],
            'emotions': None
        }

if __name__ == "__main__":
    json_file = '../data_gathering/bbc_data/bbc_raw_with_links.json'
    e = Extractor(json_file)
    b = e.extract()
    c = b['articles'][0]['alchemy']
    # embed()
