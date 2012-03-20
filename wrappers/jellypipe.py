from jelly import *
from types import *

def getJellyPipeline(inputFastqList=None, inBaseName=None, outputFolder=None, prefix=None, suffix=None, dependsOn=[], **kwargs):
    if inputFastqList is None:
        sys.exit(1)
    if outputFolder is None:
        sys.exit(1)



    inputFastqReals = []
    inputBaseNames  = []

    for inputFastq in inputFastqList:
        if not os.path.exists(inputFastq):
            print " INPUT FASTQ FILE " + inputFastq + " DOES NOT EXISTS"
            sys.exit(1)

        inputFastqReal = os.path.abspath(os.path.realpath(os.path.normpath(inputFastq)))
        inputFastqReals.append(inputFastqReal)
        inputBaseNames.append(os.path.basename(inputFastq))

        if not os.path.isfile(inputFastqReal):
            print " INPUT FASTQ FILE " + inputFastq + " ("+inputFastqReal+") IS NOT A FILE"
            #sys.exit(1)



    if prefix is None:
        prefix = ""
    else:
        prefix += '_'

    if suffix is None:
        suffix = ""
    else:
        suffix = '_' + suffix

    if dependsOn is None:
        dependsOn = []


    if not os.path.exists(outputFolder):
        print " OUTPUT FOLDER " + outputFolder + " DOES NOT EXISTS"
        #sys.exit(1)

    outputFolderReal = os.path.abspath(os.path.realpath(os.path.normpath(outputFolder)))

    if not os.path.isdir(outputFolderReal):
        print " OUTPUT FOLDER " + outputFolder + " ("+str(inputFastqReal)+") IS NOT A FOLDER"
        sys.exit(1)


    #inBaseName  = os.path.commonprefix(inputBaseNames)
    outBaseName = os.path.abspath(os.path.realpath(os.path.normpath(os.path.join(outputFolder, prefix+inBaseName+suffix))))
    outNickName = os.path.basename(outBaseName)

    jc = jellyCount(inputFastqReals , inBaseName, output=outBaseName + "_mer_counts", stats=outBaseName + ".stats", **kwargs)
    jm = jellyMerge([jc.getOutput  ], inBaseName, output=outBaseName + ".jf",                                       **kwargs)
    jh = jellyHisto([jm.getOutput  ], inBaseName, output=outBaseName + ".histo",                                    **kwargs)

    f0 = joblaunch.Job(outNickName + '_JellyCount', [ jc ], deps=dependsOn)
    f1 = joblaunch.Job(outNickName + '_JellyMerge', [ jm ], deps=[f0] )
    f2 = joblaunch.Job(outNickName + '_JellyHisto', [ jh ], deps=[f1] )

    res = [
        [ f0.getId(), f0 , jc ],
        [ f1.getId(), f1 , jm ],
        [ f2.getId(), f2 , jh ]
    ]

    return res


def getJellyMergePipeline(inputJFList=None, inBaseName=None, outputFolder=None, prefix=None, suffix=None, dependsOn=[], **kwargs):
    if inputJFList is None:
        sys.exit(1)
    if outputFolder is None:
        sys.exit(1)

    if not os.path.exists(outputFolder):
        print " OUTPUT FOLDER " + outputFolder + " DOES NOT EXISTS"
        sys.exit(1)

    outputFolderReal = os.path.abspath(os.path.realpath(os.path.normpath(outputFolder)))

    if not os.path.isdir(outputFolderReal):
        print " OUTPUT FOLDER " + outputFolder + " ("+inputFastqReal+") IS NOT A FOLDER"
        sys.exit(1)

    if prefix is None:
        prefix = ""
    else:
        prefix += '_'

    if suffix is None:
        suffix = ""
    else:
        suffix = '_' + suffix

    if dependsOn is None:
        dependsOn = []

    outBaseName = os.path.abspath(os.path.realpath(os.path.normpath(os.path.join(outputFolder, prefix+inBaseName+suffix))))
    outNickName = os.path.basename(outBaseName)

    jm = jellyMerge(inputJFList     , inBaseName, output=outBaseName + ".jf",                                       **kwargs)
    jh = jellyHisto([jm.getOutput  ], inBaseName, output=outBaseName + ".histo",                                    **kwargs)
    js = jellyStats([jm.getOutput  ], inBaseName, output=outBaseName + ".stats",                                    **kwargs)

    f0 = joblaunch.Job(outNickName + '_JellyMerge', [ jm ], deps=dependsOn )
    f1 = joblaunch.Job(outNickName + '_JellyHisto', [ jh ], deps=[f0] )
    f2 = joblaunch.Job(outNickName + '_JellyStats', [ js ], deps=[f0] )

    res = [
        [ f0.getId(), f0 , jm ],
        [ f1.getId(), f1 , jh ],
        [ f2.getId(), f2 , js ]
    ]

    return res
