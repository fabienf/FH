import numpy as np
from sklearn import neighbors, datasets, preprocessing
from pprint import pprint
def decodeEmotions(emotions):
    """
    Function that takes vector of emotions with real numbers
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
    if maxE == 1 or max == 2:
        # fear, disgust -> wow
        return [0, 0, 1, 0, 0]
    if maxE == 3:
        # sadness -> sad
        return [0, 0, 0, 1, 0]
    # angry -> angry
    return [0, 0, 0, 0, 1]
    

def makeClassifier(X, targets, n_neighbors = 1, weights = 'distance'):
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, targets)
    return clf
    
def predictReactions(clf, testset):
    return clf.predict(testset)
    
if __name__ == "__main__":
    
    # read data 
    e1 = np.array([0.8, 0.05,0.05, 0.01, 0.09, 0.8, 0.05, 0.05, 0.01, 0.09]) 
    
    X_n = [e1, 2*e1, 4*e1, 9*e1]
    
    X = preprocessing.scale(X_n)
    
    targets = [[0, 0, 0, 0, 1],
              [0, 0, 0, 1, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0]]
    
    testset_n = [7*e1, 22*e1]
    testset = preprocessing.scale(testset_n)
    pprint (X_n)
    pprint (X)  
    clf = makeClassifier(X, targets)
    
    reactions = predictReactions(clf, testset)
    print reactions
    
    
    
    
    
    
    
    
    
    
    