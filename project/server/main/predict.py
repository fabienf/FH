from from_json_to_Xs import text_emotions_x, picture_emotions_x
from extractor import Extractor

# import extractor.from_json_to_Xs
from emotionMapping import makeDataMatrix, predictReactions
# import emotionClassification.emotionMapping
import cPickle

from IPython import embed


def predict(article_link, image_link):
    """
    output: predicted emotion as: [ 0.  1.  0.  0.  0.]
    """
    e = Extractor()
    user_input = {
        "article_link": article_link,
        "image_link": image_link
    }

    friendly_json = e.user_extract(user_input)

    tax_list = friendly_json['alchemy']['taxonomy']
    tax_primary = []
    for t in tax_list:
        tax_primary.append(t['label'].split('/')[1])

    tax_primary = list(set(tax_primary))[0]

    extracted_articles = dict()
    extracted_articles['articles'] = [friendly_json]
    textEmotions = text_emotions_x(extracted_articles)
    picEmotions = picture_emotions_x(extracted_articles)

    with open('emotionClassification/trained_models/bbac_1150_all_clf.pkl','r') as f:
        clf = cPickle.load(f)

    test_article = makeDataMatrix(textEmotions, picEmotions)

    reaction = predictReactions(clf, test_article)

    return reaction[0], tax_primary

if __name__ == '__main__':
    # print predict("http://bbc.in/1pDu1Xy", "https://s3.amazonaws.com/prod-cust-photo-posts-jfaikqealaka/3065-55184dfc661ac1721a0c715326298c54.jpg")
    print predict("http://bbc.in/1SFfhmy", "https://s3.amazonaws.com/prod-cust-photo-posts-jfaikqealaka/3065-001693b125e76a7b9e7b463561c7c9f1.jpg")
