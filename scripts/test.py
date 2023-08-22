from mantid.simpleapi import *
from mantid.api import IMDHistoWorkspace
from mantid.geometry import SymmetryOperationFactory
import matplotlib.pyplot as plt
import numpy as np
import time

ws0 = mtd['normData_MnTe_370K-330K_Total']
signalArray =  ws0.getSignalArray()
errorArray = ws0.getErrorSquaredArray()
print(np.shape(signalArray))
print(len(errorArray))

signalArray1 = signalArray[0:999,:,:]
errorArray1 = errorArray[0:999,:,:]
print(np.shape(signalArray1))

ws=CreateMDHistoWorkspace(Dimensionality=3,Extents='-9.99,10.01,-14.01,14.01,-10.01,10.01', \
                           SignalInput=signalArray1,ErrorInput=errorArray1,\
                           NumberOfBins='999,934,1001',Names=('[H,0,0]','[0,0,L]','[0,K,0]'),Units='rlu,rlu,rlu')
                           
                           
slice_ws = True
ws1 = ws

# Slice the data set to desired bins to speed up the data processing.
# Make sure workspace remains centered at origin
if slice_ws:
	SliceMDHisto(InputWorkspace=ws,
   		Start='200,187,200',
        	End='801,747,801',
              	OutputWorkspace='slice')
	ws1 = 'slice'
 
# transpose to order dimensions as [H,0,0], [0,K,0], [0,0,L]
transpose = TransposeMD(str(ws1),Axes=[0,2,1])

# Delete uneeded workspaces to free up memory
#DeleteWorkspace(str(ws))
#if str(ws1) != str(ws):
	#DeleteWorkspace(str(ws1))

# DeltaPDF, 3D             
DeltaPDF3D(InputWorkspace='transpose',
           IntermediateWorkspace='intermediate',
           OutputWorkspace='fft',Method='KAREN',KARENWidth=9)

# Delete uneeded workspace to free up memory  
#DeleteWorkspace('transpose')   

# Final step, to smoooth the data with Gaussian kernel.           
SmoothMD(InputWorkspace='fft',
         WidthVector='1,1,1',
         Function='Gaussian',
         OutputWorkspace='fft_smooth')                           