#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EvWeights.py:
weights applied
to the event
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
class TrigPresc(pyframe.core.Algorithm):
    """
    Algorithm to unprescale data
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="TrigPresc", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "data" in self.sampletype: 
            #trigpresc = self.chain.triggerPrescales.at(0)
            print self.chain.triggerPrescales
            #if self.key: self.store[self.key] = trigpresc
            #self.set_weight(trigpresc*weight)
        return True

#------------------------------------------------------------------------------
class DataUnPresc(pyframe.core.Algorithm):
    """
    Algorithm to unprescale data
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="TrigPresc", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "data" in self.sampletype: 
            trigpresc = self.chain.prescale_DataWeight
            if self.key: self.store[self.key] = trigpresc
            self.set_weight(trigpresc*weight)
        return True


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
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
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
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            wmc = self.chain.mcEventWeight
            if self.key: self.store[self.key] = wmc
            self.set_weight(wmc*weight)
        return True

#------------------------------------------------------------------------------
class MuTrigSF(pyframe.core.Algorithm):
    """
    Muon trigger scale factor
    """
    #__________________________________________________________________________
    def __init__(self, name="MuTrigSF",
            #mu_index      = None,
            is_single_mu   = None,
            is_di_mu       = None,
            mu_trig_level  = None,
            mu_trig_chain  = None,
            key            = None,
            scale          = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        #self.mu_index         = mu_index
        self.is_single_mu      = is_single_mu
        self.is_di_mu          = is_di_mu
        self.mu_trig_level     = mu_trig_level
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
      assert self.mu_trig_level in allowed_levels, "ERROR: mu trig iso level %s is invalid. Check configuration!!!" % self.mu_trig_level

    #_________________________________________________________________________
    def execute(self, weight):
        trig_sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          mu_pairs = self.store['mu_pairs']
          
          num = 1.0 
          den = 1.0
          
          if self.is_single_mu:
            for i,m in enumerate(muons):
              if m.isTruthMatchedToMuon: 
                #if not m.isMatchedToTrigChain(): continue
                sf  = getattr(m,"_".join(["TrigEff","SF",str(self.mu_trig_level)])).at(0)
                eff = getattr(m,"_".join(["TrigMCEff",str(self.mu_trig_level)])).at(0)
                num *= 1 - sf * eff
                den *= 1 - eff
          
          elif self.is_di_mu:
            for i,mp in enumerate(mu_pairs):
              if mp.lead.isTruthMatchedToMuon and mp.sublead.isTruthMatchedToMuon: 
                #if not m.isMatchedToTrigChain(): continue
                
                sf_lead  = getattr(mp.lead,"_".join(["TrigEff","SF",str(self.mu_trig_level)])).at(0)
                eff_lead = getattr(mp.lead,"_".join(["TrigMCEff",str(self.mu_trig_level)])).at(0)
                
                sf_sublead  = getattr(mp.sublead,"_".join(["TrigEff","SF",str(self.mu_trig_level)])).at(0)
                eff_sublead = getattr(mp.sublead,"_".join(["TrigMCEff",str(self.mu_trig_level)])).at(0)
               
                num *= 1 - sf_lead * sf_sublead * eff_lead * eff_sublead
                den *= 1 - eff_lead * eff_sublead
          
          else: pass  
          
          num = ( 1 - num )
          den = ( 1 - den )
          
          if den > 0:
            trig_sf = num / den

          #if self.scale: pass
       
        if self.key: 
          self.store[self.key] = trig_sf
        return True

# EOF
