#!/usr/bin/python
import os

def getStem(names):
    pos      = 0
    namesD   = {}
    lenName  = 0
    lastName = ""

    for name in names:
        lenName = len(name)
        #print "ORIGINAL NAME "+name+" LEN "+str(len(name))
        namesD[name] = 1
        lastName = name

    while (( len(namesD) > 1 ) and ( lenName - pos > 0 )):
        pos   -= 1
        namesD = {}
        for name in names:
            sName = name[:pos]
            #print "    CHECKING " + sName
            namesD[sName] = 1

    if ( lenName - pos > 0 ):
        stem = lastName[:pos]
        if ( stem[-1:] == '_'):
            #print "LAST UNDERSCORE"
            stem = stem[0:(len(stem)-1)]

        #print "  FOUND STEM : "+ stem
        return stem
    else:
        return None

def checkCompression(fileName):
    zip = 'none'
    if   fileName.rfind(".gz", len(fileName) - 3) != -1:
        #print "  FILE ENDS IN GZ: "+str(self.fileName.rfind(".gz", len(self.fileName) - 3))
        zip      = 'gz'
    elif fileName.rfind(".bz2", len(fileName) - 4) != -1:
        #print "  FILE ENDS IN BZ2: "+str(self.fileName.rfind(".bz2", len(self.fileName) - 4))
        zip      = 'bz2'
    elif fileName.rfind(".xz", len(fileName) - 3) != -1:
        #print "  FILE ENDS IN XZ: "+str(self.fileName.rfind(".xz", len(self.fileName) - 3))
        zip      = 'xz'
    else:
        #print "  FILE DOES NOT ENDS IN GZ"
        zip      = 'none'
    return zip

class illRun:
    """describes a illumina run"""
    def __init__ (self, filename):
        if os.path.exists(filename):
            print "INITIALIZING RUN FILE " + filename
            self.fileName     = filename
            self.strand       = self.getStrand()
            self.absPath      = self.getAbsolutePath()
            self.baseName     = self.getBaseName()
            self.shortName    = self.getShortName()
            self.fileSize     = self.getFileSize()
            self.numSeqs      = self.getNumSeqs()
            self.version      = self.getVersion()

            self.modTime      = self.getModTime()
            self.zip          = self.getIsCompressed()

        else:
            raise os.error('File '+filename+' does not exists')

    def check(self):
        fileExists = False
        sameSize   = False
        sameDate   = False

        if os.path.exists( self.absPath ):
            fileExists = True
            if os.path.getsize( self.absPath )  == self.fileSize:
                sameSize = True
            if os.path.getmtime( self.absPath ) == self.modTime:
                #print "CURR MOD TIME " + str(os.path.getmtime( self.absPath ))
                #print "REC  MOD TIME " + str(self.modTime)
                sameDate = True

        result = self.getShortName() + "\n"+\
                 "EXISTS       : " + str(fileExists) +"\n"+\
                 "SAME SIZE    : " + str(sameSize)   +"\n"+\
                 "SAME DATE    : " + str(sameDate)   +"\n";

        veredict = fileExists and sameSize and sameDate

        return ( veredict , result )

    def export(self):
        #EXPORT SELF TO basename.XML
        #TODO
        pass

    def getNumSeqs(self):
        #TODO
        return 100

    def getVersion(self):
        #TODO
        return '1.3'

    def getStrand(self):
        #TODO
        return 'fwd'

    def getAbsolutePath(self):
        absPath = getattr(self, 'absPath', None)
        if absPath:
            return self.absPath
        else:
            self.absPath = os.path.abspath(self.fileName)
            return self.absPath

    def getBaseName(self):
        baseName = getattr(self, 'baseName', None)
        if baseName:
            return self.baseName
        else:
            self.baseName = os.path.basename(self.getAbsolutePath())
            return self.baseName

    def getShortName(self):
        shortName = getattr(self, 'shortName', None)
        if shortName:
            return self.shortName
        else:
            shortName      = self.getBaseName()
            shortName      = shortName.replace(".fastq.gz", "", 1)
            shortName      = shortName.replace(".fastq",    "", 1)
            shortName      = shortName.replace(".fq",       "", 1)
            self.shortName = shortName
            return self.shortName

    def getFileSize(self):
        fileSize = getattr(self, 'fileSize', None)
        if fileSize:
            if ( fileSize == 0 ):
                raise os.error('File '+fileName+' has size 0')
            return self.fileSize
        else:
            self.fileSize = os.path.getsize(self.fileName)
            return self.fileSize

    def getFileName(self):
        return self.fileName

    def getModTime(self):
        modTime = getattr(self, 'modTime', None)
        if modTime:
            return self.modTime
        else:
            self.modTime = os.path.getmtime(self.absPath)
            return self.modTime

    def getIsCompressed(self):
        zip = getattr(self, 'zip', None)
        if zip != None:
            #print "ZIP ALREADY SETUP. RETRIEVING" + str(zip)
            return self.zip
        else:
            #print "ZIP NOT SETUP. ACQUIRING"
            zip = checkCompression(self.fileName)
            self.zip = zip
            return self.zip

    def __str__(self):
        ver, res = self.check()
        return  "File Name    : " + self.getFileName()          +"\n"+\
                "Abs Path     : " + self.getAbsolutePath()      +"\n"+\
                "Base Name    : " + self.getBaseName()          +"\n"+\
                "Short Name   : " + self.getShortName()         +"\n"+\
                "File Size    : " + str(self.getFileSize())     +"\n"+\
                "Modif Time   : " + str(self.getModTime())      +"\n"+\
                "Strand       : " + self.getStrand()            +"\n"+\
                "Zip          : " + str(self.getIsCompressed()) +"\n"+\
                "Num Seqs     : " + str(self.getNumSeqs())      +"\n"+\
                "Version      : " + str(self.getVersion())      +"\n"+\
                "Check        : " + str(ver)                    +"\n"+\
                                    res                         +"\n"



