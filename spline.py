import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate, randn

x     = np.arange(0,5,1.0/6)
xs    = np.arange(0,5,1.0/500)

y     = np.sin(x+1) + .2*np.random.rand(len(x)) -.1

#knots = np.array([1,2,3,4])
#tck   = interpolate.splrep(x,y,s=0,k=3,t=knots,task=-1)
#ys    = interpolate.splev(xs,tck,der=0)
fp=[]
ier=111
msg=""
tck,fp,ier,msg = interpolate.splrep(x,y,s=0,k=3,full_output=True)
ys    = interpolate.splev(xs,tck, der=0)

roots = interpolate.sproot(tck, mest=10)
ints  = interpolate.splint(0, 4, tck, full_output=0)

#plt.figure()
#plt.plot(xs,ys,x,y,'x')

print "x\ty\txs\tys"
#for i in range(len(x)):
#    print str(x[i]) + "\t" + str(y[i]) + "\t" + str(xs[i]) + "\t" + str(ys[i])
for i in range(len(x)):
    #print str(x[i]) + "\t" + str(y[i])
    pass
for i in range(len(xs)):
    #print str(xs[i]) + "\t" + str(ys[i])
    pass

print str(roots)
print str(ints)
print "TCK " + str(tck)
print "FP  " + str(fp)
print "IER " + str(ier)
print "MSG " + str(msg)
