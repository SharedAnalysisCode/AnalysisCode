#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PairWeights.py:
weights applied to 
pairs in the event
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
class MuPairsAllSF(pyframe.core.Algorithm):
    """
    Muon pairs reco efficiency
    Apply weight to all pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuPairsAllSF",
            #lead_mu_level    = None,
            #sublead_mu_level = None,
            key              = None,
            scale            = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        #self.lead_mu_level    = lead_mu_level
        #self.sublead_mu_level = sublead_mu_level
        self.key              = key
        self.scale            = scale

        assert key, "Must provide key for storing mu pairs reco sf"
    #_________________________________________________________________________
    def initialize(self):
      pass
      """
      self.reco_levels = {"Loose":"Loose", "Medium":"Loose",         "Tight":"Loose"}
      self.iso_levels  = {"Loose":"Loose", "Medium":"FixedCutLoose", "Tight":"FixedCutTightTrackOnly"}
      self.ttva_levels = {"Loose": None,   "Medium": None,           "Tight": None}

      self.lead_mu_levels = ["Loose", "Medium", "Tight"]
      if self.lead_mu_level.startswith("Not"):
        self.lead_mu_levels.remove(self.lead_mu_level.replace("Not",""))
      else:
        assert self.lead_mu_level in self.lead_mu_levels, "ERROR: lead_mu_level %s not recognised!!!" % self.lead_mu_level
        self.lead_mu_levels = [self.lead_mu_level]
      
      self.sublead_mu_levels = ["Loose", "Medium", "Tight"]
      if self.sublead_mu_level.startswith("Not"):
        self.sublead_mu_levels.remove(self.sublead_mu_level.replace("Not",""))
      else:
        assert self.sublead_mu_level in self.sublead_mu_levels, "ERROR: sublead_mu_level %s not recognised!!!" % self.sublead_mu_level
        self.sublead_mu_levels = [self.sublead_mu_level]
      """

    #_________________________________________________________________________
    def execute(self, weight):
        mu_pairs = self.store['mu_pairs']

        for mp in mu_pairs:
          mp.StoreWeight(self.key, 1.0)
          if "mc" in self.sampletype: 
             sf_lead = 1.0
             sf_sublead = 1.0
             
             if mp.lead.isTruthMatchedToMuon:
               sf_lead *= getattr(mp.lead,"_".join(["RecoEff","SF","Loose"])).at(0)
               sf_lead *= getattr(mp.lead,"_".join(["TTVAEff","SF"])).at(0)
            
               if getattr(mp.lead,"isIsolated_FixedCutTightTrackOnly"):
                 sf_lead *= getattr(mp.lead,"_".join(["IsoEff","SF","FixedCutTightTrackOnly"])).at(0)
               elif getattr(mp.lead,"isIsolated_FixedCutLoose"):
                 sf_lead *= getattr(mp.lead,"_".join(["IsoEff","SF","FixedCutLoose"])).at(0)
               elif getattr(mp.lead,"isIsolated_Loose"):
                 sf_lead *= getattr(mp.lead,"_".join(["IsoEff","SF","Loose"])).at(0)
               else: pass
             
             if mp.sublead.isTruthMatchedToMuon:
               sf_sublead *= getattr(mp.sublead,"_".join(["RecoEff","SF","Loose"])).at(0)
               sf_sublead *= getattr(mp.sublead,"_".join(["TTVAEff","SF"])).at(0)
            
               if getattr(mp.sublead,"isIsolated_FixedCutTightTrackOnly"):
                 sf_sublead *= getattr(mp.sublead,"_".join(["IsoEff","SF","FixedCutTightTrackOnly"])).at(0)
               elif getattr(mp.sublead,"isIsolated_FixedCutLoose"):
                 sf_sublead *= getattr(mp.sublead,"_".join(["IsoEff","SF","FixedCutLoose"])).at(0)
               elif getattr(mp.sublead,"isIsolated_Loose"):
                 sf_sublead *= getattr(mp.sublead,"_".join(["IsoEff","SF","Loose"])).at(0)
               else: pass
             
             mp.StoreWeight(self.key, sf_lead * sf_sublead)
               
          #if self.scale: pass
        
        if self.key: 
            self.store[self.key] = 1.0
        
        return True


#------------------------------------------------------------------------------
class MuPairsFakeFactor(pyframe.core.Algorithm):
    """
    Applies the fake-factors to muon pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuPairsFakeFactor",config_file=None,mu_index=None,key=None,scale=None):
        pyframe.core.Algorithm.__init__(self,name=name)
        self.config_file = config_file
        self.mu_index    = mu_index
        self.key         = key
        self.scale       = scale
        
        assert mu_index in [0,1,2], "ERROR: mu_index must be in [0,1,2]"
        assert config_file, "Must provide config file!"
        assert key, "Must provide key for storing fakefactor"
    #_________________________________________________________________________
    def initialize(self):
        f = ROOT.TFile.Open(self.config_file)
        assert f, "Failed to open fake-factor config file: %s"%(self.config_file)

        g_ff = f.Get("g_ff_stat_sys")
        assert g_ff, "Failed to get 'g_ff' from %s"%(self.config_file)

        self.g_ff = g_ff.Clone()
        f.Close()
    #_________________________________________________________________________
    def execute(self, weight):
        mu_pairs = self.store['mu_pairs']
        for mp in mu_pairs:
          #if not self.sampletype == "datadriven": continue
          #if self.sampletype == "mc": continue
          mp.StoreWeight(self.key,1.0)
          pt_mulead = mp.lead.tlv.Pt()/GeV  
          pt_musublead = mp.sublead.tlv.Pt()/GeV  
          
          for ibin_mulead in xrange(1,self.g_ff.GetN()):
           edlow = self.g_ff.GetX()[ibin_mulead] - self.g_ff.GetEXlow()[ibin_mulead]
           edhi  = self.g_ff.GetX()[ibin_mulead] + self.g_ff.GetEXhigh()[ibin_mulead]
           if pt_mulead>=edlow and pt_mulead<edhi: break
 
          for ibin_musublead in xrange(1,self.g_ff.GetN()):
           edlow = self.g_ff.GetX()[ibin_musublead] - self.g_ff.GetEXlow()[ibin_musublead]
           edhi  = self.g_ff.GetX()[ibin_musublead] + self.g_ff.GetEXhigh()[ibin_musublead]
           if pt_musublead>=edlow and pt_musublead<edhi: break
 
          ff_mulead = 1.0 
          ff_musublead = 1.0 

          eff_up_mulead = 0.0 
          eff_up_musublead = 0.0 

          eff_dn_mulead = 0.0 
          eff_dn_musublead = 0.0 

          # error bars are asymmetric
          if self.mu_index == 0 or self.mu_index == 2:
            ff_mulead = self.g_ff.GetY()[ibin_mulead]
            eff_up_mulead = self.g_ff.GetEYhigh()[ibin_mulead]
            eff_dn_mulead = self.g_ff.GetEYlow()[ibin_mulead]
          if self.mu_index == 1 or self.mu_index == 2:
            ff_musublead = self.g_ff.GetY()[ibin_musublead]
            eff_up_musublead = self.g_ff.GetEYhigh()[ibin_musublead]
            eff_dn_musublead = self.g_ff.GetEYlow()[ibin_musublead]
 
          if self.scale == 'up': 
           ff_mulead +=eff_up_mulead
           ff_musublead +=eff_up_musublead
          if self.scale == 'dn': 
           ff_mulead +=eff_dn_mulead
           ff_musublead +=eff_dn_musublead
 
          mp.StoreWeight(self.key, ff_mulead * ff_musublead)
 
        if self.key:
           self.store[self.key] = 1.0

        return True


# EOF
