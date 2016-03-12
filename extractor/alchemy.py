
from alchemyapi_python.alchemyapi import AlchemyAPI


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
        response = self.alchemyapi.combined('text', text)

        if response['status'] == 'OK':
            return response
        else:
            print('Error in concept tagging call: ', response['statusInfo'])

        return None
