
import sys
import json
import logging

from alchemy import Alchemy
from oxford import Oxford
from watson import Watson
from IPython import embed


class Extractor:
    # djjjjjjjjjjjjjjjjj
    def __init__(self, input_file=None, output_file=None):
        # hhhhhhhhhhhhhhhh
        # print "BBBBBBBb"
        self.alchemy_options = ['main', 'sentiment', 'emotion']  # ['emotion', 'sentiment', 'main']

        self.input_file = input_file
        self.output_file = output_file

        if input_file:
            self.data = self.json_file_to_obj(input_file)

        self.alchemy = Alchemy()
        self.oxford = Oxford()
        self.watson = Watson()
        # print "BASE"
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
            data = "[" + ",".join([line.strip() for line in json_file]) + "]"
            return data

    def remove_from_input(self):
        '''
        Remove the first line of the input file.
        This is horrible implementation. But hey, it's a hackathon.
        '''
        with open(self.input_file, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(self.input_file, 'w') as fout:
            fout.writelines(data[1:])

    def write_to_json(self, article):
        json_article = json.dumps(article, sort_keys=True)
        f = open(self.output_file, "a")
        f.write(json_article + '\n')
        f.close()

    def user_extract(self, payload):
        if not payload['article_link'] or not payload['image_link']:
            raise Exception('Missing data')

        new_payload = [{
            "image_link": payload['image_link'],
            "article_link": payload['article_link'],
            "link_name": None,
            "love": -1,
            "likes": -1,
            "wow": -1,
            "angry": -1,
            "haha": -1,
            "sad": -1
        }]

        extracted = self.extract(data=new_payload)
        return extracted['articles'][0]

    def extract(self, data=None, write=False):
        if data is None:
            data = self.data

        if data is None:
            raise Exception('No data to extract')

        result_obj = {
            "articles": [],
        }

        for idx, payload in enumerate(data):
            logging.info("(" + str(idx + 1) + "/" + str(len(data)) + ") Extracting: " + payload['article_link'])

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
            article['watson'] = self.extract_watson_tone_data(text)
            article['targets'] = {}

            # store targets
            reactions = ['angry', 'haha', 'likes', 'love', 'sad', 'wow']
            for r in reactions:
                article['targets'][r] = payload[r]

            result_obj['articles'].append(article)

            if write:
                logging.info('Saving process...')
                self.remove_from_input()
                self.write_to_json(article)
                logging.info('Done')

        return result_obj

    def extract_alchemy_text(self, url):
        result = self.alchemy.run(url, target='text')
        return result['text'], result['url']

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

    def extract_watson_tone_data(self, text):
        return self.watson.run(text, target='tone_analyzer')

if __name__ == "__main__":
    logging.basicConfig(format="\033[95m\r%(asctime)s - %(levelname)s - %(message)s\033[0m", level=logging.INFO)
    logging.root.setLevel(logging.DEBUG)

    json_file = './input/prepdata.json'
    output_file = './output/bbac_1150_all.json'
    # e = Extractor(json_file, output_file)
    # e.extract(write=True)

    e = Extractor()
    user_input = {
        "article_link": "http://bbc.in/1pDu1Xy",
        "image_link": "https://s3.amazonaws.com/prod-cust-photo-posts-jfaikqealaka/3065-55184dfc661ac1721a0c715326298c54.jpg"
    }

    b = e.user_extract(user_input)

    embed()
