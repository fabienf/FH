import numpy as np
from extractor import Extractor
import cPickle
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
                for (k, e) in enumerate(['anger', 'contempt', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']):
                    f_emoion_array[j, k] = face['scores'][e]

            x[i,:] = np.mean(f_emoion_array, axis=0)

    return x


if __name__ == "__main__":
    # json_file = '../data_gathering/bbc_data_10_articles.json'
    # e = Extractor(json_file)
    # b = e.extract()
    # embed()
    # with open('extracted10.pkl','wb') as f:
    #     cPickle.dump( b, f)

    with open('extracted10.pkl','r') as f:
        extracted_articles = cPickle.load(f)

    textEmotions = text_emotions_x(extracted_articles)
    picEmotions = picture_emotions_x(extracted_articles)

    embed()

