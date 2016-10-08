'''
Author  : Aadesh Salecha
Course  : MIT 6.002x
Date    : Jan 2016
'''
def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP
    
    prob = 1 - (CURRENTRABBITPOP / MAXRABBITPOP)
    if random.random() < prob:
        CURRENTRABBITPOP += 1
                 
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP
    global MAXRABBITPOP
    
    if CURRENTFOXPOP > 10:
        a = random.random()        
        if a < (float(CURRENTRABBITPOP) / MAXRABBITPOP):
            if (CURRENTRABBITPOP > 10):
                CURRENTRABBITPOP = CURRENTRABBITPOP - 1
                if random.random() < 1.0/3:
                    CURRENTFOXPOP = CURRENTFOXPOP + 1
        else:
            if random.random() < 1.0/10:
                CURRENTFOXPOP = CURRENTFOXPOP - 1
                
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """
    xVals = []
    yVals = []
    for i in range(numSteps):
        rabbitGrowth()
        foxGrowth()
            
        xVals.append(CURRENTRABBITPOP)
        yVals.append(CURRENTFOXPOP)
        
    return yVals, xVals
     