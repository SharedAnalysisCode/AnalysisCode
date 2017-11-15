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
class MJJReweight(pyframe.core.Algorithm):
    """
    MJJReweight
    """
    #__________________________________________________________________________
    def __init__(self, 
                 cutflow=None,
                 key=None,
                 sys_peak=None,
                 sys_width=None,
                 sys_tail=None,
                 ):
        pyframe.core.Algorithm.__init__(self, name="MJJReweight", isfilter=True)

        self.cutflow = cutflow
        self.key = key
        self.sys_peak = sys_peak
        self.sys_width = sys_width
        self.sys_tail = sys_tail

        self.peak = 177.
        if self.sys_peak == "DN":
          self.peak -= 13.
        elif self.sys_peak == "UP":
          self.peak += 13.

        self.width = 877.
        if self.sys_width == "DN":
          self.width -= 22.
        elif self.sys_width == "UP":
          self.width += 22.

        self.tail = -3.0
        if self.sys_tail == "DN":
          self.tail -= 0.24
        elif self.sys_tail == "UP":
          self.tail += 0.24


    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype and self.chain.mcChannelNumber in range(364100,364127+1):
          MJJ = self.store["MJJ"]
          if MJJ < - 900:
            MJJw = 1.
            if self.key: self.store[self.key] = MJJw
            self.set_weight(MJJw*weight)
            return True

          k1 = ROOT.TMath.Log( 1.0 - ( MJJ - self.peak ) * self.tail / self.width )
          k2 = 2.3548200450309494 # 2 Sqrt( Ln(4) )
          k3 = ( 2.0 / k2 ) * ROOT.TMath.ASinH( 0.5 * k2 * self.tail)
          norm = 4.52282
          k32 = k3 * k3
          MJJw = norm*ROOT.TMath.Exp( ( -0.5 / k32 * k1 * k1 ) - ( k32 * 0.5 ) )
        else:
          MJJw = 1.

        if self.key: self.store[self.key] = MJJw
        self.set_weight(MJJw*weight)  
        return True

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
        pyframe.core.Algorithm.__init__(self, name="LPXKfactor", isfilter=True)

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
    def __init__(self, cutflow=None, key=None, sys=None):
        pyframe.core.Algorithm.__init__(self, name="MCEventWeight", isfilter=True)
        self.cutflow = cutflow
        self.key = key
        self.sys = sys

        if self.sys != None:
          assert type(self.sys)==int, "should be an intiger"
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            wmc = self.chain.mcEventWeight if self.sys==None else self.chain.mcEventWeights.at(self.sys)
            # print '======'
            # print 'weight: ',wmc
            # print 'weight nom: ',self.chain.mcEventWeight
            # print '======'
            if self.chain.mcChannelNumber in range(364100,364141)+range(361069,361074)+[364250,364253,364254,364255,361077,363356,363358,363490,363491,363492] and abs(wmc) > 30. :
              wmc = 1.
            if self.chain.mcChannelNumber in range(364170,364198) and abs(wmc) > 100. :
              wmc = 1.
            if self.key: self.store[self.key] = wmc
            self.set_weight(wmc*weight)
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
class GlobalBjet(pyframe.core.Algorithm):
    """
    GlobalBjet
    """
    #__________________________________________________________________________
    def __init__(self, name="GlobalBjet",
            key            = None,
            sys            = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.sys               = sys
        self.key               = key

        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________
    def initialize(self):
      self.bjet_sys = 0
      if self.sys == "B_SYS_DN":
        self.bjet_sys = 1
      elif self.sys == "B_SYS_UP":
        self.bjet_sys = 2
      elif self.sys == "C_SYS_DN":
        self.bjet_sys = 3
      elif self.sys == "C_SYS_UP":
        self.bjet_sys = 4
      elif self.sys == "L_SYS_DN":
        self.bjet_sys = 5
      elif self.sys == "L_SYS_UP":
        self.bjet_sys = 6
      elif self.sys == "E_SYS_DN":
        self.bjet_sys = 7
      elif self.sys == "E_SYS_UP":
        self.bjet_sys = 8
      elif self.sys == "EFC_SYS_DN":
        self.bjet_sys = 9
      elif self.sys == "EFC_SYS_UP":
        self.bjet_sys = 10

      print self.bjet_sys
    #_________________________________________________________________________
    def execute(self, weight):
      sf=1.0
      if "mc" in self.sampletype: 
        jets = self.store['jets']
        for jet in jets:
          if jet.JvtPass_Medium and jet.fJvtPass_Medium:
            sf *= getattr(jet,"SFFix77").at(self.bjet_sys)

      if self.key: 
        self.store[self.key] = sf
      return True

#------------------------------------------------------------------------------
class GlobalJVT(pyframe.core.Algorithm):
    """
    GlobalJVT
    """
    #__________________________________________________________________________
    def __init__(self, name="GlobalJVT",
            key            = None,
            sys            = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.sys               = sys
        self.key               = key

        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________
    def initialize(self):
      self.jvt_sys = 0
      if self.sys == "JVT_SYS_DN":
        self.jvt_sys = 1
      elif self.sys == "JVT_SYS_UP":
        self.jvt_sys = 2
    #_________________________________________________________________________
    def execute(self, weight):
      sf=1.0
      if "mc" in self.sampletype: 
        jets = self.store['jets']
        for jet in jets:
          sf *= getattr(jet,"JvtEff_SF_Medium").at(self.jvt_sys)
          sf *= getattr(jet,"fJvtEff_SF_Medium").at(0)

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
            sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(0)
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
              sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(self.id_sys)

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
class AllTightLepSF(pyframe.core.Algorithm):
    """
    AllTightLepSF
    """
    #__________________________________________________________________________
    def __init__(self, name="AllTightLepSF",
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
              sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(self.id_sys)

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
          muons = self.store['muons_tight']
          for mu in muons:
            sf *= getattr(mu,"_".join(["IsoEff","SF","Iso"+"FixedCutTightTrackOnly"])).at(0)
            sf *= getattr(mu,"_".join(["RecoEff","SF","Reco"+"Medium"])).at(0)
            sf *= getattr(mu,"_".join(["TTVAEff","SF"])).at(0)

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
              sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(0)
              sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)

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
            sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(0)
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
            sf *= getattr(electrons[0],"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= alpha*f2*(1.-f1)
          elif self.typeFF=="LT":
            sf *= getattr(electrons[1],"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
            sf *= getattr(electrons[0],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= alpha*f1*(1.-f2)
          elif self.typeFF=="LL":
            sf *= getattr(electrons[0],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
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
              sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(0)
              # sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
              sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)

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
            sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(self.id_sys)
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
            sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(self.id_sys)
            sf *= getattr(ele,"RecoEff_SF").at(self.reco_sys)
          else :
            pass

      if self.key: 
        self.store[self.key] = sf
      return True

class GenericFakeFactorMu(pyframe.core.Algorithm):
    """
    GenericFakeFactorMu
    """
    #__________________________________________________________________________
    def __init__(self, name="GenericFakeFactorMu",
            key            = None,
            sys            = None,
            config_file    = None,
            sys_reco       = None,
            sys_iso        = None,
            sys_TTVA       = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.sys               = sys
        self.config_file       = config_file
        self.sys_reco          = sys_reco
        self.sys_iso           = sys_iso
        self.sys_TTVA          = sys_TTVA

        assert key, "Must provide key for storing mu reco sf"
        assert config_file, "Must provide config file!"
        print config_file
        
    #_________________________________________________________________________
    def initialize(self):

      f = ROOT.TFile.Open(self.config_file)
      assert f, "Failed to open fake-factor config file: %s"%(self.config_file)
      
      g_ff = f.Get("g_ff_stat_sys")

      assert g_ff, "Failed to get 'h_ff' from %s"%(self.config_file)

      self.g_ff = g_ff.Clone()
      f.Close()

      #Muon ID
      self.reco_sys = 0
      if self.sys_reco == "UPSTAT":
        self.reco_sys = 4
      elif self.sys_reco == "UPSYS":
        self.reco_sys = 8
      elif self.sys_reco == "DNSTAT":
        self.reco_sys = 3
      elif self.sys_reco == "DNSYS":
        self.reco_sys = 7

      self.iso_sys=0
      if self.sys_iso ==   "UPSTAT":
        self.iso_sys= 2
      elif self.sys_iso == "UPSYS":
        self.iso_sys= 4
      elif self.sys_iso == "DNSTAT":
        self.iso_sys= 1
      elif self.sys_iso == "DNSYS":
        self.iso_sys= 3

      self.TTVA_sys=0
      if self.sys_TTVA ==   "UPSTAT":
        self.TTVA_sys= 2
      elif self.sys_TTVA == "UPSYS":
        self.TTVA_sys= 4
      elif self.sys_TTVA == "DNSTAT":
        self.TTVA_sys= 1
      elif self.sys_TTVA == "DNSYS":
        self.TTVA_sys= 3


    #_________________________________________________________________________
    def execute(self, weight):

      if "mc" in self.sampletype and self.chain.mcChannelNumber in range(306538,306560):
          if len(self.store['muons_tight']) != len(self.store['muons']) :
              if self.key:
                self.store[self.key] = 0.
                return True

      sf = 1.0
      if len(self.store['muons_tight']) != len(self.store['muons']):
        sf = -1.0
      muons = self.store['muons']

      for muon in muons:
        if (muon.isIsolated_FixedCutTightTrackOnly and muon.trkd0sig <= 3.0) :
          if "mc" in self.sampletype : 
            sf *= getattr(muon,"_".join(["IsoEff","SF","Iso"+"FixedCutTightTrackOnly"])).at(self.iso_sys)
            sf *= getattr(muon,"_".join(["RecoEff","SF","Reco"+"Medium"])).at(self.reco_sys)
            sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(self.TTVA_sys)
          else :
            pass
        else :
          ff_mu = 0.
          eff_up_mu = 0.
          eff_dn_mu = 0.
          for ibin_mu in xrange(1,self.g_ff.GetN()):
            edlow = self.g_ff.GetX()[ibin_mu] - self.g_ff.GetEXlow()[ibin_mu]
            edhi  = self.g_ff.GetX()[ibin_mu] + self.g_ff.GetEXhigh()[ibin_mu]
            if muon.tlv.Pt()/GeV>=edlow and muon.tlv.Pt()/GeV<edhi:
              ff_mu = self.g_ff.GetY()[ibin_mu]
              eff_up_mu = self.g_ff.GetEYhigh()[ibin_mu]
              eff_dn_mu = self.g_ff.GetEYlow()[ibin_mu]
              break
          if self.sys == 'UP': ff_mu +=eff_up_mu
          if self.sys == 'DN': ff_mu -=eff_dn_mu
          sf *= -ff_mu
          if "mc" in self.sampletype :
            sf *= getattr(muon,"_".join(["RecoEff","SF","Reco"+"Medium"])).at(self.reco_sys)
            sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(self.TTVA_sys)
          else :
            pass

      if self.key: 
        self.store[self.key] = sf
      return True

class SuperGenericFakeFactor(pyframe.core.Algorithm):
    """
    SuperGenericFakeFactor
    """
    #__________________________________________________________________________
    def __init__(self, name="SuperGenericFakeFactor",
            key            = None,
            do_FFweight    = None,
            sys_FFe        = None,
            sys_FFm        = None,
            sys_CHF        = None,
            config_file_e  = None,
            config_file_m  = None,
            config_fileCHF = None,
            sys_id_e       = None,
            sys_iso_e      = None,
            sys_reco_e     = None,
            sys_reco_m     = None,
            sys_iso_m      = None,
            sys_TTVA_m     = None,
            emu_store      = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.do_FFweight       = do_FFweight
        self.sys_FFe           = sys_FFe
        self.sys_FFm           = sys_FFm
        self.sys_CHF           = sys_CHF
        self.config_file_e     = config_file_e
        self.config_file_m     = config_file_m
        self.config_fileCHF    = config_fileCHF
        self.sys_id_e          = sys_id_e
        self.sys_iso_e         = sys_iso_e
        self.sys_reco_e        = sys_reco_e
        self.sys_reco_m        = sys_reco_m
        self.sys_iso_m         = sys_iso_m
        self.sys_TTVA_m        = sys_TTVA_m
        self.emu_store         = emu_store

        assert key, "Must provide key for storing mu reco sf"
        assert config_file_e, "Must provide config file!"
        assert config_file_m, "Must provide config file!"
        assert config_fileCHF, "Must provide config file!"
    #_________________________________________________________________________
    def initialize(self):

      f = ROOT.TFile.Open(self.config_file_e)
      assert f, "Failed to open fake-factor config file: %s"%(self.config_file_e)
      
      if self.sys_FFe=="UP":
        h_ff = f.Get("FFup")
      elif self.sys_FFe=="DN":
        h_ff = f.Get("FFdn")
      else:
        h_ff = f.Get("FF")
      assert h_ff, "Failed to get 'h_ff' from %s"%(self.config_file_e)

      self.h_ff = h_ff.Clone()
      self.h_ff.SetDirectory(0)
      f.Close()

      f = ROOT.TFile.Open(self.config_file_m)
      assert f, "Failed to open fake-factor config file: %s"%(self.config_file_m)
      
      g_ff = f.Get("g_ff_stat_sys")

      assert g_ff, "Failed to get 'h_ff' from %s"%(self.config_file_m)

      self.g_ff = g_ff.Clone()
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

      #Electron
      self.id_sys_e = 0
      if self.sys_id_e == "UP":
        self.id_sys_e = 2
      elif self.sys_id_e == "DN":
        self.id_sys_e = 1

      self.iso_sys_e = 0
      if self.sys_iso_e == "UP":
        self.iso_sys_e = 2
      elif self.sys_iso_e == "DN":
        self.iso_sys_e = 1

      self.reco_sys_e = 0
      if self.sys_reco_e == "UP":
        self.reco_sys_e = 2
      elif self.sys_reco_e == "DN":
        self.reco_sys_e = 1

      #Muon
      self.reco_sys_m = 0
      if self.sys_reco_m == "UPSTAT":
        self.reco_sys_m = 4
      elif self.sys_reco_m == "UPSYS":
        self.reco_sys_m = 8
      elif self.sys_reco_m == "DNSTAT":
        self.reco_sys_m = 3
      elif self.sys_reco_m == "DNSYS":
        self.reco_sys_m = 7

      self.iso_sys_m=0
      if self.sys_iso_m ==   "UPSTAT":
        self.iso_sys_m= 2
      elif self.sys_iso_m == "UPSYS":
        self.iso_sys_m= 4
      elif self.sys_iso_m == "DNSTAT":
        self.iso_sys_m= 1
      elif self.sys_iso_m == "DNSYS":
        self.iso_sys_m= 3

      self.TTVA_sys_m=0
      if self.sys_TTVA_m ==   "UPSTAT":
        self.TTVA_sys_m= 2
      elif self.sys_TTVA_m == "UPSYS":
        self.TTVA_sys_m= 4
      elif self.sys_TTVA_m == "DNSTAT":
        self.TTVA_sys_m= 1
      elif self.sys_TTVA_m == "DNSYS":
        self.TTVA_sys_m= 3

    #_________________________________________________________________________
    def execute(self, weight):

      MUONS_T = []
      MUONS = []
      ELECTRONS_T = []
      ELECTRONS = []
      if self.emu_store:
        EMUS = self.store['emu_store']
        for emu in EMUS:
          if emu.m < 1.:
            ELECTRONS += [emu]
            if ( emu.isIsolated_Loose and emu.LHMedium ) :
              ELECTRONS_T += [emu]
          else:
            MUONS += [emu]
            if ( emu.isIsolated_FixedCutTightTrackOnly and emu.trkd0sig<=3. ) :
              MUONS_T += [emu]
      else:
        MUONS_T = self.store['muons_tight']
        MUONS   = self.store['muons']
        ELECTRONS_T = self.store['electrons_tight_MediumLLH_isolLoose']
        ELECTRONS   = self.store['electrons_loose_LooseLLH']

      if "mc" in self.sampletype and self.chain.mcChannelNumber in range(306538,306560) + range(302657,302713) + range(309063,309073) + range(306533,306561):
          if len(MUONS_T) != len(MUONS) or len(ELECTRONS) != len(ELECTRONS_T) :
              if self.key:
                self.store[self.key] = 0.
                return True

      sf = 1.0
      if self.do_FFweight and ( len(MUONS_T) != len(MUONS) or len(ELECTRONS) != len(ELECTRONS_T) ):
        sf = -1.0
      muons = MUONS
      electrons = ELECTRONS

      for ele in electrons:
        if (ele.isIsolated_Loose and ele.LHMedium) :
          if "mc" in self.sampletype :
            if (self.chain.mcChannelNumber in range(306538,306560) + range(302657,302713) + range(309063,309073) + range(306533,306561)) or ele.electronType() in [1,2,3] :
              sf *= getattr(ele,"IsoEff_SF_"   + self.IDLevels[1] + self.isoLevels[0] ).at(self.iso_sys_e)
              sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[1] ).at(self.id_sys_e)
              sf *= getattr(ele,"RecoEff_SF").at(self.reco_sys_e)
            if self.chain.mcChannelNumber in range(306538,306560) + range(302657,302713) + range(309063,309073) + range(306533,306561):
              continue # no charge-flip SF for signal
            ptBin  = self.h_ptFunc.FindBin( ele.tlv.Pt()/GeV )
            etaBin = self.h_etaFunc.FindBin( abs( ele.caloCluster_eta ) )
            if ptBin==self.h_ptFunc.GetNbinsX()+1:
              ptBin -= 1 
            if ele.electronType() in [2,3]:
              if self.sys_CHF == None:
                sf *= self.h_ptFunc.GetBinContent( ptBin ) * self.h_etaFunc.GetBinContent( etaBin )                
              elif self.sys_CHF == "UP":
                sf *= (self.h_ptFunc.GetBinContent( ptBin )+self.h_ptFunc.GetBinError( ptBin )) * (self.h_etaFunc.GetBinContent( etaBin )+self.h_etaFunc.GetBinError( etaBin ))               
              elif self.sys_CHF == "DN":
                sf *= (self.h_ptFunc.GetBinContent( ptBin )-self.h_ptFunc.GetBinError( ptBin )) * (self.h_etaFunc.GetBinContent( etaBin )-self.h_etaFunc.GetBinError( etaBin ))
            elif ele.electronType() in [1]:
              probMC   = 0
              probData = 0
              if self.sys_CHF == None:
                probMC   = self.h_ptRateMC.GetBinContent( ptBin )   * self.h_etaRateMC.GetBinContent( etaBin )
                probData = self.h_ptRateData.GetBinContent( ptBin ) * self.h_etaRateData.GetBinContent( etaBin )
              elif self.sys_CHF == "UP":
                probMC   = (self.h_ptRateMC.GetBinContent( ptBin )  -self.h_ptRateMC.GetBinError( ptBin ))   * (self.h_etaRateMC.GetBinContent( etaBin )  -self.h_etaRateMC.GetBinError( etaBin ))
                probData = (self.h_ptRateData.GetBinContent( ptBin )+self.h_ptRateData.GetBinError( ptBin )) * (self.h_etaRateData.GetBinContent( etaBin )+self.h_etaRateData.GetBinError( etaBin ))
              elif self.sys_CHF == "DN":
                probMC   = (self.h_ptRateMC.GetBinContent( ptBin )  +self.h_ptRateMC.GetBinError( ptBin ))   * (self.h_etaRateMC.GetBinContent( etaBin )  +self.h_etaRateMC.GetBinError( etaBin ))
                probData = (self.h_ptRateData.GetBinContent( ptBin )-self.h_ptRateData.GetBinError( ptBin )) * (self.h_etaRateData.GetBinContent( etaBin )-self.h_etaRateData.GetBinError( etaBin ))
              sf *= ( 1 - probData )/( 1 - probMC )
        else :
          if "mc" in self.sampletype:
            assert self.chain.mcChannelNumber not in range(306538,306560) + range(302657,302713) + range(309063,309073) + range(306533,306561), " no fake factor for signal.."
          if self.do_FFweight:
            electron_pt = ele.tlv.Pt()/GeV
            if electron_pt > 2000.:
              electron_pt = 1999.
            sf *= -self.h_ff.GetBinContent( self.h_ff.FindBin( electron_pt, abs( ele.caloCluster_eta ) ) )
          if "mc" in self.sampletype :
            if True or ele.electronType() in [1,2,3] :
              sf *= getattr(ele,"PIDEff_SF_" + self.IDLevels[0] ).at(self.id_sys_e)
              sf *= getattr(ele,"RecoEff_SF").at(self.reco_sys_e)

      for muon in muons:
        if (muon.isIsolated_FixedCutTightTrackOnly and muon.trkd0sig <= 3.0) :
          if "mc" in self.sampletype :
            if (self.chain.mcChannelNumber in range(306538,306560) + range(302657,302713) + range(309063,309073) + range(306533,306561)) or  muon.isTrueIsoMuon() :
              sf *= getattr(muon,"_".join(["IsoEff","SF","Iso"+"FixedCutTightTrackOnly"])).at(self.iso_sys_m)
              sf *= getattr(muon,"_".join(["RecoEff","SF","Reco"+"Medium"])).at(self.reco_sys_m)
              sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(self.TTVA_sys_m)
        else :
          if "mc" in self.sampletype:
            assert self.chain.mcChannelNumber not in range(306538,306560) + range(302657,302713) + range(309063,309073) + range(306533,306561), " no fake factor for signal.."
          if self.do_FFweight:
            ff_mu = 0.
            eff_up_mu = 0.
            eff_dn_mu = 0.
            for ibin_mu in xrange(1,self.g_ff.GetN()):
              edlow = self.g_ff.GetX()[ibin_mu] - self.g_ff.GetEXlow()[ibin_mu]
              edhi  = self.g_ff.GetX()[ibin_mu] + self.g_ff.GetEXhigh()[ibin_mu]
              if muon.tlv.Pt()/GeV>=edlow and muon.tlv.Pt()/GeV<edhi:
                ff_mu = self.g_ff.GetY()[ibin_mu]
                eff_up_mu = self.g_ff.GetEYhigh()[ibin_mu]
                eff_dn_mu = self.g_ff.GetEYlow()[ibin_mu]
                break
            if self.sys_FFm == 'UP': ff_mu +=eff_up_mu
            if self.sys_FFm == 'DN': ff_mu -=eff_dn_mu
            sf *= -ff_mu
          if "mc" in self.sampletype :
            if True or muon.isTrueIsoMuon() :
              sf *= getattr(muon,"_".join(["RecoEff","SF","Reco"+"Medium"])).at(self.reco_sys_m)
              sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(self.TTVA_sys_m)

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

      if len(electrons) not in [2,3]: 
        if self.key: 
          self.store[self.key] = sf
        return True

      if "mc" not in self.sampletype:
        if self.key: 
          self.store[self.key] = sf
        return True

      # two electron case
      if len(electrons) == 2:
        for ele in electrons:
          if ele.LHMedium and ele.isIsolated_Loose:
            sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
          else:
            sf *= getattr(ele,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
        if self.key: 
          self.store[self.key] = sf
        return True

      if len(electrons)!=3: 
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
                combinationProbD  *= getattr(elePass,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)*\
                                     getattr(elePass,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
                combinationProbMC *= getattr(elePass,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
              else:
                combinationProbD  *= getattr(elePass,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)*\
                                     getattr(elePass,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
                combinationProbMC *= getattr(elePass,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
            if eleFail.LHMedium and eleFail.isIsolated_Loose:
              combinationProbD  *= 1 - ( getattr(eleFail,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)*\
                                         getattr(eleFail,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys) )
              combinationProbMC *= 1 -   getattr(eleFail,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
            else:
              combinationProbD  *= 1 - ( getattr(eleFail,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)*\
                                         getattr(eleFail,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys) )
              combinationProbMC *= 1 -   getattr(eleFail,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
            break
        P2passD  += combinationProbD   # a*b*(1-c) + a*c*(1-b) + b*c*(1-d) 
        P2passMC += combinationProbMC  # a*b*(1-c) + a*c*(1-b) + b*c*(1-d)
      for ele in electrons:
        if ele.LHMedium and ele.isIsolated_Loose:
          P3passD  *= getattr(ele,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)*\
                      getattr(ele,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
          P3passMC *= getattr(ele,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[1]+self.isoLevels[1]).at(self.trig_sys)
        else:
          P3passD  *= getattr(ele,"TrigEff_SF_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)*\
                      getattr(ele,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_"+self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)
          P3passMC *= getattr(ele,"TrigMCEff_DI_E_2015_e12_lhloose_L1EM10VH_2016_e17_lhvloose_nod0_" +self.IDLevels[0]+self.isoLevels[0]).at(self.trig_sys)

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
            sf *= getattr(electrons[0],"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= F2
          elif self.typeFF=="LT":
            sf *= getattr(electrons[1],"IsoEff_SF_" + self.IDLevels[1] + self.isoLevels[0] ).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_" + self.IDLevels[1][0:-3] ).at(0)
            sf *= getattr(electrons[1],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]+"_"+self.isoLevels[0]).at(0)
            sf *= getattr(electrons[0],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= F1
          elif self.typeFF=="LL":
            sf *= getattr(electrons[0],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
            sf *= getattr(electrons[0],"TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_"+self.IDLevels[1]).at(0)
            sf *= getattr(electrons[1],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
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
          sf *= getattr(electrons[0],"PIDEff_SF_" + self.IDLevels[0][0:-3] ).at(0)
          #sf *= getattr(electrons[0],"TrigMCEff_SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0_"+self.IDLevels[1]).at(0)
          sf *= F

        else:
          sf *= F

        if self.key: 
          self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------
class MuTrigSF(pyframe.core.Algorithm):
    """
    Muon trigger scale factor (OR of signle muon triggers)
    """
    #__________________________________________________________________________
    def __init__(self, name="MuTrigSF",
            trig_list   = None,
            match_all   = False,
            mu_iso      = None,
            mu_reco     = None,
            key         = None,
            sys_trig    = None,
            period      = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.trig_list   = trig_list # if for some reason a different list is needed
        self.match_all   = match_all
        self.mu_iso      = mu_iso
        self.mu_reco     = mu_reco
        self.key         = key
        self.sys_trig    = sys_trig
        self.period      = period

        assert key, "Must provide key for storing mu reco sf"
        assert period in [2015,2016], "Must be either 2015 or 2016"
    #_________________________________________________________________________
    def initialize(self):
      
        self.trig_sys=0
        if self.sys_trig == "UPSTAT":
            self.trig_sys = 2
        elif self.sys_trig == "UPSYS":
            self.trig_sys = 4
        elif self.sys_trig == "DNSTAT":
            self.trig_sys = 1
        elif self.sys_trig == "DNSYS":
            self.trig_sys = 3

        if not self.mu_reco:      self.mu_reco = "Loose"
        if not self.mu_iso:       self.mu_iso  = "FixedCutTightTrackOnly"
      
        if "Not" in self.mu_iso:  self.mu_iso  = "Loose"
        if "Not" in self.mu_reco: self.mu_reco = "Loose"

        if not self.trig_list: self.trig_list = self.store["reqTrig"]

    #_________________________________________________________________________
    def execute(self, weight):
        trig_sf=1.0

        if self.sampletype == "mc" :
          runNumber = self.chain.rand_run_nr
        else :
          runNumber = self.chain.runNumber

        if (runNumber < 290000. and self.period==2016) or (runNumber > 290000. and self.period==2015):
          if self.key: 
            self.store[self.key] = trig_sf
          return True
        trig_sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          
          eff_data_chain = 1.0 
          eff_mc_chain   = 1.0
          
          for i,m in enumerate(muons):
          
            eff_data_muon = 1.0 
            eff_mc_muon   = 1.0

            if m.isTruthMatchedToMuon: 
              for trig in self.trig_list:
                
                sf_muon  = getattr(m,"_".join(["TrigEff","SF",trig,"Reco"+self.mu_reco,"Iso"+self.mu_iso])).at(self.trig_sys)
                eff_muon = getattr(m,"_".join(["TrigMCEff",trig,"Reco"+self.mu_reco,"Iso"+self.mu_iso])).at( 0 )
                                
                eff_data_muon *= 1 - sf_muon * eff_muon
                eff_mc_muon   *= 1 - eff_muon
              
              eff_data_muon = ( 1 - eff_data_muon )
              eff_mc_muon   = ( 1 - eff_mc_muon )
              
              if self.match_all:
                eff_data_chain *= eff_data_muon
                eff_mc_chain   *= eff_mc_muon
              else:
                eff_data_chain *= 1. - eff_data_muon
                eff_mc_chain   *= 1. - eff_mc_muon
          
          if not self.match_all: 
            eff_data_chain = ( 1 - eff_data_chain )
            eff_mc_chain   = ( 1 - eff_mc_chain )
          
          if eff_mc_chain > 0:
            trig_sf = eff_data_chain / eff_mc_chain
                 
        if self.key: 
          self.store[self.key] = trig_sf
        return True
# EOF
