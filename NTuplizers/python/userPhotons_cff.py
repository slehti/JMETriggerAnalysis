import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.selectionLayer1.photonSelector_cfi import selectedPatPhotons

def userPhotons(process):
    
    process.userPhotonsTask = cms.Task()

    process.userPreselectedPhotons = selectedPatPhotons.clone(
      src = 'slimmedPhotons',
      cut = '(pt > 15.) && (abs(eta) < 1.3)',
    )

    process.userPhotonsTask.add(process.userPreselectedPhotons)
    _lastPhotonCollection = 'userPreselectedPhotons'

    process.userPhotonsWithUserData = cms.EDProducer('PhotonPATUserData',
      src = cms.InputTag('userPreselectedPhotons'),
      primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
      valueMaps_float = cms.vstring(),
      userFloat_copycat = cms.PSet(),
      userInt_stringSelectors = cms.PSet(),
    )

    process.userPhotonsTask.add(process.userPhotonsWithUserData)
    _lastPhotonCollection = 'userPhotonsWithUserData'

    process.userIsolatedPhotons = selectedPatPhotons.clone(
      src = 'userPhotonsWithUserData',
      #cut = '(pt > 30.) && (userInt("cutBasedPhotonID-RunIIIWinter22-122X-V1-tight") > 0)',
      cut = '(pt > 15.)',
    )

    process.userPhotonsTask.add(process.userIsolatedPhotons)
    _lastPhotonCollection = 'userIsolatedPhotons'
    

    process.userPhotonsSequence = cms.Sequence(process.userPhotonsTask)

    return process, _lastPhotonCollection