class illPair:
    """describes a illumina pairend/matepair"""

    def __init__ (self, **kwargs):
        self.runs          = kwargs.get('fastqs')
        self.insertSize    = kwargs.get('insertSize')
        self.type          = kwargs.get('type') #wgs/mp/pe

        if kwargs.has_key('name'):
            self.name = kwargs.get('name')
        else:
            self.name = self.getStem()

        #print "INITIALIZING PAIR NAME "+self.name+" WITH " + str(len(self.runs)) + " FILES TYPE " + self.type + " INSERT SIZE " + str(self.insertSize)

        self.totalFileSize = self.getTotalFileSize()
        self.totalNumSeqs  = self.getTotalNumSeqs()
        self.numRuns       = self.getNumRuns()

    def check(self):
        veredict = True
        result   = ""

        for run in self.runs:
            vere, res = run.check()
            veredict  = veredict and vere
            resl      = ["  RUN "+x for x in res.split("\n")]
            result   += "\n".join(resl) + "\n"

        status = "STATUS: "
        if veredict:
            status += "OK"
        else:
            status += "FAILED"

        result = self.getName() + "\n" + status + "\n" + result

        return (veredict, result)

    def export(self):
        #export SELF TO stem.xml
        pass

    def getName(self):
        name = getattr(self, 'name', None)
        if name:
            return self.name
        else:
            return none

    def getType(self):
        return self.type

    def getInsertSize(self):
        return self.insertSize

    def getStem(self):
        names = []
        for run in self.runs:
            names.append(run.getShortName())

        stem = getStem(names)
        if stem:
            return stem
            #print "  FOUND STEM : "+ self.stem
        else:
            #print "  NO STEM FOUND : " + str(pos)
            stem = ""
            for run in self.runs:
                stem += run.getShortName()
            return stem

    def getNumRuns(self):
        return len(self.runs)

    def getTotalFileSize(self):
        totalFileSize = getattr(self, 'totalFileSize', None)
        if totalFileSize:
            return self.totalFileSize
        else:
            totalFileSize = 0
            for run in self.runs:
                totalFileSize += run.getFileSize()
            self.totalFileSize = totalFileSize
            return self.totalFileSize

    def getTotalNumSeqs(self):
        totalNumSeqs = getattr(self, 'totalNumSeqs', None)
        if totalNumSeqs:
            return self.totalNumSeqs
        else:
            totalNumSeqs = 0
            for run in self.runs:
                totalNumSeqs += run.getNumSeqs()
            self.totalNumSeqs = totalNumSeqs
            return self.totalNumSeqs

    def getRuns(self):
        return self.runs

    def __iter__(self):
        return self.runs.__iter__()

    def __str__(self):
        fns = ""
        for run in self.runs:
            fns += "  " + run.getShortName() + "\n"

        ver, res = self.check()
        return  "Name           : "  + self.getName()               +"\n"+\
                "Type           : "  + self.getType()               +"\n"+\
                "Insert Size    : "  + str(self.getInsertSize())    +"\n"+\
                "Num Runs       : "  + str(self.getNumRuns())       +"\n"+\
                "Files          :\n" + fns                          +\
                "Total File Size: "  + str(self.getTotalFileSize()) +"\n"+\
                "Total Num Seqs : "  + str(self.getTotalNumSeqs())  +"\n"+\
                "Check          : "  + str(ver)                     +"\n"+\
                                       res


