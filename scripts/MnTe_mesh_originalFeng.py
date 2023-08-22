iptsfolder= "/SNS/CORELLI/IPTS-26082/"
nxdir=iptsfolder + "nexus/"
ccdir = iptsfolder + "shared/autoreduce/"
scriptdir = iptsfolder+"shared/scripts/"

from mantid.simpleapi import *
from mantid.api import *


BinParm='0.3,0.005,15'
BinDirect = ['1,0,0', '0,0,1', '0,1,0']
BinLimit = ['-10,-10,-10', '10,10,10']

temp = '330K'
outputdir = iptsfolder+"shared/"+temp+"/"

if not mtd.doesExist('maskfile'):
    maskfile = LoadMask(Instrument='CORELLI',
                    InputFile=scriptdir+'CCR.xml')
maskfile = mtd['maskfile']

# MnTe orientation
start = 180226
stop = 180240

runs = range(start, stop+1,1)

runs = [180356]

UBfile=scriptdir+'MnTe_006K.mat'

toMerge1=[]
toMerge2=[]


LoadCC = False
ConvertToHKL=1

for r in runs:
    print('Processing run : %s' %r)
    ows='COR_'+str(r)

    if not mtd.doesExist(ows):
        if LoadCC:
            filename=ccdir+'CORELLI_'+str(r)+'_elastic.nxs'
            if not mtd.doesExist(ows):
                LoadNexus(Filename=filename, OutputWorkspace=ows)
                #CopyInstrumentParameters(calibration, OutputWorkspace=ows)
                MaskDetectors(Workspace=ows,MaskedWorkspace=maskfile)
                #get total proton_charge from run log
                owshandle=mtd[ows]
                lrun=owshandle.getRun()
                pclog=lrun.getLogData('proton_charge')
                pc=sum(pclog.value)/1e12
                #owshandle /= pc
                print('the current proton charge :'+ str(pc))
                ConvertUnits(InputWorkspace=ows, OutputWorkspace=ows, Target='dSpacing')
                Rebin(InputWorkspace=ows, OutputWorkspace=ows, Params=BinParm)
                SetGoniometer(ows,Axis0="BL9:Mot:Sample:Axis3,0,1,0,1")
        else:
            filename=nxdir+'CORELLI_'+str(r)+'.nxs.h5'
            if not mtd.doesExist(ows):
                LoadEventNexus(Filename=filename, OutputWorkspace=ows) #,FilterByTimeStop=120)
                #CopyInstrumentParameters(calibration, OutputWorkspace=ows)
                MaskDetectors(Workspace=ows,MaskedWorkspace=maskfile)
                #get total proton_charge from run log
                owshandle=mtd[ows]
                lrun=owshandle.getRun()
                pclog=lrun.getLogData('proton_charge')
                pc=sum(pclog.value)/1e12
                #owshandle /= pc
                print('the current proton charge :'+ str(pc))
                ConvertUnits(InputWorkspace=ows, OutputWorkspace=ows, Target='dSpacing')
                Rebin(InputWorkspace=ows, OutputWorkspace=ows, Params=BinParm)
                SetGoniometer(ows,Axis0="BL9:Mot:Sample:Axis3,0,1,0,1")
    if os.path.isfile(UBfile):
        LoadIsawUB(InputWorkspace=ows,Filename=UBfile)
    if ConvertToHKL:
        omd=ows+'_mdHKL'
        #if not mtd.doesExist(omd):
        ConvertToMD(InputWorkspace=ows,
                    OutputWorkspace=omd,
                    QDimensions='Q3D',
                    dEAnalysisMode='Elastic',
                    Q3DFrames='HKL',
                    Uproj=BinDirect[0],
                    Vproj=BinDirect[1],
                    Wproj=BinDirect[2],
                    QConversionScales='HKL',
                    LorentzCorrection='1',
                    MinValues=BinLimit[0],
                    MaxValues=BinLimit[1])
    else:
        omd=ows+'_mdQsample'
        if not mtd.doesExist(omd):
            ConvertToMD(InputWorkspace=ows,
                         OutputWorkspace=omd,
                         QDimensions="Q3D",
                         dEAnalysisMode="Elastic",
                         Q3DFrames="Q_sample",
                         LorentzCorrection=1,
                         MinValues="-15,-15,-15",
                         MaxValues="15,15,15",
                         Uproj='1,0,0',
                         Vproj='0,1,0',
                         Wproj='0,0,1')

    toMerge1.append(ows)
    toMerge2.append(omd)

data=GroupWorkspaces(toMerge1)
md=GroupWorkspaces(toMerge2)
mergedMDH0L=MergeMD(toMerge2)
