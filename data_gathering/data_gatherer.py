import urllib2
import json
import datetime
import time
import mechanize


#Used to construct FB access token
app_id = "838247602881284"
app_secret = "23989f20b4a63ab4c7daf40906eae4ec" # DO NOT SHARE WITH ANYONE!
access_token = app_id + "|" + app_secret
#page name
page_id = 'bbcnews'
#get post starting from date
posts_start = datetime.datetime(2016, 3, 5)
#boolean whether we are done
reached_end = False
#json data
data = []


#Logs in to Facebook and returns a browser witha cookie
def setUpBrowser():
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	cookies = mechanize.CookieJar()
	browser.set_cookiejar(cookies)
	browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
	browser.set_handle_refresh(False)

	url = 'http://m.facebook.com/login.php'
	browser.open(url)
	browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
	browser.form['email'] = 'ffspm00@gmail.com'
	browser.form['pass'] = 'jablko'
	browser.submit()
	return browser

def getReactionsFromPost(browser,id):
	response = browser.open("https://www.facebook.com/bbcnews/posts/"+id)
	facebook_output = response.read()
	#separate part with reactions
	facebook_output = facebook_output.split('reactioncountmap":')[1].split(',"reactioncountreduced')[0]
	facebook_output = json.loads(facebook_output)
	#extract data from the structure like json recevied
	likes = facebook_output['1']['default']
	love = facebook_output['2']['default']
	wow = facebook_output['3']['default']
	haha = facebook_output['4']['default']
	sad = facebook_output['7']['default']
	angry = facebook_output['8']['default']
	return likes,love,wow,haha,sad,angry


browser = setUpBrowser()


#Due to number of requests we can get an error, keep trying until we succeed
def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)
            
            print "Error for URL %s: %s" % (url, datetime.datetime.now())

    return response.read()

#Request information from our page with specified scope as likes comments etc
def getFacebookPageFeedData(page_id, access_token, num_statuses):
    
    # construct the URL string
    base = "https://graph.facebook.com"
    node = "/" + page_id + "/feed" 
    parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data

#processes data we get for each post
def processFacebookPageFeedStatus(status):
    
    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.
    
    # Additionally, some items may not always exist,
    # so must check for existence first
    
    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else status['message'].encode('utf-8')
    link_name = '' if 'name' not in status.keys() else status['name'].encode('utf-8')
    status_type = status['type']
    #Discard links which are a video, photo etc.
    if str(status_type)!='link':
    	return None
    status_link = '' if 'link' not in status.keys() else status['link']
    
    
    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.
    status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')

    if (status_published<posts_start):
    	reached_end = True

    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs
    #Signal finished when we have reached the oldest date
  
    
    # Nested items require chaining dictionary keys.
    num_likes = 0 if 'likes' not in status.keys() else status['likes']['summary']['total_count']
    num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']


    ####### Get reactions, split t get the post number, separating from group num which we don't need
    likes,love,wow,haha,sad,angry = getReactionsFromPost(browser,status_id.split('_')[1])

    print link_name + " "+ status_published
    new_line = {"link_name":link_name,"article_link":status_link,"likes":likes,"love":love,"wow":wow,"haha":haha,"sad":sad,"angry":angry}
    return new_line


#Main method goes through all posts
def scrapeFacebookPageFeedStatus(page_id, access_token):        
        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()
        
        print "Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime)
        
        #get first posts
        statuses = getFacebookPageFeedData(page_id, access_token, 100)
        
        #keep going for all posts
        while not reached_end and has_next_page:
            for status in statuses['data']:
            	#Check if it were a link or not
            	new_line = processFacebookPageFeedStatus(status)
            	if new_line is None:
            		continue

                data.append(new_line)       
                # output progress occasionally to make sure code is not stalling
                num_processed += 1
                if num_processed % 10 == 0:
                    print "\n %s Statuses Processed: %s \n " % (num_processed, datetime.datetime.now())
                    #store intermediate
                    data_file = open('bbc_data.json', "w+")
                    data_file.write(json.dumps(data))
                    data_file.close()     
                    
            # if there is no next page, we're done.
            if 'paging' in statuses.keys():
                statuses = json.loads(request_until_succeed(statuses['paging']['next']))
            else:
                has_next_page = False

        #write file
        data_file = open('bbc_data.json', "w+")
        data_file.write(json.dumps(data))
        data_file.close()       
        
        print "\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime)




scrapeFacebookPageFeedStatus(page_id, access_token)
    