from Selection import Bentley
from Selection import FrequencyDependent
import pandas
from scipy.stats import logistic
from joblib import Parallel, delayed
import multiprocessing


# Reproduce fig. 2 in Bentley et al. using a population size of 250 individuals that is initialised with a population made
# up for random numbers of individuals bearing numbers from 1 to 250, and run for 1000 time steps. vMu contains a range of
# mutation rates.
vMu = [0.004,0.008,0.016,0.032,0.064,0.128]
for i in range(0,len(vMu)):
    for j in range(0,5):
        print("i = " + str(i) + ", j = " + str(j))
        lTest = Bentley.runAll(1000,250,vMu[i],250)
        lTemp = Bentley.getCounts(lTest)
        aName = "test_" + str(i) + "_" + str(j) + ".csv"
        lTemp.to_csv(aName, sep=',')

# Try adding frequency-dependence. Here for 100 generations for a population of 250 individuals initialised as above
# with a positive frequency dependence effect of '10'
lTest = FrequencyDependent.runAllFrequency(100,250,0.128,10,250)
lTemp = Bentley.getCounts(lTest)
lTemp.to_csv('testFreq.csv')

# A function that takes a single input that specifies what values of mutation and frequency dependence to use
# because the below parallel code only works with functions that accept single inputs
def runIterate(i):
    vMu = [0.004, 0.008, 0.016, 0.032, 0.064, 0.128,0.004, 0.008, 0.016, 0.032, 0.064, 0.128]
    vBeta = [10,10,10,10,10,10,-10,-10,-10,-10,-10,-10]
    return FrequencyDependent.replicatesMean(i, "testFreqMean", 5, 1000, 250,vMu[i], vBeta[i], 250)

# running the above in parallel over 12 cores. Replace with the number of cores on your computer
vInputs = range(0,12)
results = Parallel(n_jobs=12)(delayed(runIterate)(i) for i in vInputs)
