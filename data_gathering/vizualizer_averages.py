

import plotly
import plotly.graph_objs as go

input_file = 'bbc_data_500_articles.json'

import json
from pprint import pprint

with open(input_file) as data_file:    
    data = json.load(data_file)

likes = 0
love = 0
wow = 0
haha = 0
sad = 0
angry = 0

for line in data:
	likes += line['likes']
	love += line['love']
	wow += line['wow']
	haha += line['haha']
	sad += line['sad']
	angry += line['angry']

likes /= len(data)
love /= len(data)
wow /= len(data)
haha /= len(data)
sad /= len(data)
angry /= len(data)



data = [
    go.Bar(
        x=['likes', 'love', 'wow','haha','sad','angry'],
        y=[likes, love, wow,haha,sad,angry]
    )
]
plot_url = plotly.offline.plot(data, filename='basic-bar')
