'''
Author  : Aadesh Salecha
Course  : MIT 6.002x
Date    : Jan 2016
'''
def getAverage(die, numRolls, numTrials):
    """
      - die, a Die
      - numRolls, numTrials, are positive ints
      - Calculates the expected mean value of the longest run of a number
        over numTrials runs of numRolls rolls.
      - Calls makeHistogram to produce a histogram of the longest runs for all
        the trials. There should be 10 bins in the histogram
      - Choose appropriate labels for the x and y axes.
      - Returns the mean calculated
    """
    longs = []
    for i in range(numTrials):
        s = ''
        for j in range(numRolls):
            s = s + str(die.roll())

        curString = s[0]
        longest = s[0]
        for i in range(1, len(s)):
            if s[i] == curString[-1]:
                curString += s[i]
                if len(curString) > len(longest):
                    longest = curString
            else:
                curString = s[i]
        longs.append(len(longest))
    
    makeHistogram(longs, 10, 'x', 'y')
    return float(sum(longs)) / len(longs)