
import logging
import json
import httplib as httplib


class Oxford:

    def __init__(self):
        logging.debug("Loading Oxford...")
        self.headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '4211f4e020b74e23b73be45672d4f2c7',
        }

    def run(self, data, target):
        if data is None:
            logging.error("No data provided!")
            return None

        if target == "emotion":
            return self.get_json(data)
        else:
            logging.error("Unhandled target:" + target)

    def get_json(self, url):
        body = {"URL": url}
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/emotion/v1.0/recognize", json.dumps(body), self.headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        return json.loads(data)
