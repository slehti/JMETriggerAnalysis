#!/usr/bin/env python3

import os,sys,re

import subprocess
import argparse

from plot_hltRun3Effs_2023 import *

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
    opts.inputDir = analysisdir
    opts.output = analysisdir.replace("analysis_output_","plots_")
    recosList = {}
    cands = execute("ls %s"%analysisdir)
    for cand in cands:

        rootfile = os.path.join(analysisdir,cand,'harvesting',cand+'.root')
        if not os.path.exists(rootfile):
            print("Input rootfile not found. Did you run analysis_post_process.py?")
            sys.exit()

        recosList[cand] = rootfile
    #print(recosList)
    efficiencyPlotting(recosList,opts)

if __name__=="__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-i', '--input', dest='inputDir', required=False, action='store', default=None,
                        help='path to input harvesting/ directory')

    parser.add_argument('-o', '--output', dest='output', action='store', default='.',
                        help='path to output directory')

    parser.add_argument('--no-plots', dest='no_plots', action='store_true',
                        help='do not create output plots')

    parser.add_argument('--no-qcd-weighted', dest='no_qcd_weighted', action='store_true',
                        help='input histograms do not include weights for MB+QCD merging')

    parser.add_argument('--minCountsForValidRate', dest='minCountsForValidRate', action='store', type=float, default=-1.0,
                        help='minimum number of counts to consider a sample valid for trigger rate estimates')

    parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf', 'png', 'C', 'root'],
                        help='list of extension(s) for output file(s)')

    parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                        help='verbosity level')

    parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                        help='enable dry-run mode')

    opts, args = parser.parse_known_args()

#    parser = OptionParser(usage="Usage: %prog [options]")
#    parser.add_option("-f","--force", dest="force", default=False, action="store_true",
#                      help="Force analysis even if output already exists [default: False")
#
#    (opts, args) = parser.parse_args()

    main(opts,args)
