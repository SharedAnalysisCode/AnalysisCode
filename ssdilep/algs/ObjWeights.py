#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ObjWeights.py: 
weights applied 
to single objects
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
class MuAllSF(pyframe.core.Algorithm):
    """
    Single muon reco efficiency
    """
    #__________________________________________________________________________
    def __init__(self, name="MuAllSF",
            mu_index       = None,
            #mu_level       = None,
            key            = None,
            scale          = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.mu_index       = mu_index
        #self.mu_level       = mu_level
        self.key            = key
        self.scale          = scale

        assert key, "Must provide key for storing mu iso sf"
    
    #_________________________________________________________________________
    def initialize(self): 
      pass
      """
      self.reco_levels = {"Loose":"Loose", "Medium":"Loose",         "Tight":"Loose"}
      self.iso_levels  = {"Loose":"Loose", "Medium":"FixedCutLoose", "Tight":"FixedCutTightTrackOnly"}
      self.ttva_levels = {"Loose": None,   "Medium": None,           "Tight": None}

      self.mu_levels = ["Loose", "Medium", "Tight"]
      if self.mu_level.startswith("Not"):
        self.mu_levels.remove(self.mu_level.replace("Not",""))
      else:
        assert self.mu_level in self.mu_levels, "ERROR: mu_level %s not recognised!!!" % self.lead_mu_level
        self.mu_levels = [self.mu_level]
      """
    
    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          muon = muons[self.mu_index]
          
          if muon.isTruthMatchedToMuon:
            
            sf *= getattr(muon,"_".join(["RecoEff","SF","Loose"])).at(0)
            sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(0)
            
            if getattr(muon,"isIsolated_FixedCutTightTrackOnly"):
              sf *= getattr(muon,"_".join(["IsoEff","SF","FixedCutTightTrackOnly"])).at(0)
            #elif getattr(muon,"isIsolated_FixedCutLoose"):
            #  sf *= getattr(muon,"_".join(["IsoEff","SF","FixedCutLoose"])).at(0)
            elif getattr(muon,"isIsolated_Loose"):
              sf *= getattr(muon,"_".join(["IsoEff","SF","Loose"])).at(0)
            else: pass

            if self.scale: pass

        if self.key: 
          self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class MuFakeFactorHist(pyframe.core.Algorithm):
    """
    Applies the fake-factors to muon pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuFakeFactor",config_file=None,mu_index=None,key=None,scale=None):
        pyframe.core.Algorithm.__init__(self,name=name)
        self.config_file = config_file
        self.mu_index    = mu_index
        self.key         = key
        self.scale       = scale
        
        assert mu_index in [0,1], "ERROR: mu_index must be in [0,1,2]"
        assert config_file, "Must provide config file!"
        assert key, "Must provide key for storing fakefactor"
    #_________________________________________________________________________
    def initialize(self):
        f = ROOT.TFile.Open(self.config_file)
        assert f, "Failed to open fake-factor config file: %s"%(self.config_file)

        h_ff = f.Get("h_ff")
        assert h_ff, "Failed to get 'h_ff' from %s"%(self.config_file)
        
        self.h_ff = h_ff.Clone()
        self.h_ff.SetDirectory(0)
        f.Close()
    #_________________________________________________________________________
    def execute(self, weight):
        muons = self.store['muons']
        mu = muons[self.mu_index]
        #if not self.sampletype == "datadriven": continue
        #if self.sampletype == "mc": continue
        pt_mu = mu.tlv.Pt()/GeV  
        
        ff_mu = 1.0
        eff_mu = 0.0
        
        ibin_mu = self.h_ff.GetXaxis().FindBin(pt_mu) 
        assert ibin_mu, "ERROR: pt bin for lead mu not found!!!"
        
        # error bars are symmetric
        #if self.mu_index == 0: 
        # The previous line caused a bug in the 
        # application of the fake-factors to the
        # validation region with di-muons triggers
        
        ff_mu = self.h_ff.GetBinContent(ibin_mu)
        eff_mu = self.h_ff.GetBinError(ibin_mu)
        
        if self.scale == 'up': 
          ff_mu +=eff_mu
        if self.scale == 'dn': 
          ff_mu -=eff_mu
        
        if self.key: 
          self.store[self.key] = ff_mu

        return True

#------------------------------------------------------------------------------
class MuFakeFactorGraph(pyframe.core.Algorithm):
    """
    Applies the fake-factors to muon pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuFakeFactor",config_file=None,mu_index=None,key=None,scale=None):
        pyframe.core.Algorithm.__init__(self,name=name)
        self.config_file    = config_file
        self.mu_index       = mu_index
        self.key            = key
        self.scale          = scale
        
        assert mu_index in [0,1], "ERROR: mu_index must be in [0,1]"
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
        muons = self.store['muons']
        mu = muons[self.mu_index]
        #if not self.sampletype == "datadriven": continue
        #if self.sampletype == "mc": continue
        pt_mu = mu.tlv.Pt()/GeV  
        
        for ibin_mu in xrange(1,self.g_ff.GetN()):
          edlow = self.g_ff.GetX()[ibin_mu] - self.g_ff.GetEXlow()[ibin_mu]
          edhi  = self.g_ff.GetX()[ibin_mu] + self.g_ff.GetEXhigh()[ibin_mu]
          if pt_mu>=edlow and pt_mu<edhi: break

        # error bars are asymmetric
        ff_mu = self.g_ff.GetY()[ibin_mu]
        eff_up_mu = self.g_ff.GetEYhigh()[ibin_mu]
        eff_dn_mu = self.g_ff.GetEYlow()[ibin_mu]
        
        if self.scale == 'up': ff_mu +=eff_up_mu
        if self.scale == 'dn': ff_mu -=eff_dn_mu
       
        if self.key: 
          self.store[self.key] = ff_mu

        return True


# EOF
