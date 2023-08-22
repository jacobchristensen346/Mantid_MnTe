from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# used to subtract workspaces from one another
# useful for removing unwanted scattering

startDir = '/SNS/CORELLI/IPTS-26082/shared/MnTe_370K-330K_inelastic/' # change path where data will be saved
fName = 'normData_MnTe_370K-330K_inelastic.nxs' # change name for data
path = startDir + fName

ws1 = 'normData_MnTe_370K-330K_CC' 
ws2 = 'normData_MnTe_370K-330K_Total'

s1 = mtd[ws1]

s2 = mtd[ws2]

diff_ws = s2 - s1

SaveMD(Inputworkspace='diff_ws',Filename=path)
