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
import itertools

GeV = 1000.0

#------------------------------------------------------------------------------
class LPXKfactor(pyframe.core.Algorithm):
    """
    multiply event weight by the LPXKfactor

    if 'key' is specified the MC weight will be put in the store
    """
    #__________________________________________________________________________
    def __init__(self, 
                 cutflow=None,
                 key=None,
                 sys_beam=None,
                 sys_choice=None,
                 sys_pdf=None,
                 sys_pi=None,
                 sys_scale_z=None,
                 doAssert=True,
                 nominalTree=True
                 ):
        pyframe.core.Algorithm.__init__(self, name="MCEventWeight", isfilter=True)

        self.cutflow = cutflow
        self.key = key
        self.sys_beam = sys_beam
        self.sys_choice = sys_choice
        self.sys_pdf = sys_pdf
        self.sys_pi = sys_pi
        self.sys_scale_z = sys_scale_z
        self.doAssert = doAssert
        self.nominalTree = nominalTree

        self.kfactorSys = 0
        if self.sys_beam == "DN":
          self.kfactorSys = 3
        elif self.sys_beam == "UP":
          self.kfactorSys = 4

        elif self.sys_choice == "DN":
          self.kfactorSys = 5
        elif self.sys_choice == "UP":
          self.kfactorSys = 6

        elif self.sys_pdf == "DN":
          self.kfactorSys = 16
        elif self.sys_pdf == "UP":
          self.kfactorSys = 17

        elif self.sys_pi == "DN":
          self.kfactorSys = 18
        elif self.sys_pi == "UP":
          self.kfactorSys = 19

        elif self.sys_scale_z == "DN":
          self.kfactorSys = 23
        elif self.sys_scale_z == "UP":
          self.kfactorSys = 24


    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
          if self.nominalTree:
            lpxk = self.chain.LPXKfactorVec.at(self.kfactorSys)
            if self.key: self.store[self.key] = lpxk
            self.set_weight(lpxk*weight)

            if self.doAssert:
              assert self.chain.LPXKfactorVecNames.at(3)=="LPX_KFACTOR_BEAM_ENERGY__1down", "LPX_KFACTOR_BEAM_ENERGY__1down"
              assert self.chain.LPXKfactorVecNames.at(4)=="LPX_KFACTOR_BEAM_ENERGY__1up", "LPX_KFACTOR_BEAM_ENERGY__1up"
              assert self.chain.LPXKfactorVecNames.at(5)=="LPX_KFACTOR_CHOICE_HERAPDF20", "LPX_KFACTOR_CHOICE_HERAPDF20"
              assert self.chain.LPXKfactorVecNames.at(6)=="LPX_KFACTOR_CHOICE_NNPDF30", "LPX_KFACTOR_CHOICE_NNPDF30"
              assert self.chain.LPXKfactorVecNames.at(16)=="LPX_KFACTOR_PDF__1down", "LPX_KFACTOR_PDF__1down"
              assert self.chain.LPXKfactorVecNames.at(17)=="LPX_KFACTOR_PDF__1up", "LPX_KFACTOR_PDF__1up"
              assert self.chain.LPXKfactorVecNames.at(18)=="LPX_KFACTOR_PI__1down", "LPX_KFACTOR_PI__1down"
              assert self.chain.LPXKfactorVecNames.at(19)=="LPX_KFACTOR_PI__1up", "LPX_KFACTOR_PI__1up"
              assert self.chain.LPXKfactorVecNames.at(23)=="LPX_KFACTOR_SCALE_Z__1down", "LPX_KFACTOR_SCALE_Z__1down"
              assert self.chain.LPXKfactorVecNames.at(24)=="LPX_KFACTOR_SCALE_Z__1up", "LPX_KFACTOR_SCALE_Z__1up"
          else:
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
        print trigpresc
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
    def __init__(self, name="ExactlyOneTightEleSF",
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
class AllTightEleSF(pyframe.core.Algorithm):
    """
    AllTightEleSF
    """
    #__________________________________________________________________________
    def __init__(self, name="AllTightEleSF",
            key            = None,
            chargeFlipSF   = False,
            config_file    = None,
            sys_CF         = None,
            sys_id         = None,
            sys_iso        = None,
            sys_reco       = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.chargeFlipSF      = chargeFlipSF
        self.config_file       = config_file
        self.sys_CF            = sys_CF
        self.sys_id            = sys_id
        self.sys_iso           = sys_iso
        self.sys_reco          = sys_reco

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

      h_etaRateMC = f.Get("MCEtaRate")
      assert h_etaRateMC, "Failed to get 'h_etaRateMC' from %s"%(self.config_file)
      h_ptRateMC = f.Get("MCPtRate")
      assert h_ptRateMC, "Failed to get 'h_ptRateMC' from %s"%(self.config_file)

      h_etaRateData = f.Get("dataEtaRate")
      assert h_etaRateData, "Failed to get 'h_etaRateData' from %s"%(self.config_file)
      h_ptRateData = f.Get("dataPtRate")
      assert h_ptRateData, "Failed to get 'h_ptRateData' from %s"%(self.config_file)

      self.h_etaFunc = h_etaFunc.Clone()
      self.h_ptFunc  = h_ptFunc.Clone()
      self.h_etaFunc.SetDirectory(0)
      self.h_ptFunc.SetDirectory(0)

      self.h_etaRateMC = h_etaRateMC.Clone()
      self.h_ptRateMC  = h_ptRateMC.Clone()
      self.h_etaRateMC.SetDirectory(0)
      self.h_ptRateMC.SetDirectory(0)

      self.h_etaRateData = h_etaRateData.Clone()
      self.h_ptRateData  = h_ptRateData.Clone()
      self.h_etaRateData.SetDirectory(0)
      self.h_ptRateData.SetDirectory(0)
      f.Close()

      self.id_sys = 0
      if self.sys_id == "UP":
        self.id_sys = 2
      elif self.sys_id == "DN":
        self.id_sys = 1

      self.iso_sys = 0
      if self.sys_iso == "UP":
        self.iso_sys = 2
      elif self.sys_iso == "DN":
        self.iso_sys = 1

      self.reco_sys = 0
      if self.sys_reco == "UP":
        self.reco_sys = 2
      elif self.sys_reco == "DN":
        self.reco_sys = 1

    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          electrons = self.store['electrons_tight_' + self.IDLevels[1] + "_" + self.isoLevels[0] ]
          for ele in electrons:
            if (ele.electronType() in [1,2,3,4]) or (self.chain.mcChannelNumber in range(306538,306560)):
              sf *= getattr(ele,"RecoEff_SF").at(self.reco_sys)
              sf *= getattr(ele,"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(self.iso_sys)
              sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(self.id_sys)

            if self.chargeFlipSF and self.chain.mcChannelNumber not in range(306538,306560):
              ptBin  = self.h_ptFunc.FindBin( ele.tlv.Pt()/GeV )
              etaBin = self.h_etaFunc.FindBin( abs(ele.caloCluster_eta ) )
              if ptBin==self.h_ptFunc.GetNbinsX()+1:
                ptBin -= 1 
              if ele.electronType() in [2,3]:
                if self.sys_CF == None:
                  sf *= self.h_ptFunc.GetBinContent( ptBin ) * self.h_etaFunc.GetBinContent( etaBin )                
                elif self.sys_CF == "UP":
                  sf *= (self.h_ptFunc.GetBinContent( ptBin )+self.h_ptFunc.GetBinError( ptBin )) * (self.h_etaFunc.GetBinContent( etaBin )+self.h_etaFunc.GetBinError( etaBin ))               
                elif self.sys_CF == "DN":
                  sf *= (self.h_ptFunc.GetBinContent( ptBin )-self.h_ptFunc.GetBinError( ptBin )) * (self.h_etaFunc.GetBinContent( etaBin )-self.h_etaFunc.GetBinError( etaBin ))
              elif ele.electronType() in [1]:
                probMC   = 0
                probData = 0
                if self.sys_CF == None:
                  probMC   = self.h_ptRateMC.GetBinContent( ptBin )   * self.h_etaRateMC.GetBinContent( etaBin )
                  probData = self.h_ptRateData.GetBinContent( ptBin ) * self.h_etaRateData.GetBinContent( etaBin )
                elif self.sys_CF == "UP":
                  probMC   = (self.h_ptRateMC.GetBinContent( ptBin )  -self.h_ptRateMC.GetBinError( ptBin ))   * (self.h_etaRateMC.GetBinContent( etaBin )  -self.h_etaRateMC.GetBinError( etaBin ))
                  probData = (self.h_ptRateData.GetBinContent( ptBin )+self.h_ptRateData.GetBinError( ptBin )) * (self.h_etaRateData.GetBinContent( etaBin )+self.h_etaRateData.GetBinError( etaBin ))
                elif self.sys_CF == "DN":
                  probMC   = (self.h_ptRateMC.GetBinContent( ptBin )  +self.h_ptRateMC.GetBinError( ptBin ))   * (self.h_etaRateMC.GetBinContent( etaBin )  +self.h_etaRateMC.GetBinError( etaBin ))
                  probData = (self.h_ptRateData.GetBinContent( ptBin )-self.h_ptRateData.GetBinError( ptBin )) * (self.h_etaRateData.GetBinContent( etaBin )-self.h_etaRateData.GetBinError( etaBin ))
                sf *= ( 1 - probData )/( 1 - probMC )

        if self.key: 
          self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class ExactlyTwoTightEleOStoSS(pyframe.core.Algorithm):
    """
    ExactlyTwoTightEleOStoSS
    """
    #__________________________________________________________________________
    def __init__(self, name="ExactlyTwoTightEleOStoSS",
            key            = None,
            config_file    = None,
            sys_CF         = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.config_file       = config_file
        self.sys_CF            = sys_CF

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
      h_etaRate = None
      h_ptRate = None

      if "mc" in self.sampletype:
        h_etaRate = f.Get("MCEtaRate")
        assert h_etaRate, "Failed to get 'h_etaRate' from %s"%(self.config_file)
        h_ptRate = f.Get("MCPtRate")
        assert h_ptRate, "Failed to get 'h_ptRate' from %s"%(self.config_file)
      else:
        h_etaRate = f.Get("dataEtaRate")
        assert h_etaRate, "Failed to get 'h_etaRate' from %s"%(self.config_file)
        h_ptRate = f.Get("dataPtRate")
        assert h_ptRate, "Failed to get 'h_ptRate' from %s"%(self.config_file)

      self.h_etaRate = h_etaRate.Clone()
      self.h_ptRate  = h_ptRate.Clone()
      self.h_etaRate.SetDirectory(0)
      self.h_ptRate.SetDirectory(0)
      f.Close()

    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0

        electrons = self.store['electrons_tight_' + self.IDLevels[1] + "_" + self.isoLevels[0] ]
        if len(electrons)!=2:
          sf = 0.0
          if self.key: 
            self.store[self.key] = sf
          return True

        ptBin1  = self.h_ptRate.FindBin( electrons[0].tlv.Pt()/GeV )
        ptBin2  = self.h_ptRate.FindBin( electrons[1].tlv.Pt()/GeV )
        etaBin1 = self.h_etaRate.FindBin( abs(electrons[0].caloCluster_eta ) )
        etaBin2 = self.h_etaRate.FindBin( abs(electrons[1].caloCluster_eta ) )
        prob1 = 0
        prob2 = 0
        if ptBin1==self.h_ptRate.GetNbinsX()+1:
          ptBin1 -= 1
        if ptBin2==self.h_ptRate.GetNbinsX()+1:
          ptBin2 -= 1
        if self.sys_CF == None:
          prob1 = self.h_ptRate.GetBinContent( ptBin1 ) * self.h_etaRate.GetBinContent( etaBin1 )
          prob2 = self.h_ptRate.GetBinContent( ptBin2 ) * self.h_etaRate.GetBinContent( etaBin2 )
        elif self.sys_CF == "UP":
          prob1 = (self.h_ptRate.GetBinContent( ptBin1 )+self.h_ptRate.GetBinError( ptBin1 )) * (self.h_etaRate.GetBinContent( etaBin1 )+self.h_etaRate.GetBinError( etaBin1 ))
          prob2 = (self.h_ptRate.GetBinContent( ptBin2 )+self.h_ptRate.GetBinError( ptBin2 )) * (self.h_etaRate.GetBinContent( etaBin2 )+self.h_etaRate.GetBinError( etaBin2 ))
        elif self.sys_CF == "DN":
          prob1 = (self.h_ptRate.GetBinContent( ptBin1 )-self.h_ptRate.GetBinError( ptBin1 )) * (self.h_etaRate.GetBinContent( etaBin1 )-self.h_etaRate.GetBinError( etaBin1 ))
          prob2 = (self.h_ptRate.GetBinContent( ptBin2 )-self.h_ptRate.GetBinError( ptBin2 )) * (self.h_etaRate.GetBinContent( etaBin2 )-self.h_etaRate.GetBinError( etaBin2 )) 

        sf *= (prob1*(1-prob2)+prob2*(1-prob1))/(1-prob1*(1-prob2)-prob2*(1-prob1))

        if "mc" in self.sampletype: 
          for ele in electrons:
            if ele.electronType() in [1,2,3,4]:
              sf *= getattr(ele,"RecoEff_SF").at(0)
              sf *= getattr(ele,"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
              sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
              sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)

        if self.key: 
          self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class ExactlyOneTightEleSF(pyframe.core.Algorithm):
    """
    ExactlyOneTightEleSF
    """
    #__________________________________________________________________________
    def __init__(self, name="ExactlyOneTightEleSF",
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

        f1 = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[0].tlv.Pt()/GeV, abs( electrons[0].caloCluster_eta ) ) )
        f2 = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[1].tlv.Pt()/GeV, abs( electrons[1].caloCluster_eta ) ) )
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
            sys_CF         = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.chargeFlipSF      = chargeFlipSF
        self.config_file       = config_file
        self.sys_CF            = sys_CF

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

      h_etaRateMC = f.Get("MCEtaRate")
      assert h_etaRateMC, "Failed to get 'h_etaRateMC' from %s"%(self.config_file)
      h_ptRateMC = f.Get("MCPtRate")
      assert h_ptRateMC, "Failed to get 'h_ptRateMC' from %s"%(self.config_file)

      h_etaRateData = f.Get("dataEtaRate")
      assert h_etaRateData, "Failed to get 'h_etaRateData' from %s"%(self.config_file)
      h_ptRateData = f.Get("dataPtRate")
      assert h_ptRateData, "Failed to get 'h_ptRateData' from %s"%(self.config_file)

      self.h_etaFunc = h_etaFunc.Clone()
      self.h_ptFunc  = h_ptFunc.Clone()
      self.h_etaFunc.SetDirectory(0)
      self.h_ptFunc.SetDirectory(0)

      self.h_etaRateMC = h_etaRateMC.Clone()
      self.h_ptRateMC  = h_ptRateMC.Clone()
      self.h_etaRateMC.SetDirectory(0)
      self.h_ptRateMC.SetDirectory(0)

      self.h_etaRateData = h_etaRateData.Clone()
      self.h_ptRateData  = h_ptRateData.Clone()
      self.h_etaRateData.SetDirectory(0)
      self.h_ptRateData.SetDirectory(0)
      f.Close()

    #_________________________________________________________________________
    def execute(self, weight):
        sf=1.0
        if "mc" in self.sampletype: 
          electrons = self.store['electrons_tight_' + self.IDLevels[1] + "_" + self.isoLevels[0] ]
          for ele in electrons:
            if ele.electronType() in [1,2,3,4]:
              sf *= getattr(ele,"RecoEff_SF").at(0)
              sf *= getattr(ele,"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
              sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(0)
              sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)

            if self.chargeFlipSF and self.chain.mcChannelNumber not in range(306538,306560):
              ptBin  = self.h_ptFunc.FindBin( ele.tlv.Pt()/GeV )
              etaBin = self.h_etaFunc.FindBin( abs(ele.caloCluster_eta ) )
              if ptBin==self.h_ptFunc.GetNbinsX()+1:
                ptBin -= 1 
              if ele.electronType() in [2,3]:
                if self.sys_CF == None:
                  sf *= self.h_ptFunc.GetBinContent( ptBin ) * self.h_etaFunc.GetBinContent( etaBin )                
                elif self.sys_CF == "UP":
                  sf *= (self.h_ptFunc.GetBinContent( ptBin )+self.h_ptFunc.GetBinError( ptBin )) * (self.h_etaFunc.GetBinContent( etaBin )+self.h_etaFunc.GetBinError( etaBin ))               
                elif self.sys_CF == "DN":
                  sf *= (self.h_ptFunc.GetBinContent( ptBin )-self.h_ptFunc.GetBinError( ptBin )) * (self.h_etaFunc.GetBinContent( etaBin )-self.h_etaFunc.GetBinError( etaBin ))
              elif ele.electronType() in [1]:
                probMC   = 0
                probData = 0
                if self.sys_CF == None:
                  probMC   = self.h_ptRateMC.GetBinContent( ptBin )   * self.h_etaRateMC.GetBinContent( etaBin )
                  probData = self.h_ptRateData.GetBinContent( ptBin ) * self.h_etaRateData.GetBinContent( etaBin )
                elif self.sys_CF == "UP":
                  probMC   = (self.h_ptRateMC.GetBinContent( ptBin )  +self.h_ptRateMC.GetBinError( ptBin ))   * (self.h_etaRateMC.GetBinContent( etaBin )  +self.h_etaRateMC.GetBinError( etaBin ))
                  probData = (self.h_ptRateData.GetBinContent( ptBin )+self.h_ptRateData.GetBinError( ptBin )) * (self.h_etaRateData.GetBinContent( etaBin )+self.h_etaRateData.GetBinError( etaBin ))
                elif self.sys_CF == "DN":
                  probMC   = (self.h_ptRateMC.GetBinContent( ptBin )  -self.h_ptRateMC.GetBinError( ptBin ))   * (self.h_etaRateMC.GetBinContent( etaBin )  -self.h_etaRateMC.GetBinError( etaBin ))
                  probData = (self.h_ptRateData.GetBinContent( ptBin )-self.h_ptRateData.GetBinError( ptBin )) * (self.h_etaRateData.GetBinContent( etaBin )-self.h_etaRateData.GetBinError( etaBin ))
                sf *= ( 1 - probData )/( 1 - probMC )

        if self.key: 
          self.store[self.key] = sf
        return True

class GenericFakeFactor(pyframe.core.Algorithm):
    """
    GenericFakeFactor
    """
    #__________________________________________________________________________
    def __init__(self, name="GenericFakeFactor",
            key            = None,
            sys            = None,
            config_file    = None,
            config_fileCHF = None,
            sys_id         = None,
            sys_iso        = None,
            sys_reco       = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.sys               = sys
        self.config_file       = config_file
        self.config_fileCHF    = config_fileCHF
        self.sys_id            = sys_id
        self.sys_iso           = sys_iso
        self.sys_reco          = sys_reco

        assert key, "Must provide key for storing mu reco sf"
        assert config_file, "Must provide config file!"
        assert config_fileCHF, "Must provide config file!"
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

      fchf = ROOT.TFile.Open(self.config_fileCHF)
      assert fchf, "Failed to open charge-flip config file: %s"%(self.config_fileCHF)

      h_etaFunc = fchf.Get("etaFunc")
      assert h_etaFunc, "Failed to get 'h_etaFunc' from %s"%(self.config_fileCHF)
      h_ptFunc = fchf.Get("ptFunc")
      assert h_ptFunc, "Failed to get 'h_ptFunc' from %s"%(self.config_fileCHF)

      h_etaRateMC = fchf.Get("MCEtaRate")
      assert h_etaRateMC, "Failed to get 'h_etaRateMC' from %s"%(self.config_fileCHF)
      h_ptRateMC = fchf.Get("MCPtRate")
      assert h_ptRateMC, "Failed to get 'h_ptRateMC' from %s"%(self.config_fileCHF)

      h_etaRateData = fchf.Get("dataEtaRate")
      assert h_etaRateData, "Failed to get 'h_etaRateData' from %s"%(self.config_fileCHF)
      h_ptRateData = fchf.Get("dataPtRate")
      assert h_ptRateData, "Failed to get 'h_ptRateData' from %s"%(self.config_fileCHF)

      self.h_etaFunc = h_etaFunc.Clone()
      self.h_ptFunc  = h_ptFunc.Clone()
      self.h_etaFunc.SetDirectory(0)
      self.h_ptFunc.SetDirectory(0)

      self.h_etaRateMC = h_etaRateMC.Clone()
      self.h_ptRateMC  = h_ptRateMC.Clone()
      self.h_etaRateMC.SetDirectory(0)
      self.h_ptRateMC.SetDirectory(0)

      self.h_etaRateData = h_etaRateData.Clone()
      self.h_ptRateData  = h_ptRateData.Clone()
      self.h_etaRateData.SetDirectory(0)
      self.h_ptRateData.SetDirectory(0)
      fchf.Clone()

      self.isoLevels = [
      "isolLoose",
      "isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]

      self.id_sys = 0
      if self.sys_id == "UP":
        self.id_sys = 2
      elif self.sys_id == "DN":
        self.id_sys = 1

      self.iso_sys = 0
      if self.sys_iso == "UP":
        self.iso_sys = 2
      elif self.sys_iso == "DN":
        self.iso_sys = 1

      self.reco_sys = 0
      if self.sys_reco == "UP":
        self.reco_sys = 2
      elif self.sys_reco == "DN":
        self.reco_sys = 1

    #_________________________________________________________________________
    def execute(self, weight):

      if "mc" in self.sampletype and self.chain.mcChannelNumber in range(306538,306560):
        if self.key: 
          self.store[self.key] = 0.
        return True

      sf = -1.0
      electrons = self.store['electrons_loose_LooseLLH']

      for ele in electrons:
        if (ele.isIsolated_Loose and ele.LHMedium) :
          if "mc" in self.sampletype : 
            sf *= getattr(ele,"IsoEff_SF_"   + self.IDLevels[1] + self.isoLevels[0] ).at(self.iso_sys)
            sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(self.id_sys)
            sf *= getattr(ele,"RecoEff_SF").at(self.reco_sys)
            ptBin  = self.h_ptFunc.FindBin( ele.tlv.Pt()/GeV )
            etaBin = self.h_etaFunc.FindBin( abs( ele.caloCluster_eta ) )
            if ptBin==self.h_ptFunc.GetNbinsX()+1:
              ptBin -= 1 
            if ele.electronType() in [2,3]:
              sf *= self.h_ptFunc.GetBinContent( ptBin ) * self.h_etaFunc.GetBinContent( etaBin )                
            elif ele.electronType() in [1]:
              probMC   = self.h_ptRateMC.GetBinContent( ptBin )   * self.h_etaRateMC.GetBinContent( etaBin )
              probData = self.h_ptRateData.GetBinContent( ptBin ) * self.h_etaRateData.GetBinContent( etaBin )
              sf *= ( 1 - probData )/( 1 - probMC )
          else :
            pass
        else :
          sf *= -self.h_ff.GetBinContent( self.h_ff.FindBin( ele.tlv.Pt()/GeV, abs( ele.caloCluster_eta ) ) )
          if "mc" in self.sampletype :
            sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(self.id_sys)
            sf *= getattr(ele,"RecoEff_SF").at(self.reco_sys)
          else :
            pass

      if self.key: 
        self.store[self.key] = sf
      return True

class ThreeElectron2e17TrigWeight(pyframe.core.Algorithm):
    """
    ThreeElectron2e17TrigWeight
    """
    #__________________________________________________________________________
    def __init__(self, name="ThreeElectron2e17TrigWeight",
            key            = None,
            sys_trig       = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.sys_trig          = sys_trig

        assert key, "Must provide key for storing mu reco sf"
    #_________________________________________________________________________
    def initialize(self):

      self.isoLevels = [
      "",
      "_isolLoose",
      "_isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]

      self.trig_sys = 0
      if self.sys_trig == "UP":
        self.trig_sys = 2
      elif self.sys_trig == "DN":
        self.trig_sys = 1

    #_________________________________________________________________________
    def execute(self, weight):

      sf = 1.0
      electrons = self.store['electrons_loose_LooseLLH']

      # two electron case
      if len(electrons) == 2:
        for ele in electrons:
          if ele.electronType() in [1,2,3,4]:
            if ele.LHMedium and ele.isIsolated_Loose:
              sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
            else:
              sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
        if self.key: 
          self.store[self.key] = sf
        return True

      if len(electrons)!=3 or "mc" not in self.sampletype:
        if self.key: 
          self.store[self.key] = sf
        return True

      P2passD  = 0
      P2passMC = 0
      P3passD  = 1
      P3passMC = 1
      for pair in itertools.combinations(electrons,2) :
        combinationProbD  = 1 # e1*SF1 * e2*SF2 * (1-e3*SF3)
        combinationProbMC = 1 # e1     * e2     * (1-e3    )
        for eleFail in electrons:
          if eleFail not in pair:
            for elePass in pair:
              if elePass.LHMedium and elePass.isIsolated_Loose:
                combinationProbD  *= getattr(elePass,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)*\
                                     getattr(elePass,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
                combinationProbMC *= getattr(elePass,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
              else:
                combinationProbD  *= getattr(elePass,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)*\
                                     getattr(elePass,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
                combinationProbMC *= getattr(elePass,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
            if eleFail.LHMedium and eleFail.isIsolated_Loose:
              combinationProbD  *= 1 - ( getattr(eleFail,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)*\
                                         getattr(eleFail,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys) )
              combinationProbMC *= 1 -   getattr(eleFail,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
            else:
              combinationProbD  *= 1 - ( getattr(eleFail,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)*\
                                         getattr(eleFail,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys) )
              combinationProbMC *= 1 -   getattr(eleFail,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
            break
        P2passD  += combinationProbD   # a*b*(1-c) + a*c*(1-b) + b*c*(1-d) 
        P2passMC += combinationProbMC  # a*b*(1-c) + a*c*(1-b) + b*c*(1-d)
      for ele in electrons:
        if ele.LHMedium and ele.isIsolated_Loose:
          P3passD  *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)*\
                      getattr(ele,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
          P3passMC *= getattr(ele,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
        else:
          P3passD  *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)*\
                      getattr(ele,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
          P3passMC *= getattr(ele,"TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)

      sf = (P2passD+P3passD)/(P2passMC+P3passMC)

      if self.key: 
        self.store[self.key] = sf
      return True

class TwoElectron2e17TrigWeight(pyframe.core.Algorithm):
    """
    TwoElectron2e17TrigWeight
    """
    #__________________________________________________________________________
    def __init__(self, name="TwoElectron2e17TrigWeight",
            key            = None,
            sys            = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.sys               = sys

        assert key, "Must provide key for storing mu reco sf"
    #_________________________________________________________________________
    def initialize(self):

      self.isoLevels = [
      "",
      "_isolLoose",
      "_isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]
    #_________________________________________________________________________
    def execute(self, weight):

      sf = 1.0
      electrons = self.store['electrons_loose_LooseLLH']

      if len(electrons)!=2 or "mc" not in self.sampletype:
        if self.key: 
          self.store[self.key] = sf
        return True

      for ele in electrons:
        if ele.electronType() in [1,2,3,4]:
          if ele.LHMedium and ele.isIsolated_Loose:
            sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+self.isoLevels[1]).at(0)
          else:
            sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[0]+self.isoLevels[0]).at(0)

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

        F1 = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[0].tlv.Pt()/GeV, abs( electrons[0].caloCluster_eta ) ) )
        F2 = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[1].tlv.Pt()/GeV, abs( electrons[1].caloCluster_eta ) ) )
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

        F = self.h_ff.GetBinContent( self.h_ff.FindBin( electrons[0].tlv.Pt()/GeV, abs( electrons[0].caloCluster_eta ) ) )
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
