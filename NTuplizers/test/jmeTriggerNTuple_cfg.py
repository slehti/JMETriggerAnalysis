import os
import fnmatch

from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB

###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'default',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword to define HLT reconstruction')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('keepPFPuppi', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'keep full collection of PFlow and PFPuppi candidates')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

#opts.register('printSummaries', False,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.bool,
#              'show summaries from HLT services')

opts.parseArguments()

###
### HLT configuration
###

update_jmeCalibs = False

print("Using reco option",opts.reco)
if opts.reco == 'default':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_14_0_0_GRun_configDump import cms, process

elif opts.reco == 'MHT_eta30pt25':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_14_0_0_GRun_configDump_eta30pt25 import cms, process
elif opts.reco == 'caloTowers_thresholds':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_14_0_0_GRun_configDump import cms, process
  from HLTrigger.Configuration.common import producers_by_type
  for producer in producers_by_type(process, "CaloTowersCreator"):
        producer.EcalRecHitThresh = cms.bool(True)
  update_jmeCalibs = True

elif opts.reco == 'testMHT':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_14_0_0_GRun_configDump import cms, process

  # customize MHT definition 
  #from HLTrigger.Configuration.customizeHLTforMHT import customizeHLTforMHTeta30pt25
  #process = customizeHLTforMHTeta30pt25(process)

elif opts.reco == 'MHT_eta30pt30':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_14_0_0_GRun_configDump_eta30pt30 import cms, process
  # customize MHT definition
  #from HLTrigger.Configuration.customizeHLTforMHT import customizeHLTforMHTeta30pt30
  #process = customizeHLTforMHTeta30pt30(process)

else:
  raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')

# By pass global tag of menu if needed
if opts.globalTag is not None:
  process.GlobalTag.globaltag = cms.string(opts.globalTag)

# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.OutputModule:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print('> removed cms.OutputModule:', _modname)

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.EndPath:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print('> removed cms.EndPath:', _modname)

# remove selected cms.Path objects from HLT config-dump
print('-'*108)
print('{:<99} | {:<4} |'.format('cms.Path', 'keep'))
print('-'*108)

# list of patterns to determine paths to keep
keepPaths = [
  'MC_*Jets*',
  'MC_*MET*',
  'MC_*AK8Calo*',
  'HLT_PFJet*_v*',
  'HLT_AK4PFJet*_v*',
  'HLT_AK8PFJet*_v*',
  'HLT_PFHT*_v*',
  'HLT_PFMET*_PFMHT*_v*',
  #'AlCa_*',
  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*'
]

vetoPaths = [
  'HLT_*ForPPRef_v*',
	'AlCa_*',
]

# list of paths that are kept
listOfPaths = []

for _modname in sorted(process.paths_()):
    _keepPath = False
    for _tmpPatt in keepPaths:
      _keepPath = fnmatch.fnmatch(_modname, _tmpPatt)
      if _keepPath: break

    if _keepPath:
      for _tmpPatt in vetoPaths:
        if fnmatch.fnmatch(_modname, _tmpPatt):
          _keepPath = False
          break

    if _keepPath:
      print('{:<99} | {:<4} |'.format(_modname, '+'))
      listOfPaths.append(_modname)
      continue
    _mod = getattr(process, _modname)
    if type(_mod) == cms.Path:
      process.__delattr__(_modname)
      print('{:<99} | {:<4} |'.format(_modname, ''))
print('-'*108)


# remove FastTimerService
if hasattr(process, 'FastTimerService'):
  del process.FastTimerService

