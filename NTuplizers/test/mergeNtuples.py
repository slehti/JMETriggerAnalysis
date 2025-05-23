#!/usr/bin/env python3

import os,sys,re
import subprocess

import ROOT

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

def validate(rootfile):
    if not os.path.exists(rootfile):
        print("File %s not found"%rootfile)
        sys.exit()

    with ROOT.TFile.Open(rootfile) as fIN:
        events = fIN.Get("JMETriggerNTuple/Events")
        if events.GetEntries() == 0:
            print("\033[91mWarning, rootfile %s contains no events\033[0m"%rootfile)
        else:
            print("File %s, %s entries"%(rootfile,events.GetEntries()))

def main(opts,args):

    outputdir = args[0]
    if len(opts.dirName) > 0:
        outputdir = opts.dirName

    eospath = ""
    if '/eos/' in outputdir[:5]:
        eospath = outputdir
    else:
        #/eos/user/s/slehti/JMETriggerAnalysisNtuples_MHT_samples2023_v4/output_JMETriggerAnalysisNtuples_MHT_samples2023_v4/MHT_eta30pt25/Run3Summer23BPix_VBF_HToInvisible/
        USER = os.environ['USER']
        eospath = os.path.join('/eos/user/',USER[0],USER)
        cmd = "find %s -name '%s'"%(eospath,outputdir)
        cands = execute(cmd)
        if len(cands) == 1:
            eospath = cands[0]
        else:
            if len(cands) == 0:
                print("No eos path found")
            else:
                print("Too many eos path candidates",cands)

    #print(eospath)

    root_re = re.compile("(?P<rootfile>(\S+\.root$))")
    taskdirs = execute("ls %s"%eospath)
    for taskdirname in taskdirs:
        print("Merging",taskdirname)
        taskdir = os.path.join(eospath,taskdirname)
        ntupledirname = execute("ls %s"%taskdir)[0]
        ntupledir = os.path.join(taskdir,ntupledirname)
        cands = execute("ls %s"%ntupledir)
        rootfiles = []
        for cand in cands:
            match = root_re.search(cand)
            if match:
                rootfiles.append(os.path.join(ntupledir,cand))

        if len(rootfiles) == 0:
            print("No rootfiles found in %s"%ntupledir)
            sys.exit()

        # /eos/user/s/slehti/JMETriggerAnalysis_samples2023/test6/testMHT/samples_merged/testMHT.root
        mergepath = os.path.join(taskdir,'samples_merged')
        if not os.path.exists(mergepath):
            os.mkdir(mergepath)
        cmd = "hadd"
        if opts.force:
            cmd = "hadd -f"
        cmd += " %s %s"%(os.path.join(mergepath,taskdirname+'.root'),' '.join(rootfiles))
        #print(os.path.join(mergepath,taskdirname+'.root'))
        #os.system(cmd)
        #print(cmd)
        execute(cmd)

        validate(os.path.join(mergepath,taskdirname+'.root'))

if __name__=="__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-d", "--dir", dest="dirName", default="", type="string",
                      help="Directory containing the files to be merged [default: empty]")
    parser.add_option("-f","--force", dest="force", default=False, action="store_true",
                      help="Force merging even if merge output already exists [default: False")

    (opts, args) = parser.parse_args()

    main(opts,args)
