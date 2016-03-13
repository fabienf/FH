import numpy as np
from sklearn import neighbors, datasets, preprocessing, cross_validation
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from pprint import pprint
import cPickle

from IPython import embed

def decodeEmotions(emotions):
    """
    [Basic version] Function that takes vector of emotions with real numbers
    and outputs predicted reaction on FB

    Argument: 
    @emotions: # joy fear disgust sadness angry
    i.e. emotions = [0.8, 0.05, 0.05, 0.01, 0.09]

    Returns:
    love haha wow sad angry
    [0, 0, 0, 0, 1]
    """
    maxE = emotions.index(max(emotions))
    if maxE == 0: 
        # joy -> haha, love
        return [0.5, 0.5, 0, 0, 0]
    if maxE == 1 or maxE == 2:
        # fear, disgust -> wow
        return [0, 0, 1, 0, 0]
    if maxE == 3:
        # sadness -> sad
        return [0, 0, 0, 1, 0]
    # angry -> angry
    return [0, 0, 0, 0, 1]
    

def makeDataVector(textEmotions, picEmotions, delta=0.3):
    """
    Merges emotion vector from picture into vector from text
    By default, we only take top value from picture and increase
    corresponding text value. We assume text gives better
    emotion information than pictures
    
    Arguments:
    @textEmotions:  [joy fear disgust sadness angry]
    @picEmotions:   [anger contempt disgust fear happiness sadness surprise]
    
    Returns:
    algorithmInputVector:  [joy fear disgust sadness angry] with changed values
    """
    # By mapping find which index in textEmotions to increase
    maxPE = list(picEmotions).index(max(picEmotions))
    if maxPE == 0 or maxPE == 1: 
        # anger || contempt -> angry`
        incInd = 4
    if maxPE == 2: 
        # disgust -> disgust
        incInd = 2
    if maxPE == 3: 
        # fear -> fear
        incInd = 1
    if maxPE == 4: 
        # happiness -> joy
        incInd = 0
    if maxPE == 5: 
        # sadness -> sadness
        incInd = 3
    if maxPE == 6: 
        # surprise -> joy
        incInd = 0
   
    textEmotions[incInd] += delta
    return textEmotions

def makeDataMatrix(textEmotions, picEmotions, delta=0.01):
    assert len(textEmotions)==len(picEmotions), "hup, lengths of text and picture emotions do not match."

    n_artices = len(textEmotions)
    x = np.zeros([n_artices,5])
    for i in xrange(n_artices):
        x[i,:] = makeDataVector(textEmotions[i,:], picEmotions[i,:], delta)

    return x

def makeClassifier(X, targets, n_neighbors = 1, weights = 'distance'):
    """
    Arguments: 
    @X: list of  [joy fear disgust sadness angry]
    i.e. X = [[0.8, 0.05, 0.05, 0.01, 0.09]]
    @targets: list of [love haha wow sad angry]
    i.e. targets = [[0, 0, 0, 0, 1]]
    
    Returns:
    @clf: kNN classifier 
    """
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, targets)
    return clf
    
def predictReactions(clf, testset):
    """
    Given clf classifier and testset, classify it
    Arguments:
    @clf: sklearn classifier 
    @testset: list of  [joy fear disgust sadness angry]
    i.e. testset = [[0.8, 0.05, 0.05, 0.01, 0.09]]
    
    Returns: 
    @predictions: list of [love haha wow sad angry]
    i.e. predictions = [[0, 0, 0, 0, 1]]
    """
    return clf.predict(testset)
    
    
 
if __name__ == "__main__":
    
    # # read data 
    # e1 = np.array([0.8, 0.05,0.05, 0.01, 0.09, 0.8, 0.05, 0.05, 0.01, 0.09]) 
    
    # X_n = [e1, 2*e1, 4*e1, 9*e1]
    
    # X = preprocessing.scale(X_n)
    
    # targets = [[0, 0, 0, 0, 1],
    #           [0, 0, 0, 1, 0],
    #           [0, 1, 0, 0, 0],
    #           [0, 1, 0, 0, 0]]
    
    # testset_n = [7*e1, 22*e1]
    # testset = preprocessing.scale(testset_n)
    # pprint (X_n)
    # pprint (X)  
    # clf = makeClassifier(X, targets)
    
    # reactions = predictReactions(clf, testset)
    # print reactions

    # main prediction with all articles
    with open('../extractor/temp_results/bbac_1150_all.pkl','r') as f:
        data = cPickle.load(f)

    x = makeDataMatrix(data['textEmotions'], data['picEmotions'], delta=0.01)
    targets = data['targets']
    clf = makeClassifier(x, targets, n_neighbors=1)
    with open('trained_models/bbac_1150_all_clf.pkl','wb') as f:
        cPickle.dump(clf, f)

    scores = cross_validation.cross_val_score(clf, x, targets, cv=len(x))
    print scores
    print '\naverage accuracy: ', np.mean(scores)



    # topic specific prediction 
    with open('../extractor/temp_results/bbac_1150_all_chosen.pkl','r') as f:
        data = cPickle.load(f)

    x = makeDataMatrix(data['textEmotions'], data['picEmotions'], delta=0.01)
    targets = data['targets']
    clf = makeClassifier(x, targets, n_neighbors=1)
    with open('trained_models/bbac_1150_all_clf.pkl','wb') as f:
        cPickle.dump(clf, f)

    scores = cross_validation.cross_val_score(clf, x, targets, cv=len(x))
    print scores
    print '\naverage accuracy: ', np.mean(scores)
    
    # embed()
    
    
    
    
    
    
    
    
    
    
    