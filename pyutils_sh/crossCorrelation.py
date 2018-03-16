"""
 - This function takes 2 lists/arrays of data and calculates the normalized max cross-correlation value with its associated lag.
 - Additionally, it will also return the cross-correlation value at 0 lag, as well as the entire normalized array as a python list.
 - You can manually set the time constraints by changing the variable values.
 - Requires the numpy module.
 
 - Simon Ho (www.simonho.ca)
"""

import numpy as N


def calcCrossCorrelation(person1, person2):
    """
    negative lag means person2 lags behind person1 by x frames
    e.g.
    A = [0,1,2,3,0,0,0]
    B = [0,0,0,1,2,3,0]
    calcCrossCorrelation(A,B)


    positive lag means person1 lags behind person2 by x frames
    e.g.
    A = [0,0,0,1,2,3,0]
    B = [0,1,2,3,0,0,0]
    calcCrossCorrelation(A,B)
    """

    # convert lists to numpy arrays
    x = N.array(person1)
    y = N.array(person2)

    # set number of seconds to constrain to
    videoFramerate = 25
    numSecondsConstrain = 2
    lagLimits = numSecondsConstrain*videoFramerate

    # calculate cross correlation values
    correlations = N.correlate(x, y, 'full')

    # trim the cross-correlation values to a range (-lagLimits : +lagLimits)
    # trim AFTER cross correlation calculation to avoid 0 padding of signals
    # assumes x and y are equal length
    trimmedCorrelations = correlations[len(x)-1-lagLimits:len(x)+lagLimits]

    # normalize the cross-correlation values for ease of comparison between
    # subjects
    normArray = trimmedCorrelations / (N.linalg.norm(x) * N.linalg.norm(y))

    # get maximum normalized cross-correlation value
    nR = max(normArray)
    # get lag of max correlation value
    maxLag = N.argmax(normArray)

    # trimmed array is now 2(lagLimits)+1 elements long
    # adjust it so that lag 0 is a complete match
    maxLag_adj = maxLag - lagLimits

    # Get the normalized zero lag correlation value
    zeroLagR = normArray[lagLimits]

    # returns (max cross correlation, lag of max correlation), 0 lag
    # correlation, the entire normalized array (can be removed if not needed)
    return (float(nR), float(maxLag_adj), float(zeroLagR), normArray.tolist())
