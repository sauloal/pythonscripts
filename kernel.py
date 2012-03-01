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
basename = os.path.basename(infile) + ".dist.poly"


if False:
#if True:
    #############
    # SELF TEST
    #############
    def measure(n):
        #"Measurement model, return two coupled measurements."
        m1 = np.random.normal(size=n)
        m2 = np.random.normal(scale=0.5, size=n)
        return m1+m2, m1-m2

    m1, m2 = measure(2000)
    xmin = m1.min()
    xmax = m1.max()
    ymin = m2.min()
    ymax = m2.max()

    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    print values
    kernel = ss.gaussian_kde(values)
    print kernel
    Z = np.reshape(kernel(positions).T, X.shape)
    print Z

#############
# READ HISTOGRAM
#############
print "READING HISTOGRAM"
exp_data_x=[]
exp_data_y=[]
exp_data_h=[]
d = open(infile, 'r')
for line in d:
    line  = line.rstrip()
    cols  = line.rsplit(" ")
    pos   = int(cols[0])
    count = int(cols[1])
    if pos <= min:
        #pass
        continue
    if pos >= max:
        #pass
        continue
#    if len(exp_data_x) == 0:
#        exp_data_x.append(float(0))
#        exp_data_y.append(float(count))

    #print cols
    exp_data_x.append(float(pos))
    exp_data_y.append(float(count))

    maxrange=int(count/prop)
    for i in range(maxrange):
        exp_data_h.append(pos)


d.close
#print exp_data_x
#print exp_data_y
#exit(0)



#############
# PRINT INPUT TABLE
#############
#print "PRINTING INPUT TABLE"
#t = open(basename+'.table.in', 'w')
#t.write(str(exp_data))
#t.close



#############
# PRINT INPUT HISTOGRAM
#############
print "PRINTING INPUT HISTOGRAM"
bins = np.arange(min,max)
#histogramOrig = np.histogram(exp_data_h, bins=bins, normed=True)[0]
histogramOrig = np.histogram(exp_data_h, bins=bins)[0]
ho = open(basename+'.histo.in', 'w')
for i in range(len(histogramOrig)):
    ho.write(str(i) + "\t" + str(histogramOrig[i]) + "\n")
ho.close







#############
# DO FITTING
#############
print "LOADING ARRAY"
#datax = np.array(exp_data_x)
datay = np.array([exp_data_x, exp_data_y])
print "FITTING"
kernel = ss.gaussian_kde(datay)
print "KERNEL"
print kernel
print "DATASET"
print kernel.dataset
print "DIMENTIONS"
print kernel.d
print "DATAPOINTS"
print kernel.n
print "FACTOR"
print kernel.factor
print "COVARIANCE"
print kernel.covariance
print "INV COVARIANCE"
print kernel.inv_cov
#print "INTEGRATE"
#print kernel.integrate_box_1d(0, 200)
#print "INTEGRATE BOX"
#print kernel.integrate_box([0, 1],[200])
print "INTEGRATE EVALUATE"
print kernel.evaluate([100, 0])

exit(0)

#############
# GET STATISTICS
#############
print "PRITING STATISTICS"
s=open(basename+'.stats', 'w')

#data_stats_mean     = ss.gamma.stats( fit_alpha, loc=fit_loc, scale=fit_beta, moments='m')
#data_stats_var      = ss.gamma.stats( fit_alpha, loc=fit_loc, scale=fit_beta, moments='v')
#data_stats_skew     = ss.gamma.stats( fit_alpha, loc=fit_loc, scale=fit_beta, moments='s')
#data_stats_kurtosis = ss.gamma.stats( fit_alpha, loc=fit_loc, scale=fit_beta, moments='k')
#data_median         = ss.gamma.median(fit_alpha, loc=fit_loc, scale=fit_beta)
#data_stdvar         = math.sqrt(data_stats_var)
#data_accu           = plt.semilogy(np.abs(x - gamma.ppf(prb, a)) + 1e-20)

#s.write("STATS\n")
#s.write("  MEAN     " + str(data_stats_mean) + "\n")
#s.write("  VAR      " + str(data_stats_var) + "\n")
#s.write("  SKEW     " + str(data_stats_skew) + "\n")     #assimetry
#s.write("  KURTOSIS " + str(data_stats_kurtosis) + "\n") #tailness
#s.write("  MEDIAN   " + str(data_median) + "\n")
#s.write("  STDVAR   " + str(data_stdvar) + "\n")

#peak = data_stats_mean
#if data_stats_skew > 0:
#    peak = int(peak + .5)
#else:
#    peak = int(peak)



p = np.poly1d(z)
t=open(basename+'.histo.out', 'w')
for i in range(min, max+1):
    data_r = p(float(i))
    t.write(str(i) + "\t" + str(data_r) + "\n")

t.close()
s.close
exit(0)

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

