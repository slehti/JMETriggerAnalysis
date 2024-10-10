#!/usr/bin/env python3

import os,sys,re

import subprocess

from optparse import OptionParser

def usage():
    print
    print("### Usage:   ",os.path.basename(sys.argv[0])," <analysis_output dir>")
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

    if len(args) == 0:
        usage()

    analysisdir = args[0]

    cands = execute("ls %s"%analysisdir)
    for cand in cands:
        inputdir = os.path.join(analysisdir,cand)
        outputdir = inputdir

        rootfile = os.path.join(analysisdir,cand,'outputs',cand+'.root')
        if not os.path.exists(rootfile) or opts.force:
            merge_cmd = "merge_batchOutputs.py -l 0 -i %s/*.root -o %s/outputs"%(inputdir,outputdir)
            print(merge_cmd)
            os.system(merge_cmd)

        #analysis_output_JMETriggerAnalysisNtuples_MHT_samples2023_v4/MHT_eta30pt25/outputs/MHT_eta30pt25.root
        harvester_cmd = "jmeAnalysisHarvester.py -l 0 -i %s -o %s/harvesting"%(rootfile,outputdir)
        print(harvester_cmd)
        os.system(harvester_cmd)
        
if __name__=="__main__":

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-f","--force", dest="force", default=False, action="store_true",
                      help="Force analysis even if output already exists [default: False")

    (opts, args) = parser.parse_args()

    main(opts,args)
