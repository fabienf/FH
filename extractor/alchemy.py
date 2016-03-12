
from alchemyapi_python.alchemyapi import AlchemyAPI
from IPython import embed


class Alchemy:

    def __init__(self, text):
        self.text = text
        self.alchemyapi = AlchemyAPI()

    def run(self, option="combined"):
        if option == "combined":
            return self.combined(self.text)
        else:
            print("Unhandled option:" + option)

    def combined(self, text):
        response_default = self.alchemyapi.combined('text', text)
        response_sentiment = self.alchemyapi.combined('text', text, options={"extract": ('doc-sentiment')})
        response_emotion = self.alchemyapi.combined('text', text, options={"extract": ('doc-emotion')})

        if response_default['status'] == 'OK' and response_sentiment['status'] == 'OK' and response_emotion['status'] == 'OK':
            response = response_default
            response[u'docSentiment'] = response_sentiment['docSentiment']
            response[u'docEmotions'] = response_emotion['docEmotions']
            return response
        else:
            # TODO: fix error msg
            print('Error in concept tagging call: ', response_default['statusInfo'])

        return None