if update_jmeCalibs:
  ## ES modules for PF-Hadron Calibrations
  #process.pfhcESSource = cms.ESSource('PoolDBESSource',
  #  _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/PFCalibration.db'),
  #  #_CondDB.clone(connect = 'sqlite_file:PFCalibration.db'),
  #  toGet = cms.VPSet(
  #    cms.PSet(
  #      record = cms.string('PFCalibrationRcd'),
  #      tag = cms.string('PFCalibration_CMSSW_13_0_0_HLT_126X_v6_mcRun3_2023'),
  #      label = cms.untracked.string('HLT'),
  #    ),
  #  ),
  #)
  #process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

  ##ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    #_CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Run3Winter23Digi.db'),
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/WCalo_Run3Winter24Digi.db'),
    #_CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Run3Winter23Digi_OfflinePFHC_skipFwd.db'),
    #_CondDB.clone(connect = 'sqlite_file:Run3Winter23Digi.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter24Digi_AK4CaloHLT'),
        label = cms.untracked.string('AK4CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter24Digi_AK4PFHLT'),
        label = cms.untracked.string('AK4PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter24Digi_AK8CaloHLT'),
        label = cms.untracked.string('AK8CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter24Digi_AK8PFHLT'),
        label = cms.untracked.string('AK8PFHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')



