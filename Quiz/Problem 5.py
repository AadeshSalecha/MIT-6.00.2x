'''
Author  : Aadesh Salecha
Course  : MIT 6.002x
Date    : Jan 2016
'''
def drawing_without_replacement_sim(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    4 red and 4 green balls. Balls are not replaced once
    drawn. Returns a float - the fraction of times 3 
    balls of the same color were drawn in the first 3 draws.
    '''
    fraction = 0
    for j in range(numTrials):
        bucket = [1,1,1,0,0,0]
        choice = []
        for i in range(3):
            select = random.choice(bucket)
            bucket.remove(select)
            choice.append(select)

        if (choice[0] == 1 and choice[1] == 1 and choice[2] == 1) or (choice[0] == 0 and choice[1] == 0 and choice[2] == 0):
        #if (choice[0] == 1 and choice[1] == 1) or (choice[0] == 0 and choice[1] == 0):
            fraction += 1
  
    return (float(fraction) / numTrials)
    
    
    
    
    
    