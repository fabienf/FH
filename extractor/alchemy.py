
import logging

from alchemyapi_python.alchemyapi import AlchemyAPI
from IPython import embed


class Alchemy:

    def __init__(self):
        logging.debug("Loading Alchemy...")
        self.alchemyapi = AlchemyAPI()

    def run(self, data, option="combined"):
        if option == "combined":
            return self.combined(data)
        elif option == "text":
            return self.text(data)
        else:
            logging.error("Unhandled option:" + option)

    def text(self, url):
        logging.debug("[T] Requestions data from Alchemy...")
        response = self.alchemyapi.text('url', url)
        logging.debug("Fininshed!")

        if response['status'] == 'OK':
            return response
        else:
            logging.error('Error in concept tagging call: ', response['statusInfo'])

        return None

    def combined(self, text):
        logging.debug("[C] Requestions data from Alchemy...")
        response_default = self.alchemyapi.combined('text', text)
        response_sentiment = self.alchemyapi.combined('text', text, options={"extract": ('doc-sentiment')})
        response_emotion = self.alchemyapi.combined('text', text, options={"extract": ('doc-emotion')})
        logging.debug("Fininshed!")

        if response_default['status'] == 'OK' and response_sentiment['status'] == 'OK' and response_emotion['status'] == 'OK':
            response = response_default
            response[u'docSentiment'] = response_sentiment['docSentiment']
            response[u'docEmotions'] = response_emotion['docEmotions']
            return response
        else:
            # TODO: fix error msg
            logging.error('Error in concept tagging call: ', response_default['statusInfo'])

        return None
