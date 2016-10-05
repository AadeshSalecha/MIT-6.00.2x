import numpy
import random
import pylab
from ps3b_precompiled_27 import *    

class NoChildException(Exception):
	"""
	NoChildException is raised by the reproduce() method in the SimpleVirus
	and ResistantVirus classes to indicate that a virus particle does not
	reproduce. You can use NoChildException as is, you do not need to
	modify/add any code.
	"""	
random.seed(0)

class SimpleVirus(object):
	"""
	Representation of a simple virus (does not model drug effects/resistance).
	"""
	
	def __init__(self, maxBirthProb, clearProb):
		"""
		Initialize a SimpleVirus instance, saves all parameters as attributes
		of the instance.
		maxBirthProb: Maximum reproduction probability (a float between 0-1)				
		clearProb: Maximum clearance probability (a float between 0-1).
		"""
		self.maxBirthProb = maxBirthProb
		self.clearProb = clearProb
		
	def doesClear(self):
		"""
		Stochastically determines whether this virus is cleared from the
		patient's body at a time step. 
		
		returns: Using a random number generator (random.random()), this method
		returns True with probability self.clearProb and otherwise returns
		False.
		"""
		if random.random() <= self.clearProb:
			return True
		else:
			return False
	
	def reproduce(self, popDensity):
		"""
		Stochastically determines whether this virus particle reproduces at a
		time step. Called by the update() method in the SimplePatient and
		Patient classes. The virus particle reproduces with probability
		self.maxBirthProb * (1 - popDensity).
		
		If this virus particle reproduces, then reproduce() creates and returns
		the instance of the offspring SimpleVirus (which has the same
		maxBirthProb and clearProb values as its parent).		 
		
		popDensity: the population density (a float), defined as the current
		virus population divided by the maximum population.		 
		
		returns: a new instance of the SimpleVirus class representing the
		offspring of this virus particle. The child should have the same
		maxBirthProb and clearProb values as this virus. Raises a
		NoChildException if this virus particle does not reproduce.			   
		"""
		if random.random() <= ( self.maxBirthProb * ( 1 - popDensity ) ):
			# print "virus reproduces"
			return SimpleVirus( self.maxBirthProb, self.clearProb )
		else:
			raise NoChildException('In reproduce()')
	

class Patient(object):
	"""
	Representation of a simplified patient. The patient does not take any drugs
	and his/her virus populations have no drug resistance.
	"""
	
	def __init__(self, viruses, maxPop):
		"""
		Initialization function, saves the viruses and maxPop parameters as
		attributes.
		
		viruses: the list representing the virus population (a list of
		SimpleVirus instances)
		
		maxPop: the  maximum virus population for this patient (an integer)
		"""
		self.viruses = viruses
		self.maxPop = maxPop
	
	def getTotalPop(self):
		"""
		Gets the current total virus population. 
		returns: The total virus population (an integer)
		"""	
		return len( self.viruses )
	
	def update(self):
		"""
		Update the state of the virus population in this patient for a single
		time step. update() should execute the following steps in this order:
		- Determine whether each virus particle survives and updates the list
		  of virus particles accordingly.
		- The current population density is calculated. This population density
		  value is used until the next call to update() 
		- Determine whether each virus particle should reproduce and add
		  offspring virus particles to the list of viruses in this patient.					
		returns: the total virus population at the end of the update (an
		integer)
		"""
		# Determine whether each virus particle survives and updates the 
		# list of virus particles accordingly.
		newViruses = []
		for index, virus in reversed( list( enumerate( self.viruses ) ) ):
			if virus.doesClear():
				# print "Virus clears"
				# pop virus from viruses list
				self.viruses.pop( index )
			else:
				popDensity = self.getTotalPop()/float(self.maxPop)
				try:
					# determine if surving virus reproduces
					# append any offspring to new virus list
					newViruses.append( virus.reproduce( popDensity ) )
				except NoChildException:
					continue
		# print "self.viruses =", self.viruses
		# print "newViruses =",  newViruses
		# add the new viruses to the list of patient viruses
		self.viruses = self.viruses + newViruses
		# print self.viruses

		return self.getTotalPop()


#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,numTrials):
   avg = [0] * 300
   for i in range(numTrials):
       viruses = []
       for j in range(numViruses):
           viruses.extend([SimpleVirus(maxBirthProb, clearProb)])

       patient = Patient(viruses, maxPop)
       for k in range(300):
           avg[k] = float(avg[k]) + patient.update()
    
   for l in range(300):
       avg[l] = avg[l] / float(numTrials)


   pylab.figure("SimpleVirus simulation")
   pylab.title("SimpleVirus simulation")
   pylab.plot(avg,label = "SimpleVirus")
   pylab.xlabel("Time Steps")
   pylab.ylabel("Population of virus")
   pylab.legend()
   pylab.show()


# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
   """
   Representation of a virus which can have drug resistance.
   """   

   def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
       """
       Initialize a ResistantVirus instance, saves all parameters as attributes
       of the instance.

       maxBirthProb: Maximum reproduction probability (a float between 0-1)       

       clearProb: Maximum clearance probability (a float between 0-1).

       resistances: A dictionary of drug names (strings) mapping to the state
       of this virus particle's resistance (either True or False) to each drug.
       e.g. {'guttagonol':False, 'srinol':False}, means that this virus
       particle is resistant to neither guttagonol nor srinol.

       mutProb: Mutation probability for this virus particle (a float). This is
       the probability of the offspring acquiring or losing resistance to a drug.
       """
	SimpleVirus.__init__(self, maxBirthProb, clearProb)
	self.resistances = resistances
	self.mutProb = mutProb

   def getResistances(self):
       """
       Returns the resistances for this virus.
       """
       return self.resistances

   def getMutProb(self):
       """
       Returns the mutation probability for this virus.
       """
       return self.mutProb

   def isResistantTo(self, drug):
       """
       Get the state of this virus particle's resistance to a drug. This method
       is called by getResistPop() in TreatedPatient to determine how many virus
       particles have resistance to a drug.       

       drug: The drug (a string)

       returns: True if this virus instance is resistant to the drug, False
       otherwise.
       """
       if drug in self.resistances.keys():
           return self.resistances[drug]
       return False

   def reproduce(self, popDensity, activeDrugs):
       """
       Stochastically determines whether this virus particle reproduces at a
       time step. Called by the update() method in the TreatedPatient class.

       A virus particle will only reproduce if it is resistant to ALL the drugs
       in the activeDrugs list. For example, if there are 2 drugs in the
       activeDrugs list, and the virus particle is resistant to 1 or no drugs,
       then it will NOT reproduce.

       Hence, if the virus is resistant to all drugs
       in activeDrugs, then the virus reproduces with probability:      

       self.maxBirthProb * (1 - popDensity).                       

       If this virus particle reproduces, then reproduce() creates and returns
       the instance of the offspring ResistantVirus (which has the same
       maxBirthProb and clearProb values as its parent). The offspring virus
       will have the same maxBirthProb, clearProb, and mutProb as the parent.

       For each drug resistance trait of the virus (i.e. each key of
       self.resistances), the offspring has probability 1-mutProb of
       inheriting that resistance trait from the parent, and probability
       mutProb of switching that resistance trait in the offspring.       

       For example, if a virus particle is resistant to guttagonol but not
       srinol, and self.mutProb is 0.1, then there is a 10% chance that
       that the offspring will lose resistance to guttagonol and a 90%
       chance that the offspring will be resistant to guttagonol.
       There is also a 10% chance that the offspring will gain resistance to
       srinol and a 90% chance that the offspring will not be resistant to
       srinol.

       popDensity: the population density (a float), defined as the current
       virus population divided by the maximum population       

       activeDrugs: a list of the drug names acting on this virus particle
       (a list of strings).

       returns: a new instance of the ResistantVirus class representing the
       offspring of this virus particle. The child should have the same
       maxBirthProb and clearProb values as this virus. Raises a
       NoChildException if this virus particle does not reproduce.
       """
       for drug in activeDrugs:
           if not(self.isResistantTo(drug)):
               raise NoChildException()
               
       # virus is resistant to all drugs
       if random.random() < self.maxBirthProb * (1 - popDensity):
           new_resistances = {}
           for resistant in self.resistances:
               if random.random() < 1 - self.mutProb:
                   new_resistances[resistant] = self.resistances[resistant]
               else:
                   new_resistances[resistant] = not(self.resistances[resistant])
           return ResistantVirus(self.maxBirthProb, self.clearProb, new_resistances, self.mutProb)
           
       raise NoChildException()

class TreatedPatient(Patient):
   """
   Representation of a patient. The patient is able to take drugs and his/her
   virus population can acquire resistance to the drugs he/she takes.
   """

   def __init__(self, viruses, maxPop):
       """
       Initialization function, saves the viruses and maxPop parameters as
       attributes. Also initializes the list of drugs being administered
       (which should initially include no drugs).              

       viruses: The list representing the virus population (a list of
       virus instances)

       maxPop: The  maximum virus population for this patient (an integer)
       """
       Patient.__init__(self, viruses, maxPop)
       self.activeDrugs = []

   def addPrescription(self, newDrug):
       """
       Administer a drug to this patient. After a prescription is added, the
       drug acts on the virus population for all subsequent time steps. If the
       newDrug is already prescribed to this patient, the method has no effect.

       newDrug: The name of the drug to administer to the patient (a string).

       postcondition: The list of drugs being administered to a patient is updated
       """
       if newDrug not in self.activeDrugs:
           self.activeDrugs.extend([str(newDrug)])

   def getPrescriptions(self):
       """
       Returns the drugs that are being administered to this patient.

       returns: The list of drug names (strings) being administered to this
       patient.
       """
       return self.activeDrugs

   def getResistPop(self, drugResist):
       """
       Get the population of virus particles resistant to the drugs listed in
       drugResist.       

       drugResist: Which drug resistances to include in the population (a list
       of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

       returns: The population of viruses (an integer) with resistances to all
       drugs in the drugResist list.
       """
       resistant_viruses = 0
       virus_resistant = False
       
       for virus in self.viruses:
           virus_resistant = True
           for drug in drugResist:
               if not(virus.isResistantTo(drug)):
                   virus_resistant = False
           
           if virus_resistant:
               resistant_viruses += 1
               
       return resistant_viruses

   def update(self):
       """
       Update the state of the virus population in this patient for a single
       time step. update() should execute these actions in order:

       - Determine whether each virus particle survives and update the list of
         virus particles accordingly

       - The current population density is calculated. This population density
         value is used until the next call to update().

       - Based on this value of population density, determine whether each 
         virus particle should reproduce and add offspring virus particles to 
         the list of viruses in this patient.
         The list of drugs being administered should be accounted for in the
         determination of whether each virus particle reproduces.

       returns: The total virus population at the end of the update (an
       integer)
       """
	newViruses = []
	for index, virus in reversed( list( enumerate( self.viruses ) ) ):
		if virus.doesClear():
			# print "Virus clears"
			# pop virus from viruses list
			self.viruses.pop( index )
		else:
				popDensity = self.getTotalPop()/float(self.maxPop)
		try:
			# determine if surving virus reproduces
			# append any offspring to new virus list
			newViruses.append( virus.reproduce( popDensity, self.activeDrugs ) )
		except NoChildException:
			continue
	# print "self.viruses =", self.viruses
	# print "newViruses =",  newViruses
	# add the new viruses to the list of patient viruses
	self.viruses = self.viruses + newViruses
		# print self.viruses
	return self.getTotalPop()
		
