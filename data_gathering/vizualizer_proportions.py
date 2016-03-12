

import plotly
import plotly.graph_objs as go

input_file = 'bbc_data_500_articles.json'

import json
from pprint import pprint

with open(input_file) as data_file:    
    data = json.load(data_file)

values  = []
names =[]



for line in data:
	line_vals = [line['love'],line['wow'],line['haha'],line['sad'],line['angry']]
	max_val = max(line_vals)
	total = sum(line_vals)
	if total ==0:
		values.append(0)
	else:
		values.append(max_val/float(total))


data = [
    go.Histogram(
        x=values,    
        autobinx=False,
    	xbins=dict(
        start=0,
        end=1,
        size=0.1
    ), 
    )
]
plot_url = plotly.offline.plot(data, filename='basic-histogram')
