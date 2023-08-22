# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# script used to obtain linecuts through a workspace

startDir = '/SNS/CORELLI/IPTS-26082/shared/MnTe_370K-330K_CC/'
fName = 'normData_MnTe_370K-330K_CC_fft_linecut_x00.nxs'
saveName = startDir + fName

ws = mtd['fft_smooth']
ws_cut = IntegrateMDHistoWorkspace(InputWorkspace=ws,P1Bin=[-20,0,20], P2Bin=[-0.1,0.1], P3Bin=[-0.1,0.1])
ConvertMDHistoToMatrixWorkspace(InputWorkspace=ws_cut,OutputWorkspace='linecut')
SaveNexus(InputWorkspace='linecut',FileName=saveName)
