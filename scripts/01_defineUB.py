iptsfolder= "/SNS/CORELLI/IPTS-16390/"
nxdir=iptsfolder + "nexus/"
ccdir = iptsfolder + "shared/autoreduce/"
scriptdir = iptsfolder+"shared/scripts/"

BinParm='0.3,0.005,15'

# 005 K
start = 37338
stop = 37397

runs = range(start,stop+1,3)
temp = '005K'

toMerge1=[]
toMerge2=[]

LoadCC = False

for r in runs:
    print('Processing run : %s' %r)
    ows='COR_'+str(r)
    omd=ows+'_md'
    toMerge1.append(ows)
    toMerge2.append(omd)

    if not mtd.doesExist(ows):
        if LoadCC :
            filename=ccdir+'CORELLI_'+str(r)+'_elastic.nxs'
            if not mtd.doesExist(ows):
                LoadNexus(Filename=filename, OutputWorkspace=ows)
        else:
            filename=nxdir+'CORELLI_'+str(r)+'.nxs.h5'
            if not mtd.doesExist(ows):
                LoadEventNexus(Filename=filename, OutputWorkspace=ows,FilterByTimeStop=120)

    #get total proton_charge from run log
    owshandle=mtd[ows]
    lrun=owshandle.getRun()
    pclog=lrun.getLogData('proton_charge')
    pc=sum(pclog.value)/1e12
    print('the current proton charge :'+ str(pc))

    ConvertUnits(InputWorkspace=ows, OutputWorkspace=ows, Target='dSpacing')
    Rebin(InputWorkspace=ows, OutputWorkspace=ows, Params=BinParm)
    SetGoniometer(ows,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
    ConvertToMD(InputWorkspace=ows,
                OutputWorkspace=omd,
                QDimensions='Q3D',
                dEAnalysisMode='Elastic',
                Q3DFrames='Q_sample',
                LorentzCorrection='1',
                MinValues="-15,-15,-25",
                MaxValues="15,15,25",
                Uproj='1,0,0',
                Vproj='0,1,0',
                Wproj='0,0,1')
data=GroupWorkspaces(toMerge1)
mdQsample=GroupWorkspaces(toMerge2)
mergedMD=MergeMD(toMerge2)

UBfile=scriptdir+'NCNO_005K.mat'

# Finding peaks in Q-sample, and save UB
FindPeaksMD(InputWorkspace='mergedMD', MaxPeaks=800,
            DensityThresholdFactor=2000, OutputWorkspace='peaks')

# To keep the UB consistent
if not os.path.isfile(UBfile):
    FindUBUsingLatticeParameters(PeaksWorkspace='peaks', a=10.28, b=10.28, c=10.28,
                                 alpha=90, beta=90, gamma=90, Tolerance=0.12)
else:
    LoadIsawUB(InputWorkspace='peaks', Filename=UBfile)
    IndexPeaks(PeaksWorkspace='peaks', Tolerance=0.10,RoundHKLs=False)

IndexPeaks(PeaksWorkspace='peaks', Tolerance=0.10, RoundHKLs=False)
OptimizeLatticeForCellType(PeaksWorkspace='peaks', Apply=True,
                           Tolerance=0.10)
SaveIsawUB(InputWorkspace='peaks', Filename=UBfile)
