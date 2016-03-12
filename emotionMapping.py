# joy fear disgust sadness angry
emotions = [0.8, 0.05, 0.05, 0.01, 0.09]

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
    
print decodeEmotions(emotions)