#!/usr/bin/python
from techs import *

base = '/home/aflit001/filter/Data/'
spp  = 'F5/'
fold = 'F5_Illumina/'
libf = 'F5_Illumina_GOG18L3_pairedend_300/'

lf11  = illumina.illRun(base+spp+fold+libf+'110126_SN132_B_s_3_1_seq_GOG-18.fastq')
#print "F11\n" + str(lf11)
lf12  = illumina.illRun(base+spp+fold+libf+'110126_SN132_B_s_3_2_seq_GOG-18.fastq')
#print "F12\n" + str(lf12)
lp1   = illumina.illPair(fastqs=[lf11, lf12], insertSize=300, type='PE')
#print "P1\n" + str(lp1)

libf = 'F5_Illumina_GOG18L8_pairedend_300/'

lf21  = illumina.illRun(base+spp+fold+libf+'110127_SN365_B_s_8_1_seq_GOG-18.fastq')
#print "F21\n" + str(lf21)
lf22  = illumina.illRun(base+spp+fold+libf+'110127_SN365_B_s_8_2_seq_GOG-18.fastq')
#print "F22\n" + str(lf22)
lp2   = illumina.illPair(fastqs=[lf21, lf22], insertSize=300, type='PE')
#print "P2\n" + str(lp2)

spp  = 'Pig/'
fold = 'Pig_Illumina/'
libf = 'Pig_Illumina_WGS/'

lf31  = illumina.illRun(base+spp+fold+libf+'sus_ACAGTG_L001_R1_001.fastq.gz')
#print "F31\n" + str(f31)
lf32  = illumina.illRun(base+spp+fold+libf+'sus_ACAGTG_L001_R2_001.fastq.gz')
#print "F32\n" + str(f32)
lp3   = illumina.illPair(fastqs=[lf31, lf32], type='WGS')
#print "P3\n" + str(lp3)

ll1   = illumina.illLibrary(pairs=[lp1, lp2, lp3], name='PE300')
#print "L1\n" + str(ll1)

ldataset = illumina.illDataset(libraries=[ll1], name='F5')
#print "DATASET\n" + str(ldataset)

#for lib in ldataset:
#    print lib.getName()
