#! /usr/bin/env python3

crabSubmitFile = open("SubmitCrabJobsData.sh","w")
crabSubmitFile.write("#!/bin/bash\n")

storeDir = "TriggerObjects"

samples_muons = {
  #2022
  'Muon0_Run2022CV1':["/Muon/Run2022C-PromptReco-v1/MINIAOD","Winter22Run3_RunC_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'Muon0_Run2022DV1':["/Muon/Run2022D-PromptReco-v1/MINIAOD","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'Muon0_Run2022DV2':["/Muon/Run2022D-PromptReco-v2/MINIAOD","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'Muon0_Run2022DV3':["/Muon/Run2022D-PromptReco-v3/MINIAOD","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'Muon0_Run2022EV1':["/Muon/Run2022E-PromptReco-v1/MINIAOD","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'Muon0_Run2022FV1':["/Muon/Run2022F-PromptReco-v1/MINIAOD","Summer22EEPrompt22_RunF_V1_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'Muon0_Run2022GV1':["/Muon/Run2022G-PromptReco-v1/MINIAOD","Summer22EEPrompt22_RunG_V1_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  #2023 Muon0
  #'/Muon0/Run2023A-PromptReco-v2/MINIAOD':["Muon0_Run2023AV2","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon0_Run2023BV1':["/Muon0/Run2023B-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon0_Run2023CV1':["/Muon0/Run2023C-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon0_Run2023CV2':["/Muon0/Run2023C-PromptReco-v2/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon0_Run2023CV3':["/Muon0/Run2023C-PromptReco-v3/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon0_Run2023CV4':["/Muon0/Run2023C-PromptReco-v4/MINIAOD","Summer23Prompt23_RunCv4_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon0_Run2023DV1':["/Muon0/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","Cert_Collisions2023_369844-369863_Golden_Run2023D1PreBPix.json","130X_dataRun3_Prompt_v2"],
  'Muon0_Run2023DV1BPix':["/Muon0/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","Cert_Collisions2023_369864-370580_Golden_Run2023D1BPix.json","130X_dataRun3_Prompt_v2"],
  'Muon0_Run2023DV2BPix':["/Muon0/Run2023D-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  #2023 Muon1
  #'/Muon1/Run2023A-PromptReco-v2/MINIAOD':["Muon1_Run2023AV2","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon1_Run2023BV1':["/Muon1/Run2023B-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon1_Run2023CV1':["/Muon1/Run2023C-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon1_Run2023CV2':["/Muon1/Run2023C-PromptReco-v2/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon1_Run2023CV3':["/Muon1/Run2023C-PromptReco-v3/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon1_Run2023CV4':["/Muon1/Run2023C-PromptReco-v4/MINIAOD","Summer23Prompt23_RunCv4_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'Muon1_Run2023DV1':["/Muon1/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","Cert_Collisions2023_369844-369863_Golden_Run2023D1PreBPix.json","130X_dataRun3_Prompt_v2"],
  'Muon1_Run2023DV1BPix':["/Muon1/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","Cert_Collisions2023_369864-370580_Golden_Run2023D1BPix.json","130X_dataRun3_Prompt_v2"],
  'Muon1_Run2023DV2BPix':["/Muon1/Run2023D-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  #2024 Muon0
  'Muon0_Run2024B':["/Muon0/Run2024B-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraB_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024C':["/Muon0/Run2024C-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraC_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024D':["/Muon0/Run2024D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraD_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024E1':["/Muon0/Run2024E-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraE_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024E2':["/Muon0/Run2024E-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraE_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024F':["/Muon0/Run2024F-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_381984-383779_Golden_Run2024F.json","140X_dataRun3_Prompt_v4"],
  'Muon0_Run2024G':["/Muon0/Run2024G-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Collisions24_13p6TeV_378981_385016_DCSOnly_TkPx.json","140X_dataRun3_Prompt_v4"],
  'Muon0_Run2024H':["/Muon0/Run2024H-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Collisions24_13p6TeV_378981_386047_DCSOnly_TkPx.json","140X_dataRun3_Prompt_v4"],
  #2024 Muon1
  'Muon1_Run2024B':["/Muon1/Run2024B-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraB_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024C':["/Muon1/Run2024C-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraC_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024D':["/Muon1/Run2024D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraD_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024E1':["/Muon1/Run2024E-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraE_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024E2':["/Muon1/Run2024E-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraE_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024F':["/Muon1/Run2024F-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_381984-383779_Golden_Run2024F.json","140X_dataRun3_Prompt_v4"],
  'Muon1_Run2024G':["/Muon1/Run2024G-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Collisions24_13p6TeV_378981_385016_DCSOnly_TkPx.json","140X_dataRun3_Prompt_v4"],
  'Muon1_Run2024H':["/Muon1/Run2024H-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Collisions24_13p6TeV_378981_386047_DCSOnly_TkPx.json","140X_dataRun3_Prompt_v4"],
}

samples = {
  #2022
  'JetMET0_Run2022CV1':["/JetMET/Run2022C-PromptReco-v1/MINIAOD","Winter22Run3_RunC_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'JetMET0_Run2022DV1':["/JetMET/Run2022D-PromptReco-v1/MINIAOD","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'JetMET0_Run2022DV2':["/JetMET/Run2022D-PromptReco-v2/MINIAOD","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'JetMET0_Run2022DV3':["/JetMET/Run2022D-PromptReco-v3/MINIAOD","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'JetMET0_Run2022EV1':["/JetMET/Run2022E-PromptReco-v1/MINIAOD","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'JetMET0_Run2022FV1':["/JetMET/Run2022F-PromptReco-v1/MINIAOD","Summer22EEPrompt22_RunF_V1_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  'JetMET0_Run2022GV1':["/JetMET/Run2022G-PromptReco-v1/MINIAOD","Summer22EEPrompt22_RunG_V1_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  #2023 JetMET0
  #'/JetMET0/Run2023A-PromptReco-v2/MINIAOD':["JetMET0_Run2023AV2","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET0_Run2023BV1':["/JetMET0/Run2023B-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET0_Run2023CV1':["/JetMET0/Run2023C-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET0_Run2023CV2':["/JetMET0/Run2023C-PromptReco-v2/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET0_Run2023CV3':["/JetMET0/Run2023C-PromptReco-v3/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET0_Run2023CV4':["/JetMET0/Run2023C-PromptReco-v4/MINIAOD","Summer23Prompt23_RunCv4_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET0_Run2023DV1':["/JetMET0/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","Cert_Collisions2023_369844-369863_Golden_Run2023D1PreBPix.json","130X_dataRun3_Prompt_v2"],
  'JetMET0_Run2023DV1BPix':["/JetMET0/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","Cert_Collisions2023_369864-370580_Golden_Run2023D1BPix.json","130X_dataRun3_Prompt_v2"],
  'JetMET0_Run2023DV2BPix':["/JetMET0/Run2023D-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  #2023 JetMET1
  #'/JetMET1/Run2023A-PromptReco-v2/MINIAOD':["JetMET1_Run2023AV2","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET1_Run2023BV1':["/JetMET1/Run2023B-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET1_Run2023CV1':["/JetMET1/Run2023C-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET1_Run2023CV2':["/JetMET1/Run2023C-PromptReco-v2/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET1_Run2023CV3':["/JetMET1/Run2023C-PromptReco-v3/MINIAOD","Summer23Prompt23_RunCv123_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET1_Run2023CV4':["/JetMET1/Run2023C-PromptReco-v4/MINIAOD","Summer23Prompt23_RunCv4_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  'JetMET1_Run2023DV1':["/JetMET1/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","Cert_Collisions2023_369844-369863_Golden_Run2023D1PreBPix.json","130X_dataRun3_Prompt_v2"],
  'JetMET1_Run2023DV1BPix':["/JetMET1/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","Cert_Collisions2023_369864-370580_Golden_Run2023D1BPix.json","130X_dataRun3_Prompt_v2"],
  'JetMET1_Run2023DV2BPix':["/JetMET1/Run2023D-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_RunD_V1_DATA","/eos/home-c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  
  'QCD_PT-15to30':["/QCD_PT-15to30_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-30to50':["/QCD_PT-30to50_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-50to80':["/QCD_PT-50to80_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-80to120':["/QCD_PT-80to120_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-120to170':["/QCD_PT-120to170_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-170to300':["/QCD_PT-170to300_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-300to470':["/QCD_PT-300to470_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-470to600':["/QCD_PT-470to600_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-600to800':["/QCD_PT-600to800_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-800to1000':["/QCD_PT-800to1000_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-1000to1400':["/QCD_PT-1000to1400_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-1400to1800':["/QCD_PT-1400to1800_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-1800to2400':["/QCD_PT-1800to2400_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-2400to3200':["/QCD_PT-2400to3200_TuneCP5_13p6TeV_pythia8/Run3Summer23MiniAODv4-130X_mcRun3_2023_realistic_v14-v2/MINIAODSIM","Summer23Prompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],

  'QCD_PT-15to30_BPix':["/QCD_PT-15to30_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-30to50_BPix':["/QCD_PT-30to50_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-50to80_BPix':["/QCD_PT-50to80_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-80to120_BPix':["/QCD_PT-80to120_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-120to170_BPix':["/QCD_PT-120to170_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-170to300_BPix':["/QCD_PT-170to300_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-300to470_BPix':["/QCD_PT-300to470_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-470to600_BPix':["/QCD_PT-470to600_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-600to800_BPix':["/QCD_PT-600to800_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-800to1000_BPix':["/QCD_PT-800to1000_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-1000to1400_BPix':["/QCD_PT-1000to1400_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-1400to1800_BPix':["/QCD_PT-1400to1800_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-1800to2400_BPix':["/QCD_PT-1800to2400_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  'QCD_PT-2400to3200_BPix':["/QCD_PT-2400to3200_TuneCP5_13p6TeV_pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v2/MINIAODSIM","Summer23BPixPrompt23_V1_MC","","130X_mcRun3_2023_realistic_v14"],
  #2024 JetMET0
  'JetMET0_Run2024B':["/JetMET0/Run2024B-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraB_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024C':["/JetMET0/Run2024C-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraC_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024D':["/JetMET0/Run2024D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraD_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024E1':["/JetMET0/Run2024E-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraE_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024E2':["/JetMET0/Run2024E-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraE_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024F':["/JetMET0/Run2024F-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_381984-383779_Golden_Run2024F.json","140X_dataRun3_Prompt_v4"],
  'JetMET0_Run2024G':["/JetMET0/Run2024G-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Collisions24_13p6TeV_378981_385016_DCSOnly_TkPx.json","140X_dataRun3_Prompt_v4"],
  'JetMET0_Run2024H':["/JetMET0/Run2024H-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Collisions24_13p6TeV_378981_386047_DCSOnly_TkPx.json","140X_dataRun3_Prompt_v4"],
  #2024 JetMET1
  'JetMET1_Run2024B':["/JetMET1/Run2024B-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraB_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024C':["/JetMET1/Run2024C-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraC_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024D':["/JetMET1/Run2024D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraD_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024E1':["/JetMET1/Run2024E-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraE_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024E2':["/JetMET1/Run2024E-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraE_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024F':["/JetMET1/Run2024F-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_381984-383779_Golden_Run2024F.json","140X_dataRun3_Prompt_v4"],
  'JetMET1_Run2024G':["/JetMET1/Run2024G-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Collisions24_13p6TeV_378981_385016_DCSOnly_TkPx.json","140X_dataRun3_Prompt_v4"],
  'JetMET1_Run2024H':["/JetMET1/Run2024H-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_V1_MC","Collisions24_13p6TeV_378981_386047_DCSOnly_TkPx.json","140X_dataRun3_Prompt_v4"],
}

def main():
  for sample, sample_attributes in samples.items():
    name=sample_attributes[0]
    jecsName=sample_attributes[1]
    lumiJSON=sample_attributes[2]
    globalTag=sample_attributes[3]

    print("Creating file: "+name)

    crabSubmitFile.write("rm -rf crab_"+name+"\n")
    crabSubmitFile.write("crab submit -c crab3_"+name+".py\n")

    file = open("crab3_"+name+".py","w")
    file.write("import sys\n")
    file.write("from CRABClient.UserUtilities import config\n")
    file.write("config = config()")
    file.write("\n")
    file.write("store_dir = \'"+storeDir+"\'\n")
    file.write("sample_name = \'"+name+"\'\n")
    file.write("\n")
    file.write("input_file_dir = \'/afs/cern.ch/work/t/tchatzis/private/run3_2023/CMSSW_13_0_7_patch1/src/JMETriggerAnalysis/NTuplizers/test/\'\n")
    file.write("\n")
    file.write("config.section_(\'General\')\n")
    file.write("config.General.requestName = sample_name\n")
    file.write("config.General.transferOutputs = True\n")
    file.write("config.General.transferLogs = False\n")
    file.write("\n")
    file.write("config.section_(\'JobType\')\n")
    file.write("config.JobType.pluginName = \'Analysis\'\n")
    file.write("config.JobType.maxMemoryMB = 2500\n")
    file.write("config.JobType.psetName = input_file_dir+\'jmeTriggerNTuple2023Data_miniAOD_testObjects_cfg.py\'\n")
    file.write("config.JobType.pyCfgParams = [\'offlineJecs="+jecsName+"\',\'globalTag="+globalTag+"\']\n")
    file.write("config.JobType.allowUndistributedCMSSW = True\n")
    file.write("config.JobType.inputFiles = [input_file_dir+\'"+jecsName+".db\']\n")
    file.write("\n")
    file.write("config.section_(\'Data\')\n")
    file.write("config.Data.publication = False\n")
    file.write("config.Data.ignoreLocality = False\n")
    file.write("config.Data.inputDataset = \'"+sample+"\'\n")
    file.write("config.Data.splitting = \'Automatic\'\n")
    file.write("config.Data.unitsPerJob = 200\n")
    file.write("config.Data.totalUnits = -1\n")
    file.write("\n")
    file.write("config.Data.lumiMask = input_file_dir+\'"+lumiJSON+"\'\n")
    file.write("config.Data.outLFNDirBase = \'/store/user/tchatzis/\'+store_dir+\'/\'+sample_name\n")
    file.write("\n")
    file.write("config.section_(\'Site\')\n")
    file.write("config.Site.storageSite = \'T3_CH_CERNBOX\'\n")
    file.close()

  crabSubmitFile.close()

if __name__=="__main__":
  main()
