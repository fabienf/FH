from facepy import GraphAPI
import json

#Used to construct FB access token
app_id = "838247602881284"
app_secret = "23989f20b4a63ab4c7daf40906eae4ec" # DO NOT SHARE WITH ANYONE!
access = app_id + "|" + app_secret

def get_data_from_post(link):
	id = link.split('/')[-1]
	graph = GraphAPI(access)
	page_id= id+'/?fields=picture,link'
	datas= graph.get(page_id, page=True, retry=2)

	posts=[]

	for data in datas:
	    posts.append(data)
	picture = posts[0]['picture']
	picture = picture.split('url=')[1].split('&')[0].replace('%3A',':').replace('%2F','/')

	link = posts[0]['link']
	print picture
	print link


get_data_from_post('https://www.facebook.com/bbcnews/posts/10153445261692217')