## Output NTuple
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',
  TTreeName = cms.string('Events'),
  TriggerResults = cms.InputTag('TriggerResults'),
  TriggerResultsFilterOR = cms.vstring(),
  TriggerResultsFilterAND = cms.vstring(),
  TriggerResultsCollections = cms.vstring(
    sorted(list(set([(_tmp[:_tmp.rfind('_v')] if '_v' in _tmp else _tmp) for _tmp in listOfPaths])))
  ),
  outputBranchesToBeDropped = cms.vstring(),

  HepMCProduct = cms.InputTag('generatorSmeared'),
  GenEventInfoProduct = cms.InputTag('generator'),
  PileupSummaryInfo = cms.InputTag('addPileupInfo'),

  doubles = cms.PSet(

    #hltFixedGridRhoFastjetAllCalo = cms.InputTag('hltFixedGridRhoFastjetAllCalo'),
    #hltFixedGridRhoFastjetAllPFCluster = cms.InputTag('hltFixedGridRhoFastjetAllPFCluster'),
    hltFixedGridRhoFastjetAll = cms.InputTag('hltFixedGridRhoFastjetAll'),
    #offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),

    #hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
  ),

  vdoubles = cms.PSet(
  ),

  recoVertexCollections = cms.PSet(

    #hltPixelVertices = cms.InputTag('hltPixelVertices'),
    #hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    #hltVerticesPF = cms.InputTag('hltVerticesPF'),
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    #ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
    hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

    #hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
    #hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

# recoPFClusterJetCollections = cms.PSet(

#   hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
#   hltAK4PFClusterJetsCorrected = cms.InputTag('hltAK4PFClusterJetsCorrected'),

#   hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
#   hltAK8PFClusterJetsCorrected = cms.InputTag('hltAK8PFClusterJetsCorrected'),
# ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

    #hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
    #hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),

    #hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
    #hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),

    #hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    #hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),

    #hltAK8PFCHSJets = cms.InputTag('hltAK8PFCHSJets'),
    #hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),

    #hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
    #hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),
  ),

  patJetCollections = cms.PSet(

    #offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    offlineAK4PFPuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    #offlineAK8PFPuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

  recoGenMETCollections = cms.PSet(

    #genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

#  recoCaloMETCollections = cms.PSet(

#    hltCaloMET = cms.InputTag('hltMet'),
#    hltCaloMETTypeOne = cms.InputTag('hltCaloMETTypeOne'),
#  ),

# recoPFClusterMETCollections = cms.PSet(

#   hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
#   hltPFClusterMETTypeOne = cms.InputTag('hltPFClusterMETTypeOne'),
# ),

  recoPFMETCollections = cms.PSet(

    hltPFMET = cms.InputTag('hltPFMETProducer'),
    #hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),

    #hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    #hltPFCHSMETTypeOne = cms.InputTag('hltPFCHSMETTypeOne'),

    #hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),
    #hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
  ),

  patMETCollections = cms.PSet(

    #offlinePFMET = cms.InputTag('slimmedMETs'),
    offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

  recoMuonCollections = cms.PSet(
    #hltMuons = cms.InputTag('hltIterL3Muons'), # this collection uses the miniAOD definition muon::isLooseTriggerMuon(reco::Muon)
  )
)

if opts.keepPFPuppi:
  process.hltPFPuppi.puppiDiagnostics = True
  process.JMETriggerNTuple.vdoubles = cms.PSet(
    hltPFPuppi_PuppiRawAlphas = cms.InputTag('hltPFPuppi:PuppiRawAlphas'),
    hltPFPuppi_PuppiAlphas = cms.InputTag('hltPFPuppi:PuppiAlphas'),
    hltPFPuppi_PuppiAlphasMed = cms.InputTag('hltPFPuppi:PuppiAlphasMed'),
    hltPFPuppi_PuppiAlphasRms = cms.InputTag('hltPFPuppi:PuppiAlphasRms'),
  )
  process.JMETriggerNTuple.recoPFCandidateCollections = cms.PSet(
    hltParticleFlow = cms.InputTag('hltParticleFlow'),
    hltPFPuppi = cms.InputTag('hltPFPuppi'),
  )

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
process.schedule.append(process.analysisNTupleEndPath)

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = max(opts.numThreads, 8)
process.options.numberOfStreams = max(opts.numStreams, 0)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

## update process.GlobalTag.globaltag
#if opts.globalTag is not None:
#   from Configuration.AlCa.GlobalTag import GlobalTag
#   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# input EDM files [primary]
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
    #'/store/mc/Run3Summer23BPixMiniAODv4/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/0d367f04-06bc-407c-a118-0e1d14974b87.root'
    #'/store/mc/Run3Summer23BPixMiniAODv4/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/1c1439be-73ca-41ed-a72d-751ac7c3d317.root'
    '/store/relval/CMSSW_14_0_9/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_140X_mcRun3_2024_realistic_EOR3_TkDPGv6_RV245_2024-v1/2580000/0008bc3f-5e69-45fb-a46d-103c9ee4c9aa.root'
    #'/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/00500cd3-78c5-44f0-959e-87343b2f925b.root'
    #'/store/mc/Run3Winter24Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/133X_mcRun3_2024_realistic_v9-v3/50000/017d210f-c527-402b-8e13-e6119e79fe6c.root'
    #'/store/mc/Run3Winter23MiniAOD/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/MINIAODSIM/FlatPU0to80_126X_mcRun3_2023_forPU65_v1-v2/2540000/10e9c9ff-b431-42c5-a1ec-e3143eafee20.root',
    #'/store/mc/Run3Winter23Digi/DYToMuMu_M-20_TuneCP5_13p6TeV-pythia8/GEN-SIM-RAW/GTv4Digi_126X_mcRun3_2023_forPU65_v4-v2/2820000/0070321e-e4e6-4769-900f-0c0ad3831215.root'
    #'/store/mc/Run3Winter23MiniAOD/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/126X_mcRun3_2023_forPU65_v1-v2/2550000/19e43825-6b8e-426e-9cca-e23cf318737c.root',
    #'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/033373ea-6628-4bd0-b0ce-a35145622552.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/1b0db43a-d38e-4e8b-8ad5-a2b255a54445.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/6259374b-6865-4dd4-9414-25e393cb30ae.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/8aae5414-96dc-414b-b277-e3da177b5fd6.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/1b62be66-8f21-4c37-ada8-0e9094b754c3.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/9292ed8b-e6e9-4e25-9ca2-bea39913b662.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/7f0077e6-e6f7-45bb-8d09-688fbe898716.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/33ca1f69-b3b2-4f6c-8505-66d405c7dc85.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/0379f27a-2c28-4e23-9d1f-beb1fbae45dd.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/216d41af-b3b1-4669-b496-682e7eefd6cb.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/6ef59234-3b07-49e4-96b3-03b499901f22.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/755f6116-2539-4d13-89cd-874fe989d755.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/6137a5b1-f72c-4fd0-93e5-2f2eaa238dc0.root',

  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/00500cd3-78c5-44f0-959e-87343b2f925b.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/04a68f00-e9d3-4062-ba47-dd28ef92571b.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/055ac909-a375-4028-8b4f-841d5f3d0ce3.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/05a7c648-6a52-4d05-88b9-4abd614bdccc.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/090d4abe-fdc2-482f-879b-bc8672654e3c.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/127d6eae-bdb3-4f9b-bd61-810788271c7e.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/15df1dd3-a63e-41f1-8622-0ef22caf6cfe.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/17692f08-b459-4b06-a481-1765803c6752.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/191c9b01-bf9c-44dd-a029-e448cb3fa6a5.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/1bf89189-5567-4759-ba48-8e03c5b294fd.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/1cfd894b-a21b-47d8-bd94-4756a954c7fe.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/1d1fe1ee-0ce2-43d9-8a72-020cb8ae1a34.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/210ce983-4da0-45ed-a3ca-cb4dc242a5a1.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/27f907b2-4dbc-48b3-b511-a51b69c576ed.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/28b4f122-a2f0-4999-9b75-6224aa0126cf.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/295409f0-6cca-4c84-ab7a-c24cbe51bf6f.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/29b8a348-f33d-492e-a9fa-353db6d5a389.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/2af7d1ed-81b8-4362-b862-2c2f750a4ae5.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/2d738014-4b8d-433b-b49d-cc98b4615272.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/308f0d9f-1017-4fb8-8665-dcb88eed17af.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/32aa7506-43ad-42a0-a093-c14bd479477c.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/3a7be0c8-8e07-492e-b1d5-8cc6b8ee09a8.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/3acc3543-5716-4c5e-acfc-aa8c93365ece.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/3e9025d7-6d01-4b29-9870-e26ca9410fc6.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/42ee02f5-3fe9-42cf-b1a0-3109f5e66e6c.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/43178de5-e452-4805-8dd6-bb103e42605a.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/475c9c30-d701-46d5-bba0-572ffd47b6bf.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/4b1e3963-b84f-4d00-a781-c5b9c5bf86c2.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/4b4e81fc-2622-4cde-8acf-87f4ae5e8fdd.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/4f598861-138b-4b53-a27c-2ada4d041185.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/4ff103ad-23ba-4426-a7b6-17cbc1be2362.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/594bc876-28fd-4e7e-a155-8dc8955c409a.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/5f54675f-453d-4406-b2f5-415616692190.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/65d75698-b1bc-431f-8fc8-2d9ba2da7f89.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/662b3f21-6ac1-4549-a30e-70b3225aa937.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/665069ce-5e87-4d81-a0b2-7fc31647a3e1.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/6983c928-8af1-4afa-b533-6e99a446ad5c.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/6c9f41c4-3455-4da0-861c-1f04d29484f9.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/6d0398b3-ee61-4b01-bf9e-595e14cd42b3.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/6d0a23e6-f12d-4e1a-9f60-159ee0a31823.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/6d24589a-63eb-458f-be1f-1e4f92579f40.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/71672c03-585d-49e0-a1a3-d84eefd873dd.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/7434d7e0-1678-44ab-bcec-df5eacf6de89.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/74b00bef-f409-4586-ab61-1aa2cf4b6a77.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/791b55df-4064-4d8a-9aad-4c0b6d215045.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/79660777-9e63-413e-ad09-589298f041c9.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/7a3835fc-b68e-49ce-bc66-3e427934b43c.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/7c249d4f-4073-4ddc-80c0-c61a2f179ffd.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/7ea17efc-9388-40cc-9a27-994e78b7f9d5.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/7ef3b9fc-cd46-485c-954f-f1ae32a88f1c.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/7fcfd08d-4bde-49cf-8f30-d01dabfc0d90.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/81ef4d9e-f55c-4adc-9c84-750823d929d3.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/82cef863-f1e0-4f1d-b644-e049111bd575.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/832f5255-10bc-4822-b20c-4b7c0c229fa9.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/85196881-f601-4e75-a906-331f4a242b5d.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/89418a9b-12c9-4586-9b81-18159afb46d0.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/8a1b0932-83cc-43a3-98d7-deffc2734d8e.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/8c2d3572-211c-4244-b61b-ecfa3eb06deb.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/8f22f9eb-4aba-4077-86ac-a09fd1701df8.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/94660fc9-25c3-409c-93d9-2fdbb3dd6c0b.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/9508a6a1-1287-4572-bd17-70ec0688b26a.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/97ad2438-a1a8-47c0-9418-6de0a234e4f8.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/9fa6b3b2-9e21-4146-9443-4b9966c07af7.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/a0a4bcad-2f01-4636-8f9c-86227d233fc9.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/a4b00e29-70cb-4110-b251-6e3e036d84db.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/a6ea4083-4afe-42e0-a9d1-09f5c785e213.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/ac3c9c53-ed1b-4ba7-871d-8e5c46b3db74.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/ad59f10b-c13e-4f5a-b7ea-7d96127e796a.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/b28dc317-e1ac-49bb-ba2b-a338e9cabf26.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/b2d5c9b3-60af-4850-b4f0-d739bdb37f47.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/b5e860f8-11bf-4df1-84b1-ff2c5103a53f.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/c17305f1-27a8-4ceb-95d4-fe555df4f92e.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/c415a345-84de-48d6-a4fe-6f7bfe040dd7.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/c6140c49-919b-4691-9c7a-4bd58f4b0c2f.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/c7926e84-0a27-4466-910f-9ab1616ac95f.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/ca1b974c-2aa0-4915-b7ce-48ef90308c1e.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/ce0a42bc-3131-4630-a60a-94434ae99113.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/d02e5c89-6819-42a6-9d50-88676e2f9b8d.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/d2b7b80f-daae-4f2b-a909-de4536713154.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/d4b23016-86d8-4f46-a7d0-a8403bc574ed.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/d6a3ea51-ebb1-4155-b9ac-3cc85872f2cb.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/dd06ea10-235e-4d4e-8e58-c297703230ef.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/dee349db-4601-405a-b415-3b70adb5acde.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/df574551-b5c5-4340-8f47-9d30fbdf6267.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/e1b4337d-3b36-4db4-8e63-352a779a2a59.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/e2233ff5-518b-42d3-989e-44fdbb5e7cd2.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/e2ca5887-58fc-4b87-a879-b1d973fc5e89.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/e5226f24-6c2d-4505-a170-8027b914767b.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/e53d6406-e2a5-4393-817a-644265af412b.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/e623f23a-5bae-4361-8c38-451a1860b59f.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/e6ee04aa-98df-4a54-aff8-bbeb13176e65.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/ea8162cf-4c85-4952-ba75-358300a1dba4.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/ec1e4821-8e98-412a-bb3e-a8f927e49009.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/ec246d35-b3a2-4b5d-b6b2-14190eec5687.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/f1e23021-e88c-489f-9dad-20efbd96e72e.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/f232011f-f636-4b85-a6f5-0c9bf424f8a3.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/f506d2c5-6f87-4cce-a2f1-96a7ba6e57ec.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/fd15568f-22cf-4e24-a9db-c1a55d1fd621.root',
    '/store/mc/Run3Summer23BPixDRPremix/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/130X_mcRun3_2023_realistic_postBPix_v6-v2/2830000/fe03b936-6d75-4598-ba1d-a9be01de8c90.root',
    #'/store/mc/Run3Winter23Digi/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_126X_mcRun3_2023_forPU65_v1-v1/2560000/00d203d8-3ef3-4ca2-884d-a6b2f3bfbb6e.root',
    #
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/f61dc979-f42d-443f-8a1f-587b3353b109.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/e465ec59-571a-4dd5-b429-93b2b55f643b.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/f90d178a-8997-43ca-b9c9-edc49b733fcb.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/572aa6f8-a7a2-4db2-b332-5729c37ba743.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/5d2ccf3f-7f9f-4237-b210-a48c838dfa6a.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/b17347c9-536a-4b06-9a68-f8199e76ddf2.root',
  ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# printouts
if opts.verbosity > 0:
   print('--- jmeTriggerNTuple_cfg.py ---')
   print('')
   print('option: output =', opts.output)
   print('option: reco =', opts.reco)
   print('option: dumpPython =', opts.dumpPython)
   print('')
   print('process.GlobalTag =', process.GlobalTag.dumpPython())
   print('process.source =', process.source.dumpPython())
   print('process.maxEvents =', process.maxEvents.dumpPython())
   print('process.options =', process.options.dumpPython())
   print('-------------------------------')
