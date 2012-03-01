#!/usr/bin/python
import scipy.stats as ss
import scipy as sp
import numpy as np
import sys
import os
import math
#from StringIO import StringIO

#http://stackoverflow.com/questions/2896179/fitting-a-gamma-distribution-with-python-scipy


#sys.argv.append("../out/Data_0_mer/F5/F5_Illumina.histo")

min            = 4      # min line in histogram
max            = 201    # max line in histogram
prop           = 10000  # sampling of histogram
propMaxAllowed = .90    # how much % of the peak should be looked as options to peak (closer to mean)
gammaSampling  = 30000  # number of random numbers to test

#############
# CHECK FILE
#############
if len(sys.argv) < 2:
    print "NO INPUT FILE PASSED"
    exit(1)

infile = sys.argv[1]

if not infile or infile == '' or infile is None:
    print "NO INPUT FILE DEFINED"
    exit(2)

if not os.path.exists(infile):
    print "INPUT FILE " + infile + " DOES NOT EXISTS"
    exit(3)

print "INPUT FILE " + infile
basename = os.path.basename(infile) + ".dist.gamma"


if False:
    #############
    # SELF TEST
    #############
    alpha=5
    loc=100.5
    beta=22
    data=ss.gamma.rvs(alpha,loc=loc,scale=beta,size=gammaSampling)
    print(data)
    # [ 202.36035683  297.23906376  249.53831795 ...,  271.85204096  180.75026301
    #   364.60240242]
    #Here we fit the data to the gamma distribution:

    fit_alpha,fit_loc,fit_beta=ss.gamma.fit(data)
    print(fit_alpha,fit_loc,fit_beta)
    # (5.0833692504230008, 100.08697963283467, 21.739518937816108)

    print(alpha,loc,beta)
    # (5, 100.5, 22)
    exit(0)


#############
# READ HISTOGRAM
#############
print "READING HISTOGRAM"
exp_data=[]
d = open(infile, 'r')
for line in d:
    line  = line.rstrip()
    cols  = line.rsplit(" ")
    pos   = int(cols[0])
    count = int(cols[1])
    if pos <= min:
        continue
    if pos >= max:
        continue
    #print cols
    maxrange=int(count/prop)
    for i in range(maxrange):
        exp_data.append(pos)
d.close
#print exp_data
#exit(0)



#############
# PRINT INPUT TABLE
#############
print "PRINTING INPUT TABLE"
t = open(basename+'.table.in', 'w')
t.write(str(exp_data))
t.close

#############
# PRINT INPUT HISTOGRAM
#############
print "PRINTING INPUT HISTOGRAM"
bins = np.arange(min,max)
histogramOrig = np.histogram(exp_data, bins=bins, normed=True)[0]
#histogramOrig = np.histogram(exp_data, bins=bins)[0]
ho = open(basename+'.histo.in', 'w')
for i in range(len(histogramOrig)):
    ho.write(str(i) + "\t" + str(histogramOrig[i]) + "\n")
ho.close







#############
# DO FITTING
#############
print "LOADING ARRAY"
data                         = sp.array(exp_data)
print "FITTING"
fit_alpha, fit_loc, fit_beta = ss.gamma.fit(data, loc=0)


#############
# GET STATISTICS
#############
print "PRITING STATISTICS"
s=open(basename+'.stats', 'w')
s.write("Alpha " + str(fit_alpha) + "\n")
s.write("Loc   " + str(fit_loc)   + "\n")
s.write("Beta  " + str(fit_beta)  + "\n")

#data_rvs            = ss.gamma.rvs(   fit_alpha, loc=fit_loc, scale=fit_beta, size=gammaSampling) # random variates
data_stats_mean     = ss.gamma.stats( fit_alpha, loc=fit_loc, scale=fit_beta, moments='m')
data_stats_var      = ss.gamma.stats( fit_alpha, loc=fit_loc, scale=fit_beta, moments='v')
data_stats_skew     = ss.gamma.stats( fit_alpha, loc=fit_loc, scale=fit_beta, moments='s')
data_stats_kurtosis = ss.gamma.stats( fit_alpha, loc=fit_loc, scale=fit_beta, moments='k')
data_median         = ss.gamma.median(fit_alpha, loc=fit_loc, scale=fit_beta)
data_stdvar         = math.sqrt(data_stats_var)
#data_accu           = plt.semilogy(np.abs(x - gamma.ppf(prb, a)) + 1e-20)

