
import logging
import sys

from alchemyapi_python.alchemyapi import AlchemyAPI
from IPython import embed


class Alchemy:

    def __init__(self):
        logging.debug("Loading Alchemy...")
        self.alchemyapi = AlchemyAPI()

    def run(self, data, target, options=None):
        if target == "combined":
            if options is None:
                options = ['main', 'sentiment', 'emotion']  # defualt
            return self.combined(data, options)
        elif target == "text":
            return self.text(data)
        else:
            logging.error("Unhandled target:" + target)

    def text(self, url):
        logging.debug("[T] Requestions data from Alchemy...")
        response = self.alchemyapi.text('url', url)
        logging.debug("Fininshed!")

        if response['status'] == 'OK':
            return response
        else:
            logging.error('Error in concept tagging call: ' + str(response['statusInfo']))
            sys.exit(0)

        return None

    def combined(self, text, options):
        logging.debug("[C] Requestions data from Alchemy...")

        result = {}
        for n in options:
            if n == "main":
                response = self.combined_helper(text)
                result[u'entities'] = response['entities']
                result[u'taxonomy'] = response['taxonomy']
                result[u'concepts'] = response['concepts']
                result[u'keywords'] = response['keywords']

                result = response
            elif n == "sentiment":
                response = self.combined_helper(text, options={"extract": ('doc-sentiment')})
                result[u'docSentiment'] = response['docSentiment']
            elif n == "emotion":
                response = self.combined_helper(text, options={"extract": ('doc-emotion')})
                result[u'docEmotions'] = response['docEmotions']

        self.combined_helper(text)

        logging.debug("Fininshed!")

        return result

    def combined_helper(self, text, options={}):
        response = self.alchemyapi.combined('text', text, options=options)

        if response['status'] == 'OK':
            return response
        else:
            logging.error('Error in concept tagging call: ', response['statusInfo'])

        return None
