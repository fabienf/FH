import json
from pprint import pprint

with open('bbc_raw_with_links.json') as data_file:    
    data = json.load(data_file)

pprint(data)