#s.write("RVS\n" + str(data_rvs) + "\n")
s.write("STATS\n")
s.write("  MEAN     " + str(data_stats_mean) + "\n")
s.write("  VAR      " + str(data_stats_var) + "\n")
s.write("  SKEW     " + str(data_stats_skew) + "\n")     #assimetry
s.write("  KURTOSIS " + str(data_stats_kurtosis) + "\n") #tailness
s.write("  MEDIAN   " + str(data_median) + "\n")
s.write("  STDVAR   " + str(data_stdvar) + "\n")

peak = data_stats_mean
if data_stats_skew > 0:
    peak = int(peak + .5)
else:
    peak = int(peak)





probs={}
t=open(basename+'.histo.out', 'w')
a=open(basename+'.histo.acc', 'w')
for i in range(min, max+1):
    data_pdf = ss.gamma.pdf(i, fit_alpha, loc=fit_loc, scale=fit_beta)             # probability density function
    data_pdf = round(data_pdf, 6)

    data_cdf = ss.gamma.cdf(i, fit_alpha, loc=fit_loc, scale=fit_beta)             # cumulative density function
    data_cdf = round(data_cdf, 6)


    t.write(str(i) + "\t" + str(data_pdf) + "\n")
    a.write(str(i) + "\t" + str(data_cdf) + "\n")

    if str(data_pdf) in probs:
        probs[data_pdf] = [ i, probs[data_pdf] ]
    else:
        probs[data_pdf] = [ i ]

    #print "PDF " + str(i) + " " + str(data_pdf)
    #print "CDF " + str(i) + " " + str(data_cdf)
t.close()
a.close()

probsNum = probs.keys()
probsNum.sort()
probsNum.reverse()
probsMax = probsNum[0]
distPeak = 1e10
peak2    = -1
peaks    = {}
#print "PROBS MAX " + str(probsMax)
for probsN in probsNum:
    #print "PROBS NUM " + str(probsN)
    if probsN <= ( propMaxAllowed * probsMax ):
        #print "  DELETING " + str(probsN)
        del probs[probsN]
    else:
        #print " KEEPING " + str(probsN) + " BECAUSE > " + str(.9 * probsMax)
        poses=probs[probsN]
        #data_stats_mean
        #print poses
        for pos in poses:
            dist = abs(peak - pos)
            peaks[pos] = 1
            #print "  DIST " + str(dist)
            if dist < distPeak:
                distPeak = dist
                peak2    = pos
peaksL = peaks.keys()
peaksL.sort()
s.write("DISTANCE TO PEAK " + str(distPeak)        + "\n")
s.write("PEAK1            " + str(peak)            + "\n")
s.write("PEAK2            " + str(peak2)           + "\n")
s.write("PEAKS .95        " + str(peaksL)          + "\n")
s.write("PROBS MAX        " + str(probsMax)        + "\n")
s.write("MAX POS          " + str(probs[probsMax]) + "\n")





#dataBack = data_rvs.tolist()
#dataBack.sort()

#s.write("BINS\n" + str(bins) + "\n");
#s.write("MIN " + str(dataBack[1]) + " MAX " + str(dataBack[-1]) + "\n");
s.close




from scipy import optimize as optimize

dista=[]
for pos in range(0, len(exp_data)):
    yR = exp_data[pos]
    yT = ss.gamma.pdf(pos, fit_alpha, loc=fit_loc, scale=fit_beta)
    err = yT - yR
    dista.append(err)
    #print "POS " + str(pos) + " Real " + str(int(yR)) + " CALC " + str(int(yT)) + " ERR " + str(err)
    #fit_alpha, loc=fit_loc, scale=fit_beta
    #data_pdf = ss.gamma.pdf(i, fit_alpha, loc=fit_loc, scale=fit_beta)             # probability density function
    #data_pdf = round(data_pdf, 6)

