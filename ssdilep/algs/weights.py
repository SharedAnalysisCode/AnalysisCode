#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
weights.py
"""

#import fnmatch
#import os
#import sys
from math import sqrt
from array import array
# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# ROOT
import ROOT
import metaroot

# pyframe
import pyframe

# pyutils
import rootutils

import mcutils

GeV = 1000.0

#------------------------------------------------------------------------------
class Pileup(pyframe.core.Algorithm):
    """
    multiply event weight by pileup weight

    if 'key' is specified the pileup weight will be put in the store
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="Pileup", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #_________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            #wpileup = self.chain.pileup_weight
            wpileup = self.chain.weight_pileup
            if self.key: self.store[self.key] = wpileup
            self.set_weight(wpileup*weight)
        return True

#------------------------------------------------------------------------------
class MCEventWeight(pyframe.core.Algorithm):
    """
    multiply event weight by MC weight

    if 'key' is specified the MC weight will be put in the store
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="MCEventWeight", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #_________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            wmc = self.chain.mcEventWeight
            if self.key: self.store[self.key] = wmc
            self.set_weight(wmc*weight)
        return True


#------------------------------------------------------------------------------
class MuAllSF(pyframe.core.Algorithm):
    """
    Signle muon reco efficiency
    """
    #__________________________________________________________________________
    def __init__(self, name="MuIsoSF",
            mu_index       = None,
            mu_level       = None,
            key            = None,
            scale          = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.mu_index       = mu_index
        self.mu_level       = mu_level
        self.key            = key
        self.scale          = scale

        assert key, "Must provide key for storing mu iso sf"
    #_________________________________________________________________________
    def initialize(self):
      if self.mu_level = "Loose":
        self.mu_reco_level = "Loose"
        self.mu_iso_level  = "Loose"
        self.mu_ttva_level = None
      
      elif self.mu_level = "Medium":
        self.mu_reco_level = "Loose"
        self.mu_iso_level  = "FixedCutLoose"
        self.mu_ttva_level = None
      
      elif self.mu_level = "Tight":
        self.mu_reco_level = "Loose"
        self.mu_iso_level  = "FixedCutTightTrackOnly"
        self.mu_ttva_level = None

    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          muon = muons[self.mu_index]
          
          if muon.isTruthMatchedToMuon:
              sf *= getattr(muon,"_".join(["RecoEff","SF",str(self.mu_reco_level)])).at(0)
              sf *= getattr(muon,"_".join(["IsoEff","SF",str(self.mu_iso_level)])).at(0)
              sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(0)
              
              if self.scale: pass
        
          if self.key: 
            self.store[self.key] = sf
        return True


#------------------------------------------------------------------------------
class MuTrigSF(pyframe.core.Algorithm):
    """
    Muon trigger scale factor
    """
    #__________________________________________________________________________
    def __init__(self, name="MuTrigSF",
            #mu_index         = None,
            mu_trig_iso_level = None,
            mu_trig_chain     = None,
            key               = None,
            scale             = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        #self.mu_index         = mu_index
        self.mu_trig_iso_level = mu_trig_iso_level
        self.mu_trig_chain     = mu_trig_chain
        self.key               = key
        self.scale             = scale

        assert key, "Must provide key for storing mu reco sf"
    #_________________________________________________________________________
    def initialize(self):
      allowed_levels = [
          "Loose_Loose",
          "Loose_FixedCutTightTrackOnly",
          ]
      assert self.mu_trig_iso_level in allowed_levels, "ERROR: mu trig iso level %s is invalid. Check configuration!!!" % self.mu_trig_iso_level

    #_________________________________________________________________________
    def execute(self, weight):
        trig_sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          
          num = 1.0 
          den = 1.0

          for m in muons:
           if m.isTruthMatchedToMuon: 
             if not m.isMatchedToTrigChain(self.mu_trig_iso_level): continue
             sf  =  getattr(m,"_".join(["TrigEff","SF",str(self.mu_trig_iso_level)])).at(0)
             eff = getattr(m,"_".join(["TrigMCEff",str(self.mu_trig_iso_level)])).at(0)
             num *= 1 - sf * eff
             den *= 1 - eff
          
          num = ( 1 - num )
          den = ( 1 - den )
          
          if den > 0:
            trig_sf = num / den

          #if self.scale: pass

          if self.key: 
            self.store[self.key] = trig_sf
        return True


#------------------------------------------------------------------------------
class MuRecoSF(pyframe.core.Algorithm):
    """
    Signle muon reco efficiency
    """
    #__________________________________________________________________________
    def __init__(self, name="MuRecoSF",
            mu_index      = None,
            mu_reco_level = None,
            key           = None,
            scale         = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.mu_index      = mu_index
        self.mu_reco_level = mu_reco_level
        self.key           = key
        self.scale         = scale

        assert key, "Must provide key for storing mu reco sf"
    #_________________________________________________________________________
    def initialize(self):
      allowed_levels = [
          "Loose",
          ]
      assert self.mu_reco_level in allowed_levels, "ERROR: mu reco level %s is invalid. Check configuration!!!" % self.mu_reco_level

    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          muon = muons[self.mu_index]
          
          if muon.isTruthMatchedToMuon:
              sf *= getattr(muon,"_".join(["RecoEff","SF",str(self.mu_reco_level)])).at(0)
              if self.scale: pass
        
          if self.key: 
            self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class MuPairsRecoSF(pyframe.core.Algorithm):
    """
    Muon pairs reco efficiency
    Apply weight to all pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuPairsRecoSF",
            lead_mu_reco_level    = None,
            sublead_mu_reco_level = None,
            key                   = None,
            scale                 = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.lead_mu_reco_level    = lead_mu_reco_level
        self.sublead_mu_reco_level = sublead_mu_reco_level
        self.key                   = key
        self.scale                 = scale

        assert key, "Must provide key for storing mu pairs reco sf"
    #_________________________________________________________________________
    def initialize(self):
      allowed_levels = [
          "Loose",
          ]
      assert self.lead_mu_reco_level in allowed_levels, "ERROR: lead mu reco level %s is invalid. Check configuration!!!" % self.lead_mu_reco_level
      assert self.sublead_mu_reco_level in allowed_levels, "ERROR: sublead mu reco level %s is invalid. Check configuration!!!" % self.sublead_mu_reco_level

    #_________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
          mu_pairs = self.store['mu_pairs']

          for mp in mu_pairs:
            sf_lead = 1.0
            sf_sublead = 1.0
            
            if mp.lead.isTruthMatchedToMuon:
              sf_lead = getattr(mp.lead,"_".join(["RecoEff","SF",str(self.lead_mu_reco_level)])).at(0)
            if mp.sublead.isTruthMatchedToMuon:
              sf_sublead = getattr(mp.sublead,"_".join(["RecoEff","SF",str(self.sublead_mu_reco_level)])).at(0)
            
            mp.StoreWeight(sf_lead * sf_sublead)
              
          #if self.scale: pass
        
          if self.key: 
              self.store[self.key] = 1.0
        return True



