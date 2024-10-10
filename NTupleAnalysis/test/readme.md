### Tools for Jet/MET Analysis

Workflow to produce Jet/MET performance plots from "flat" ROOT NTuples

#### Fast example
Running the analysis with the ntuple outputdir as an input
```
runAnalysis_hltRun3.py ../../NTuplizers/test/output_JMETriggerAnalysisNtuples_MHT_samples2023_v4
```

Merge output and harvest
```
analysis_postprocess.py analysis_output_JMETriggerAnalysisNtuples_MHT_samples2023_v4
```

Plot
```
plot.py analysis_output_JMETriggerAnalysisNtuples_MHT_samples2023_v4/
```

#### Setup

* Update global environment variables:
```
source env.sh
```

#### Prepare Analysis NTuples from batch/crab3 outputs

* Create output directory with one .root for each crab3 task:
```
hadd_ntuples.py -i [DIRS] -o [OUTDIR] -l 0 -s DQM
```

#### Submit Analysis Jobs to Batch System (HT-Condor)

* Create scripts for submission of batch jobs:
```
batch_driver.py -i ${NTUDIR}/*root -o ${OUTDIR}/jobs -n 50000 -l 0 # -p $PLUGIN
```

* Monitoring and (re)submission of batch jobs:
```
batch_monitor.py -i ${OUTDIR}
```

#### Harvesting of Outputs

* Merge outputs of batch jobs:
```
merge_batchOutputs.py -i ${OUTDIR}/jobs/*.root -o ${OUTDIR}/outputs -l 0
```

* Harvest outputs (manipulates histograms, produces profiles, efficiencies, etc):
```
jmeAnalysisHarvester.py -i ${OUTDIR}/outputs/*.root -o ${OUTDIR}/harvesting -l 0
```
