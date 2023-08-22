iptsfolder = "/SNS/CORELLI/IPTS-23929/"
nxfiledir = iptsfolder+"nexus/"
sharedir = iptsfolder+"/shared/"
ccfiledir = iptsfolder+"shared/autoreduce/"
scriptdir = iptsfolder + "/shared/scripts/"

import numpy as np

temp = '175K'

outputdir = sharedir+temp+'/'
if not os.path.isdir(outputdir):
    os.mkdir(outputdir)

dataMD = LoadMD(Filename=outputdir+'dataMD_'+temp+'.nxs', LoadHistory=False)
normMD = LoadMD(Filename=outputdir+'normMD_'+temp+'.nxs', LoadHistory=False)

data = dataMD.getSignalArray()
dataError = dataMD.getErrorSquaredArray()
norm = normMD.getSignalArray()
normError = normMD.getErrorSquaredArray()

def symmetrize(array):
    array = np.asarray(array)
    array = array[:,:,:] \
               + array[::-1,::-1,::1]\
               + array[::1,::-1,::-1]\
               + array[::-1,:: 1,::-1]\
               + array[::-1,::1,::1]\
               + array[::1,::-1,::1]\
               + array[::1,::1,::-1]\
               + array[::-1,::-1,::-1]
    return array

data = symmetrize(data)
dataError = symmetrize(dataError)
norm = symmetrize(norm)
normError = symmetrize(normError)

dataSymmMD= CloneMDWorkspace(dataMD)
normSymmMD = CloneMDWorkspace(normMD)

dataSymmMD.setSignalArray(data)
dataSymmMD.setErrorSquaredArray(dataError)
normSymmMD.setSignalArray(norm)
normSymmMD.setErrorSquaredArray(normError)

symmData = dataSymmMD/normSymmMD

SaveMD(Inputworkspace=dataSymmMD, Filename=outputdir+'dataMD_Symm_'+temp+'.nxs')
SaveMD(Inputworkspace=normSymmMD, Filename=outputdir+'normMD_Symm'+temp+'.nxs')
SaveMD(Inputworkspace=symmData, Filename=outputdir+'DataNormalized_Symm_'+temp+'.nxs')
