from mantid.simpleapi import *
from mantid.geometry import SymmetryOperationFactory
import matplotlib.pyplot as plt
import time
import numpy as np

IPTS = 26082
iptsfolder= "/SNS/CORELLI/IPTS-"+str(IPTS)+'/'
shareddir=iptsfolder+"shared/"
nxdir=iptsfolder + "nexus/"
ccdir = shareddir+"autoreduce/"
workdir = iptsfolder+"shared/"
scriptdir = shareddir+"scripts/"

vdir = '/SNS/CORELLI/shared/Vanadium/2021A_0211_CCR/'
if not mtd.doesExist('sa'):
    LoadNexus(Filename=vdir+'sa_CCR.nxs', OutputWorkspace='sa')
if not mtd.doesExist('flux'):
    LoadNexus(Filename=vdir+'flux_CCR.nxs', OutputWorkspace='flux')

#MaskBTP(Workspace='sa',Bank="1-48,59-91")       # top and bottom not in use

# Define if we need to load CC or not
LoadCC = 0

# large range in Q
binD = ['1,0,0', '0,0,1', '0,1,0']
binS = ['-10.01, 0.02, 10.01', '-14.01, 0.03, 14.01', '-10.01,0.02,10.01'] # may need to choose these values more carefully

# update names and run numbers according to desired temp below

start = 180226 # update this according to temperature
stop =  start + 120
temp = 'MnTe_330K_Total' # update name according to temp and whether total or elastic (elastic if LoadCC = 1)
UBfile=scriptdir+'MnTe_330K.mat' # update according to temperature


## large region at 330 K
#start = 180226
#stop =  start + 120
##temp = 'MnTe_330K_Total' 
#temp = 'MnTe_330K_CC' # use if LoadCC=1
#UBfile=scriptdir+'MnTe_330K.mat'


#runs = range(start,stop+1,1)
runs = np.arange(120)+start
print(runs)
print(len(runs))

#runs = list(range(178225, 178285+1,1))+list(range(178463,178521+1,1))
#print(len(runs))

# Loading tube calibration
tubedb = '/SNS/CORELLI/shared/calibration/tube'
LoadNexus(Filename=tubedb+'/calibration_corelli_20200109.nxs.h5', OutputWorkspace='tube_table')
 
outputdir = workdir+str(temp)+'/'
if not os.path.isdir(outputdir):
    os.mkdir(outputdir)

if mtd.doesExist('normMD'):
    DeleteWorkspace('normMD')
if mtd.doesExist('dataMD'):
    DeleteWorkspace('dataMD')

dataMD=None
normMD=None
outputfile = outputdir + 'norm_in_running.nxs'

print(len(runs))

for idx, r in enumerate(runs):
    print('Processing run : %s' %r)
    if LoadCC:
        filename=ccdir+'CORELLI_'+str(r)+'_elastic.nxs'
    else:
        filename=nxdir+'CORELLI_'+str(r)+'.nxs.h5'
    filethere = os.path.isfile(filename)
    if filethere:
        if LoadCC :
            dataR = LoadNexus(Filename=filename)
        else:
            dataR = LoadEventNexus(Filename=filename)
            ApplyCalibration(Workspace='dataR', CalibrationTable='tube_table')

        dataR  = ConvertUnits(dataR, Target="Momentum", EMode="Elastic")
        MaskDetectors(Workspace=dataR, MaskedWorkspace='sa')
        dataR=CropWorkspaceForMDNorm(InputWorkspace='dataR', XMin=2.5, XMax=10)
        SetGoniometer(dataR, Axis0="BL9:Mot:Sample:Axis3,0,1,0,1")
        LoadIsawUB(InputWorkspace=dataR, Filename=UBfile)

        ConvertToMD(InputWorkspace=dataR,
                QDimensions='Q3D',
                dEAnalysisMode='Elastic',
                Q3DFrames='Q_sample',
                LorentzCorrection='0',
                MinValues='-20.1,-20.1,-20.1',
                MaxValues='20.1,20.1,20.1',
                OutputWorkspace='md')
        MDNorm(InputWorkspace= 'md',
           SolidAngleWorkspace='sa',
           FluxWorkspace='flux',
           QDimension0= binD[0],
           QDimension1= binD[1],
           QDimension2= binD[2],
           Dimension0Name='QDimension0',
           Dimension0Binning=binS[0],
           Dimension1Name='QDimension1',
           Dimension1Binning=binS[1],
           Dimension2Name='QDimension2',
           Dimension2Binning= binS[2],
           SymmetryOperations='P 63/m m c', # input space group
           TemporaryDataWorkspace='dataMD' if mtd.doesExist('dataMD') else None,
           TemporaryNormalizationWorkspace='normMD' if mtd.doesExist('normMD') else None,
           OutputWorkspace='normData',
           OutputDataWorkspace='dataMD',
           OutputNormalizationWorkspace='normMD')
        #if np.mod(idx, 5) == 0:
        #    dataMD = mtd['dataMD']
        #    normMD= mtd['normMD']
        #    normData=dataMD/normMD
            #SaveMD(Inputworkspace='normData',
                   #Filename=outputfile)
            #normData *=1e4
    #        fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
    #        im = ax.pcolormesh(normData,
    #                           slicepoint=(None, None, 0),
    #                           vmin=0,
    #                           vmax=2e-4,
    #                           cmap='viridis'
    #                          )
    #        ax.set_xlim(-10.1,10.1)
    #        ax.set_ylim(-10.1,10.1)
    #        fig.colorbar(im, ax=ax)
    #        ax.set_title('HK0, T={:3.0f}K'.format(6))
    #        fig.show()
    #        time.sleep(10)
    #        figfile = outputdir+"normcc_330K_{}angles.png".format(str(idx).zfill(3))
    #        #fig.savefig(figfile)
    #        time.sleep(10)
    #        plt.close()
    else:
        print("file: " + filename + " not found.   Waiting for it to appear... ")
        time.sleep(120)

SaveMD(Inputworkspace='normData',Filename=outputdir+'normData_'+str(temp)+'.nxs')
SaveMD(Inputworkspace='dataMD',Filename=outputdir+'dataMD_'+str(temp)+'.nxs')
SaveMD(Inputworkspace='normMD',Filename=outputdir+'normMD_'+str(temp)+'.nxs')