class illLibrary:
    """describes a illumina library containing illumina unities (PE/MP or singleton)"""

    def __init__(self, **kwargs):
        self.pairs = kwargs.get('pairs')
        self.name  = kwargs.get('name')

        print "INITIALIZING LIBRARY NAME " + self.name + " WITH " + str(len(self.pairs)) + " PAIRS"

        self.numPairs      = self.getNumPairs()
        self.totalNumRuns  = self.getTotalNumRuns()
        self.totalFileSize = self.getTotalFileSize()
        self.totalNumSeqs  = self.getTotalNumSeqs()

    def check(self):
        veredict = True
        result   = ""

        for pair in self.pairs:
            vere, res = pair.check()
            veredict  = veredict and vere
            resl    = ["  PAIR "+x for x in res.split("\n")]
            result += "\n".join(resl) + "\n"

        status = "STATUS: "
        if veredict:
            status += "OK"
        else:
            status += "FAILED"

        result = self.name + "\n" + status + "\n" + result

        return (veredict, result)

    def export(self):
        pass

    def getNumPairs(self):
        return len(self.pairs)

    def getTotalNumRuns(self):
        totalNumRuns = getattr(self, 'totalNumRuns', None)
        if totalNumRuns:
            return self.totalNumRuns
        else:
            totalNumRuns = 0
            for pair in self.pairs:
                totalNumRuns += pair.getNumRuns()

            self.totalNumRuns = totalNumRuns
            return self.totalNumRuns

    def getTotalFileSize(self):
        totalFileSize = getattr(self, 'totalFileSize', None)
        if totalFileSize:
            return self.totalFileSize
        else:
            totalFileSize = 0
            for pair in self.pairs:
                totalFileSize += pair.getTotalFileSize()
            self.totalFileSize = totalFileSize
            return self.totalFileSize

    def getTotalNumSeqs(self):
        totalNumSeqs = getattr(self, 'totalNumSeqs', None)
        if totalNumSeqs:
            return self.totalNumSeqs
        else:
            totalNumSeqs = 0
            for pair in self.pairs:
                totalNumSeqs += pair.getTotalNumSeqs()
            self.totalNumSeqs = totalNumSeqs
            return self.totalNumSeqs

    def getName(self):
        return self.name

    def getPairs(self):
        return self.pairs

    def __iter__(self):
        return self.pairs.__iter__()

    def __str__(self):
        pns = ""
        for pair in self.pairs:
            pns += "  " + pair.getName() + "\n"

        ver, res = self.check()
        return  "Name           : "  + self.getName()               +"\n"+\
                "Num Pairs      : "  + str(self.getNumPairs())      +"\n"+\
                "Pairs          :\n" + pns                          +\
                "Total Num Runs : "  + str(self.getTotalNumRuns())  +"\n"+\
                "Total File Size: "  + str(self.getTotalFileSize()) +"\n"+\
                "Total Num Seqs : "  + str(self.getTotalNumSeqs())  +"\n"+\
                "Check          : "  + str(ver)                     +"\n"+\
                                       res