#------------------------------------------------------------------------------
class MuIsoSF(pyframe.core.Algorithm):
    """
    Signle muon reco efficiency
    """
    #__________________________________________________________________________
    def __init__(self, name="MuIsoSF",
            mu_index      = None,
            mu_iso_level  = None,
            key           = None,
            scale         = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.mu_index      = mu_index
        self.mu_iso_level  = mu_iso_level
        self.key           = key
        self.scale         = scale

        assert key, "Must provide key for storing mu iso sf"
    #_________________________________________________________________________
    def initialize(self):
      allowed_levels = [
          "LooseTrackOnly",
          "Loose",
          "Tight",
          "Gradient",
          "GradientLoose",
          "FixedCutTightTrackOnly",
          ]
      assert self.mu_iso_level in allowed_levels, "ERROR: mu iso level %s is invalid. Check configuration!!!" % self.mu_iso_level
    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          muon = muons[self.mu_index]
          
          if muon.isTruthMatchedToMuon:
              sf *= getattr(muon,"_".join(["IsoEff","SF",str(self.mu_iso_level)])).at(0)
              if self.scale: pass
        
          if self.key: 
            self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class MuPairsIsoSF(pyframe.core.Algorithm):
    """
    Muon pairs iso efficiency
    Apply weight to all pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuPairsIsoSF",
            lead_mu_iso_level    = None,
            sublead_mu_iso_level = None,
            key                   = None,
            scale                 = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.lead_mu_iso_level    = lead_mu_iso_level
        self.sublead_mu_iso_level = sublead_mu_iso_level
        self.key                   = key
        self.scale                 = scale

        assert key, "Must provide key for storing mu pairs iso sf"
    #_________________________________________________________________________
    def initialize(self):
      allowed_levels = [
          "LooseTrackOnly",
          "Loose",
          "Tight",
          "Gradient",
          "GradientLoose",
          "FixedCutTightTrackOnly",
          ]
      assert self.lead_mu_iso_level in allowed_levels, "ERROR: lead mu iso level %s is invalid. Check configuration!!!" % self.lead_mu_iso_level
      assert self.sublead_mu_iso_level in allowed_levels, "ERROR: sublead mu iso level %s is invalid. Check configuration!!!" % self.sublead_mu_iso_level
    #_________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
          mu_pairs = self.store['mu_pairs']

          for mp in mu_pairs:
            sf_lead = 1.0
            sf_sublead = 1.0
            
            if mp.lead.isTruthMatchedToMuon:
              sf_lead = getattr(mp.lead,"_".join(["IsoEff","SF",str(self.lead_mu_iso_level)])).at(0)
            if mp.sublead.isTruthMatchedToMuon:
              sf_sublead = getattr(mp.sublead,"_".join(["IsoEff","SF",str(self.sublead_mu_iso_level)])).at(0)
            
            mp.StoreWeight(sf_lead * sf_sublead)
              
          #if self.scale: pass
        
          if self.key: 
              self.store[self.key] = 1.0
        return True

#------------------------------------------------------------------------------
class MuTTVASF(pyframe.core.Algorithm):
    """
    Signle muon TTVA efficiency
    """
    #__________________________________________________________________________
    def __init__(self, name="MuTTVASF",
            mu_index      = None,
            mu_ttva_level = None,
            key           = None,
            scale         = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.mu_index      = mu_index
        self.mu_ttva_level = mu_ttva_level
        self.key           = key
        self.scale         = scale

        assert key, "Must provide key for storing mu TTVA sf"
    #_________________________________________________________________________
    def initialize(self):
      allowed_levels = None
      assert self.mu_ttva_level == allowed_levels, "ERROR: mu TTVA level %s is invalid. Check configuration!!!" % self.mu_ttva_level
    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          muon = muons[self.mu_index]
          
          if muon.isTruthMatchedToMuon:
              sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(0)
              if self.scale: pass
        
          if self.key: 
            self.store[self.key] = sf
        return True


#------------------------------------------------------------------------------
class MuPairsTTVASF(pyframe.core.Algorithm):
    """
    Muon pairs ttva efficiency
    Apply weight to all pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuPairsTTVASF",
            lead_mu_ttva_level    = None,
            sublead_mu_ttva_level = None,
            key                   = None,
            scale                 = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.lead_mu_ttva_level    = lead_mu_ttva_level
        self.sublead_mu_ttva_level = sublead_mu_ttva_level
        self.key                   = key
        self.scale                 = scale

        assert key, "Must provide key for storing mu pairs ttva sf"
    #_________________________________________________________________________
    def initialize(self):
      allowed_levels = None
      assert self.lead_mu_ttva_level == allowed_levels, "ERROR: lead mu ttva level %s is invalid. Check configuration!!!" % self.lead_mu_ttva_level
      assert self.sublead_mu_ttva_level == allowed_levels, "ERROR: sublead mu ttva level %s is invalid. Check configuration!!!" % self.sublead_mu_ttva_level
    #_________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
          mu_pairs = self.store['mu_pairs']

          for mp in mu_pairs:
            sf_lead = 1.0
            sf_sublead = 1.0
            
            if mp.lead.isTruthMatchedToMuon:
              sf_lead = getattr(mp.lead,"_".join(["TTVAEff","SF"])).at(0)
            if mp.sublead.isTruthMatchedToMuon:
              sf_sublead = getattr(mp.sublead,"_".join(["TTVAEff","SF"])).at(0)
            
            mp.StoreWeight(sf_lead * sf_sublead)
              
          #if self.scale: pass
        
          if self.key: 
              self.store[self.key] = 1.0
        return True



#------------------------------------------------------------------------------
class KFactor(pyframe.core.Algorithm):
    """
    multiply the event weight by the kfactor for Z/DY samples

    setting 'qcd_only = True' will use QCD-only k-factors for DYtautau, which 
    is used when reweighting DYtautau to Z'tautau signal samples.

    if 'key' is specified the kfactor will be put in the store
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,scale=None,qcd_only=False,key=None):
        pyframe.core.Algorithm.__init__(self, name="KFactor", isfilter=True)
        self.cutflow = cutflow
        self.qcd_only = qcd_only
        self.key = key
        ROOT.gSystem.Load('libkfactors')

        assert scale in [None,'up','dn'],"Invalid scale: %s"%(scale)
        self.sys_code = 0
        if scale == 'up': self.sys_code = 1
        if scale == 'dn': self.sys_code = 2


    #_________________________________________________________________________
    def execute(self, weight):
        kf=1.0
        if "mc" in self.sampletype:
            if mcutils.isditau_pythia(self.chain.mc_channel_number):
                resomass = self.chain.RESOMASS
                if self.qcd_only:
                    kf = ROOT.kfactors.DiTauSig(resomass,self.sys_code)
                else:
                    kf = ROOT.kfactors.DiTauBkg(resomass,self.sys_code)
            elif mcutils.isdilep_powheg(self.chain.mc_channel_number):
                resomass = self.chain.RESOMASS
                kf = ROOT.kfactors.DiLepBkg(resomass,self.sys_code)
            if self.key: self.store[self.key] = kf
        self.set_weight(kf*weight)
        return True


#------------------------------------------------------------------------------
class FakeFactor(pyframe.core.Algorithm):
    """
    python implementation of the fake-factor getter.

    takes input histograms from the FakeWeights package.

    'key' must be specified as the fakefactor is put in the store
    """
    #__________________________________________________________________________
    def __init__(self, name="FakeFactor",config_file=None,tau_index=None,key=None,scale=None):
        pyframe.core.Algorithm.__init__(self,name=name)
        self.config_file = config_file
        self.tau_index = tau_index
        self.key = key
        self.scale = scale

        assert config_file, "Must provide config file!"
        assert key, "Must provide key for storing fakefactor"
    #_________________________________________________________________________
    def initialize(self):
        f = ROOT.TFile.Open(self.config_file)
        assert f, "Failed to open fake-factor config file: %s"%(self.config_file)
        
        h_1P_NoS = f.Get("fake_factor_1P_NoS")
        assert h_1P_NoS, "Failed to get 'fake_factor_1P_NoS' from %s"%(self.config_file)

        h_3P_NoS = f.Get("fake_factor_3P_NoS")
        assert h_3P_NoS, "Failed to get 'fake_factor_3P_NoS' from %s"%(self.config_file)

        self.h_1P_NoS = h_1P_NoS.Clone()
        #self.h_1P_NoS.SetDirectory(0)

        self.h_3P_NoS = h_3P_NoS.Clone()
        #self.h_3P_NoS.SetDirectory(0)

        f.Close()

    #_________________________________________________________________________
    def execute(self, weight):
        taus = self.store['taus']
        tau = taus[self.tau_index]

        pt = tau.tlv.Pt()/GeV

        for ibin in xrange(0,self.h_1P_NoS.GetN()):
          edlow = self.h_1P_NoS.GetX()[ibin] - self.h_1P_NoS.GetEX()[ibin]
          edhi  = self.h_1P_NoS.GetX()[ibin] + self.h_1P_NoS.GetEX()[ibin]
          if pt>=edlow and pt<edhi: break

        #ibin = self.h_1P_NoS.GetXaxis().FindBin(pt)

        # error bars are symmetric
        if tau.numTrack == 1: 
          ff = self.h_1P_NoS.GetY()[ibin]
          eff = self.h_1P_NoS.GetEY()[ibin]
        elif tau.numTrack == 3:
          ff = self.h_3P_NoS.GetY()[ibin]
          eff = self.h_3P_NoS.GetEY()[ibin]
        else: 
            assert False, "Cannot compute fake-factor for tau with %d tracks"%(tau.numTrack)

        if self.scale == 'up': ff +=eff
        if self.scale == 'dn': ff -=eff

        if self.key: self.store[self.key] = ff

        return True


#------------------------------------------------------------------------------
class FakeWeight(pyframe.core.Algorithm):
    """
    python wrapper for FakeWeight tool
   
    tau_id_level: 
      1 - loose
      2 - medium
      3 - tight

    has_trigger
      True  - ID+Trigger
      False - ID

    fail_id - for fail ID control regions

    'key' must be specified as the fakeweight is put in the store
    """
    #__________________________________________________________________________
    def __init__(self, name="FakeWeight",
            config_file=None,
            tau_index=None,
            tau_id_level=None,
            has_trigger=False,
            fail_id=False,
            key=None,
            uncertainty=None,
            scale=None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.config_file = config_file
        self.tau_index = tau_index
        self.tau_id_level = tau_id_level
        self.has_trigger = has_trigger
        self.fail_id = fail_id
        self.key = key
        self.scale = scale
        self.uncertainty = uncertainty

        assert config_file, "Must provide config file!"
        assert key, "Must provide key for storing fakefactor"
    #_________________________________________________________________________
    def initialize(self):

        ROOT.gSystem.Load('libFakeWeightTool')
        self.tool = ROOT.FakeWeightScaler()
        self.tool.readGraphsFromFile(self.config_file)

    #_________________________________________________________________________
    def execute(self, weight):
        fw=1.0
        if "mc" in self.sampletype: 
            taus = self.store['taus']
            charge_product = int(taus[0].charge * taus[1].charge)
            tau = taus[self.tau_index]
            ## only apply fake weight to fake-taus   
            # pT has to be passed in MeV
            if not tau.trueTauAssoc_matched:
                fw = self.tool.getWeight(
                        tau.tlv.Pt(),
                        tau.numTrack,
                        self.tau_id_level,
                        self.has_trigger,
                        charge_product,
                        self.fail_id,
                        )

                ## if is_statonly take unc from the tool
                if not self.uncertainty:
                  unc_dir = 0 
                  if self.scale == 'up': unc_dir =  1
                  if self.scale == 'dn': unc_dir = -1

                  efw = self.tool.getUncertainty(
                           tau.tlv.Pt(),
                           tau.numTrack,
                           self.tau_id_level,
                           self.has_trigger,
                           charge_product,
                           unc_dir,
                           )
                  if self.scale   == 'up': fw += efw
                  elif self.scale == 'dn': fw -= efw

                else:
                  if self.scale   == 'up': fw *= (1.+self.uncertainty)
                  elif self.scale == 'dn': fw *= (1.-self.uncertainty)

        if self.key: self.store[self.key] = fw

        return True


#------------------------------------------------------------------------------
class TauTriggerSFLowPt(pyframe.core.Algorithm):
    """
    Same as TauTriggerSF but only applies a weight to 
    low pt (<100 GeV) taus. Used to split the tau
    trigger systematics in different components

    """
    #__________________________________________________________________________
    def __init__(self, name="TauTriggerUncertainty",
            config_file=None,
            tau_id_level=None,
            tau_index=None,
            key=None,
            scale=None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.config_file = config_file
        self.tau_id_level = tau_id_level
        self.tau_index = tau_index
        self.key = key
        self.scale = scale

        assert key, "Must provide key for storing trigger sf"
        assert scale in [None,'up','dn'], "scale must be in [None,'up','dn']"

    #_________________________________________________________________________
    def initialize(self):
        if self.config_file: 
            ROOT.gSystem.Load('libTrigTauEfficiency') 
            self.tool = ROOT.TrigTauEfficiency()
            assert self.tool.loadInputFile(self.config_file) == 0, "Failed initialising from input file: %s"%(self.config_file)
            
            if   self.tau_id_level == 1: self.level = 'BDTl' 
            elif self.tau_id_level == 2: self.level = 'BDTm' 
            elif self.tau_id_level == 3: self.level = 'BDTt'
            else:
                assert False, "Invalid tau ID level, must be in [1,2,3]!"
   
    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
            taus = self.store['taus']
            tau = taus[self.tau_index]
            ## only apply trigger sf if trigger-matched tau is truth-matched
            if tau.trueTauAssoc_matched:
                ## pt < 100 GeV -> SF from tag and probe
                if self.config_file and tau.tlv.Pt()<100.0*GeV:
                    pt = tau.tlv.Pt()
                    eta = tau.tlv.Eta()
                    prong_str = '1p' if tau.numTrack == 1 else '3p'
                    eveto_str = 'EVnone'
                    run = self.chain.RandomRunNumber
                    # pT has to be in MeV for the tool
                    if tau.tlv.Pt()<55.0*GeV: 
                      sf = self.tool.getSF(pt,eta,0,run,prong_str,self.level,eveto_str)
                    else: pass
                    sf_tool = self.tool.getSF(pt,eta,0,run,prong_str,self.level,eveto_str)
                    # WARNING: flip the uncertainty due to bug in trigger package
                    if self.scale: 
                        if self.scale=='up':
                            data_stat = self.tool.getSF(pt,eta,+1,run,prong_str,self.level,eveto_str) 
                            mc_stat   = self.tool.getSF(pt,eta,+2,run,prong_str,self.level,eveto_str) 
                            sys       = self.tool.getSF(pt,eta,+3,run,prong_str,self.level,eveto_str) 
                        elif self.scale=='dn':
                            data_stat = self.tool.getSF(pt,eta,-1,run,prong_str,self.level,eveto_str) 
                            mc_stat   = self.tool.getSF(pt,eta,-2,run,prong_str,self.level,eveto_str) 
                            sys       = self.tool.getSF(pt,eta,-3,run,prong_str,self.level,eveto_str) 
                        # sum all in quadrature and then obtain relative unc
                        unc = sqrt(sum([pow(p,2) for p in [data_stat,mc_stat,sys]]))
                        rel_unc = unc / sf_tool
                        if self.scale=='up':   sf += rel_unc * sf
                        elif self.scale=='dn': sf -= rel_unc * sf
                ## pt > 100 -> does not do anything
                else: pass

        if self.key: 
          self.store[self.key] = sf

        return True


# EOF
