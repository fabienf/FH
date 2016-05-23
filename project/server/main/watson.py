
import logging
from watson_developer_cloud import ToneAnalyzerV3Beta


class Watson:

    def __init__(self):
        logging.debug("Loading Watson...")

        self.tone_analyzer = ToneAnalyzerV3Beta(
            username='50705f69-a1ad-4432-8eaa-25c0c7b23bb9',
            password='CVK1hMPA1V3o',
            version='2016-02-11')

    def run(self, data, target):
        if data is None:
            logging.error("No data provided!")
            return None

        if target == "tone_analyzer":
            return self.get_tone_analyses(data)
        else:
            logging.error("Unhandled target:" + target)

    def get_tone_analyses(self, data):
        return self.tone_analyzer.tone(text=data)
