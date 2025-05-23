#!/usr/bin/env python3

# 04102024/SLehti

import os,sys,re
import subprocess

from optparse import OptionParser

def usage():
    print
    print("### Usage:   ",os.path.basename(sys.argv[0])," <output dir>")
    print
    sys.exit()

def execute(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

    stdin  = p.stdout
    stdout = p.stdout
    ret    = []
    for line in stdout:
        line = str(line,'utf-8')
        ret.append(line.replace("\n", ""))

    stdout.close()
    return ret

def main(opts,args):

    if 'CMSSW_BASE' not in os.environ:
        print("cmsenv not set. Exiting..")
        sys.exit()

    inputdir = args[0]
    if inputdir[-1] == '/':
        inputdir = inputdir[:-1]
    inputdirname = os.path.basename(inputdir)
    print("Reading",inputdir,inputdirname)

    outputdir = "analysis_"+inputdirname

    USER = os.environ['USER']

    eos_home = os.path.join('/eos/user/',USER[0],USER)
    eos_cmd = "find %s -name '%s'"%(eos_home,inputdirname)
    print(eos_cmd)
    eosdirname = execute(eos_cmd)[0]
    print(eosdirname)
    taskdirnames = execute("ls %s"%eosdirname)

    for d in taskdirnames:
        print("Analyzing",d)
        taskdir = os.path.join(outputdir,d)
        if not os.path.exists(os.path.join(taskdir,'jobs')):
            os.makedirs(os.path.join(taskdir,'jobs'))
        else:
            if not opts.force:
                print("Outputdir",outputdir,"already exists, exiting..")
                sys.exit()
        merged_ntuple = os.path.join(eosdirname,d,'samples_merged',d+'.root')
        if not os.path.exists(merged_ntuple):
            print("Merged ntuple not found. Did you run mergeNtuples.py <outputdir>?")
            sys.exit()
        #cmd = "runAnalysis_hltRun3_2023Data.sh %s %s"%(merged_ntuple,outputdir)
        cmd = "batch_driver.py -l 1 -n 5000 -p JMETriggerAnalysisDriverRun3 -i %s -o %s/jobs -od %s --JobFlavour espresso --submit"%(merged_ntuple,taskdir,taskdir)
        print(cmd)
        os.system(cmd)


if __name__=="__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-f","--force", dest="force", default=False, action="store_true",
                      help="Force analysis even if output already exists [default: False")

    (opts, args) = parser.parse_args()

    main(opts,args)
"""
batch_driver.py -l 1 -n 5000 -p JMETriggerAnalysisDriverRun3 \
  -i ${OUTDIR}/ntuples/*.root -o ${OUTDIR}/jobs \
  -od ${OUTPUTDIR} \
  --JobFlavour espresso \
  --submit
"""
