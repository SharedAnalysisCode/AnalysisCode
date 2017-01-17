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
class LPXKfactor(pyframe.core.Algorithm):
    """
    multiply event weight by the LPXKfactor

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
            lpxk = self.chain.LPXKfactor
            if self.key: self.store[self.key] = lpxk
            self.set_weight(lpxk*weight)
        return True

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

#------------------------------------------------------------------------------
class OneOrTwoBjetsSF(pyframe.core.Algorithm):
    """
    OneOrTwoBjetsSF
    """
    #__________________________________________________________________________
    def __init__(self, name="OneOrTwoBjetsSF",
            key            = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key

        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________
    def initialize(self):
      pass
    #_________________________________________________________________________
    def execute(self, weight):
      sf=1.0
      if "mc" in self.sampletype: 
        jets = self.store['jets']
        for jet in jets:
          if jet.isFix77:
            sf *= getattr(jet,"jvtSF").at(0)
            sf *= getattr(jet,"SFFix77").at(0)

      if self.key: 
        self.store[self.key] = sf
      return True

#------------------------------------------------------------------------------
class ExactlyOneTightEleSF(pyframe.core.Algorithm):
    """
    ExactlyOneTightEleSF
    """
    #__________________________________________________________________________
    def __init__(self, name="ExactlyTwoTightEleSF",
            key            = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key

        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________
    def initialize(self):
      self.isoLevels = [
          "isolLoose",
          "isolTight",
          ]
      self.IDLevels = [
          "LooseAndBLayerLLH",
          "MediumLLH",
          "TightLLH",
          ]

    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          electrons = self.store['electrons_tight_' + self.IDLevels[1] + "_" + self.isoLevels[0] ]
          for ele in electrons:
            sf *= getattr(ele,"RecoEff_SF").at(0)
            sf *= getattr(ele,"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
            #sf *= getattr(ele,"TrigMCEff_SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)

        if self.key: 
          self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class ExactlyTwoTightEleSF(pyframe.core.Algorithm):
    """
    ExactlyTwoTightEleSF
    """
    #__________________________________________________________________________
    def __init__(self, name="ExactlyTwoTightEleSF",
            key            = None,
            chargeFlipSF   = False,
            config_file    = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.chargeFlipSF      = chargeFlipSF
        self.config_file       = config_file

        assert config_file, "Must provide a charge-flip config file!"
        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________
    def initialize(self):
      self.isoLevels = [
          "isolLoose",
          "isolTight",
          ]
      self.IDLevels = [
          "LooseAndBLayerLLH",
          "MediumLLH",
          "TightLLH",
          ]


      f = ROOT.TFile.Open(self.config_file)
      assert f, "Failed to open charge-flip config file: %s"%(self.config_file)

      h_etaFunc = f.Get("etaFunc")
      assert h_etaFunc, "Failed to get 'h_etaFunc' from %s"%(self.config_file)
      h_ptFunc = f.Get("ptFunc")
      assert h_ptFunc, "Failed to get 'h_ptFunc' from %s"%(self.config_file)

      self.h_etaFunc = h_etaFunc.Clone()
      self.h_ptFunc  = h_ptFunc.Clone()
      self.h_etaFunc.SetDirectory(0)
      self.h_ptFunc.SetDirectory(0)
      f.Close()

    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          electrons = self.store['electrons_tight_' + self.IDLevels[1] + "_" + self.isoLevels[0] ]
          for ele in electrons:
            sf *= getattr(ele,"RecoEff_SF").at(0)
            sf *= getattr(ele,"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)

            if self.chargeFlipSF:
              if ele.electronType() in [2,3]:
                ptBin = self.h_ptFunc.FindBin( ele.tlv.Pt()/GeV )
                if ptBin==self.h_ptFunc.GetNbinsX()+1:
                  ptBin -= 1
                sf *= self.h_ptFunc. GetBinContent( ptBin ) *\
                      self.h_etaFunc.GetBinContent( self.h_etaFunc.FindBin( abs(ele.tlv.Eta()) ) )

        if self.key: 
          self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class ExactlyOneTightEleSF(pyframe.core.Algorithm):
    """
    ExactlyOneTightEleSF
    """
    #__________________________________________________________________________
    def __init__(self, name="ExactlyTwoTightEleSF",
            key            = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key

        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________
    def initialize(self):
      self.isoLevels = [
          "isolLoose",
          "isolTight",
          ]
      self.IDLevels = [
          "LooseAndBLayerLLH",
          "MediumLLH",
          "TightLLH",
          ]

    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          electrons = self.store['electrons_tight_' + self.IDLevels[1] + "_" + self.isoLevels[0] ]
          for ele in electrons:
            sf *= getattr(ele,"RecoEff_SF").at(0)
            sf *= getattr(ele,"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
            #sf *= getattr(ele,"TrigMCEff_SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)

        if self.key: 
          self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class ExactlyTwoLooseEleFF(pyframe.core.Algorithm):
    """
    ExactlyTwoLooseEleFF
    """
    #__________________________________________________________________________
    def __init__(self, name="ExactlyTwoLooseEleFF",
            key            = None,
            typeFF         = "TL",
            sys            = None,
            config_file    = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.typeFF            = typeFF
        self.sys               = sys
        self.config_file       = config_file

        assert key, "Must provide key for storing mu reco sf"
        assert typeFF in ["TL","LT","LL"], "allowed types: TL, LT, LL"
        assert config_file, "Must provide config file!"
    #_________________________________________________________________________
    def initialize(self):

      f = ROOT.TFile.Open(self.config_file)
      assert f, "Failed to open fake-factor config file: %s"%(self.config_file)
      
      if self.sys=="UP":
        h_ff = f.Get("FFup")
      elif self.sys=="DN":
        h_ff = f.Get("FFdn")
      else:
        h_ff = f.Get("FF")
      assert h_ff, "Failed to get 'h_ff' from %s"%(self.config_file)

      self.h_ff = h_ff.Clone()
      self.h_ff.SetDirectory(0)
      f.Close()

      self.isoLevels = [
      "isolLoose",
      "isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]
    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)!=2:
          if self.key: 
            self.store[self.key] = sf
          return True

        f1 = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[0].tlv.Pt()/GeV, abs( electrons[0].eta ) ) )
        f2 = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[1].tlv.Pt()/GeV, abs( electrons[1].eta ) ) )
        if f1*f2==0:
          sf=0
          if self.key: 
            self.store[self.key] = sf
            return True
        alpha = 1./((1-f1)*(1-f2))

        if "mc" in self.sampletype: 
          sf *= getattr(electrons[0],"RecoEff_SF").at(0)
          sf *= getattr(electrons[1],"RecoEff_SF").at(0)
          if self.typeFF=="TL":
            sf *= getattr(electrons[0],"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(electrons[0],"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= alpha*f2*(1.-f1)
          elif self.typeFF=="LT":
            sf *= getattr(electrons[1],"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
            sf *= getattr(electrons[0],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= alpha*f1*(1.-f2)
          elif self.typeFF=="LL":
            sf *= getattr(electrons[0],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= -alpha*f1*f2

        else:
          if self.typeFF=="TL":
            sf *= alpha*f2*(1.-f1)
          elif self.typeFF=="LT":
            sf *= alpha*f1*(1.-f2)
          elif self.typeFF=="LL":
            sf *= -alpha*f1*f2

        if self.key: 
          self.store[self.key] = sf
        return True

class ExactlyTwoLooseEleFakeFactor(pyframe.core.Algorithm):
    """
    ExactlyTwoLooseEleFakeFactor
    """
    #__________________________________________________________________________
    def __init__(self, name="ExactlyTwoLooseEleFakeFactor",
            key            = None,
            typeFF         = "TL",
            sys            = None,
            config_file    = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.typeFF            = typeFF
        self.sys               = sys
        self.config_file       = config_file

        assert key, "Must provide key for storing mu reco sf"
        assert typeFF in ["TL","LT","LL"], "allowed types: TL, LT, LL"
        assert config_file, "Must provide config file!"
    #_________________________________________________________________________
    def initialize(self):

      f = ROOT.TFile.Open(self.config_file)
      assert f, "Failed to open fake-factor config file: %s"%(self.config_file)
      
      if self.sys=="UP":
        h_ff = f.Get("FFup")
      elif self.sys=="DN":
        h_ff = f.Get("FFdn")
      else:
        h_ff = f.Get("FF")
      assert h_ff, "Failed to get 'h_ff' from %s"%(self.config_file)

      self.h_ff = h_ff.Clone()
      self.h_ff.SetDirectory(0)
      f.Close()

      self.isoLevels = [
      "isolLoose",
      "isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]
    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)!=2:
          if self.key: 
            self.store[self.key] = sf
          return True

        F1 = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[0].tlv.Pt()/GeV, abs( electrons[0].eta ) ) )
        F2 = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[1].tlv.Pt()/GeV, abs( electrons[1].eta ) ) )
        if F1*F2==0:
          sf=0
          if self.key: 
            self.store[self.key] = sf
            return True

        if "mc" in self.sampletype: 
          sf *= getattr(electrons[0],"RecoEff_SF").at(0)
          sf *= getattr(electrons[1],"RecoEff_SF").at(0)
          if self.typeFF=="TL":
            sf *= getattr(electrons[0],"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(electrons[0],"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= F2
          elif self.typeFF=="LT":
            sf *= getattr(electrons[1],"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
            sf *= getattr(electrons[0],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= F1
          elif self.typeFF=="LL":
            sf *= getattr(electrons[0],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= -F1*F2

        else:
          if self.typeFF=="TL":
            sf *= F2
          elif self.typeFF=="LT":
            sf *= F1
          elif self.typeFF=="LL":
            sf *= -F1*F2

        if self.key: 
          self.store[self.key] = sf
        return True

class ExactlyOneLooseEleFakeFactor(pyframe.core.Algorithm):
    """
    ExactlyOneLooseEleFakeFactor
    """
    #__________________________________________________________________________
    def __init__(self, name="ExactlyOneLooseEleFakeFactor",
            key            = None,
            sys            = None,
            config_file    = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.sys               = sys
        self.config_file       = config_file

        assert key, "Must provide key for storing mu reco sf"
        assert config_file, "Must provide config file!"
    #_________________________________________________________________________
    def initialize(self):

      f = ROOT.TFile.Open(self.config_file)
      assert f, "Failed to open fake-factor config file: %s"%(self.config_file)
      
      if self.sys=="UP":
        h_ff = f.Get("FFup")
      elif self.sys=="DN":
        h_ff = f.Get("FFdn")
      else:
        h_ff = f.Get("FF")
      assert h_ff, "Failed to get 'h_ff' from %s"%(self.config_file)

      self.h_ff = h_ff.Clone()
      self.h_ff.SetDirectory(0)
      f.Close()

      self.isoLevels = [
      "isolLoose",
      "isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]
    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)!=1:
          if self.key: 
            self.store[self.key] = sf
          return True

        F = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[0].tlv.Pt()/GeV, abs( electrons[0].eta ) ) )
        if F==0:
          sf=0
          if self.key: 
            self.store[self.key] = sf
            return True

        if "mc" in self.sampletype: 
          sf *= getattr(electrons[0],"RecoEff_SF").at(0)
          sf *= getattr(electrons[0],"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(0)
          #sf *= getattr(electrons[0],"TrigMCEff_SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0_"+self.IDLevels[1]).at(0)
          sf *= F

        else:
          sf *= F

        if self.key: 
          self.store[self.key] = sf
        return True

# EOF
