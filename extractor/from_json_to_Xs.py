import numpy as np
# from extractor import Extractor
import cPickle
import json
from IPython import embed


def text_emotions_x(articles):
    """
    returns X array NxM with emotion values from text,
    N = number of articles, M = 5 ordered emotions ['joy', 'fear', 'disgust', 'sadness', 'anger']
    """
    # dictionary of aticles extracted from the IBM json
    articles = articles['articles']

    x = np.zeros([len(articles), 5])
    for i in xrange(len(articles)):
        emotions = articles[i]['alchemy']['docEmotions']
        for (j, e) in enumerate(['joy', 'fear', 'disgust', 'sadness', 'anger']):
            x[i, j] = emotions[e]

    return x

def picture_emotions_x(articles):
    """
    returns X array NxM with emotion values from picture,
    N = number of articles, M = 7 ordered emotions [anger contempt disgust fear happiness sadness surprise]
    """
    articles = articles['articles']

    debug_faces = []
    x = np.zeros([len(articles), 7])
    for i in xrange(len(articles)):
        face_emotion_list = articles[i]['oxford']
        n_faces = len(face_emotion_list)
        if n_faces==0:
            #no faces recognized on the picture
            x[i,:] = 0
        else:
            # array of emotions for each face in the picture which will be averged
            f_emoion_array = np.zeros([n_faces,7])
            for (j, face) in enumerate(face_emotion_list):
                if face=="error" or face=="activityId" or face=="message" or face=="statusCode":
                    x[i,:] = 0
                    debug_faces.append(face)
                else:
                    for (k, e) in enumerate(['anger', 'contempt', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']):
                        try:
                            f_emoion_array[j, k] = face['scores'][e]
                        except Exception, e:
                            embed()
                        # f_emoion_array[j, k] = face['scores'][e]

            x[i,:] = np.mean(f_emoion_array, axis=0)

    print 'debug_faces', len(debug_faces), debug_faces
    return x

def target_vectors(articles):
    articles = articles['articles']

    targets = np.zeros([len(articles), 5])
    for i in xrange(len(articles)):
        targets_dic = articles[i]['targets']
        targets_list = np.zeros(5)
        for (j, t) in enumerate(['love', 'haha', 'wow', 'sad', 'angry']):
            targets_list[j] = targets_dic[t]

        max_target_ind = list(targets_list).index(max(targets_list))
        targets[i, max_target_ind] = 1

    return targets


if __name__ == "__main__":
    # json_file = '../data_gathering/bbc_data_10_articles.json'
    # e = Extractor(json_file)
    # b = e.extract()
    # embed()
    # with open('temp_results/extracted10.pkl','wb') as f:
    #     cPickle.dump( b, f)

    # with open('temp_results/extracted10.pkl','r') as f:
    #     extracted_articles = cPickle.load(f)

    articles = []
    with open('output/bbac_1150_all.json') as f:
        for article in f:
            obj = json.loads(article.strip())
            articles.append(obj)

    extracted_articles = dict()
    extracted_articles['articles'] = articles
    # e = Extractor(json_file)
    # extracted_articles = e.extract()
    # with open('temp_results/bbac_1150_all_extracted.pkl','wb') as f:
    #     cPickle.dump( extracted_articles, f)

    # embed()

                # textEmotions = text_emotions_x(extracted_articles)
                # picEmotions = picture_emotions_x(extracted_articles)
                # targets = target_vectors(extracted_articles)

                # data = dict()
                # data['textEmotions'] = textEmotions
                # data['picEmotions'] = picEmotions
                # data['targets'] = targets

                # with open('temp_results/bbac_1150_all.pkl','wb') as f:
                #     cPickle.dump(data, f)





    json_chosen_links = json.loads('{"count": 57, "urls": ["http://www.bbc.co.uk/news/entertainment-arts-35774506?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/world-asia-china-35761285?OCID=fbasia&ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35735617?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35693784?OCID=fbasia&ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35693198?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35693784?OCID=fbasia&ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/world-asia-35690403?OCID=fbasia&ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35693198?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/blogs-trending-35686381?ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook&ocid=socialflow_facebook", "http://www.bbc.co.uk/news/entertainment-arts-35670715?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35670715?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35313266?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35670715?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/world-us-canada-35684586?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35670715?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35670715?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35670715?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35313266?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35302982?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35670715?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35313266?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35668918?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.com/culture/story/20160219-who-was-oscar-a-history-of-the-academy-awards-statuette?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35670715?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35681384?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35650665?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35648682?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35648682?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/world-asia-35634604?OCID=fbasia&ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/magazine-35472490?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/world-australia-35592263?OCID=fbasia", "http://www.bbc.co.uk/news/entertainment-arts-35475743?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/world-australia-35557262?OCID=fbasia&ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/world-australia-35557262?OCID=fbasia&ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35551374?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/entertainment-arts-35559488?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35551374?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/live/entertainment-arts-35551374?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/uk-35545391?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/news/world-europe-35560492?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook", "http://www.bbc.co.uk/newsbeat/article/35548964/this-years-grammy-statuettes-will-contain-built-in-cameras", "http://www.bbc.co.uk/news/entertainment-arts-35516095?ocid=socialflow_facebook&ns_mchannel=social&ns_campaign=bbcnews&ns_source=facebook"]}')
    chosen_links = []
    for i in xrange(int(json_chosen_links['count'])):
        chosen_links.append(json_chosen_links['urls'][i])

    chosen_links = list(set(chosen_links))
    print "len(chosen_links:", len(chosen_links)
    articles = []
    with open('output/bbac_1150_all.json') as f:
        for article in f:
            obj = json.loads(article.strip())
            if obj['real_url'] in chosen_links:
                articles.append(obj)
                chosen_links.remove(obj['real_url'])


    extracted_articles = dict()
    extracted_articles['articles'] = articles
    textEmotions = text_emotions_x(extracted_articles)
    picEmotions = picture_emotions_x(extracted_articles)
    targets = target_vectors(extracted_articles)

    data = dict()
    data['textEmotions'] = textEmotions
    data['picEmotions'] = picEmotions
    data['targets'] = targets

    with open('temp_results/bbac_1150_all_chosen.pkl','wb') as f:
        cPickle.dump(data, f)

    embed()

