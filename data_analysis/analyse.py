
import logging
import json
import operator

from collections import Counter
from IPython import embed


class Analyse:

    def __init__(self, file_to_analyse):
        self.data = self.load_file(file_to_analyse)

    def load_file(self, filename):
        articles = []
        with open(filename) as f:
            for article in f:
                obj = json.loads(article.strip())
                articles.append(obj)

        return articles

    def get_taxonomy(self):
        logging.info('Extracting taxonomies')
        taxonomies = []
        for n in self.data:
            taxonomy = n['alchemy']['taxonomy']
            taxonomies.append((taxonomy, n['real_url']))

        return taxonomies

    def get_category_info(self):
        c = self.get_taxonomy()

        taxonomies = []
        for n in c:
            for m in n[0]:
                taxonomies.append((m['label'], n[1]))

        categories = {}
        for n, m in taxonomies:
            # embed()
            # break
            primary = n.split('/')[1]
            if len(n.split('/')) > 2:
                secondary = n.split('/')[2]
            else:
                secondary = None
            if primary not in categories:
                categories[primary] = {
                    'all_count': 0,
                    'secondaries': dict()
                }

            if secondary and secondary not in categories[primary]['secondaries']:
                categories[primary]['secondaries'][secondary] = {
                    'count': 0,
                    'urls': []
                }

            categories[primary]['all_count'] += 1

            try:
                if secondary:
                    categories[primary]['secondaries'][secondary]['count'] += 1
                    categories[primary]['secondaries'][secondary]['urls'].append(m)
            except Exception, e:
                raise e

        return categories

    def find_specific_category(self, primary, secondary):
        categories = self.get_category_info()
        return categories[primary]['secondaries'][secondary]

    def show_categories(self, primary=None):
        categories = self.get_category_info()
        if primary and primary in categories:
            return categories[primary]['secondaries'].keys()
        else:
            return categories.keys()

if __name__ == "__main__":
    file_name = "../extractor/output/bbac_1150_all.json"
    a = Analyse(file_name)
    # print a.show_categories('art and entertainment')
    # b = a.find_specific_category('art and entertainment', 'movies')

    embed()
