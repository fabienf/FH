
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
            taxonomies.append(taxonomy)

        return taxonomies

if __name__ == "__main__":
    file_name = "../extractor/output/bbac_1150_all.json"
    a = Analyse(file_name)
    c = a.get_taxonomy()

    taxonomies = []
    for n in c:
        for m in n:
            taxonomies.append(m['label'])
    z = Counter(taxonomies)
    sorted_z = sorted(z.items(), key=operator.itemgetter(1))

    categories = {}
    for n in z:
        main = n.split('/')[1]
        if main not in categories:
            categories[main] = 0

        categories[main] += z[n]

    embed()
