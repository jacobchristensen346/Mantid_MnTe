# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# used to extract signal data from a multidimensional mantid workspace

start_dir = '/SNS/CORELLI/IPTS-26082/shared/MnTe_330K_CC/' # change path where data will be saved
name = 'normData_MnTe_330K_CC' # change name for data
path = start_dir + name

ws = mtd['normData_MnTe_330K_CC'] # name of workspace to have data extracted from
ws_signal = ws.getSignalArray()
np.save(path,ws_signal,'wb')
