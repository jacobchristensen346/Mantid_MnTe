#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 20:44:50 2018

@author: 2fy
"""
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
#from lmfit import Model, Parameters
#from lmfit.models import GaussianModel, LinearModel
from scipy.interpolate import griddata

datafolder= '/SNS/CORELLI/IPTS-23929/shared/Tdep_diffuse_warming/'
#data = np.loadtxt(datafolder+'tdep_warming.index')
#temp = data[np.argsort(data[:,1]),1]
#runs = data[np.argsort(data[:,1]),0]
#runs =np.asarray(runs).astype(int)


# T = 2 K, Field up
scanlist = np.concatenate([ [174982], np.arange(175086,175158,3)] )
templist = np.concatenate( [ [6], np.arange(15,95,10),np.arange(95,171,5)] )

#print(len(scanlist))
#print(len(templist))

runs =np.asarray(scanlist).astype(int)
temp = np.asarray(templist*100).astype(int)/100.
print(templist)

print(scanlist)
print(runs)
print(temp)

# mod1 = GaussianModel(prefix='g1_')
newZ = []

fitresult = []
print(runs)
nn = 22

for idx,r in enumerate(runs[:nn]):
    infile = datafolder+'run'+str(r)+'_linecut.dat'
    if os.path.isfile(infile):
        data = np.loadtxt(datafolder+'run'+str(r)+'_linecut.dat')
        temp0 = temp[idx]
        x = data[:,0].flatten()
        z = data[:,1].flatten()
        err = data[:,2].flatten()
        y = np.ones(len(x))*temp0
        test = np.transpose([x,y,z])
        if newZ == []:
            newZ = test
        else:
            newZ = np.vstack((newZ,test))

x = newZ[:,0]
y = newZ[:,1]
z = newZ[:,2]
xi = np.linspace(4.17, 4.35, 31)
yi = temp[:nn]
print(yi)
X, Y = np.meshgrid(xi,yi)
# print(np.shape(Z))
# print(np.shape(X))
# # Z = griddata((x,y),z,(X,Y),method='cubic')
Z=z.reshape(-1,len(xi))
print(np.shape(Z))

origin = 'lower'
#X, Y = np.meshgrid(x,temp)
fig, ax = plt.subplots(figsize=(11,8.5))

cs = ax.contourf(X, Y, np.log(Z),60,
    cmap=plt.cm.jet,
     #vmin = -12.,
     #vmax = -8,
     #norm = LogNorm (vmin=Z.min(), vmax=Z.max() ),
    origin=origin)

#cs = plt.pcolormesh(X,Y,Z,
#        cmap = plt.cm.jet,
#        norm = LogNorm (vmin=Z.min(), vmax=Z.max() ),
#        )

cbar = plt.colorbar(cs)

#ax.set_xlim([0,16])
#ax.set_ylim([100,400])
ax.set_ylabel('Temperature ($K$)',fontsize=18)
ax.set_xlabel('[H,-H,0.5]-scan (rlu)',fontsize=18)
plt.title('Linecut, Warming, CC off')
plt.show()

#fig.savefig('/SNS/TOPAZ/IPTS-24689/shared/Summary/Figure_'+str(current).zfill(2)+'mA_3ndSample_caxis.png',dpi=600)
#fig.savefig('/SNS/TOPAZ/IPTS-24689/shared/summary/Figure_20mA.eps')