def getfunc(x):
    res=[]
    for y in x:
        if y >= len(exp_data) or y < 0:
            res.append(0)
        else:
            res.append(exp_data[int(y)])
    return res
def getcalc(x):
    res=[]
    return ss.gamma.pdf(x, fit_alpha, loc=fit_loc, scale=fit_beta)

errfunc = lambda x: getcalc(x) - getfunc(x)
p1, success = optimize.leastsq(errfunc, [ fit_alpha, fit_loc, fit_beta ])
print "P1      " + str(p1)
print "SUCCESS " + str(success)
print (fit_alpha, fit_loc, fit_beta)


u=open(basename+'.histo.out2', 'w')
for i in range(min, max+1):
    data_pdf = ss.gamma.pdf(i, p1[0], loc=p1[1], scale=p1[2])             # probability density function
    data_pdf = round(data_pdf, 6)

    u.write(str(i) + "\t" + str(data_pdf) + "\n")

    #if str(data_pdf) in probs:
    #    probs[data_pdf] = [ i, probs[data_pdf] ]
    #else:
    #    probs[data_pdf] = [ i ]

    #print "PDF " + str(i) + " " + str(data_pdf)
    #print "CDF " + str(i) + " " + str(data_cdf)
u.close()


#############
# PRINT TABLE OUT
#############
#print "PRINTING TABLE OUT"
#t = open(basename+'.table.out', 'w')
#t.write(str(dataBack))
#t.close



#############
# PRINT HISTOGRAM OUT
#############
#print "PRINTING HISTOGRAM OUT"
#histogram = np.histogram(dataBack, bins=bins, normed=True)[0]
#histogram = np.histogram(dataBack, bins=bins)[0]
#h = open(basename+'.histo.out', 'w')
#for i in range(len(histogram)):
#    h.write(str(i) + "\t" + str(histogram[i]) + "\n")
#h.close


print "FINISHED"


#The normal distribution has two parameters: 
#a location parameter MI and a scale parameter SIGMA. 
#In practice the normal distribution is often parameterized 
#in terms of the squared scale SIGMA^2, which corresponds 
#to the variance of the distribution.


#A shape parameter is any parameter of a probability 
#distribution that is neither a location parameter nor a 
#scale parameter (nor a function of either or both of 
#these only, such as a rate parameter). Such a parameter 
#must affect the shape of a distribution rather than 
#simply shifting it (as a location parameter does) or 
#stretching/shrinking it (as a scale parameter does).


#Skewness: indicator used in distribution analysis as a sign of asymmetry and deviation from a normal distribution. 
#Interpretation: 
#Skewness > 0 - Right skewed distribution - most values are concentrated on left of the mean, with extreme values to the right.
#Skewness < 0 - Left skewed distribution - most values are concentrated on the right of the mean, with extreme values to the left.
#Skewness = 0 - mean = median, the distribution is symmetrical around the mean.

#Kurtosis - indicator used in distribution analysis as a sign of flattening or "peakedness" of a distribution. 
#Interpretation: 
#Kurtosis > 3 - Leptokurtic distribution, sharper than a normal distribution, with values concentrated around the mean and thicker tails. This means high probability for extreme values.
#Kurtosis < 3 - Platykurtic distribution, flatter than a normal distribution with a wider peak. The probability for extreme values is less than for a normal distribution, and the values are wider spread around the mean.
#Kurtosis = 3 - Mesokurtic distribution - normal distribution for example.



#data2.sort()
##print(data2.tolist())

#gammainc = sp.special.gammainc(fit_alpha, 36)
#print gammainc

#int_to_zero = sp.special.gdtr(fit_alpha, fit_beta, 200)
#print int_to_zero

#int_to_inf = sp.special.gdtrc(fit_alpha, fit_beta, 0)
#print int_to_inf

#ln = sp.special.gammaln(data2)
#print ln

#ln = sp.special.gammaln(data2)
#print ln


#sp.special.gammainc(fit_alpha, 0)
#sp.special.gammaincinv(fit_alpha, 0)
#sp.special.gammaincc(fit_alpha, 0)
#sp.special.gammainccinv(fit_alpha, 0)