#
PROBLEM 5

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                      mutProb, numTrials):
   """
   Runs simulations and plots graphs for problem 5.

   For each of numTrials trials, instantiates a patient, runs a simulation for
   150 timesteps, adds guttagonol, and runs the simulation for an additional
   150 timesteps.  At the end plots the average virus population size
   (for both the total virus population and the guttagonol-resistant virus
   population) as a function of time.

   numViruses: number of ResistantVirus to create for patient (an integer)
   maxPop: maximum virus population for patient (an integer)
   maxBirthProb: Maximum reproduction probability (a float between 0-1)        
   clearProb: maximum clearance probability (a float between 0-1)
   resistances: a dictionary of drugs that each ResistantVirus is resistant to
                (e.g., {'guttagonol': False})
   mutProb: mutation probability for each ResistantVirus particle
            (a float between 0-1). 
   numTrials: number of simulation runs to execute (an integer)
   
   """
   viruses = []
   avg = [0] * 150
   for i in range(75): #change
       viruses.extend([ResistantVirus(maxBirthProb, clearProb,resistances.copy(), mutProb)])
       
   for i in range(5):
       patient = TreatedPatient(viruses, maxPop)
       
       for i in range(150):
           avg[i] += patient.update()

   for i in range(150):
      avg[i] = avg[i] / float(5) #change
   print avg
   pylab.figure(1)
   pylab.title("ResistantVirus simulation")
   pylab.plot(avg , label = "Total ResistantVirus", )
   #pylab.plot(guttagonol , label = "Guttagonol-Resistant Virus")
   pylab.xlabel("time step")
   pylab.ylabel("# viruses")
   pylab.legend()
   #pylab.show()
   

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                      mutProb, numTrials):
   steps = 300
   treatOnStep = 150
   trialResultsTot = [[] for s in range(steps)]
   trialResultsRes = [[] for s in range(steps)]
   for a in range(numTrials):
       viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                 resistances.copy(), mutProb)
                  for v in range(numViruses)]
       patient = TreatedPatient(viruses, maxPop)
       for step in range(steps):
           if step == treatOnStep:
               patient.addPrescription("guttagonol")
           patient.update()
           trialResultsTot[step].append(patient.getTotalPop())
           trialResultsRes[step].append(patient.getResistPop(["guttagonol"]))
   resultsSummaryTot = [sum(l) / float(len(l)) for l in trialResultsTot]
   resultsSummaryRes = [sum(l) / float(len(l)) for l in trialResultsRes]
   print resultsSummaryTot
   print
   print resultsSummaryRes


def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials):
    avg = [0] * 300
    avg1 = [0] * 300
    for i in range(numTrials):
        viruses = []
        for j in range(numViruses):
            viruses.extend([ResistantVirus(maxBirthProb, clearProb , resistances, mutProb )])

        patient = TreatedPatient(viruses, maxPop)
        for k in range(300):
            if k == 150:
                patient.addPrescription("guttagonol")  
            patient.update()
            avg[k] = float(avg[k]) + patient.getTotalPop()
            avg1[k] = float(avg1[k]) + patient.getResistPop(["guttagonol"]) 
     
    for l in range(300):
        avg[l] = avg[l] / float(numTrials)
        avg1[l] = avg1[l] / float(numTrials)
        
    pylab.figure("ResistantVirus simulation")
    pylab.title("ResistantVirus simulation")
    pylab.plot(avg,label = "Total Virus Population")
    pylab.plot(avg1,label = "Resistant Virus Population")
    pylab.xlabel("time step")
    pylab.ylabel("#viruses")
    pylab.legend()
    pylab.show()
    
simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)