class illDataset:
    """describes a illumina dataset containing one or more libraries"""

    def __init__(self, **kwargs):
        self.libraries     = kwargs['libraries']
        self.name          = kwargs['name']
        self.numLibraries  = self.getNumLibraries()
        self.totalNumRuns  = self.getTotalNumRuns()
        self.totalNumPairs = self.getTotalNumPairs()
        self.totalFileSize = self.getTotalFileSize()
        self.totalNumSeqs  = self.getTotalNumSeqs()
        print "INITIALIZING DATASET NAME " + self.name + " WITH " + str(self.numLibraries) + " LIBRARIES"

    def check(self):
        veredict = True
        result   = ""

        for lib in self.libraries:
           vere, res = lib.check()
           veredict  = veredict and vere
           resl      = ["  LIB "+x for x in res.split("\n")]
           result   += "\n".join(resl) + "\n"

        status = "STATUS: "
        if veredict:
           status += "OK"
        else:
           status += "FAILED"

        result = self.getName() + "\n" + status + "\n" + result

        return (veredict, result)

    def export(self):
        pass

    def getLibraries(self):
        return self.libraries

    def getName(self):
        return self.name

    def getNumLibraries(self):
        return len(self.libraries)

    def getTotalNumPairs(self):
        totalNumPairs = getattr(self, 'totalNumPairs', None)
        if totalNumPairs:
            return self.totalNumPairs
        else:
            totalNumPairs = 0
            for lib in self.libraries:
                totalNumPairs += lib.getNumPairs()
            self.totalNumPairs = totalNumPairs
            return self.totalNumPairs

    def getTotalNumRuns(self):
        totalNumRuns = getattr(self, 'totalNumRuns', None)
        if totalNumRuns:
            return self.totalNumRuns
        else:
            totalNumRuns = 0
            for lib in self.libraries:
                totalNumRuns += lib.getTotalNumRuns()

            self.totalNumRuns = totalNumRuns
            return self.totalNumRuns

    def getTotalFileSize(self):
        totalFileSize = getattr(self, 'totalFileSize', None)
        if totalFileSize:
            return self.totalFileSize
        else:
            totalFileSize = 0
            for lib in self.libraries:
                totalFileSize += lib.getTotalFileSize()
            self.totalFileSize = totalFileSize
            return self.totalFileSize

    def getTotalNumSeqs(self):
        totalNumSeqs = getattr(self, 'totalNumSeqs', None)
        if totalNumSeqs:
            return self.totalNumSeqs
        else:
            totalNumSeqs = 0
            for lib in self.libraries:
                    totalNumSeqs += lib.getTotalNumSeqs()
            self.totalNumSeqs = totalNumSeqs
            return self.totalNumSeqs

    def __iter__(self):
        return self.libraries.__iter__()

    def __str__(self):
        lns = ""
        for lib in self.libraries:
            lns += "  " + lib.name + "\n"

        ver, res = self.check()
        return  "Name           : "  + self.name                    +"\n"+\
                "Num Libs       : "  + str(self.getNumLibraries())  +"\n"+\
                "Libraries      :\n" + lns                          +\
                "Total Num Pairs: "  + str(self.getTotalNumPairs()) +"\n"+\
                "Total Num Runs : "  + str(self.getTotalNumRuns())  +"\n"+\
                "Total File Size: "  + str(self.getTotalFileSize()) +"\n"+\
                "Total Num Seqs : "  + str(self.getTotalNumSeqs())  +"\n"+\
                "Check          : "  + str(ver)                     +"\n"+\
                                       res

if __name__ == "__main__":
    base = '/home/aflit001/filter/Data/'
    spp  = 'F5/'
    fold = 'F5_Illumina/'
    libf = 'F5_Illumina_GOG18L3_pairedend_300/'
    f11  = illRun(base+spp+fold+libf+'110126_SN132_B_s_3_1_seq_GOG-18.fastq')
    #print "F11\n" + str(f11)
    f12  = illRun(base+spp+fold+libf+'110126_SN132_B_s_3_2_seq_GOG-18.fastq')
    #print "F12\n" + str(f12)
    p1   = illPair(fastqs=[f11, f12], insertSize=300, type='PE')
    #print "P1\n" + str(p1)

    libf = 'F5_Illumina_GOG18L8_pairedend_300/'
    f21  = illRun(base+spp+fold+libf+'110127_SN365_B_s_8_1_seq_GOG-18.fastq')
    #print "F21\n" + str(f21)
    f22  = illRun(base+spp+fold+libf+'110127_SN365_B_s_8_2_seq_GOG-18.fastq')
    #print "F22\n" + str(f22)
    p2   = illPair(fastqs=[f21, f22], insertSize=300, type='PE')
    #print "P2\n" + str(p2)

    spp  = 'Pig/'
    fold = 'Pig_Illumina/'
    libf = 'Pig_Illumina_WGS/'
    f31  = illRun(base+spp+fold+libf+'sus_ACAGTG_L001_R1_001.fastq.gz')
    #print "F31\n" + str(f31)
    f32  = illRun(base+spp+fold+libf+'sus_ACAGTG_L001_R2_001.fastq.gz')
    #print "F32\n" + str(f32)
    p3   = illPair(fastqs=[f31, f32], type='WGS')
    #print "P3\n" + str(p3)

    l1   = illLibrary(pairs=[p1, p2, p3], name='PE300')
    #print "L1\n" + str(l1)

    dataset = illDataset(libraries=[l1], name='F5')
    print "DATASET\n" + str(dataset)
