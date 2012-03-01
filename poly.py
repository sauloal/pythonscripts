#!/usr/bin/python
import scipy.stats as ss
import scipy as sp
import numpy as np
import sys
import os
import math
#from StringIO import StringIO

#http://stackoverflow.com/questions/2896179/fitting-a-gamma-distribution-with-python-scipy

#http://pingswept.org/2009/01/24/least-squares-polynomial-fitting-in-python/

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
    x = np.array([0.0, 1.0, 2.0, 3.0,  4.0,  5.0])
    y = np.array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0])
    z = np.polyfit(x, y, 3)
    print z
    print "[ 0.08703704, -0.81349206,  1.69312169, -0.03968254]"
    exit(0)


#############
# READ HISTOGRAM
#############
print "READING HISTOGRAM"
exp_data_x=[]
exp_data_y=[]
exp_data_h=[]
sum_y=0
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
        pass
        #continue
    if len(exp_data_x) == 0:
        exp_data_x.append(float(0))
        exp_data_y.append(float(count))

    #print cols
    exp_data_x.append(float(pos))
    exp_data_y.append(float(count))
    sum_y += count

    maxrange=int(count/prop)
    for i in range(maxrange):
        exp_data_h.append(pos)


d.close
#print exp_data_x
#print exp_data_y
#exit(0)

exp_data_y_p = [x/sum_y for x in exp_data_y]

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
datax = np.array(exp_data_x)
datay = np.array(exp_data_y)
#datayp = np.array(exp_data_y_p)


#t = np.linspace(0, 200)
#print "T " + str(t)
#A = np.vander(datayp, 5)
#print "A " + str(A)
#(coeffs, residuals, rank, sing_vals) = np.linalg.lstsq(A, datayp)
#print "COEFFS    " + str(coeffs)
#print "RESIDUALS " + str(residuals)
#print "RANK      " + str(rank)
#print "SING_VALS " + str(sing_vals)

#f = np.poly1d(coeffs)
#print "F " + str(f)

#res = f(range(0,200))
#print "RES " + str(res)


print "FITTING"
z = np.polyfit(datax, datay, 5)



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
#p = np.poly1d(coeffs)
t=open(basename+'.histo.out', 'w')
for i in range(min, max+1):
    data_r = p(float(i))
    t.write(str(i) + "\t" + str(data_r) + "\n")

t.close()
s.close


#print z
from pylab import *
from scipy import *
from scipy import optimize as optimize
#p1, success = optimize.leastsq(errfunc, p0[:], args=(datax, datay))

#print "Z " + str(z)
#print "Z " + str(z.tolist()[:])



dista=[]
for pos in range(0, len(exp_data_y)):
    yR = exp_data_y[pos]
    yT = p(float(exp_data_x[pos]))
    err = yT - yR
    dista.append(err)
    #print "POS " + str(pos) + " Real " + str(int(yR)) + " CALC " + str(int(yT)) + " ERR " + str(err)
def getfunc(x):
    res=[]
    for y in x:
        if y >= len(exp_data_y) or y < 0:
            res.append(0)
        else:
            res.append(exp_data_y[int(y)])
    return res

errfunc = lambda x: p(x) - getfunc(x)
p1, success = optimize.leastsq(errfunc, z)
print "Z       " + str(z)
print "P1      " + str(p1)
print "SUCCESS " + str(success)


q = np.poly1d(p1)
#p = np.poly1d(coeffs)
u=open(basename+'.histo.out2', 'w')
for i in range(min, max+1):
    data_r = q(float(i))
    u.write(str(i) + "\t" + str(data_r) + "\n")

u.close()


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

