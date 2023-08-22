from mantid.simpleapi import *
from mantid.api import IMDHistoWorkspace
from mantid.geometry import SymmetryOperationFactory
import matplotlib.pyplot as plt
import numpy as np
import time

# used to calculate the 3D-pdf of a multidimensional histogram mantid workspace 

start_dir = '/SNS/CORELLI/IPTS-26082/shared/MnTe_370K-330K_CC/' # update according to desired folder
name_fft = 'normData_MnTe_370K-330K_CC_fft.nxs' # update according to desired name
name_int = 'normData_MnTe_370K-330K_CC_int.nxs' # update according to desired name
save_fft = start_dir+name_fft
save_int = start_dir+name_int

slice_ws = True # set to true to slice the workspace
ws = 'normData_MnTe_370K-330K_CC' # update according to name of workspace to be processed

# Slice the data set to desired bins to speed up the data processing.
# Make sure workspace remains centered at origin
if slice_ws:
	SliceMDHisto(InputWorkspace=str(ws),
   		Start='200,187,200',
        	End='801,747,801',
              	OutputWorkspace='slice')
	ws = 'slice'
 
# transpose as needed to order dimensions as [H,0,0], [0,K,0], [0,0,L]
ws = TransposeMD(str(ws),Axes=[0,2,1])

# Delete uneeded workspaces to free up memory
#DeleteWorkspace(str(ws))
#if str(ws1) != str(ws):
	#DeleteWorkspace(str(ws1))

# DeltaPDF, 3D   
DeltaPDF3D(InputWorkspace=ws,
	IntermediateWorkspace='intermediate',
        OutputWorkspace='fft',Method='KAREN',KARENWidth=7)

# Delete uneeded workspace to free up memory  
#DeleteWorkspace('transpose')   

# Final step, to smooth the data with Gaussian kernel.           
SmoothMD(InputWorkspace='fft',
         WidthVector='1,1,1',
         Function='Gaussian',
         OutputWorkspace='fft_smooth')
         
# Save resulting fft and intermediate workspaces
SaveMD(InputWorkspace='fft_smooth',FileName=save_fft)
SaveMD(InputWorkspace='intermediate',FileName=save_int)
