#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/stream/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <CommonTools/Utils/interface/StringCutObjectSelector.h>
#include <CommonTools/Utils/interface/StringObjectFunction.h>
#include <DataFormats/Common/interface/ValueMap.h>
#include <DataFormats/PatCandidates/interface/Photon.h>
#include <DataFormats/VertexReco/interface/Vertex.h>
#include <DataFormats/VertexReco/interface/VertexFwd.h>
//#include <DataFormats/MuonReco/interface/MuonSelectors.h>

#include <string>
#include <vector>
#include <memory>
#include <utility>

class PhotonPATUserData : public edm::stream::EDProducer<> {
public:
  explicit PhotonPATUserData(const edm::ParameterSet&);

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetToken src_;

  std::vector<std::string> vmaps_bool_;
  std::vector<edm::EDGetToken> vmaps_bool_token_;

  std::vector<std::string> vmaps_float_;
  std::vector<edm::EDGetToken> vmaps_float_token_;

  std::vector<std::pair<std::string, std::string> > v_float_copycats_;

  std::vector<std::pair<std::string, StringCutObjectSelector<pat::Photon, true> > > userInt_stringSelects_;
  std::vector<std::pair<std::string, StringObjectFunction<pat::Photon, true> > > userFloat_stringFuncs_;

  edm::EDGetTokenT<edm::View<reco::Vertex> > primaryVertices_;

  // Muon IDs HZZ
  //bool IDLooseHZZ(const reco::Muon&, const reco::Vertex&);
  //bool IDTightHZZ(const reco::Muon&, const reco::Vertex&);
};

PhotonPATUserData::PhotonPATUserData(const edm::ParameterSet& iConfig) {
  src_ = consumes<edm::View<pat::Photon> >(iConfig.getParameter<edm::InputTag>("src"));

  // ValueMaps [bool]
  vmaps_bool_ = iConfig.exists("valueMaps_bool") ? iConfig.getParameter<std::vector<std::string> >("valueMaps_bool")
                                                 : std::vector<std::string>();

  for (const auto& vm_str : vmaps_bool_) {
    vmaps_bool_token_.emplace_back(consumes<edm::ValueMap<bool> >(edm::InputTag(vm_str)));
  }
  // -----------------

  // ValueMaps [float]
  vmaps_float_ = iConfig.exists("valueMaps_float") ? iConfig.getParameter<std::vector<std::string> >("valueMaps_float")
                                                   : std::vector<std::string>();

  for (const auto& vm_str : vmaps_float_) {
    vmaps_float_token_.emplace_back(consumes<edm::ValueMap<float> >(edm::InputTag(vm_str)));
  }
  // -----------------

  // PSet for userFloat copycat(s)
  const edm::ParameterSet pset_userFloat_copycat = iConfig.exists("userFloat_copycat")
                                                       ? iConfig.getParameter<edm::ParameterSet>("userFloat_copycat")
                                                       : edm::ParameterSet();
  for (unsigned int i = 0; i < pset_userFloat_copycat.getParameterNames().size(); ++i) {
    const std::string pset_arg = pset_userFloat_copycat.getParameterNames().at(i);
    const std::string pset_val = pset_userFloat_copycat.getParameter<std::string>(pset_arg);

    v_float_copycats_.emplace_back(std::make_pair(pset_arg, pset_val));
  }
  // -----------------

  // PSet for userInts from StringCutObjectSelector(s)
  const edm::ParameterSet& pset_userInt_stringSelects =
      iConfig.exists("userInt_stringSelectors") ? iConfig.getParameter<edm::ParameterSet>("userInt_stringSelectors")
                                                : edm::ParameterSet();
  for (const std::string& vname : pset_userInt_stringSelects.getParameterNamesForType<std::string>()) {
    userInt_stringSelects_.emplace_back(std::pair<std::string, StringCutObjectSelector<pat::Photon, true> >(
        vname, pset_userInt_stringSelects.getParameter<std::string>(vname)));
  }
  // -----------------

  // PSet for userFloats from StringObjectFunction(s)
  const edm::ParameterSet& pset_userFloat_stringFuncs =
      iConfig.exists("userFloat_stringFunctions") ? iConfig.getParameter<edm::ParameterSet>("userFloat_stringFunctions")
                                                  : edm::ParameterSet();
  for (const std::string& vname : pset_userFloat_stringFuncs.getParameterNamesForType<std::string>()) {
    userFloat_stringFuncs_.emplace_back(std::pair<std::string, StringObjectFunction<pat::Photon, true> >(
        vname, pset_userFloat_stringFuncs.getParameter<std::string>(vname)));
  }
  // -----------------

  primaryVertices_ = consumes<edm::View<reco::Vertex> >(iConfig.getParameter<edm::InputTag>("primaryVertices"));

  produces<pat::PhotonCollection>();
}

void PhotonPATUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<pat::Photon> > patPhotons;
  iEvent.getByToken(src_, patPhotons);

  // ValueMaps [bool]
  std::vector<edm::Handle<edm::ValueMap<bool> > > v_vmap_bool;
  for (unsigned int i = 0; i < vmaps_bool_token_.size(); ++i) {
    edm::Handle<edm::ValueMap<bool> > vmap;
    iEvent.getByToken(vmaps_bool_token_.at(i), vmap);
    v_vmap_bool.emplace_back(vmap);
  }
  // -----------------

  // ValueMaps [float]
  std::vector<edm::Handle<edm::ValueMap<float> > > v_vmap_float;
  for (unsigned int i = 0; i < vmaps_float_token_.size(); ++i) {
    edm::Handle<edm::ValueMap<float> > vmap;
    iEvent.getByToken(vmaps_float_token_.at(i), vmap);
    v_vmap_float.emplace_back(vmap);
  }
  // -----------------

  // PV
  edm::Handle<edm::View<reco::Vertex> > recoVtxs;
  iEvent.getByToken(primaryVertices_, recoVtxs);

  const auto* PV = (!recoVtxs->empty()) ? &(recoVtxs->at(0)) : nullptr;

  if (PV == nullptr) {
    edm::LogWarning("Input") << "@@@ PhotonPATUserData::produce -- empty collection of primary vertices";
  }
  // -----------------

  std::unique_ptr<pat::PhotonCollection> newPhotons(new pat::PhotonCollection);
  newPhotons->reserve(patPhotons->size());

  for (unsigned int i_photon = 0; i_photon < patPhotons->size(); ++i_photon) {
    newPhotons->emplace_back(patPhotons->at(i_photon));
    pat::Photon& muo = newPhotons->back();

    // ValueMaps [bool]
    for (unsigned int i = 0; i < v_vmap_bool.size(); ++i) {
      if (muo.hasUserInt(vmaps_bool_.at(i))) {
        throw cms::Exception("InputError")
            << "@@@ PhotonPATUserData::produce -- PAT user-int label already exists: " << vmaps_bool_.at(i);
      }

      if (v_vmap_bool.at(i)->contains(patPhotons->refAt(i_photon).id())) {
        const bool val = (*(v_vmap_bool.at(i)))[patPhotons->refAt(i_photon)];
        muo.addUserInt(vmaps_bool_.at(i), int(val));
      } else {
        throw cms::Exception("InputError")
            << "@@@ PhotonPATUserData::produce -- object reference not found in ValueMap<bool> \"" << vmaps_bool_.at(i)
            << "\"";
      }
    }
    // -----------------

    // ValueMaps [float]
    for (unsigned int i = 0; i < v_vmap_float.size(); ++i) {
      if (muo.hasUserFloat(vmaps_float_.at(i))) {
        throw cms::Exception("InputError")
            << "@@@ PhotonPATUserData::produce -- PAT user-float label already exists: " << vmaps_float_.at(i);
      }

      if (v_vmap_float.at(i)->contains(patPhotons->refAt(i_photon).id())) {
        const float val = (*(v_vmap_float.at(i)))[patPhotons->refAt(i_photon)];
        muo.addUserFloat(vmaps_float_.at(i), val);
      } else {
        throw cms::Exception("InputError")
            << "@@@ PhotonPATUserData::produce -- object reference not found in ValueMap<float> \"" << vmaps_float_.at(i)
            << "\"";
      }
    }
    // -----------------

    // userFloat copycat(s)
    for (const auto& userfloat_copycat : v_float_copycats_) {
      const std::string& ref = userfloat_copycat.second;
      const std::string& out = userfloat_copycat.first;

      if (muo.hasUserFloat(ref) == false) {
        throw cms::Exception("InputError")
            << "@@@ PhotonPATUserData::produce -- PAT user-float key \"" + ref + "\" not found";
      }

      if (muo.hasUserFloat(out) == true) {
        throw cms::Exception("InputError")
            << "@@@ PhotonPATUserData::produce -- target PAT user-float key \"" + out + "\" already exists";
      }

      muo.addUserFloat(out, muo.userFloat(ref));
    }
  }

  iEvent.put(std::move(newPhotons));

  return;
}

void PhotonPATUserData::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();

  descriptions.add("PhotonPATUserData", desc);
}

DEFINE_FWK_MODULE(PhotonPATUserData);
