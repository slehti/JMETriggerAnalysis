#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  # example: makeNTuples_run3_latest.sh MHT_samples2023_v2
  printf "\n%s\n\n" ">> argument missing - specify path to output directory"
  exit 1
fi

NEVT=500000


<<<<<<< HEAD
OUTPUT_DIR_EOS=/eos/user/${USER:0:1}/${USER}/JMETriggerAnalysisNtuples_${1}
ODIR=output_JMETriggerAnalysisNtuples_${1}
=======
OUTPUT_DIR_EOS=/eos/user/${USER:0:1}/${USER}/samples2023
ODIR=${1}
>>>>>>> theo/run3_14_0_X


declare -A samplesMap

# QCD 
samplesMap["Run3Winter23_QCD_Pt15to7000_13p6TeV_PU65"]='/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/Run3Winter24MiniAOD-NoPU_133X_mcRun3_2024_realistic_v9-v2/MINIAODSIM'

# 
# 
# VBF H(125)->Invisible
#samplesMap["Run3Winter23_VBF_HToInvisible_13p6TeV_PU65"]="/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Winter24MiniAOD-133X_mcRun3_2024_realistic_v9-v3/MINIAODSIM"
#samplesMap["Run3Summer23BPix_VBF_HToInvisible"]="/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v6-v2/MINIAODSIM"
#"/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer23BPixDRPremix-130X_mcRun3_2023_realistic_postBPix_v6-v2/GEN-SIM-RAW"


#recoKeys=(
#    default
#    MHT_eta30pt25
#    MHT_eta30pt30
#}
recoKeys=(
  default
  caloTowers_thresholds
)

if [ -d ${OUTPUT_DIR_EOS}/${ODIR} ]; then
  printf "%s\n" "output directory already exists: ${ODIR}"
  echo "If you continue the following directories will get overwritten: "
  for recoKey in "${recoKeys[@]}"; do
    find ${OUTPUT_DIR_EOS}/${ODIR} -path ${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}
  done
  read -p "Do you want to continue? [y/n]" yn
  case $yn in
      [Yy]* ) echo "Continuing the process...";;
      [Nn]* ) echo "Exiting..."; unset recoKey recoKeys samplesMap NEVT ODIR; exit 1;;
      * ) echo "Please answer with y/n.";;
  esac
fi



for recoKey in "${recoKeys[@]}"; do
  python3 ${CMSSW_BASE}/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py dumpPython=.tmp_cfg.py reco=${recoKey}

  for sampleKey in ${!samplesMap[@]}; do
    sampleName=${samplesMap[${sampleKey}]}
    
    # number of events per sample
    numEvents=${NEVT}
    
    # directory for the jobs output ntuples
    FINAL_OUTPUT_DIR=${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}/${sampleKey} 

    # removing the output directory and its contents if it already exists
    if [ -d ${FINAL_OUTPUT_DIR} ]; then rm -rf ${OUTPUT_DIR_EOS}/${ODIR}/${recoKey}/; fi
  
    mkdir -p ${FINAL_OUTPUT_DIR}
    
    if [ -d ${ODIR}/${recoKey}/${sampleKey} ]; then rm -rf ${ODIR}/${recoKey}/${sampleKey}; fi
    
    bdriver -c .tmp_cfg.py --customize-cfg -m ${numEvents} -n 1000 --memory 2G --time 02:00:00 \
      -d ${sampleName} -p 2 -o ${ODIR}/${recoKey}/${sampleKey} \
      --final-output ${FINAL_OUTPUT_DIR} \
      --submit \
      --customise-commands \
      '# output [TFileService]' \
      "if hasattr(process, 'TFileService'):" \
      '  process.TFileService.fileName = opts.output'
  done
  unset sampleKey numEvents sampleName

  rm -f .tmp_cfg.py

  

  #bmonitor -i ${ODIR} -r -f 60 --repeat 20 

done
unset recoKey recoKeys samplesMap NEVT ODIR
