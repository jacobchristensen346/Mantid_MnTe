# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# used to extract the data from a 2D mantid workspace

start_dir = '/SNS/CORELLI/IPTS-26082/shared/MnTe_370K-330K_CC/' # change path where data will be saved
name = 'normData_MnTe_370K-330K_CC_fft_linecut_x00.txt' # change name for data
path = start_dir + name

ws = mtd['linecut'] # name of workspace to have data extracted from
for i in range (ws.getNumberHistograms()):
    x = ws.readX(i)
    y = ws.readY(i)
x = np.delete(x,len(x)-1)
np.savetxt(path,np.transpose([x,y]))
