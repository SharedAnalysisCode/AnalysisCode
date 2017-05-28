#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
algs.py

This module contains a set of analysis specific algs 
for calculating variables, applying selection and 
plotting.
"""

## std modules
import itertools
import os
import math
import ROOT
import random

## logging
import logging
log = logging.getLogger(__name__)

## python
from itertools import combinations
from copy import copy

## pyframe
import pyframe

import mcutils

GeV = 1000.0
g_mZ = 91.1876*GeV

#------------------------------------------------------------------------------
class CutAlg(pyframe.core.Algorithm):
    """
    Filtering alg for applying a single cut.  The predefined cuts must be
    implemeneted as a function with the prefix "cut_". One can then specify the
    cut to be applied by passing the cut=<cut name> in the constructor, which
    will execture the cut_<cut name>() function.
    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = None,
                 cut      = None,
                 cutflow  = None,
                 isfilter = True,
                 ):
        pyframe.core.Algorithm.__init__(self, name if name else cut,isfilter=isfilter)
        self.cutflow = cutflow
         
    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)

        return self.apply_cut(self.name)

    #__________________________________________________________________________
    def apply_cut(self,cutname):
        if self.store.has_key(cutname): return self.store[cutname]
        cut_function = 'cut_%s'%cutname
        assert hasattr(self,cut_function),"cut %s doesnt exist!'"%(cutname)
        self.store[cutname] = result = getattr(self,cut_function)()
        return result
    
    #__________________________________________________________________________
    def cut_AtLeastOneMuon(self):
        return self.chain.nmuon > 0
    
    #__________________________________________________________________________
    def cut_AtLeastTwoMuons(self):
      return self.chain.nmuon > 1
    
    #__________________________________________________________________________
    def cut_OneMuon(self):
        return self.chain.nmuon == 1
    
    #__________________________________________________________________________
    def cut_TwoMuons(self):
        return self.chain.nmuon == 2
    
    #__________________________________________________________________________
    def cut_TwoSSMuons(self):
      muons  = self.store['muons']
      if len(muons)==2:
        if muons[0].trkcharge * muons[1].trkcharge > 0.0:
          return True
      return False
    
    #__________________________________________________________________________
    def cut_TwoOSMuons(self):
      muons  = self.store['muons']
      if len(muons)==2:
        if muons[0].trkcharge * muons[1].trkcharge < 0.0:
          return True
      return False
    
    #__________________________________________________________________________
    def cut_OneJet(self):
        return self.chain.njets == 1
    
    #__________________________________________________________________________
    def cut_AtLeastOneJet(self):
        return self.chain.njets > 0
    
    #__________________________________________________________________________
    def cut_AtLeastTwoJets(self):
        return self.chain.njets > 1
    
    #__________________________________________________________________________
    def cut_AllMuPt22(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and m.tlv.Pt()>=22.0*GeV
      return passed
    
    #__________________________________________________________________________
    def cut_AllMuEta247(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and abs(m.tlv.Eta())<2.47
      return passed
    
    #__________________________________________________________________________
    def cut_MuTT(self):
      muons = self.store['muons']
      lead_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      return lead_is_tight and sublead_is_tight
    #__________________________________________________________________________
    def cut_MuTL(self):
      muons = self.store['muons']
      lead_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      return lead_is_tight and sublead_is_loose
    #__________________________________________________________________________
    def cut_MuLT(self):
      muons = self.store['muons']
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      return lead_is_loose and sublead_is_tight
    #__________________________________________________________________________
    def cut_MuLL(self):
      muons = self.store['muons']
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      return lead_is_loose and sublead_is_loose
    
    
    #__________________________________________________________________________
    def cut_LeadMuIsoTight(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return lead_mu.isIsolated_FixedCutTightTrackOnly
    
    #__________________________________________________________________________
    def cut_SubLeadMuIsoTight(self):
      muons = self.store['muons']
      sublead_mu = muons[1]
      return sublead_mu.isIsolated_FixedCutTightTrackOnly

    #__________________________________________________________________________
    def cut_LeadMuIsoNotTight(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return not lead_mu.isIsolated_FixedCutTightTrackOnly
    
    #__________________________________________________________________________
    def cut_SubLeadMuIsoNotTight(self):
      muons = self.store['muons']
      sublead_mu = muons[1]
      return not sublead_mu.isIsolated_FixedCutTightTrackOnly

    #__________________________________________________________________________
    def cut_MuPairsIsoTight(self):
      cname = "MuPairsIsoTight"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc": pass
          #if not p.isTruthMatchedToMuonPair(): continue
        if not (p.lead.isIsolated_FixedCutTightTrackOnly and p.sublead.isIsolated_FixedCutTightTrackOnly): 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsLeadIsoTightSubLeadIsoNotTight(self):
      cname = "MuPairsLeadIsoTightSubLeadIsoNotTight"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc": pass
          #if not p.isTruthMatchedToMuonPair(): continue
        if not (p.lead.isIsolated_FixedCutTightTrackOnly and (p.sublead.isIsolated_Loose or p.sublead.isIsolated_FixedCutLoose)): 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsLeadIsoNotTightSubLeadIsoTight(self):
      cname = "MuPairsLeadIsoNotTightSubLeadIsoTight"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc": pass
          #if not p.isTruthMatchedToMuonPair(): continue
        if not (p.sublead.isIsolated_FixedCutTightTrackOnly and (p.lead.isIsolated_Loose or p.lead.isIsolated_FixedCutLoose)): 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsLeadIsoNotTightSubLeadIsoNotTight(self):
      cname = "MuPairsLeadIsoNotTightSubLeadIsoNotTight"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc": pass
          #if not p.isTruthMatchedToMuonPair(): continue
        if not ((p.sublead.isIsolated_Loose or p.sublead.isIsolated_FixedCutLoose) and (p.lead.isIsolated_Loose or p.lead.isIsolated_FixedCutLoose)): 
          p.StoreCut(cname,False)
      return True

    #__________________________________________________________________________
    def cut_MuPairsLeadPt25SubLeadPt22(self):
      cname = "MuPairsLeadPt25SubLeadPt22"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if p.lead.tlv.Pt()<25*GeV and p.sublead.tlv.Pt()<22*GeV: 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsLeadPt20SubLeadPt15(self):
      cname = "MuPairsLeadPt20SubLeadPt15"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if p.lead.tlv.Pt()<20*GeV and p.sublead.tlv.Pt()<15*GeV: 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsLeadPt25SubLeadPt20(self):
      cname = "MuPairsLeadPt25SubLeadPt20"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if p.lead.tlv.Pt()<25*GeV and p.sublead.tlv.Pt()<20*GeV: 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsMVis15(self):
      cname = "MuPairsMVis15"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if p.m_vis<15*GeV: 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsMZwindow(self):
      cname = "MuPairsMZwindow"
      mZ = 91.1876*GeV
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if abs(p.m_vis - mZ)<10*GeV: 
          p.StoreCut(cname,False)
      return True

    #__________________________________________________________________________
    def cut_MZwindow(self):
      mZ = 91.1876*GeV
      muons = self.store['muons']
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis - mZ) > 30*GeV
    
    #__________________________________________________________________________
    def cut_M15(self):
      muons = self.store['muons']
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis)>15*GeV

    #__________________________________________________________________________
    def cut_MuPairsInvMZwindow(self):
      cname = "MuPairsInvMZwindow"
      mZ = 91.1876*GeV
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if abs(p.m_vis - mZ)>10*GeV: 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsAreSS(self):
      cname = "MuPairsAreSS"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if p.charge_product<0.0: 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsAreOS(self):
      cname = "MuPairsAreOS"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if p.charge_product>0.0: 
          p.StoreCut(cname,False)
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsDeltaRJet04(self):
      cname = "MuPairsDeltaRJet04"
      jets = self.store['jets']
      pairs = self.store['mu_pairs']
      
      for p in pairs:
        p.StoreCut(cname,True)
        for j in jets:
          if j.tlv.DeltaR(p.lead.tlv)<0.4 or j.tlv.DeltaR(p.sublead.tlv)<0.4:
            p.StoreCut(cname,False)
      return True
    
    
    #__________________________________________________________________________
    def cut_MuPairsTT(self):
      cname = "MuPairsTT"
      pairs = self.store['mu_pairs']
      for p in pairs:
        lead_is_tight = bool(p.lead.isIsolated_FixedCutTightTrackOnly and p.lead.trkd0sig<3.)
        sublead_is_tight = bool(p.sublead.isIsolated_FixedCutTightTrackOnly and p.sublead.trkd0sig<3.)
        p.StoreCut(cname,lead_is_tight and sublead_is_tight)
      return True 
    #__________________________________________________________________________
    def cut_MuPairsTL(self):
      cname = "MuPairsTL"
      pairs = self.store['mu_pairs']
      for p in pairs:
        lead_is_tight = bool(p.lead.isIsolated_FixedCutTightTrackOnly and p.lead.trkd0sig<3.)
        sublead_is_loose = bool(not p.sublead.isIsolated_FixedCutTightTrackOnly and p.sublead.trkd0sig<10.)
        p.StoreCut(cname,lead_is_tight and sublead_is_loose)
      return True 
    #__________________________________________________________________________
    def cut_MuPairsLT(self):
      cname = "MuPairsLT"
      pairs = self.store['mu_pairs']
      for p in pairs:
        lead_is_loose = bool(not p.lead.isIsolated_FixedCutTightTrackOnly and p.lead.trkd0sig<10.)
        sublead_is_tight = bool(p.sublead.isIsolated_FixedCutTightTrackOnly and p.sublead.trkd0sig<3.)
        p.StoreCut(cname,lead_is_loose and sublead_is_tight)
      return True 
    #__________________________________________________________________________
    def cut_MuPairsLL(self):
      cname = "MuPairsLL"
      pairs = self.store['mu_pairs']
      for p in pairs:
        lead_is_loose = bool(not p.lead.isIsolated_FixedCutTightTrackOnly and p.lead.trkd0sig<10.)
        sublead_is_loose = bool(not p.sublead.isIsolated_FixedCutTightTrackOnly and p.sublead.trkd0sig<10.)
        p.StoreCut(cname,lead_is_loose and sublead_is_loose)
      return True 
    
    #__________________________________________________________________________
    def cut_MuPairsMatchSingleMuIsoChain(self):
      cname = "MuPairsMatchSingleMuIsoChain"
      pairs = self.store['mu_pairs']
      #trig = {"HLT_mu20_L1MU15":0, "HLT_mu20_iloose_L1MU15":1, "HLT_mu50":2} # for the "ntuples" file
      trig = {"HLT_mu20_L1MU15":0, "HLT_mu20_iloose_L1MU15":0, "HLT_mu50":1}
      
      for p in pairs:
        p.StoreCut(cname,False)
        
        if p.lead.isTrigMatchedToChain.at(trig["HLT_mu20_iloose_L1MU15"]) or p.lead.isTrigMatchedToChain.at(trig["HLT_mu50"]):
          if p.sublead.isTrigMatchedToChain.at(trig["HLT_mu20_iloose_L1MU15"]) or p.sublead.isTrigMatchedToChain.at(trig["HLT_mu50"]): 
            p.StoreCut(cname,True)
        
        #if p.lead.isTrigMatchedToChain.at(trig["HLT_mu20_iloose_L1MU15"]) or p.lead.isTrigMatchedToChain.at(trig["HLT_mu50"]) : p.StoreCut(cname,True)
        #if p.sublead.isTrigMatchedToChain.at(trig["HLT_mu20_iloose_L1MU15"]) or p.sublead.isTrigMatchedToChain.at(trig["HLT_mu50"]) : p.StoreCut(cname,True)
      
      return True

    #__________________________________________________________________________
    def cut_MatchSingleMuIsoChain(self):
      muons = self.store['muons']
      #trig = {"HLT_mu20_L1MU15":0, "HLT_mu20_iloose_L1MU15":1, "HLT_mu50":2} # for the "ntuples" file
      trig = {"HLT_mu20_L1MU15":0, "HLT_mu20_iloose_L1MU15":0, "HLT_mu50":1}
      for m in muons:
        if m.isTrigMatchedToChain.at(trig["HLT_mu20_iloose_L1MU15"]) or m.isTrigMatchedToChain.at(trig["HLT_mu50"]) : return True
      return False
    #__________________________________________________________________________
    def cut_PassSingleMuIsoChain(self):
      chain = ["HLT_mu20_iloose_L1MU15","HLT_mu50"]
      for i in xrange(self.chain.passedTriggers.size()):
        if self.chain.passedTriggers.at(i) in chain: return True
      return False
    
    
    
    #__________________________________________________________________________
    def cut_MatchSingleMuPrescChainLow(self):
      muons = self.store['muons']
      trig = {"HLT_mu20_L1MU15":0,"HLT_mu24":1}
      for m in muons:
        #if m.isTrigMatchedToChain.at(trig["HLT_mu20_L1MU15"]) or m.isTrigMatchedToChain.at(trig["HLT_mu24"]): return True
        if m.isTrigMatchedToChain.at(trig["HLT_mu20_L1MU15"]): return True
      return False
    #__________________________________________________________________________
    def cut_PassSingleMuPrescChainLow(self):
      #chain = ["HLT_mu20_L1MU15","HLT_mu24"]
      chain = ["HLT_mu20_L1MU15"]
      for i in xrange(self.chain.passedTriggers.size()):
        if self.chain.passedTriggers.at(i) in chain: return True
      return False
    
    #__________________________________________________________________________
    def cut_MatchSingleMuPrescChainAll(self):
      muons = self.store['muons']
      trig = {"HLT_mu20_L1MU15":0,"HLT_mu24":1}
      for m in muons:
        if m.isTrigMatchedToChain.at(trig["HLT_mu20_L1MU15"]) or m.isTrigMatchedToChain.at(trig["HLT_mu24"]): return True
      return False
    #__________________________________________________________________________
    def cut_PassSingleMuPrescChainAll(self):
      chain = ["HLT_mu20_L1MU15","HLT_mu24"]
      for i in xrange(self.chain.passedTriggers.size()):
        if self.chain.passedTriggers.at(i) in chain: return True
      return False
    
    
    
    #__________________________________________________________________________
    def cut_PassDiMuChain(self):
      chain = ["HLT_2mu10"]
      for i in xrange(self.chain.passedTriggers.size()):
        if self.chain.passedTriggers.at(i) in chain: return True
      return False
    
    #__________________________________________________________________________
    def cut_LeadMuTruthFilter(self):
      muons = self.store['muons'] 
      if self.sampletype == "mc":
        return muons[0].isTrueIsoMuon()
      return True
    
    #__________________________________________________________________________
    def cut_SubLeadMuTruthFilter(self):
      muons = self.store['muons'] 
      if self.sampletype == "mc":
        return muons[1].isTrueIsoMuon()
      return True
    
    #__________________________________________________________________________
    def cut_MuTruthFilter(self):
      muons = self.store['muons'] 
      if self.sampletype == "mc":
        for m in muons:
          if not m.isTrueIsoMuon(): return False
      return True 
    
    #__________________________________________________________________________
    def cut_MuPairsTruthFilter(self):
      cname = "MuPairsTruthFilter"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc":
          if not (p.lead.isTrueIsoMuon() and p.sublead.isTrueIsoMuon()):
            p.StoreCut(cname,False)
      return True
   
    #__________________________________________________________________________
    def cut_MuPairsAngleHi10Low25(self):
      cname = "MuPairsAngleHi10Low25"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if p.angle < 1.0 or p.angle > 2.5:
          p.StoreCut(cname,False)
      
      for p in pairs:
        if (p.angle < 1.0 or p.angle > 2.5):
         print p, p.cdict, len(pairs), p.angle
      return True
    
    #__________________________________________________________________________
    def cut_MuPairsZ0SinThetaNot002(self):
      cname = "MuPairsZ0SinThetaNot002"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if not (abs(p.lead.trkz0sintheta)>0.02 and abs(p.sublead.trkz0sintheta)>0.02):
          p.StoreCut(cname,False)
      return True
   
    #__________________________________________________________________________
    def cut_MuPairsFilterTT(self):
      cname = "MuPairsFilterTT"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc":
          if not (p.lead.isTrueIsoMuon() and p.sublead.isTrueIsoMuon()):
            p.StoreCut(cname,False)
      return True
    #__________________________________________________________________________
    def cut_MuPairsFilterLT(self):
      cname = "MuPairsFilterLT"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc":
          if not (p.lead.isTrueNonIsoMuon() and p.sublead.isTrueIsoMuon()):
            p.StoreCut(cname,False)
      return True
    #__________________________________________________________________________
    def cut_MuPairsFilterTL(self):
      cname = "MuPairsFilterTL"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc":
          if not (p.lead.isTrueIsoMuon() and p.sublead.isTrueNonIsoMuon()):
            p.StoreCut(cname,False)
      return True
    #__________________________________________________________________________
    def cut_MuPairsFilterLL(self):
      cname = "MuPairsFilterLL"
      pairs = self.store['mu_pairs']
      for p in pairs:
        p.StoreCut(cname,True)
        if self.sampletype == "mc":
          if not (p.lead.isTrueNonIsoMuon() and p.sublead.isTrueNonIsoMuon()):
            p.StoreCut(cname,False)
      return True
   
   
    #__________________________________________________________________________
    def cut_LeadMuD0Sig2(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<2. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig3(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<3. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig4(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<4. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig5(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<5. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig6(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<6. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig10(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<10. 
    
    
    #__________________________________________________________________________
    def cut_LeadMuD0SigNot2(self):
      muons = self.store['muons']
      return muons[0].trkd0sig>2. 
    #__________________________________________________________________________
    def cut_LeadMuD0SigNot3(self):
      muons = self.store['muons']
      return muons[0].trkd0sig>3. 
    #__________________________________________________________________________
    def cut_LeadMuD0SigNot4(self):
      muons = self.store['muons']
      return muons[0].trkd0sig>4. 
    #__________________________________________________________________________
    def cut_LeadMuD0SigNot5(self):
      muons = self.store['muons']
      return muons[0].trkd0sig>5. 
    #__________________________________________________________________________
    def cut_LeadMuD0SigNot6(self):
      muons = self.store['muons']
      return muons[0].trkd0sig>6. 
    #__________________________________________________________________________
    def cut_LeadMuD0SigNot10(self):
      muons = self.store['muons']
      return muons[0].trkd0sig>10. 
    
    
    
    
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinTheta1(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)<1.0
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinTheta01(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)<0.1
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinTheta005(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)<0.05
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinTheta02(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)<0.2
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinTheta05(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)<0.5
    
    
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinThetaNot1(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>1.0
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinThetaNot01(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>0.1
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinThetaNot005(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>0.05
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinThetaNot02(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>0.2
    
    
    #__________________________________________________________________________
    def cut_OneZ0SinThetaNot002(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>0.02 or abs(muons[1].trkz0sintheta)>0.02
    #__________________________________________________________________________
    def cut_OneZ0SinThetaNot005(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>0.05 or abs(muons[1].trkz0sintheta)>0.05
    #__________________________________________________________________________
    def cut_Z0SinThetaNot002(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>0.02 and abs(muons[1].trkz0sintheta)>0.02
    #__________________________________________________________________________
    def cut_Z0SinThetaNot005(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>0.05 and abs(muons[1].trkz0sintheta)>0.05
    #__________________________________________________________________________
    def cut_MuLeadZ0SinThetaNot005(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)>0.05 
    #__________________________________________________________________________
    def cut_MuSubLeadZ0SinThetaNot005(self):
      muons = self.store['muons']
      return abs(muons[1].trkz0sintheta)>0.05 
    
    
    #__________________________________________________________________________
    def cut_AllMuPairsMedium(self):
      pairs = self.store['mu_pairs']
      passed = True
      
      for p in pairs:
        if "mc" in self.sampletype:
          if not (p.lead.isTruthMatchedToMuon and p.sublead.isTruthMatchedToMuon): continue
        passed = passed and p.lead.isMedium and p.sublead.isMedium
      return passed 
    
    #__________________________________________________________________________
    def cut_METlow40(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 40 * GeV
    
    #__________________________________________________________________________
    def cut_METlow50(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 50 * GeV
    
    #__________________________________________________________________________
    def cut_METlow30(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 30 * GeV
    
    #__________________________________________________________________________
    def cut_METhigher10(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() > 10 * GeV
    
    #__________________________________________________________________________
    def cut_METhigher40(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() > 40 * GeV
    
    #__________________________________________________________________________
    def cut_METhigher50(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() > 50 * GeV

    #__________________________________________________________________________
    def cut_METtrkLow25(self):
      met = self.store["met_trk"]
      return met.tlv.Pt() < 25 * GeV

    #__________________________________________________________________________
    def cut_METtrkLow60(self):
      met = self.store["met_trk"]
      return met.tlv.Pt() < 60 * GeV

    #__________________________________________________________________________
    def cut_METtrkLow60(self):
      met = self.store["met_trk"]
      return met.tlv.Pt() < 60 * GeV

    #__________________________________________________________________________
    def cut_METhigher25(self):
      met = self.store["met_trk"]
      return met.tlv.Pt() > 25 * GeV

    #__________________________________________________________________________
    def cut_MThigher50(self):
      met = self.store["met_trk"]
      ele = self.store["electrons_loose_LooseLLH"][0]
      return math.sqrt( 2*ele.tlv.Pt()*met.tlv.Pt()*(1-math.cos(ele.tlv.Phi()-met.tlv.Phi())) ) > 50 * GeV

    def cut_MTlow120(self):
      met = self.store["met_trk"]
      ele = self.store["electrons_loose_LooseLLH"][0]
      return math.sqrt( 2*ele.tlv.Pt()*met.tlv.Pt()*(1-math.cos(ele.tlv.Phi()-met.tlv.Phi())) ) < 120 * GeV

    #__________________________________________________________________________
    def cut_EleJetDphi28(self):
      lead_ele = self.store["electrons_loose_LooseLLH"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_ele.tlv.DeltaPhi(lead_jet.tlv)) > 2.8
      else: return False
   
    #__________________________________________________________________________
    def cut_SumCosDPhi02(self):
      met = self.store["met_clus"]
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        scdphi = 0.0
        scdphi += ROOT.TMath.Cos(met.tlv.Phi() - lead_mu.tlv.Phi())
        scdphi += ROOT.TMath.Cos(met.tlv.Phi() - lead_jet.tlv.Phi())
        return scdphi > -0.2
      else: return False

    #__________________________________________________________________________
    def cut_MuJetDphi27(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.7
      else: return False
    
    #__________________________________________________________________________
    def cut_MuJetDphi28(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.8
      else: return False
    
    
    #__________________________________________________________________________
    def cut_MuJetDphi26(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.6
      else: return False
    
    
    #__________________________________________________________________________
    def cut_MuJetDphi24(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.4
      else: return False
    
    
    #__________________________________________________________________________
    def cut_AllJetPt25(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 25 * GeV: return False
      return True
    
    #__________________________________________________________________________
    def cut_AllJetPt35(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 35 * GeV: return False
      return True
    
    #__________________________________________________________________________
    def cut_AllJetPt40(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 35 * GeV: return False
      return True


    #HERE implement all my cuts for electrons:
    #__________________________________________________________________________   

    def cut_AtLeastOneLooseElectrons(self):
        return self.chain.nel > 0

    #__________________________________________________________________________                                                                                                  
    def cut_AtLeastTwoLooseElectrons(self):
      return self.chain.nel > 1

    #__________________________________________________________________________                                                                                                  
    def cut_OneLooseElectron(self):
        return self.chain.nel == 1

    #__________________________________________________________________________                                                                                                  
    def cut_TwoLooseElectrons(self):
        return self.chain.nel == 2

    def cut_TwoLooseLeptons(self):
        if ((self.chain.nel==1 and self.chain.nmuon==1) or (self.chain.nel==0 and self.chain.nmuon==2) or (self.chain.nel==2 and self.chain.nmuon==0)): return True;

    #__________________________________________________________________________                                                                                                  
    def cut_LeadElectronIsLoose(self):
        cname = "LeadElectronIsLoose"
        electrons  = self.store['electrons']
        if bool(len(electrons)):
           if electrons[0].tlv.Pt()>30*GeV and electrons[0].LHLoose and electrons[0].tlv.Eta()<2.47 and not(1.37<electrons[0].tlv.Eta()<1.52) and electrons[0].trkd0sig<5 and electrons[0].trkz0sintheta<0.5 : return True;
         
        return False;    

    #__________________________________________________________________________                                                                                                  
    def cut_SubLeadElectronIsLoose(self):
        cname = "SubLeadElectronIsLoose"
        electrons  = self.store['electrons']
        if bool(len(electrons)): 
           if electrons[1].tlv.Pt()>30*GeV and electrons[1].LHLoose and electrons[1].tlv.Eta()<2.47 and not(1.37<electrons[1].tlv.Eta()<1.52) and electrons[1].trkd0sig<5 and electrons[1].trkz0sintheta<0.5 : return True;
        
        return False;    

    #__________________________________________________________________________                                                                                                  
    def cut_LeadElectronIsTight(self):
        cname = "LeadElectronIsTight"
        electrons  = self.store['electrons']
        if bool(len(electrons)): 
           if electrons[0].tlv.Pt()>30*GeV and electrons[0].LHMedium and electrons[0].tlv.Eta()<2.47 and not(1.37<electrons[0].tlv.Eta()<1.52) and electrons[0].trkd0sig<5 and electrons[0].trkz0sintheta<0.5 and electrons[0].isIsolated_Loose : return True;

        return False;

    #__________________________________________________________________________ 

    def cut_SubLeadElectronIsTight(self):
        cname = "SubLeadElectronIsTight"
        electrons  = self.store['electrons']
        if bool(len(electrons)): 
           if electrons[1].tlv.Pt()>30*GeV and electrons[1].LHMedium and electrons[1].tlv.Eta()<2.47 and not(1.37<electrons[1].tlv.Eta()<1.52) and electrons[1].trkd0sig<5 and electrons[1].trkz0sintheta<0.5 and electrons[1].isIsolated_Loose : return True;

        return False;

    #__________________________________________________________________________                                                                                               
    def cut_TwoOSElectrons(self):
      electrons  = self.store['electrons']
      if len(electrons)==2:
        if electrons[0].trkcharge * electrons[1].trkcharge < 0.0:
          return True
      return False

    #__________________________________________________________________________                                                                                                  
    def cut_TwoSSElectrons(self):
      electrons  = self.store['electrons']
      if len(electrons)==2:
        if electrons[0].trkcharge * electrons[1].trkcharge > 0.0:
          return True
      return False

    def cut_TwoSSEleMuon(self):
      electrons  = self.store['electrons']
      muons = self.store['muons']
      if len(electrons)==1 and len(muons)==1:
        if electrons[0].trkcharge * muons[0].trkcharge > 0.0:
          return True
      return False

     #__________________________________________________________________________                                                                               
                     
    def cut_ElectronMassAbove200GeV(self):
      electrons = self.store['electrons']
      if len(electrons)==2:
         self.store['ee_invM'] = (electrons[0].tlv + electrons[1].tlv).M()
         if  bool(self.store['ee_invM'] > 200*GeV): return True;

      return False
    
    def cut_ElectronMassInZWindow(self):
        mZ = 91.1876*GeV
        electrons = self.store['electrons']
        if len(electrons)==2: 
           if bool(((electrons[0].tlv + electrons[1].tlv).M() - mZ) <10*GeV): return True;
            
        return False

    def cut_LeptonMassInZWindow(self):
        mZ = 91.1876*GeV
        electrons = self.store['electrons']
        muons= self.store['muons']
        if len(electrons)==2: 
           if bool(((electrons[0].tlv + electrons[1].tlv).M() - mZ) <10*GeV): return True;
        if len(muons)==2:   
           if bool(((muons[0].tlv + muons[1].tlv).M() - mZ) <10*GeV): return True;
        return False

    def cut_PassHLTe60lhmedium(self):
        chain = ["HLT_e60_lhmedium"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTe26lhtightnod0ivarloose(self):
        chain = ["HLT_e26_lhtight_nod0_ivarloose"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTe24lhmediumL1EM18VH(self):
        chain = ["HLT_e24_lhmedium_L1EM18VH"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTe24lhmediumL1EM20VH(self):
        chain = ["HLT_e24_lhmedium_L1EM20VH"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTe120lhloose(self):
        chain = ["HLT_e120_lhloose"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassSingleEleChain(self):
      chain = ["HLT_e24_lhmedium_L1EM18VH","HLT_e24_lhmedium_L1EM20VH","HLT_e60_lhmedium","HLT_e120_lhloose"]
      for i in xrange(self.chain.passedTriggers.size()):
        if self.chain.passedTriggers.at(i) in chain: return True
      return False

    def cut_PassHLT2e17lhloose(self):
        chain = ["HLT_2e17_lhloose"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTmu26imedium(self):
        chain = ["HLT_mu26_imedium"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTmu26ivarmedium(self):
        chain = ["HLT_mu26_ivarmedium"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTmu50(self):
        chain = ["HLT_mu50"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTmu22mu8noL1(self):
        chain = ["HLT_mu22_mu8noL1"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTe17lhloosenod0mu14(self):
        chain = ["HLT_e17_lhloose_nod0_mu14"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTe26lhmediumnod0L1EM22VHImu8noL1(self):
        chain = ["HLT_e26_lhmedium_nod0_L1EM22VHI_mu8noL1"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassHLTe7lhmediumnod0mu24(self):
        chain = ["HLT_e7_lhmedium_nod0_mu24"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassORSingleLeptonTriggerMuon(self):
        chain = ["HLT_mu26_ivarmedium","HLT_mu50"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_PassSingleEleChain(self):
        # SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0
        runNumber = self.chain.runNumber
        chain = []
        if runNumber < 290000. :
          chain = ["HLT_e24_lhmedium_L1EM20VH", "HLT_e60_lhmedium","HLT_e120_lhloose"]
        else :
          chain = ["HLT_e26_lhtight_nod0", "HLT_e60_lhmedium_nod0","HLT_e140_lhloose_nod0"]
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in chain: return True

        return False

    def cut_isEEEvent(self):
        if (self.chain.nel==2 and self.chain.nmuon==0): return True
        return False

    def cut_isEMuEvent(self):
        if (self.chain.nel==1 and self.chain.nmuon==1): return True
        return False
    
    def cut_isMuMuEvent(self):
        if (self.chain.nel==0 and self.chain.nmuon==2): return True
        return False

    # -- stuff added by Miha --------------

    def cut_ZVetoLooseEleLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)<1: return False
        for pair in itertools.combinations(electrons,2):
          if abs( (pair[0].tlv + pair[1].tlv).M() - g_mZ) < 20*GeV:
            return False
        return True

    def cut_DYVetoTightEleMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)>1: return False
        return True

    ##  tight: MediumLLH isolLoose   loose: LooseLLH
    # ---------------------------------------------------
    def cut_ExactlyZeroMuons(self):
        muons = self.store['muons']
        if len(muons)==0: 
          return True
        return False

    def cut_ExactlyZeroElectrons(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==0: 
          return True
        return False

    def cut_ExactlyOneLooseEleLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==1: 
          return True
        return False

    def cut_ExactlyOneTightEleMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==1: 
          return True
        return False

    def cut_ExactlyZeroTightEleMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==0: 
          return True
        return False

    def cut_AtLeastOneLooseEleLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)>0: 
          return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2: 
          return True
        return False

    def cut_AtLeastTwoLooseEleLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)>1: 
          return True
        return False

    def cut_AtLeastTwoLooseMuons(self):
        muons = self.store['muons']
        if len(muons)>1: 
          return True
        return False

    def cut_OneOrTwoEmus90GeV(self):
      leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
      if not ( 2 <= len(leptons) <= 4):
        return False 
      SSEmu = 0
      for pair in itertools.combinations(leptons,2):
        if pair[0].trkcharge * pair[1].trkcharge > 0 and pair[0].m != pair[1].m:
          if (pair[0].tlv + pair[1].tlv).M() >= 90*GeV :
            SSEmu += 1
      if SSEmu in [1,2]:
        return True
      return False

    def cut_TwoOrThreeElectronsOneSS200GeV(self):
        electronsL = self.store['electrons_loose_LooseLLH']
        electronsT = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electronsL)==2 and len(electronsT)==2:
          for pair in itertools.combinations(electronsL,2):
            if pair[0].trkcharge == pair[1].trkcharge : 
              if (pair[0].tlv + pair[1].tlv).M() > 200*GeV:
                return True
        elif len(electronsL)==3 and len(electronsT)==3:
          NSS = 0
          SS200 = False
          for pair in itertools.combinations(electronsL,2):
            if pair[0].trkcharge == pair[1].trkcharge :
              NSS += 1
              if (pair[0].tlv + pair[1].tlv).M() > 200*GeV:
                SS200 = True
          if NSS==1 and SS200:
            return True
        return False

    def cut_LooseEleVetoCrack(self):
        electrons = self.store['electrons_loose_LooseLLH']
        for ele in electrons:
          if 1.37 < abs(ele.tlv.Eta()) < 1.52:
            return False
        return True

    def cut_NoStrictlyLooseEleTwoOrThreeTight(self):
        electrons = self.store['electrons_loose_LooseLLH']
        ntight = 0
        for ele in electrons:
          if not (ele.isIsolated_Loose and ele.LHMedium):
            return False
          else:
            ntight += 1
        if ntight in [2,3]:
          return True
        return False

    def cut_NotNoStrictlyLooseEleTwoOrThreeTight(self):
        electrons = self.store['electrons_loose_LooseLLH']
        ntight = 0
        for ele in electrons:
          if (ele.isIsolated_Loose and ele.LHMedium):
            ntight += 1
        if len(electrons) in [2,3] and ntight < len(electrons):
          return True
        return False

    def cut_NoStrictlyLooseEle(self):
        electrons = self.store['electrons_loose_LooseLLH']
        for ele in electrons:
          if not (ele.isIsolated_Loose and ele.LHMedium):
            return False
        return True

    def cut_NoStrictlyLooseLep(self):
        leptons_tight = self.store['electrons_tight_MediumLLH_isolLoose'] + self.store['muons_tight']
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if len(leptons_tight) == len(leptons):
          return True
        return False

    def cut_NotNoStrictlyLooseLep(self):
        leptons_tight = self.store['electrons_tight_MediumLLH_isolLoose'] + self.store['muons_tight']
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if len(leptons_tight) == len(leptons):
          return False
        return True

    def cut_NotNoStrictlyLooseEle(self):
        electrons = self.store['electrons_loose_LooseLLH']
        ntight = 0
        for ele in electrons:
          if (ele.isIsolated_Loose and ele.LHMedium):
            ntight += 1
        if ntight < len(electrons):
          return True
        return False

    def cut_ExactlyThreeLooseEleLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==3: 
          return True
        return False

    def cut_ExactlyThreeLooseLep(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if len(leptons)==3: 
          return True
        return False

    def cut_ExactlyTwoTightEleMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==2: 
          return True
        return False

    def cut_ExactlyThreeLooseEleLooseLLHOSZmass(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if not len(electrons)==3: 
          return False
        OSPairZmass = 0
        OS2PairMass = 0
        for pair in itertools.combinations(electrons,2):
          if pair[0].trkcharge != pair[1].trkcharge : 
            if abs( (pair[0].tlv + pair[1].tlv).M() - g_mZ) <= 10*GeV:
              OSPairZmass += 1
            elif 20. < (pair[0].tlv + pair[1].tlv).M()/GeV < 300.:
              OS2PairMass += 1
        # if OSPairZmass == 1 and OS2PairMass == 1:
        if OSPairZmass>0:
          return True
        return False

    def cut_ExactlyThreeLooseLepOSZmass(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if not len(leptons)==3: 
          return False
        OSPairZmass = 0
        for pair in itertools.combinations(leptons,2):
          if pair[0].trkcharge != pair[1].trkcharge : 
            if abs( (pair[0].tlv + pair[1].tlv).M() - g_mZ) <= 10*GeV and (pair[0].m == pair[1].m):
              OSPairZmass += 1
        if OSPairZmass>0:
          return True
        return False

    def cut_ExactlyThreeLooseEleLooseLLHOSZVeto(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if not len(electrons)==3: 
          return False
        OSPairZmass = 0
        OS2PairMass = 0
        for pair in itertools.combinations(electrons,2):
          if pair[0].trkcharge != pair[1].trkcharge : 
            if abs( (pair[0].tlv + pair[1].tlv).M() - g_mZ) <= 10*GeV:
              OSPairZmass += 1
            elif 20. < (pair[0].tlv + pair[1].tlv).M()/GeV < 300.:
              OS2PairMass += 1
        # if OSPairZmass == 1 and OS2PairMass == 1:
        if OSPairZmass==0:
          return True
        return False

    def cut_LooseEleLooseLLHOSZVeto(self):
        electrons = self.store['electrons_loose_LooseLLH']
        for pair in itertools.combinations(electrons,2):
          if pair[0].trkcharge != pair[1].trkcharge : 
            if abs( (pair[0].tlv + pair[1].tlv).M() - g_mZ) <= 10*GeV:
              return False
        return True

    def cut_ExactlyThreeLooseEleLooseLLH1SS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if not len(electrons)==3: 
          return False
        SSPair = 0
        for pair in itertools.combinations(electrons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            SSPair += 1
        if SSPair == 1:
          return True
        return False

    def cut_ExactlyThreeLooseEleLooseLLHSS90M200(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if not len(electrons)==3: 
          return False
        SSPair = 0
        SSPairMass = 0
        for pair in itertools.combinations(electrons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            SSPair += 1
            SSPairMass = (pair[0].tlv + pair[1].tlv).M()
        if SSPair == 1 and (90*GeV < SSPairMass < 200*GeV):
          return True
        return False

    def cut_ExactlyThreeLeptonsSS90M200(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if not len(leptons)==3: 
          return False
        SSPair = 0
        SSPairMass = 0
        for pair in itertools.combinations(leptons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            SSPair += 1
            SSPairMass = (pair[0].tlv + pair[1].tlv).M()
        if SSPair == 1 and (90*GeV < SSPairMass < 200*GeV):
          return True
        return False

    def cut_ExactlyThreeLeptonsSS60M200(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if not len(leptons)==3: 
          return False
        SSPair = 0
        SSPairMass = 0
        for pair in itertools.combinations(leptons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            SSPair += 1
            SSPairMass = (pair[0].tlv + pair[1].tlv).M()
        if SSPair == 1 and (60*GeV < SSPairMass < 200*GeV):
          return True
        return False

    def cut_ExactlyThreeLooseEleLooseLLHSS200M(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if not len(electrons)==3: 
          return False
        SSPair = 0
        SSPairMass = 0
        for pair in itertools.combinations(electrons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            SSPair += 1
            SSPairMass = (pair[0].tlv + pair[1].tlv).M()
        if SSPair == 1 and SSPairMass > 200*GeV:
          return True
        return False

    def cut_ExactlyThreeLooseLepSS200M(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if not len(leptons)==3: 
          return False
        SSPair = 0
        SSPairMass = 0
        for pair in itertools.combinations(leptons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            SSPair += 1
            SSPairMass = (pair[0].tlv + pair[1].tlv).M()
        if SSPair == 1 and SSPairMass > 200*GeV:
          return True
        return False

    def cut_LooseEleLooseLLHSS200M(self):
        electrons = self.store['electrons_loose_LooseLLH']
        SSPair = 0
        SSPairMass = 0
        for pair in itertools.combinations(electrons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            if (pair[0].tlv + pair[1].tlv).M() < 200*GeV:
              return False
            SSPair += 1
        if SSPair in [1,2]:
          return True
        return False

    def cut_LooseLepSS200M(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        SSPair = 0
        SSPairMass = 0
        for pair in itertools.combinations(leptons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            if (pair[0].tlv + pair[1].tlv).M() < 200*GeV:
              return False
            SSPair += 1
        if SSPair in [1,2]:
          return True
        return False

    def cut_ExactlyThreeTightLep(self):
        leptons = self.store['electrons_tight_MediumLLH_isolLoose'] + self.store['muons_tight']
        if len(leptons)==3: 
          return True
        return False

    def cut_FailExactlyThreeTightLep(self):
        leptons = self.store['electrons_tight_MediumLLH_isolLoose'] + self.store['muons_tight']
        if len(leptons)==3: 
          return False
        return True

    def cut_ExactlyThreeTightEleMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==3: 
          return True
        return False

    def cut_FailExactlyThreeTightEleMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==3: 
          return False
        return True

    def cut_NotExactlyTwoTightEleMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==2: 
          return False
        return True

    def cut_ExactlyTwoTightLeptons(self):
        leptons = self.store['electrons_tight_MediumLLH_isolLoose'] + self.store["muons_tight"]
        if len(leptons)==2: 
          return True
        return False

    def cut_NotExactlyTwoTightLeptons(self):
        leptons = self.store['electrons_tight_MediumLLH_isolLoose'] + self.store["muons_tight"]
        if len(leptons)==2: 
          return False
        return True

    def cut_ExactlyTwoLooseEleLooseLLHTL(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if electrons[0].isIsolated_Loose and electrons[0].LHMedium and not (electrons[1].isIsolated_Loose and electrons[1].LHMedium):
            return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHLT(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if electrons[1].isIsolated_Loose and electrons[1].LHMedium and not (electrons[0].isIsolated_Loose and electrons[0].LHMedium):
            return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHLL(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if not (electrons[0].isIsolated_Loose and electrons[0].LHMedium) and not (electrons[1].isIsolated_Loose and electrons[1].LHMedium):
            return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHTLOS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if electrons[0].isIsolated_Loose and electrons[0].LHMedium and not (electrons[1].isIsolated_Loose and electrons[1].LHMedium):
            if electrons[0].trkcharge*electrons[1].trkcharge == -1:
              return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHLTOS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if electrons[1].isIsolated_Loose and electrons[1].LHMedium and not (electrons[0].isIsolated_Loose and electrons[0].LHMedium):
            if electrons[0].trkcharge*electrons[1].trkcharge == -1:
              return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHLLOS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if not (electrons[0].isIsolated_Loose and electrons[0].LHMedium) and not (electrons[1].isIsolated_Loose and electrons[1].LHMedium):
            if electrons[0].trkcharge*electrons[1].trkcharge == -1:
              return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHTLSS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if electrons[0].isIsolated_Loose and electrons[0].LHMedium and not (electrons[1].isIsolated_Loose and electrons[1].LHMedium):
            if electrons[0].trkcharge*electrons[1].trkcharge == 1:
              return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHLTSS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if electrons[1].isIsolated_Loose and electrons[1].LHMedium and not (electrons[0].isIsolated_Loose and electrons[0].LHMedium):
            if electrons[0].trkcharge*electrons[1].trkcharge == 1:
              return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHLLSS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2:
          if not (electrons[0].isIsolated_Loose and electrons[0].LHMedium) and not (electrons[1].isIsolated_Loose and electrons[1].LHMedium):
            if electrons[0].trkcharge*electrons[1].trkcharge == 1:
              return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHOS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2: 
          if electrons[0].trkcharge*electrons[1].trkcharge == -1: return True
        return False

    def cut_ExactlyTwoLooseEleLooseLLHSS(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2: 
          if electrons[0].trkcharge*electrons[1].trkcharge == 1: return True
        return False

    def cut_ExactlyTwoLooseMuonSS(self):
        muons = self.store['muons']
        if len(muons)==2: 
          if muons[0].trkcharge*muons[1].trkcharge == 1: return True
        return False

    def cut_ExactlyTwoLooseLeptons(self):
        leptons = self.store['muons'] + self.store['electrons_loose_LooseLLH']
        if len(leptons)==2:
          assert leptons[0].trkcharge*leptons[1].trkcharge == 1 and leptons[0].m!=leptons[1].m, "OneOrTwoEmus90GeV not working !!"
          if leptons[0].trkcharge*leptons[1].trkcharge == 1: return True
        return False

    def cut_SameSignLooseElePtZ100(self):
        electrons = self.store['electrons_loose_LooseLLH']
        SSPair = 0
        for pair in itertools.combinations(electrons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            if (pair[0].tlv+pair[1].tlv).Pt() < 100*GeV:
              return False
            SSPair += 1
        if SSPair in [1,2]:
          return True
        return False

    def cut_SameSignLooseLepPtZ100(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        SSPair = 0
        for pair in itertools.combinations(leptons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            if (pair[0].tlv+pair[1].tlv).Pt() < 100*GeV:
              return False
            SSPair += 1
        if SSPair in [1,2]:
          return True
        return False

    def cut_SameSignLooseEleDR4(self):
        electrons = self.store['electrons_loose_LooseLLH']
        SSPair = 0
        SSPairPass = 0
        for pair in itertools.combinations(electrons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            SSPair += 1
            if pair[0].tlv.DeltaR(pair[1].tlv) < 4.0:
              SSPairPass += 1
        if SSPair == 1 and SSPairPass == 1:
          return True
        return False

    def cut_SameSignLooseEleDR35(self):
        electrons = self.store['electrons_loose_LooseLLH']
        SSPair = 0
        for pair in itertools.combinations(electrons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            if not pair[0].tlv.DeltaR(pair[1].tlv) < 3.5:
              return False
            SSPair += 1
        if SSPair in [1,2]:
          return True
        return False

    def cut_SameSignLooseLepDR35(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        SSPair = 0
        for pair in itertools.combinations(leptons,2):
          if (pair[0].trkcharge * pair[1].trkcharge) > 0.5 : 
            if not pair[0].tlv.DeltaR(pair[1].tlv) < 3.5:
              return False
            SSPair += 1
        if SSPair in [1,2]:
          return True
        return False

    def cut_LooseEleHT300(self):
        electrons = self.store['electrons_loose_LooseLLH']
        HT = 0
        for ele in electrons:
          HT += ele.tlv.Pt()
        if HT > 300*GeV:
          return True
        return False

    def cut_LooseLepHT300(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        HT = 0
        for ele in leptons:
          HT += ele.tlv.Pt()
        if HT > 300*GeV:
          return True
        return False
 
    def cut_ExactlyTwoTightEleMediumLLHisolLooseOS(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==2: 
          if electrons[0].trkcharge*electrons[1].trkcharge == -1: return True
        return False

    def cut_ExactlyTwoTightEleMediumLLHisolLooseSS(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==2: 
          if electrons[0].trkcharge*electrons[1].trkcharge == 1: return True
        return False

    def cut_ZMassWindowMediumLLHisolLooseNominal(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = 91*GeV
        if len(electrons)==2 :
          if abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) < 14.0*GeV:
            return True;
        return False

    def cut_ZMassWindowMediumLLHisolLooseSidebandNominal(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = 91*GeV
        if len(electrons)==2 :
          if (abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) > 14.0*GeV) and (abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) < 28.0*GeV):
            return True;
        return False

    def cut_ZMassWindowMediumLLHisolLooseSSNominal(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = 89*GeV # 2 GeV shift for the SS Z peak
        if len(electrons)==2 :
          if abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) < 15.8*GeV:
            return True;
        return False

    def cut_ZMassWindowMediumLLHisolLooseSSSidebandNominal(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = 89*GeV # 2 GeV shift for the SS Z peak
        if len(electrons)==2 :
          if (abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) > 15.8*GeV) and (abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) < 31.6*GeV):
            return True;
        return False

    def cut_ZMassWindowMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = 91.1876*GeV
        if len(electrons)==2 :
          if abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) < 15*GeV:
            return True;
        return False

    def cut_ZMassWindowMediumLLHisolLooseSS(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = (91.1876-2.0)*GeV # 2 GeV shift for the SS Z peak
        if len(electrons)==2 :
          if abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) < 15*GeV:
            return True;
        return False

    def cut_ZMassWindowMediumLLHisolLooseSideband(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = 91.1876*GeV
        if len(electrons)==2 :
          if (abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) > 15*GeV) and (abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) < 30*GeV):
            return True;
        return False

    def cut_ZMassWindowMediumLLHisolLooseSSSideband(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = (91.1876-2.0)*GeV # 2 GeV shift for the SS Z peak
        if len(electrons)==2 :
          if (abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) > 15*GeV) and (abs( (electrons[0].tlv + electrons[1].tlv).M() - mZ) < 30*GeV):
            return True;
        return False

    def cut_ZMassWindowMediumLLHisolLooseWide(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        mZ = 91.1876*GeV
        if len(electrons)==2 :
          if (electrons[0].tlv + electrons[1].tlv).M() < 5000*GeV:
            if (electrons[0].tlv + electrons[1].tlv).M() > 0*GeV:
              return True;
        return False

    def cut_Mass130GeVMediumLLHisolLoose(self):
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)==2 :
          if (electrons[0].tlv + electrons[1].tlv).M() > 130*GeV:
            return True;
        return False

    def cut_Mass130GeVLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2 :
          if (electrons[0].tlv + electrons[1].tlv).M() > 130*GeV:
            return True;
        return False

    def cut_Mass130GeV300LooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2 :
          tempMass = (electrons[0].tlv + electrons[1].tlv).M()
          if tempMass > 130*GeV and tempMass < 300*GeV :
            return True;
        return False

    def cut_Mass300GeV1200LooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2 :
          tempMass = (electrons[0].tlv + electrons[1].tlv).M()
          if tempMass > 300*GeV and tempMass < 1200*GeV :
            return True;
        return False

    def cut_Mass1200GeVLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2 :
          tempMass = (electrons[0].tlv + electrons[1].tlv).M()
          if tempMass > 1200*GeV :
            return True;
        return False

    def cut_Mass130GeV200LooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2 :
          tempMass = (electrons[0].tlv + electrons[1].tlv).M()
          if tempMass > 130*GeV and tempMass < 200*GeV :
            return True
        return False

    def cut_Mass130GeV200Leptons(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if len(leptons)==2 :
          tempMass = (leptons[0].tlv + leptons[1].tlv).M()
          if tempMass > 130*GeV and tempMass < 200*GeV :
            return True
        return False

    def cut_Mass60GeV200Leptons(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if len(leptons)==2 :
          tempMass = (leptons[0].tlv + leptons[1].tlv).M()
          if tempMass > 60*GeV and tempMass < 200*GeV :
            return True
        return False

    def cut_Mass200GeVLooseLLH(self):
        electrons = self.store['electrons_loose_LooseLLH']
        if len(electrons)==2 :
          tempMass = (electrons[0].tlv + electrons[1].tlv).M()
          if tempMass > 200*GeV:
            return True
        return False

    def cut_Mass200GeVLooseLep(self):
        leptons = self.store['electrons_loose_LooseLLH'] + self.store['muons']
        if len(leptons)==2 :
          tempMass = (leptons[0].tlv + leptons[1].tlv).M()
          if tempMass > 200*GeV:
            return True
        return False

    #----- exactly two prompt
    def cut_ExactlyTwoTightEleMediumLLHisolLooseBothPrompt(self):
        if not self.sampletype == "mc" : return False
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)!=2 : return False
        elif electrons[0].electronType() == 1 and electrons[1].electronType() == 1 : return True
        else : return False

    #----- one prompt + charge-flip type 1
    def cut_ExactlyTwoTightEleMediumLLHisolLoosePromptAndCHF1(self):
        if not self.sampletype == "mc" : return False
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)!=2 : return False
        elif electrons[0].electronType() == 1 and electrons[1].electronType() == 2 : return True
        elif electrons[1].electronType() == 1 and electrons[0].electronType() == 2 : return True
        else : return False

    #----- one prompt + charge-flip type 2
    def cut_ExactlyTwoTightEleMediumLLHisolLoosePromptAndCHF2(self):
        if not self.sampletype == "mc" : return False
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)!=2 : return False
        elif electrons[0].electronType() == 1 and electrons[1].electronType() == 3 : return True
        elif electrons[1].electronType() == 1 and electrons[0].electronType() == 3 : return True
        else : return False

    #----- 2 charge flip
    def cut_ExactlyTwoTightEleMediumLLHisolLooseBothCHF(self):
        if not self.sampletype == "mc" : return False
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)!=2 : return False
        elif electrons[0].electronType() in [2,3] and electrons[1].electronType() in [2,3] : return True
        else : return False

    #----- one prompt + brem
    def cut_ExactlyTwoTightEleMediumLLHisolLoosePromptAndBrem(self):
        if not self.sampletype == "mc" : return False
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)!=2 : return False
        elif electrons[0].electronType() == 1 and electrons[1].electronType() == 4 : return True
        elif electrons[1].electronType() == 1 and electrons[0].electronType() == 4 : return True
        else : return False

    #----- one prompt + FSR
    def cut_ExactlyTwoTightEleMediumLLHisolLoosePromptAndFSR(self):
        if not self.sampletype == "mc" : return False
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)!=2 : return False
        elif electrons[0].electronType() == 1 and electrons[1].electronType() == 5 : return True
        elif electrons[1].electronType() == 1 and electrons[0].electronType() == 5 : return True
        else : return False

    #----- one prompt + fake
    def cut_ExactlyTwoTightEleMediumLLHisolLoosePromptAndFake(self):
        if not self.sampletype == "mc" : return False
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)!=2 : return False
        elif electrons[0].electronType() == 1 and electrons[1].electronType() == 6 : return True
        elif electrons[1].electronType() == 1 and electrons[0].electronType() == 6 : return True
        else : return False

    #----- exactly two non-prompt
    def cut_ExactlyTwoTightEleMediumLLHisolLooseBothNonPrompt(self):
        if not self.sampletype == "mc" : return False
        electrons = self.store['electrons_tight_MediumLLH_isolLoose']
        if len(electrons)!=2 : return False
        elif electrons[0].electronType() != 1 and electrons[1].electronType() != 1 : return True
        else : return False

    #----- one or two b-jets
    def cut_OneOrTwoBjets(self):
        nbjets = 0
        jets = self.store['jets']
        for jet in jets:
          if jet.isFix77:
            nbjets += 1
        if nbjets in [1,2]:
          return True
        else:
          return False

    #----- b-veto
    def cut_bjetveto(self):
        nbjets = 0
        jets = self.store['jets']
        for jet in jets:
          if jet.isFix77:
            nbjets += 1
        if nbjets == 0:
          return True
        else:
          return False

    def cut_BadJetVeto(self):
        jets = self.store['jets']
        for jet in jets:
          if not jet.isClean:
            return False
        return True

    def cut_NoFakesInMC(self):
      electrons = self.store['electrons']
      if ("mc" not in self.sampletype):
        return True
      elif self.chain.mcChannelNumber in range(306538,306560):
        return True
      for ele in electrons:
        if ele.electronType() not in [1,2,3] :
          if ( ele.pt>30*GeV and ele.LHLoose and ele.trkd0sig<5.0 and abs(ele.trkz0sintheta)<0.5 ) :
            return False
      return True

    def cut_NoFakeMuonsInMC(self):
      muons = self.store['muons']
      if ("mc" not in self.sampletype):
        return True
      elif self.chain.mcChannelNumber in range(306538,306560):
        return True
      for mu in muons:
        if not mu.isTrueIsoMuon() :
          return False
      return True

    def cut_DCHAllElectron(self):
      if ("mc" not in self.sampletype):
        return True
      elif self.chain.mcChannelNumber not in range(306538,306560):
        return True
      pdgId_branchHL = []
      pdgId_branchHR = []
      for pdgId in self.chain.HLpp_Daughters: pdgId_branchHL += [pdgId]
      for pdgId in self.chain.HLmm_Daughters: pdgId_branchHL += [pdgId]
      for pdgId in self.chain.HRpp_Daughters: pdgId_branchHR += [pdgId]
      for pdgId in self.chain.HRmm_Daughters: pdgId_branchHR += [pdgId]
      assert len(pdgId_branchHL)==4 or len(pdgId_branchHR)==4, "less than 4 leptons.. something wrong"
      LallEle = True
      RallEle = True
      for pdgId in pdgId_branchHL:
        if abs(pdgId)!=11:
          LallEle = False
      for pdgId in pdgId_branchHR:
        if abs(pdgId)!=11:
          RallEle = False
      if RallEle or LallEle:
        return True
      return False

    def cut_DCHFilter(self):
      if ("mc" not in self.sampletype):
        return True
      elif self.chain.mcChannelNumber not in range(306538,306560):
        return True
      return False

    def cut_DCHFiltereeee(self):
      if ("mc" not in self.sampletype):
        return True
      elif self.chain.mcChannelNumber not in range(306538,306560):
        return False
      pdgId_branchHL = []
      pdgId_branchHR = []
      for pdgId in self.chain.HLpp_Daughters: pdgId_branchHL += [pdgId]
      for pdgId in self.chain.HLmm_Daughters: pdgId_branchHL += [pdgId]
      for pdgId in self.chain.HRpp_Daughters: pdgId_branchHR += [pdgId]
      for pdgId in self.chain.HRmm_Daughters: pdgId_branchHR += [pdgId]
      assert len(pdgId_branchHL)==4 or len(pdgId_branchHR)==4, "less than 4 leptons.. something wrong"
      if sum( [ abs(n) for n in pdgId_branchHL ] ) == 44 or sum( [ abs(n) for n in pdgId_branchHR ] ) == 44:
        return True
      return False

    def cut_DCHFiltermmmm(self):
      if ("mc" not in self.sampletype):
        return True
      elif self.chain.mcChannelNumber not in range(306538,306560):
        return False
      pdgId_branchHL = []
      pdgId_branchHR = []
      for pdgId in self.chain.HLpp_Daughters: pdgId_branchHL += [pdgId]
      for pdgId in self.chain.HLmm_Daughters: pdgId_branchHL += [pdgId]
      for pdgId in self.chain.HRpp_Daughters: pdgId_branchHR += [pdgId]
      for pdgId in self.chain.HRmm_Daughters: pdgId_branchHR += [pdgId]
      assert len(pdgId_branchHL)==4 or len(pdgId_branchHR)==4, "less than 4 leptons.. something wrong"
      if sum( [ abs(n) for n in pdgId_branchHL ] ) == 52 or sum( [ abs(n) for n in pdgId_branchHR ] ) == 52:
        return True
      return False

    def cut_DCHFiltereemm(self):
      if ("mc" not in self.sampletype):
        return False
      elif self.chain.mcChannelNumber not in range(306538,306560):
        return True
      if [abs(l) for l in self.chain.HLpp_Daughters]==[11,11] and [ abs(l) for l in self.chain.HLmm_Daughters]==[13,13] :
        return True
      elif [abs(l) for l in self.chain.HLpp_Daughters]==[13,13] and [abs(l) for l in self.chain.HLmm_Daughters]==[11,11] :
        return True
      elif [abs(l) for l in self.chain.HRpp_Daughters]==[11,11] and [abs(l) for l in self.chain.HRmm_Daughters]==[13,13] :
        return True
      elif [abs(l) for l in self.chain.HRpp_Daughters]==[13,13] and [abs(l) for l in self.chain.HRmm_Daughters]==[11,11] :
        return True
      return False

    def cut_DCHFilteremem(self):
      if ("mc" not in self.sampletype):
        return False
      elif self.chain.mcChannelNumber not in range(306538,306560):
        return True
      if len(self.chain.HLpp_Daughters) not in [0,1]:
        if self.chain.HLpp_Daughters[0] == self.chain.HLpp_Daughters[1]:
          return False
      if len(self.chain.HLmm_Daughters) not in [0,1]:
        if self.chain.HLmm_Daughters[0] == self.chain.HLmm_Daughters[1]:
          return False
      if len(self.chain.HRpp_Daughters) not in [0,1]:
        if self.chain.HRpp_Daughters[0] == self.chain.HRpp_Daughters[1]:
          return False
      if len(self.chain.HRmm_Daughters) not in [0,1]:
        if self.chain.HRmm_Daughters[0] == self.chain.HRmm_Daughters[1]:
          return False
      return True

    def cut_DCHFilteremmm(self):
      if ("mc" not in self.sampletype):
        return False
      elif self.chain.mcChannelNumber not in range(306538,306560):
        return True
      if sum([abs(l) for l in self.chain.HLpp_Daughters])==24 and sum([abs(l) for l in self.chain.HLmm_Daughters])==26 :
        return True
      elif sum([abs(l) for l in self.chain.HLpp_Daughters])==26 and sum([abs(l) for l in self.chain.HLmm_Daughters])==24 :
        return True
      elif sum([abs(l) for l in self.chain.HRpp_Daughters])==24 and sum([abs(l) for l in self.chain.HRmm_Daughters])==26 :
        return True
      elif sum([abs(l) for l in self.chain.HRpp_Daughters])==26 and sum([abs(l) for l in self.chain.HRmm_Daughters])==24 :
        return True
      return False


    #__________________________________________________________________________
    def cut_PASS(self):
      return True

    #__________________________________________________________________________
    def cut_DeltaMassOverMass(self):
      #Legend: 1 eeee, 2 mmmm, 3 emem, 4 eemm, 5 eeem, 6 mmem
      alpha = [0.09, 0.005, 0.003, 0.004, 0.007, 0.004]
      beta  = [0.74, 1.46,  1.47,  1.46,  1.30,  1.50 ]
      flavour = 0
      if self.store['fourLepFlavor'] in ["eeee"]: flavour = 0
      if self.store['fourLepFlavor'] in ["mmmm"]: flavour = 1
      if self.store['fourLepFlavor'] in ["emem"]: flavour = 2
      if self.store['fourLepFlavor'] in ["eemm","mmee"]: flavour = 3
      if self.store['fourLepFlavor'] in ["eeem","emee"]: flavour = 4
      if self.store['fourLepFlavor'] in ["mmem","emmm"]: flavour = 5
      mpos = self.store['mVis1'] 
      mneg = self.store['mVis2'] 
      massDiff = (mpos - mneg)/GeV
      mass     = (mpos + mneg)/(2*GeV)

      massCut = (abs(massDiff)/(alpha[flavour]*(pow(mass,beta[flavour]))))
      if(abs(massCut) < 3): return True
      return False

    #__________________________________________________________________________
    def cut_PassTriggersDLT(self):
      if self.sampletype == "mc" :
        runNumber = self.chain.rand_run_nr
      else :
        runNumber = self.chain.runNumber
      
      if runNumber < 290000. :
        trigchains={"HLT_2e17_lhloose","HLT_2mu14","HLT_e17_lhloose_nod0_mu14"}
        for i in xrange(self.chain.passedTriggers.size()):
          if self.chain.passedTriggers.at(i) in trigchains:
            return True
      else:
        trigchains={"HLT_2e17_lhloose","HLT_2mu14","HLT_e17_lhloose_nod0_mu14"}
        for i in xrange(self.chain.passedTriggers.size()):
            if self.chain.passedTriggers.at(i) in trigchains:
              return True
      return False

    #__________________________________________________________________________
    def cut_NoStrictlyLooseElectrons(self):
      if len(self.store["electrons_loose_LooseLLH"]) == len(self.store['electrons_tight_MediumLLH_isolLoose']):
        return True
      return False

    #__________________________________________________________________________
    def cut_FourTightLeptons(self):
      if (len(self.store["muons"]) + len(self.store['electrons_tight_MediumLLH_isolLoose']))==4:
        return True
      return False

    #__________________________________________________________________________
    def cut_FourLeptons(self):
      if (len(self.store["muons"]) + len(self.store['electrons_loose_LooseLLH']))==4:
        return True
      return False

    #__________________________________________________________________________
    def cut_EleTTTT(self):
      if len(self.store['electrons_tight_MediumLLH_isolLoose'])==4:
        return True
      return False

    #__________________________________________________________________________
    def cut_ZeroTotalCharge(self):
      electrons = self.store['electrons_loose_LooseLLH']
      muons     = self.store['muons']
      leptons = electrons + muons
      totalCharge=0.
      for l in leptons:
        totalCharge += l.trkcharge
      if(totalCharge==0):
        return True
      return False

    #__________________________________________________________________________
    def cut_TwoSSElectronPairs(self):
      if self.store["fourLepFlavor"] and self.store["fourLepFlavor"] in ["eeee"]:
        return True
      return False

    #__________________________________________________________________________
    def cut_TwoSSMuonPairs(self):
      if self.store["fourLepFlavor"] in ["mmmm"]:
        return True
      return False

    #__________________________________________________________________________
    def cut_TwoSSElectronMuonPairsEEMM(self):
      if self.store["fourLepFlavor"] in ["eemm","mmee"]:
        return True
      return False

    #__________________________________________________________________________
    def cut_TwoSSElectronMuonPairsEMEM(self):
      if self.store["fourLepFlavor"] in ["emem"]:
        return True
      return False

    #__________________________________________________________________________
    def cut_TwoSSElectronMuonPairsEEEM(self):
      if self.store["fourLepFlavor"] in ["eeem","emee"]:
        return True
      return False

    #__________________________________________________________________________
    def cut_TwoSSElectronMuonPairsMMEM(self):
      if self.store["fourLepFlavor"] in ["mmem","emmm"]:
        return True
      return False

    #____________________________________________________________________________
    def cut_IsSignalRegion2(self):
      posmass = self.store['mVis1']
      negmass = self.store['mVis2']

      if((posmass>200*GeV) and (negmass>200*GeV)):
        return True
      return False

    def cut_ZVeto(self):
      electrons = self.store['electrons_loose_LooseLLH']
      muons     = self.store['muons']
      leptons = electrons + muons
      for pair in itertools.combinations(leptons,2):
        if pair[0].trkcharge * pair[1].trkcharge < 0 and pair[0].m == pair[1].m:
          if abs( (pair[0].tlv + pair[1].tlv).M() - g_mZ) < 10*GeV:
            return False
      return True
    
#------------------------------------------------------------------------------
class PlotAlg(pyframe.algs.CutFlowAlg,CutAlg):
    """

    For making a set of standard plots after each cut in a cutflow.  PlotAlg
    inherets from CutAlg so all the functionality from CutAlg is available for
    applying selection. In addition you can apply weights at different points
    in the selection.

    The selection should be configured by specifying 'cut_flow' in the
    constructor as such:

    cut_flow = [
        ['Cut1', ['Weight1a','Weight1b'],
        ['Cut2', ['Weight2']],
        ['Cut3', None],
        ...
        ]

    The weights must be available in the store.

    'region' will set the name of the dir where the plots are saved

    Inhereting from CutFlowAlg provides the functionality to produce cutflow
    histograms that will be named 'cutflow_<region>' and 'cutflow_raw_<region>'

    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = 'PlotAlg',
                 region   = '',
                 obj_keys = [], # make cutflow hist for just this objects
                 cut_flow = None,
                 plot_all = True,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region,obj_keys=obj_keys)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow = cut_flow
        self.region   = region
        self.plot_all = plot_all
        self.obj_keys = obj_keys
    
    #_________________________________________________________________________
    def initialize(self):
        pyframe.algs.CutFlowAlg.initialize(self)
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            # obj cutflow is computed at the end of the cutflow
            #if len(list_cuts)==len(self.cut_flow):
            if self.obj_keys:
             for k in self.obj_keys:
              for o in self.store[k]:
               if hasattr(o,"cdict") and hasattr(o,"wdict"):
                obj_passed = True
                obj_weight = 1.0
                if list_weights:
                 for w in list_weights:
                  if w.startswith("MuPairs"):
                   obj_weight *= o.GetWeight(w) 
                for c in list_cuts:
                 if c.startswith("MuPairs"):
                  obj_passed = o.HasPassedCut(c) and obj_passed
                self.hists[self.region+"_"+k].count_if(obj_passed and passed, c, obj_weight * weight)
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               #if passed:             
               self.plot(region, passed, list_cuts, cut, list_weights=list_weights, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):
        
        # should probably make this configurable
        ## get event candidate
        muons      = self.store['muons'] 
        electrons  = self.store['electrons']
        if bool(len(muons)): mu_lead    = muons[0]
        if bool(len(electrons)): el_lead    = electrons[0]
        #mu_sublead = muons[1]
        jets       = self.store['jets']
        #jet_lead   = jets[0]
        
        met_trk    = self.store['met_trk']
        met_clus   = self.store['met_clus']
        #mupairs    = self.store['mu_pairs']
        
        ## plot directories
        EVT    = os.path.join(region, 'event')
        MUONS  = os.path.join(region, 'muons')
        MET    = os.path.join(region, 'met')
        JETS   = os.path.join(region, 'jets')
        ELECTRONS = os.path.join(region, 'electrons')
        #PAIRS  = os.path.join(region, 'pairs')
        
        # -----------------
        # Create histograms
        # -----------------
        ## event plots
        self.h_averageIntPerXing = self.hist('h_averageIntPerXing', "ROOT.TH1F('$', ';averageInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_actualIntPerXing = self.hist('h_actualIntPerXing', "ROOT.TH1F('$', ';actualInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_NPV = self.hist('h_NPV', "ROOT.TH1F('$', ';NPV;Events', 35, 0., 35.0)", dir=EVT)
        self.h_nmuons = self.hist('h_nmuons', "ROOT.TH1F('$', ';N_{#mu};Events', 8, 0, 8)", dir=EVT)
        self.h_nelectrons = self.hist('h_nelectrons', "ROOT.TH1F('$', ';N_{e};Events', 8, 0, 8)", dir=EVT)
        self.h_njets = self.hist('h_njets', "ROOT.TH1F('$', ';N_{jet};Events', 8, 0, 8)", dir=EVT)
        #self.h_nmuonpairs = self.hist('h_nmuonpairs', "ROOT.TH1F('$', ';N_{#mu#mu};Events ', 8, 0, 8)", dir=EVT)
             
        #self.h_muons_chargeprod = self.hist('h_muons_chargeprod', "ROOT.TH1F('$', ';q(#mu_{lead}) #timesq (#mu_{sublead});Events ', 4, -2,2)", dir=EVT)
        #self.h_muons_dphi = self.hist('h_muons_dphi', "ROOT.TH1F('$', ';#Delta#phi(#mu_{lead},#mu_{sublead});Events ', 64, -3.2, 3.2)", dir=EVT)
        #self.h_muons_deta = self.hist('h_muons_deta', "ROOT.TH1F('$', ';#Delta#eta(#mu_{lead},#mu_{sublead});Events ', 50, -2.5, 2.5)", dir=EVT)
        #self.h_muons_mVis = self.hist('h_muons_mVis', "ROOT.TH1F('$', ';m_{vis}(#mu_{lead},#mu_{sublead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.)", dir=EVT)
        #self.h_muons_mTtot = self.hist('h_muons_mTtot', "ROOT.TH1F('$', ';m^{tot}_{T}(#mu_{lead},#mu_{sublead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.)", dir=EVT)
             
        self.h_mujet_dphi = self.hist('h_mujet_dphi', "ROOT.TH1F('$', ';#Delta#phi(#mu_{lead},jet_{lead});Events ', 64, -3.2, 3.2)", dir=EVT)
        self.h_scdphi = self.hist('h_scdphi', "ROOT.TH1F('$', ';#Sigma cos#Delta#phi;Events ', 400, -2., 2.)", dir=EVT)
        self.h_MuMuInvariantMass = self.hist('h_MuMuInvariantMass', "ROOT.TH1F('$', ';M_{#mu#mu};Events / (1 GeV)', 50, 0.0, 200000.0)", dir=EVT)
        self.h_ElElInvariantMass = self.hist('h_ElElInvariantMass', "ROOT.TH1F('$', ';M_{ee};Events / (1 GeV)', 50, 0.0, 200000.0)", dir=EVT)
        
        ## jets plots
        self.h_jetlead_pt = self.hist('h_jetlead_pt', "ROOT.TH1F('$', ';p_{T}(jet_{lead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=JETS)


        ## muon plots
        # leading
        self.h_mulead_pt = self.hist('h_mulead_pt', "ROOT.TH1F('$', ';p_{T}(#mu_{lead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MUONS)
        self.h_mulead_eta = self.hist('h_mulead_eta', "ROOT.TH1F('$', ';#eta(#mu_{lead});Events / (0.1)', 50, -2.5, 2.5)", dir=MUONS)
        self.h_mulead_phi = self.hist('h_mulead_phi', "ROOT.TH1F('$', ';#phi(#mu_{lead});Events / (0.1)', 64, -3.2, 3.2)", dir=MUONS)
        self.h_mulead_trkd0 = self.hist('h_mulead_trkd0', "ROOT.TH1F('$', ';d^{trk}_{0}(#mu_{lead}) [mm];Events / (0.01)', 80, -0.4, 0.4)", dir=MUONS)
        self.h_mulead_trkd0sig = self.hist('h_mulead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(#mu_{lead});Events / (0.1)', 100, 0., 10.)", dir=MUONS)
        self.h_mulead_trkz0 = self.hist('h_mulead_trkz0', "ROOT.TH1F('$', ';z^{trk}_{0}(#mu_{lead}) [mm];Events / (0.1)', 40, -2, 2)", dir=MUONS)
        self.h_mulead_trkz0sintheta = self.hist('h_mulead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(#mu_{lead}) [mm];Events / (0.01)', 200, -1, 1)", dir=MUONS)
              
        self.h_mulead_topoetcone20 = self.hist('h_mulead_topoetcone20', "ROOT.TH1F('$', ';topoetcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_mulead_topoetcone30 = self.hist('h_mulead_topoetcone30', "ROOT.TH1F('$', ';topoetcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_mulead_topoetcone40 = self.hist('h_mulead_topoetcone40', "ROOT.TH1F('$', ';topoetcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_mulead_ptvarcone20 = self.hist('h_mulead_ptvarcone20', "ROOT.TH1F('$', ';ptvarcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_mulead_ptvarcone30 = self.hist('h_mulead_ptvarcone30', "ROOT.TH1F('$', ';ptvarcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_mulead_ptvarcone40 = self.hist('h_mulead_ptvarcone40', "ROOT.TH1F('$', ';ptvarcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
              
        self.h_mulead_ptcone20 = self.hist('h_mulead_ptcone20', "ROOT.TH1F('$', ';ptcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_mulead_ptcone30 = self.hist('h_mulead_ptcone30', "ROOT.TH1F('$', ';ptcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_mulead_ptcone40 = self.hist('h_mulead_ptcone40', "ROOT.TH1F('$', ';ptcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        
        
        # subleading
        """
        self.h_musublead_pt = self.hist('h_musublead_pt', "ROOT.TH1F('$', ';p_{T}(#mu_{sublead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MUONS)
        self.h_musublead_eta = self.hist('h_musublead_eta', "ROOT.TH1F('$', ';#eta(#mu_{sublead});Events / (0.1)', 50, -2.5, 2.5)", dir=MUONS)
        self.h_musublead_phi = self.hist('h_musublead_phi', "ROOT.TH1F('$', ';#phi(#mu_{sublead});Events / (0.1)', 64, -3.2, 3.2)", dir=MUONS)
        self.h_musublead_trkd0 = self.hist('h_musublead_trkd0', "ROOT.TH1F('$', ';d^{trk}_{0}(#mu_{sublead}) [mm];Events / (0.01)', 80, -0.4, 0.4)", dir=MUONS)
        self.h_musublead_trkd0sig = self.hist('h_musublead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(#mu_{sublead});Events / (0.1)', 100, 0., 10.)", dir=MUONS)
        self.h_musublead_trkz0 = self.hist('h_musublead_trkz0', "ROOT.TH1F('$', ';z^{trk}_{0}(#mu_{sublead}) [mm];Events / (0.1)', 40, -2, 2)", dir=MUONS)
        self.h_musublead_trkz0sintheta = self.hist('h_musublead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(#mu_{sublead}) [mm];Events / (0.01)', 200, -1, 1)", dir=MUONS)
              
        self.h_musublead_topoetcone20 = self.hist('h_musublead_topoetcone20', "ROOT.TH1F('$', ';topoetcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_topoetcone30 = self.hist('h_musublead_topoetcone30', "ROOT.TH1F('$', ';topoetcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_topoetcone40 = self.hist('h_musublead_topoetcone40', "ROOT.TH1F('$', ';topoetcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone20 = self.hist('h_musublead_ptvarcone20', "ROOT.TH1F('$', ';ptvarcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone30 = self.hist('h_musublead_ptvarcone30', "ROOT.TH1F('$', ';ptvarcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone40 = self.hist('h_musublead_ptvarcone40', "ROOT.TH1F('$', ';ptvarcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
              
        self.h_musublead_ptcone20 = self.hist('h_musublead_ptcone20', "ROOT.TH1F('$', ';ptcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptcone30 = self.hist('h_musublead_ptcone30', "ROOT.TH1F('$', ';ptcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptcone40 = self.hist('h_musublead_ptcone40', "ROOT.TH1F('$', ';ptcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        
        """ 
        ##Electron plots
        self.h_ellead_pt = self.hist('h_ellead_pt', "ROOT.TH1F('$', ';p_{T}(#mu_{lead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_ellead_eta = self.hist('h_ellead_eta', "ROOT.TH1F('$', ';#eta(#mu_{lead});Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_ellead_phi = self.hist('h_ellead_phi', "ROOT.TH1F('$', ';#phi(#mu_{lead});Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_ellead_trkd0 = self.hist('h_ellead_trkd0', "ROOT.TH1F('$', ';d^{trk}_{0}(#mu_{lead}) [mm];Events / (0.01)', 80, -0.4, 0.4)", dir=ELECTRONS)
        self.h_ellead_trkd0sig = self.hist('h_ellead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(#mu_{lead});Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_ellead_trkz0 = self.hist('h_ellead_trkz0', "ROOT.TH1F('$', ';z^{trk}_{0}(#mu_{lead}) [mm];Events / (0.1)', 40, -2, 2)", dir=ELECTRONS)
        self.h_ellead_trkz0sintheta = self.hist('h_ellead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(#mu_{lead}) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
              
        self.h_ellead_topoetcone20 = self.hist('h_ellead_topoetcone20', "ROOT.TH1F('$', ';topoetcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_topoetcone30 = self.hist('h_ellead_topoetcone30', "ROOT.TH1F('$', ';topoetcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_topoetcone40 = self.hist('h_ellead_topoetcone40', "ROOT.TH1F('$', ';topoetcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptvarcone20 = self.hist('h_ellead_ptvarcone20', "ROOT.TH1F('$', ';ptvarcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptvarcone30 = self.hist('h_ellead_ptvarcone30', "ROOT.TH1F('$', ';ptvarcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptvarcone40 = self.hist('h_ellead_ptvarcone40', "ROOT.TH1F('$', ';ptvarcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
              
        self.h_ellead_ptcone20 = self.hist('h_ellead_ptcone20', "ROOT.TH1F('$', ';ptcone20/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptcone30 = self.hist('h_ellead_ptcone30', "ROOT.TH1F('$', ';ptcone30/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        self.h_ellead_ptcone40 = self.hist('h_ellead_ptcone40', "ROOT.TH1F('$', ';ptcone40/p_{T}(#mu_{lead}); Events / 0.001', 10000, 0.0, 10.0)", dir=ELECTRONS)
        
        
        # subleading
        """
        self.h_musublead_pt = self.hist('h_musublead_pt', "ROOT.TH1F('$', ';p_{T}(#mu_{sublead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MUONS)
        self.h_musublead_eta = self.hist('h_musublead_eta', "ROOT.TH1F('$', ';#eta(#mu_{sublead});Events / (0.1)', 50, -2.5, 2.5)", dir=MUONS)
        self.h_musublead_phi = self.hist('h_musublead_phi', "ROOT.TH1F('$', ';#phi(#mu_{sublead});Events / (0.1)', 64, -3.2, 3.2)", dir=MUONS)
        self.h_musublead_trkd0 = self.hist('h_musublead_trkd0', "ROOT.TH1F('$', ';d^{trk}_{0}(#mu_{sublead}) [mm];Events / (0.01)', 80, -0.4, 0.4)", dir=MUONS)
        self.h_musublead_trkd0sig = self.hist('h_musublead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(#mu_{sublead});Events / (0.1)', 100, 0., 10.)", dir=MUONS)
        self.h_musublead_trkz0 = self.hist('h_musublead_trkz0', "ROOT.TH1F('$', ';z^{trk}_{0}(#mu_{sublead}) [mm];Events / (0.1)', 40, -2, 2)", dir=MUONS)
        self.h_musublead_trkz0sintheta = self.hist('h_musublead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(#mu_{sublead}) [mm];Events / (0.01)', 200, -1, 1)", dir=MUONS)
              
        self.h_musublead_topoetcone20 = self.hist('h_musublead_topoetcone20', "ROOT.TH1F('$', ';topoetcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_topoetcone30 = self.hist('h_musublead_topoetcone30', "ROOT.TH1F('$', ';topoetcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_topoetcone40 = self.hist('h_musublead_topoetcone40', "ROOT.TH1F('$', ';topoetcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone20 = self.hist('h_musublead_ptvarcone20', "ROOT.TH1F('$', ';ptvarcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone30 = self.hist('h_musublead_ptvarcone30', "ROOT.TH1F('$', ';ptvarcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptvarcone40 = self.hist('h_musublead_ptvarcone40', "ROOT.TH1F('$', ';ptvarcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
              
        self.h_musublead_ptcone20 = self.hist('h_musublead_ptcone20', "ROOT.TH1F('$', ';ptcone20/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptcone30 = self.hist('h_musublead_ptcone30', "ROOT.TH1F('$', ';ptcone30/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        self.h_musublead_ptcone40 = self.hist('h_musublead_ptcone40', "ROOT.TH1F('$', ';ptcone40/p_{T}(#mu_{sublead}); Events / 0.001', 10000, 0.0, 10.0)", dir=MUONS)
        """

        ## met plots
        self.h_met_clus_et = self.hist('h_met_clus_et', "ROOT.TH1F('$', ';E^{miss}_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_clus_phi = self.hist('h_met_clus_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(clus));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_trk_et = self.hist('h_met_trk_et', "ROOT.TH1F('$', ';E^{miss}_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_phi = self.hist('h_met_trk_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(trk));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_clus_sumet = self.hist('h_met_clus_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_sumet = self.hist('h_met_trk_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        
        ## muons pairs
        """
        self.h_mumu_mVis = self.hist('h_mumu_mVis', "ROOT.TH1F('$', ';m_{vis}(#mu#mu) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=PAIRS)
        self.h_mumu_mTtot = self.hist('h_mumu_mTtot', "ROOT.TH1F('$', ';m^{tot}_{T}(#mu#mu) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=PAIRS)
        self.h_mumu_angle = self.hist('h_mumu_angle', "ROOT.TH1F('$', ';#omega(#mu#mu);Events', 320, 0.0, 3.2)", dir=PAIRS)
        self.h_mumu_sumcosdphi = self.hist('h_mumu_sumcosdphi', "ROOT.TH1F('$', ';#Sigmacos#Delta#phi(#mu_{lead/sublead},E^{miss}_{T});Events / 0.1', 40, -2, 2)", dir=PAIRS)
        self.h_mumu_mulead_pt = self.hist('h_mumu_mulead_pt', "ROOT.TH1F('$', ';p_{T}(#mu#mu_{lead}) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=PAIRS)
        self.h_mumu_musublead_pt = self.hist('h_mumu_musublead_pt', "ROOT.TH1F('$', ';p_{T}(#mu#mu_{sublead}) [GeV];Events / (1 GeV)',2000,0.0,2000.0)",dir=PAIRS)
        self.h_mumu_mulead_eta = self.hist('h_mumu_mulead_eta', "ROOT.TH1F('$', ';#eta(#mu#mu_{lead});Events / (0.1)', 50, -2.5, 2.5)", dir=PAIRS)
        self.h_mumu_musublead_eta = self.hist('h_mumu_musublead_eta', "ROOT.TH1F('$', ';#eta(#mu#mu_{sublead});Events / (0.1)', 50, -2.5, 2.5)", dir=PAIRS)
        self.h_mumu_mulead_phi = self.hist('h_mumu_mulead_phi', "ROOT.TH1F('$', ';#phi(#mu#mu_{lead});Events / (0.1)', 64, -3.2, 3.2)", dir=PAIRS)
        self.h_mumu_musublead_phi = self.hist('h_mumu_musublead_phi', "ROOT.TH1F('$', ';#phi(#mu#mu_{sublead});Events / (0.1)', 64, -3.2, 3.2)", dir=PAIRS)
        """ 
        
        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          ## event plots
          self.h_averageIntPerXing.Fill(self.chain.averageInteractionsPerCrossing, weight)
          self.h_actualIntPerXing.Fill(self.chain.actualInteractionsPerCrossing, weight)
          self.h_NPV.Fill(self.chain.NPV, weight)
          self.h_nmuons.Fill(self.chain.nmuon, weight)
          self.h_nelectrons.Fill(self.chain.nel, weight)
          self.h_njets.Fill(self.chain.njets, weight)
          
          if bool(len(electrons)==2):
             a=self.store['ee_invM']
             self.h_ElElInvariantMass.Fill(a,weight)

          
          if bool(len(muons)==2):
            a=self.store['mumu_invM']
            #print "Invariant Mass %d" %a 
            self.h_MuMuInvariantMass.Fill(a,weight)
          #self.h_nmuonpairs.Fill(len(mupairs), weight)
          
          """
          if bool(len(muons)==2):
            self.h_muons_chargeprod.Fill(self.store['charge_product'], weight)
            self.h_muons_dphi.Fill(self.store['muons_dphi'], weight)
            self.h_muons_deta.Fill(self.store['muons_deta'], weight)
            self.h_muons_mVis.Fill(self.store['mVis']/GeV, weight)
            self.h_muons_mTtot.Fill(self.store['mTtot']/GeV, weight)
          """ 

          if bool(len(jets)) and bool(len(muons)):
            self.h_mujet_dphi.Fill(self.store['mujet_dphi'], weight)
            self.h_scdphi.Fill(self.store['scdphi'], weight)
         
          ## jets plots
          #if bool(len(jets)):
          #  self.h_jetlead_pt.Fill(jet_lead.tlv.Pt()/GeV, weight)
          
          
          ## muon plots
          # leading
          if bool(len(muons)):  
           self.h_mulead_pt.Fill(mu_lead.tlv.Pt()/GeV, weight)
           self.h_mulead_eta.Fill(mu_lead.tlv.Eta(), weight)
           self.h_mulead_phi.Fill(mu_lead.tlv.Phi(), weight)
           self.h_mulead_trkd0.Fill(mu_lead.trkd0, weight)
           self.h_mulead_trkd0sig.Fill(mu_lead.trkd0sig, weight)
           self.h_mulead_trkz0.Fill(mu_lead.trkz0, weight)
           self.h_mulead_trkz0sintheta.Fill(mu_lead.trkz0sintheta, weight)
           
           self.h_mulead_topoetcone20.Fill(mu_lead.topoetcone20/mu_lead.tlv.Pt(), weight)
           self.h_mulead_topoetcone30.Fill(mu_lead.topoetcone30/mu_lead.tlv.Pt(), weight)
           self.h_mulead_topoetcone40.Fill(mu_lead.topoetcone40/mu_lead.tlv.Pt(), weight)
           self.h_mulead_ptvarcone20.Fill(mu_lead.ptvarcone20/mu_lead.tlv.Pt(), weight)
           self.h_mulead_ptvarcone30.Fill(mu_lead.ptvarcone30/mu_lead.tlv.Pt(), weight)
           self.h_mulead_ptvarcone40.Fill(mu_lead.ptvarcone40/mu_lead.tlv.Pt(), weight)
           
           self.h_mulead_ptcone20.Fill(mu_lead.ptcone20/mu_lead.tlv.Pt(), weight)
           self.h_mulead_ptcone30.Fill(mu_lead.ptcone30/mu_lead.tlv.Pt(), weight)
           self.h_mulead_ptcone40.Fill(mu_lead.ptcone40/mu_lead.tlv.Pt(), weight)
           
         
          # subleading
          """
          self.h_musublead_pt.Fill(mu_sublead.tlv.Pt()/GeV, weight)
          self.h_musublead_eta.Fill(mu_sublead.tlv.Eta(), weight)
          self.h_musublead_phi.Fill(mu_sublead.tlv.Phi(), weight)
          self.h_musublead_trkd0.Fill(mu_sublead.trkd0, weight)
          self.h_musublead_trkd0sig.Fill(mu_sublead.trkd0sig, weight)
          self.h_musublead_trkz0.Fill(mu_sublead.trkz0, weight)
          self.h_musublead_trkz0sintheta.Fill(mu_sublead.trkz0sintheta, weight)
          
          self.h_musublead_topoetcone20.Fill(mu_sublead.topoetcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_topoetcone30.Fill(mu_sublead.topoetcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_topoetcone40.Fill(mu_sublead.topoetcone40/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone20.Fill(mu_sublead.ptvarcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone30.Fill(mu_sublead.ptvarcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone40.Fill(mu_sublead.ptvarcone40/mu_sublead.tlv.Pt(), weight)
          
          self.h_musublead_ptcone20.Fill(mu_sublead.ptcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptcone30.Fill(mu_sublead.ptcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptcone40.Fill(mu_sublead.ptcone40/mu_sublead.tlv.Pt(), weight)
          """ 
          
          ##Electrons Plots
          if bool(len(electrons)):     
              self.h_ellead_pt.Fill(el_lead.tlv.Pt()/GeV, weight)
              self.h_ellead_eta.Fill(el_lead.tlv.Eta(), weight)
              self.h_ellead_phi.Fill(el_lead.tlv.Phi(), weight)
              self.h_ellead_trkd0.Fill(el_lead.trkd0, weight)
              self.h_ellead_trkd0sig.Fill(el_lead.trkd0sig, weight)
              self.h_ellead_trkz0.Fill(el_lead.trkz0, weight)
              self.h_ellead_trkz0sintheta.Fill(el_lead.trkz0sintheta, weight)
              
              self.h_ellead_topoetcone20.Fill(el_lead.topoetcone20/el_lead.tlv.Pt(), weight)
              self.h_ellead_topoetcone30.Fill(el_lead.topoetcone30/el_lead.tlv.Pt(), weight)
              self.h_ellead_topoetcone40.Fill(el_lead.topoetcone40/el_lead.tlv.Pt(), weight)
              self.h_ellead_ptvarcone20.Fill(el_lead.ptvarcone20/el_lead.tlv.Pt(), weight)
              self.h_ellead_ptvarcone30.Fill(el_lead.ptvarcone30/el_lead.tlv.Pt(), weight)
              self.h_ellead_ptvarcone40.Fill(el_lead.ptvarcone40/el_lead.tlv.Pt(), weight)
              
              self.h_ellead_ptcone20.Fill(el_lead.ptcone20/el_lead.tlv.Pt(), weight)
              self.h_ellead_ptcone30.Fill(el_lead.ptcone30/el_lead.tlv.Pt(), weight)
              self.h_ellead_ptcone40.Fill(el_lead.ptcone40/el_lead.tlv.Pt(), weight)
              
         
          # subleading
          """
          self.h_elsublead_pt.Fill(mu_sublead.tlv.Pt()/GeV, weight)
          self.h_elsublead_eta.Fill(mu_sublead.tlv.Eta(), weight)
          self.h_musublead_phi.Fill(mu_sublead.tlv.Phi(), weight)
          self.h_musublead_trkd0.Fill(mu_sublead.trkd0, weight)
          self.h_musublead_trkd0sig.Fill(mu_sublead.trkd0sig, weight)
          self.h_musublead_trkz0.Fill(mu_sublead.trkz0, weight)
          self.h_musublead_trkz0sintheta.Fill(mu_sublead.trkz0sintheta, weight)
          
          self.h_musublead_topoetcone20.Fill(mu_sublead.topoetcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_topoetcone30.Fill(mu_sublead.topoetcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_topoetcone40.Fill(mu_sublead.topoetcone40/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone20.Fill(mu_sublead.ptvarcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone30.Fill(mu_sublead.ptvarcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptvarcone40.Fill(mu_sublead.ptvarcone40/mu_sublead.tlv.Pt(), weight)
          
          self.h_musublead_ptcone20.Fill(mu_sublead.ptcone20/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptcone30.Fill(mu_sublead.ptcone30/mu_sublead.tlv.Pt(), weight)
          self.h_musublead_ptcone40.Fill(mu_sublead.ptcone40/mu_sublead.tlv.Pt(), weight)
          """ 
              


          ## met plots
          self.h_met_clus_et.Fill(met_clus.tlv.Pt()/GeV, weight)
          self.h_met_clus_phi.Fill(met_clus.tlv.Phi(), weight)
          self.h_met_trk_et.Fill(met_trk.tlv.Pt()/GeV, weight)
          self.h_met_trk_phi.Fill(met_trk.tlv.Phi(), weight)
          self.h_met_clus_sumet.Fill(met_clus.sumet/GeV, weight)
          self.h_met_trk_sumet.Fill(met_trk.sumet/GeV, weight)
          
          """
          ## muon pairs plots
          for mp in mupairs:
           
            pcut = True 
            for c in list_cuts:
             if c.startswith("MuPairs"):
              #print c, mp.angle, mp.HasPassedCut(c)
              pcut = pcut and mp.HasPassedCut(c)
             
            pweight = 1.0
            if list_weights:
             for w in list_weights: 
              if w.startswith("MuPairs"):
               pweight *= mp.GetWeight(w)
            
            if pcut: 
             #if mp.angle < 1.0 or mp.angle > 2.5: print "What the fuck"
             self.h_mumu_angle.Fill(mp.angle, pweight * weight)
             self.h_mumu_mVis.Fill(mp.m_vis/GeV, pweight * weight)
             self.h_mumu_mTtot.Fill(mp.mt_tot/GeV, pweight * weight)
             self.h_mumu_sumcosdphi.Fill(mp.SumCosDphi, pweight * weight)
             self.h_mumu_mulead_pt.Fill(mp.lead.tlv.Pt()/GeV, pweight * weight)
             self.h_mumu_musublead_pt.Fill(mp.sublead.tlv.Pt()/GeV,pweight*weight)
             self.h_mumu_mulead_eta.Fill(mp.lead.tlv.Eta(), pweight * weight)
             self.h_mumu_musublead_eta.Fill(mp.sublead.tlv.Eta(), pweight * weight)
             self.h_mumu_mulead_phi.Fill(mp.lead.tlv.Phi(), pweight * weight)
             self.h_mumu_musublead_phi.Fill(mp.sublead.tlv.Phi(), pweight * weight)
          """   

    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
    
    """ 
    #__________________________________________________________________________
    def get_obj_cutflow(self, obj_key, cut, list_weights=None, cut_prefix=""):
        for o in self.store[obj_key]:
          if hasattr(o,"cdict") and hasattr(o,"wdict"):
            obj_weight = 1.0
            if list_weights: 
              for w in list_weights:
                obj_weight *= o.GetWeight(w)
                if cut_prefix: 
                  if cut.startswith(cut_prefix): 
                    obj_passed = o.HasPassedCut(cut) and passed
            self.hists[self.region+"_"+obj_key].count_if(obj_passed, cut, obj_weight * weight)
    """

    #__________________________________________________________________________
    def reset_attributes(self,objects):
        for o in objects:
          o.ResetCuts()
          o.ResetWeights()
        return 
        
#------------------------------------------------------------------------------
class PlotAlgZee(pyframe.algs.CutFlowAlg,CutAlg):
    """

    For making a set of standard plots after each cut in a cutflow.  PlotAlg
    inherets from CutAlg so all the functionality from CutAlg is available for
    applying selection. In addition you can apply weights at different points
    in the selection.

    The selection should be configured by specifying 'cut_flow' in the
    constructor as such:

    cut_flow = [
        ['Cut1', ['Weight1a','Weight1b'],
        ['Cut2', ['Weight2']],
        ['Cut3', None],
        ...
        ]

    The weights must be available in the store.

    'region' will set the name of the dir where the plots are saved

    Inhereting from CutFlowAlg provides the functionality to produce cutflow
    histograms that will be named 'cutflow_<region>' and 'cutflow_raw_<region>'

    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = 'PlotAlgZee',
                 region   = '',
                 obj_keys = [], # make cutflow hist for just this objects
                 cut_flow = None,
                 plot_all = True,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region,obj_keys=obj_keys)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow = cut_flow
        self.region   = region
        self.plot_all = plot_all
        self.obj_keys = obj_keys
    
    #_________________________________________________________________________
    def initialize(self):
        pyframe.algs.CutFlowAlg.initialize(self)
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            # obj cutflow is computed at the end of the cutflow
            #if len(list_cuts)==len(self.cut_flow):
            if self.obj_keys:
             for k in self.obj_keys:
              for o in self.store[k]:
               if hasattr(o,"cdict") and hasattr(o,"wdict"):
                obj_passed = True
                obj_weight = 1.0
                if list_weights:
                 for w in list_weights:
                  if w.startswith("MuPairs"):
                   obj_weight *= o.GetWeight(w) 
                for c in list_cuts:
                 if c.startswith("MuPairs"):
                  obj_passed = o.HasPassedCut(c) and obj_passed
                self.hists[self.region+"_"+k].count_if(obj_passed and passed, c, obj_weight * weight)
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               #if passed:             
               self.plot(region, passed, list_cuts, cut, list_weights=list_weights, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):
        
        # should probably make this configurable
        ## get event candidate
        electrons  = self.store['electrons_tight_MediumLLH_isolLoose']
        met_trk    = self.store['met_trk']
        met_clus   = self.store['met_clus']
        
        EVT    = os.path.join(region, 'event')
        ELECTRONS = os.path.join(region, 'electrons')
        MET    = os.path.join(region, 'met')
        
        # -----------------
        # Create histograms
        # -----------------
        ## event plots
        self.h_averageIntPerXing = self.hist('h_averageIntPerXing', "ROOT.TH1F('$', ';averageInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_actualIntPerXing = self.hist('h_actualIntPerXing', "ROOT.TH1F('$', ';actualInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_NPV = self.hist('h_NPV', "ROOT.TH1F('$', ';NPV;Events', 35, 0., 35.0)", dir=EVT)
        self.h_nelectrons = self.hist('h_nelectrons', "ROOT.TH1F('$', ';N_{e};Events', 8, 0, 8)", dir=EVT)
        #self.h_invMass = self.hist('h_invMass', "ROOT.TH1F('$', ';m(ee) [GeV];Events / (1 GeV)', 10000, 0, 10000)", dir=EVT)
        self.h_invMass = self.hist('h_invMass', "ROOT.TH1F('$', ';m(ee) [GeV];Events / (0.2 GeV)', 50000, 0, 10000)", dir=EVT)
        self.h_ZbosonPt = self.hist('h_ZbosonPt', "ROOT.TH1F('$', ';p_{T}(Z) [GeV];Events / (1 GeV)', 2000, 0, 2000)", dir=EVT)
        self.h_ZbosonEta = self.hist('h_ZbosonEta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 120, -6.0, 6.0)", dir=EVT)
        ## met plots
        self.h_met_clus_et = self.hist('h_met_clus_et', "ROOT.TH1F('$', ';E^{miss}_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_clus_phi = self.hist('h_met_clus_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(clus));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_trk_et = self.hist('h_met_trk_et', "ROOT.TH1F('$', ';E^{miss}_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_phi = self.hist('h_met_trk_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(trk));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_clus_sumet = self.hist('h_met_clus_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_sumet = self.hist('h_met_trk_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)

        ##Electron plots
        self.h_el_random_pt = self.hist('h_el_random_pt', "ROOT.TH1F('$', ';p_{T}(random e) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_pt = self.hist('h_el_pt', "ROOT.TH1F('$', ';p_{T}(e) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_random_eta = self.hist('h_el_random_eta', "ROOT.TH1F('$', ';#eta(random e);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_eta = self.hist('h_el_eta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_phi = self.hist('h_el_phi', "ROOT.TH1F('$', ';#phi(e);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_trkd0sig = self.hist('h_el_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_trkz0sintheta = self.hist('h_el_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
        #leading
        self.h_el_lead_pt = self.hist('h_el_lead_pt', "ROOT.TH1F('$', ';p_{T}(e lead) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_lead_eta = self.hist('h_el_lead_eta', "ROOT.TH1F('$', ';#eta(e lead);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_lead_phi = self.hist('h_el_lead_phi', "ROOT.TH1F('$', ';#phi(e lead);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_lead_trkd0sig = self.hist('h_el_lead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e lead);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_lead_trkz0sintheta = self.hist('h_el_lead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e lead) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
        #subleading
        self.h_el_sublead_pt = self.hist('h_el_sublead_pt', "ROOT.TH1F('$', ';p_{T}(e sublead) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_sublead_eta = self.hist('h_el_sublead_eta', "ROOT.TH1F('$', ';#eta(e sublead);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_sublead_phi = self.hist('h_el_sublead_phi', "ROOT.TH1F('$', ';#phi(e sublead);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_sublead_trkd0sig = self.hist('h_el_sublead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e sublead);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_sublead_trkz0sintheta = self.hist('h_el_sublead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e sublead) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
              
        # charge-flip histograms
        ### last pt bin is open until 27. feb 2017
        #pt_bins  = [30., 34., 38., 43., 48., 55., 62., 70., 100., 140., 200.]
        #eta_bins = [0.0, 0.50, 1.0, 1.20, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
        #################################
        pt_bins  = [30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 115., 140., 200.] # last pt bin is open
        # eta_bins = [0.0, 0.30, 0.50, 1.0, 1.20, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
        eta_bins = [0.0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
        tot_bins = len(pt_bins)*len(pt_bins)*(len(eta_bins)-1)*(len(eta_bins)-1)
        self.h_chargeFlipHist = self.hist('h_chargeFlipHist', "ROOT.TH1F('$', ';pt: "+str(len(pt_bins))+" eta: "+str(len(eta_bins)-1)+";Events',"+str(tot_bins)+",0,"+str(tot_bins)+")", dir=EVT)
        ### true charge-flip
        if self.sampletype == "mc":
          self.h_el_pt_eta_all  = self.hist2DVariable('h_el_pt_eta_all',  pt_bins, eta_bins, dir=ELECTRONS)
          self.h_el_pt_eta_chf2 = self.hist2DVariable('h_el_pt_eta_chf2', pt_bins, eta_bins, dir=ELECTRONS)
          self.h_el_pt_eta_chf4 = self.hist2DVariable('h_el_pt_eta_chf4', pt_bins, eta_bins, dir=ELECTRONS)

        self.h_el_lead_pt_eta     = self.hist2DVariable('h_el_lead_pt_eta',  pt_bins, eta_bins, dir=ELECTRONS)
        self.h_el_sublead_pt_eta  = self.hist2DVariable('h_el_sublead_pt_eta',  pt_bins, eta_bins, dir=ELECTRONS)
        self.h_el_pt_eta          = self.hist2DVariable('h_el_pt_eta',  pt_bins, eta_bins, dir=ELECTRONS)


        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          assert len(electrons)==2, "should have exactly two tight electrons at this point"
          ## event plots
          self.h_averageIntPerXing.Fill(self.chain.averageInteractionsPerCrossing, weight)
          self.h_actualIntPerXing.Fill(self.chain.actualInteractionsPerCrossing, weight)
          self.h_NPV.Fill(self.chain.NPV, weight)
          self.h_nelectrons.Fill(len(electrons), weight)
          self.h_invMass.Fill( (electrons[0].tlv+electrons[1].tlv).M()/GeV, weight)
          self.h_ZbosonPt.Fill( (electrons[0].tlv+electrons[1].tlv).Pt()/GeV, weight)
          self.h_ZbosonEta.Fill( (electrons[0].tlv+electrons[1].tlv).Eta(), weight)
          ## met plots
          self.h_met_clus_et.Fill(met_clus.tlv.Pt()/GeV, weight)
          self.h_met_clus_phi.Fill(met_clus.tlv.Phi(), weight)
          self.h_met_trk_et.Fill(met_trk.tlv.Pt()/GeV, weight)
          self.h_met_trk_phi.Fill(met_trk.tlv.Phi(), weight)
          self.h_met_clus_sumet.Fill(met_clus.sumet/GeV, weight)
          self.h_met_trk_sumet.Fill(met_trk.sumet/GeV, weight)

          
          #electron
          for ele in electrons:
            self.h_el_pt.Fill(ele.tlv.Pt()/GeV, weight)
            self.h_el_eta.Fill(ele.eta, weight)
            self.h_el_phi.Fill(ele.tlv.Phi(), weight)
            self.h_el_trkd0sig.Fill(ele.trkd0sig, weight)
            self.h_el_trkz0sintheta.Fill(ele.trkz0sintheta, weight)
            self.h_el_pt_eta.Fill(ele.tlv.Pt()/GeV, abs(ele.tlv.Eta()), weight)

          ele1 = electrons[1]
          ele2 = electrons[0]
          if electrons[0].tlv.Pt() > electrons[1].tlv.Pt():
            ele1 = electrons[0]
            ele2 = electrons[1]
          assert ele1.tlv.Pt() >= ele2.tlv.Pt(), "leading electron has smaller pt than subleading"
 
          self.h_el_lead_pt.Fill(ele1.tlv.Pt()/GeV, weight)
          self.h_el_lead_eta.Fill(ele1.eta, weight)
          self.h_el_lead_phi.Fill(ele1.tlv.Phi(), weight)
          self.h_el_lead_trkd0sig.Fill(ele1.trkd0sig, weight)
          self.h_el_lead_trkz0sintheta.Fill(ele1.trkz0sintheta, weight)
          self.h_el_lead_pt_eta.Fill(ele1.tlv.Pt()/GeV, abs(ele1.tlv.Eta()), weight)

          self.h_el_sublead_pt.Fill(ele2.tlv.Pt()/GeV, weight)
          self.h_el_sublead_eta.Fill(ele2.eta, weight)
          self.h_el_sublead_phi.Fill(ele2.tlv.Phi(), weight)
          self.h_el_sublead_trkd0sig.Fill(ele2.trkd0sig, weight)
          self.h_el_sublead_trkz0sintheta.Fill(ele2.trkz0sintheta, weight)
          self.h_el_sublead_pt_eta.Fill(ele2.tlv.Pt()/GeV, abs(ele2.tlv.Eta()), weight)

          if bool(random.getrandbits(1)):
            self.h_el_random_pt.Fill(ele1.tlv.Pt()/GeV, weight)
            self.h_el_random_eta.Fill(ele1.eta, weight)
          else:
            self.h_el_random_pt.Fill(ele2.tlv.Pt()/GeV, weight)
            self.h_el_random_eta.Fill(ele2.eta, weight)


          # charge-flip histograms
          ptbin1 = digitize( ele1.tlv.Pt()/GeV, pt_bins )
          ptbin2 = digitize( ele2.tlv.Pt()/GeV, pt_bins )
          etabin1 = digitize( abs(ele1.tlv.Eta()), eta_bins )
          etabin2 = digitize( abs(ele2.tlv.Eta()), eta_bins )
          assert ptbin1!=0 and ptbin2!=0 and etabin1!=0 and etabin2!=0, "bins shouldn't be 0"
          # encode pt1, pt2, eta1, eta2 into 1D bins given pt_bins and eta_bins
          totBin = ( (ptbin1-1)*(len(eta_bins)-1) + etabin1-1 )*(len(eta_bins)-1)*len(pt_bins) + ( (ptbin2-1)*(len(eta_bins)-1) + etabin2 )
          self.h_chargeFlipHist.Fill(totBin,weight)
          ### true charge-flip
          if self.sampletype == "mc":
            for ele in electrons:
              self.h_el_pt_eta_all.Fill(ele.tlv.Pt()/GeV, abs(ele.tlv.Eta()), weight)
              if(ele.electronType()==2):
                self.h_el_pt_eta_chf2.Fill(ele.tlv.Pt()/GeV, abs(ele.tlv.Eta()), weight)
              if(ele.electronType()==3):
                self.h_el_pt_eta_chf4.Fill(ele.tlv.Pt()/GeV, abs(ele.tlv.Eta()), weight)


    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
    
    """ 
    #__________________________________________________________________________
    def get_obj_cutflow(self, obj_key, cut, list_weights=None, cut_prefix=""):
        for o in self.store[obj_key]:
          if hasattr(o,"cdict") and hasattr(o,"wdict"):
            obj_weight = 1.0
            if list_weights: 
              for w in list_weights:
                obj_weight *= o.GetWeight(w)
                if cut_prefix: 
                  if cut.startswith(cut_prefix): 
                    obj_passed = o.HasPassedCut(cut) and passed
            self.hists[self.region+"_"+obj_key].count_if(obj_passed, cut, obj_weight * weight)
    """

    #__________________________________________________________________________
    def reset_attributes(self,objects):
        for o in objects:
          o.ResetCuts()
          o.ResetWeights()
        return 

#------------------------------------------------------------------------------
class PlotAlgFFee(pyframe.algs.CutFlowAlg,CutAlg):
    """

    For making a set of standard plots after each cut in a cutflow.  PlotAlg
    inherets from CutAlg so all the functionality from CutAlg is available for
    applying selection. In addition you can apply weights at different points
    in the selection.

    The selection should be configured by specifying 'cut_flow' in the
    constructor as such:

    cut_flow = [
        ['Cut1', ['Weight1a','Weight1b'],
        ['Cut2', ['Weight2']],
        ['Cut3', None],
        ...
        ]

    The weights must be available in the store.

    'region' will set the name of the dir where the plots are saved

    Inhereting from CutFlowAlg provides the functionality to produce cutflow
    histograms that will be named 'cutflow_<region>' and 'cutflow_raw_<region>'

    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = 'PlotAlgFFee',
                 region   = '',
                 obj_keys = [], # make cutflow hist for just this objects
                 cut_flow = None,
                 plot_all = True,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region,obj_keys=obj_keys)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow = cut_flow
        self.region   = region
        self.plot_all = plot_all
        self.obj_keys = obj_keys
    
    #_________________________________________________________________________
    def initialize(self):
        pyframe.algs.CutFlowAlg.initialize(self)
        self.pt_bins  = [30., 35., 40., 45., 50., 55., 60., 65., 70., 75., 80., 90., 100., 120., 140., 180., 250., 350., 500., 2000.]
        self.eta_bins = [0.0, 1.37, 1.52, 2.01, 2.47]
        # self.trigger_strings   = ["HLT_e24_lhvloose_nod0_L1EM20VH","HLT_e26_lhvloose_nod0_L1EM20VH","HLT_e60_lhvloose_nod0","HLT_e120_lhloose_nod0","HLT_e140_lhloose_nod0"]
        # self.trigger_bounds    = [31.                             ,65.                             ,125.                   ,145.                   ,99999999.]
        # self.trigger_prescaled = [138.43197                       ,112.3913                        ,25.5606                ,6.69107                ,1.0      ]
        self.trigger_strings   = ["HLT_e26_lhvloose_nod0_L1EM20VH","HLT_e60_lhvloose_nod0","HLT_e120_lhloose_nod0","HLT_e140_lhloose_nod0"]
        self.trigger_bounds    = [65.                             ,125.                   ,145.                   ,99999999.]
        self.trigger_prescaled = [112.3913                        ,25.5606                ,6.69107                ,1.0      ]
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            # obj cutflow is computed at the end of the cutflow
            #if len(list_cuts)==len(self.cut_flow):
            if self.obj_keys:
             for k in self.obj_keys:
              for o in self.store[k]:
               if hasattr(o,"cdict") and hasattr(o,"wdict"):
                obj_passed = True
                obj_weight = 1.0
                if list_weights:
                 for w in list_weights:
                  if w.startswith("MuPairs"):
                   obj_weight *= o.GetWeight(w) 
                for c in list_cuts:
                 if c.startswith("MuPairs"):
                  obj_passed = o.HasPassedCut(c) and obj_passed
                self.hists[self.region+"_"+k].count_if(obj_passed and passed, c, obj_weight * weight)
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               #if passed:             
               self.plot(region, passed, list_cuts, cut, list_weights=list_weights, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):
        
        # should probably make this configurable
        ## get event candidate
        electrons  = self.store['electrons_loose_LooseLLH']
        met_trk    = self.store['met_trk']
        met_clus   = self.store['met_clus']
        jets       = self.store['jets']
        
        EVT    = os.path.join(region, 'event')
        ELECTRONS = os.path.join(region, 'electrons')
        MET    = os.path.join(region, 'met')
        
        # -----------------
        # Create histograms
        # -----------------
        ## event plots
        self.h_averageIntPerXing = self.hist('h_averageIntPerXing', "ROOT.TH1F('$', ';averageInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_actualIntPerXing = self.hist('h_actualIntPerXing', "ROOT.TH1F('$', ';actualInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_NPV = self.hist('h_NPV', "ROOT.TH1F('$', ';NPV;Events', 35, 0., 35.0)", dir=EVT)
        self.h_nelectrons = self.hist('h_nelectrons', "ROOT.TH1F('$', ';N_{e};Events', 8, 0, 8)", dir=EVT)
        self.h_nbjets = self.hist('h_nbjets', "ROOT.TH1F('$', ';N_{b};Events', 20, 0, 20)", dir=EVT)
        self.h_njets = self.hist('h_njets', "ROOT.TH1F('$', ';N_{j};Events', 20, 0, 20)", dir=EVT)
        ## met plots
        self.h_met_clus_et = self.hist('h_met_clus_et', "ROOT.TH1F('$', ';E^{miss}_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_clus_phi = self.hist('h_met_clus_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(clus));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_trk_et = self.hist('h_met_trk_et', "ROOT.TH1F('$', ';E^{miss}_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_phi = self.hist('h_met_trk_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(trk));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_clus_sumet = self.hist('h_met_clus_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_sumet = self.hist('h_met_trk_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)

        ##Electron plots
        # tight
        self.h_el_t_pt = self.hist('h_el_t_pt', "ROOT.TH1F('$', ';p_{T}(e) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_t_eta = self.hist('h_el_t_eta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_t_phi = self.hist('h_el_t_phi', "ROOT.TH1F('$', ';#phi(e);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_t_trkd0sig = self.hist('h_el_t_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_t_trkz0sintheta = self.hist('h_el_t_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
        self.h_el_t_2D_pt_eta = self.hist2DVariable('h_el_t_2D_pt_eta',  self.pt_bins, self.eta_bins, dir=ELECTRONS)
        self.h_el_t_2D_pt_Ceta = self.hist2DVariable('h_el_t_2D_pt_Ceta',  self.pt_bins, self.eta_bins, dir=ELECTRONS)
        # loose
        self.h_el_l_pt = self.hist('h_el_l_pt', "ROOT.TH1F('$', ';p_{T}(e) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_l_eta = self.hist('h_el_l_eta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_l_phi = self.hist('h_el_l_phi', "ROOT.TH1F('$', ';#phi(e);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_l_trkd0sig = self.hist('h_el_l_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_l_trkz0sintheta = self.hist('h_el_l_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
        self.h_el_l_2D_pt_eta = self.hist2DVariable('h_el_l_2D_pt_eta',  self.pt_bins, self.eta_bins, dir=ELECTRONS)
        self.h_el_l_2D_pt_Ceta = self.hist2DVariable('h_el_l_2D_pt_Ceta',  self.pt_bins, self.eta_bins, dir=ELECTRONS)
        # strictly loose
        self.h_el_sl_pt = self.hist('h_el_sl_pt', "ROOT.TH1F('$', ';p_{T}(e) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_sl_eta = self.hist('h_el_sl_eta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_sl_phi = self.hist('h_el_sl_phi', "ROOT.TH1F('$', ';#phi(e);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_sl_trkd0sig = self.hist('h_el_sl_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_sl_trkz0sintheta = self.hist('h_el_sl_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
        self.h_el_sl_2D_pt_eta = self.hist2DVariable('h_el_sl_2D_pt_eta',  self.pt_bins, self.eta_bins, dir=ELECTRONS)
        self.h_el_sl_2D_pt_Ceta = self.hist2DVariable('h_el_sl_2D_pt_Ceta',  self.pt_bins, self.eta_bins, dir=ELECTRONS)


        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          ## event plots
          self.h_averageIntPerXing.Fill(self.chain.averageInteractionsPerCrossing, weight)
          self.h_actualIntPerXing.Fill(self.chain.actualInteractionsPerCrossing, weight)
          self.h_NPV.Fill(self.chain.NPV, weight)
          self.h_nelectrons.Fill(len(electrons), weight)
          nbjets = 0
          for jet in jets:
            if jet.isFix77:
              nbjets += 1
          self.h_njets.Fill(len(jets), weight)
          self.h_nbjets.Fill(nbjets, weight)
          ## met plots
          self.h_met_clus_et.Fill(met_clus.tlv.Pt()/GeV, weight)
          self.h_met_clus_phi.Fill(met_clus.tlv.Phi(), weight)
          self.h_met_trk_et.Fill(met_trk.tlv.Pt()/GeV, weight)
          self.h_met_trk_phi.Fill(met_trk.tlv.Phi(), weight)
          self.h_met_clus_sumet.Fill(met_clus.sumet/GeV, weight)
          self.h_met_trk_sumet.Fill(met_trk.sumet/GeV, weight)

          #electron
          for ele in electrons:
            # trigger
            assert len(ele.isTrigMatchedToChain)==(len(self.chain.el_listTrigChains)/self.chain.nel),"size of isTrigMatchedToChain not the same as listTrigChains"
            elePassTrigger = 0
            for trig,bound,scale in zip(self.trigger_strings,self.trigger_bounds,self.trigger_prescaled):
              if ele.tlv.Pt()/GeV <= bound:
                for isMatched,triggerStr in zip(ele.isTrigMatchedToChain,self.chain.el_listTrigChains):
                  if triggerStr==trig and isMatched==1:
                    for i in xrange(self.chain.passedTriggers.size()):
                      if self.chain.passedTriggers.at(i) == trig:
                        elePassTrigger = 1. if self.sampletype == "mc" else scale
                        break
                    break
                break

            # loose (all of them are loose here)
            elSF_LooseLLH = 1.
            if("mc" in self.sampletype):
              elSF_LooseLLH *= getattr(ele,"RecoEff_SF").at(0)
              elSF_LooseLLH *= getattr(ele,"PIDEff_SF_LHLooseAndBLayer").at(0)
            self.h_el_l_pt.Fill(ele.tlv.Pt()/GeV,             weight*elePassTrigger*elSF_LooseLLH)
            self.h_el_l_eta.Fill(ele.eta,                     weight*elePassTrigger*elSF_LooseLLH)
            self.h_el_l_phi.Fill(ele.tlv.Phi(),               weight*elePassTrigger*elSF_LooseLLH)
            self.h_el_l_trkd0sig.Fill(ele.trkd0sig,           weight*elePassTrigger*elSF_LooseLLH)
            self.h_el_l_trkz0sintheta.Fill(ele.trkz0sintheta, weight*elePassTrigger*elSF_LooseLLH)
            self.h_el_l_2D_pt_eta.Fill(ele.tlv.Pt()/GeV, abs(ele.eta), weight*elePassTrigger*elSF_LooseLLH)
            self.h_el_l_2D_pt_Ceta.Fill(ele.tlv.Pt()/GeV, abs(ele.caloCluster_eta), weight*elePassTrigger*elSF_LooseLLH)
            if ele.isIsolated_Loose and ele.LHMedium:
              # tight
              elSF_MediumLLH_isolLoose =  1.
              if("mc" in self.sampletype):
                elSF_MediumLLH_isolLoose *= getattr(ele,"RecoEff_SF").at(0)
                elSF_MediumLLH_isolLoose *= getattr(ele,"PIDEff_SF_LHLooseAndBLayer").at(0)
                elSF_MediumLLH_isolLoose *= getattr(ele,"IsoEff_SF_MediumLLHisolLoose").at(0)
              self.h_el_t_pt.Fill(ele.tlv.Pt()/GeV,             weight*elePassTrigger*elSF_MediumLLH_isolLoose)
              self.h_el_t_eta.Fill(ele.eta,                     weight*elePassTrigger*elSF_MediumLLH_isolLoose)
              self.h_el_t_phi.Fill(ele.tlv.Phi(),               weight*elePassTrigger*elSF_MediumLLH_isolLoose)
              self.h_el_t_trkd0sig.Fill(ele.trkd0sig,           weight*elePassTrigger*elSF_MediumLLH_isolLoose)
              self.h_el_t_trkz0sintheta.Fill(ele.trkz0sintheta, weight*elePassTrigger*elSF_MediumLLH_isolLoose)
              self.h_el_t_2D_pt_eta.Fill(ele.tlv.Pt()/GeV, abs(ele.eta), weight*elePassTrigger*elSF_MediumLLH_isolLoose)
              self.h_el_t_2D_pt_Ceta.Fill(ele.tlv.Pt()/GeV, abs(ele.caloCluster_eta), weight*elePassTrigger*elSF_MediumLLH_isolLoose)
            else:
              # strictly loose (they failed the tight criteria)
              self.h_el_sl_pt.Fill(ele.tlv.Pt()/GeV,             weight*elePassTrigger*elSF_LooseLLH)
              self.h_el_sl_eta.Fill(ele.eta,                     weight*elePassTrigger*elSF_LooseLLH)
              self.h_el_sl_phi.Fill(ele.tlv.Phi(),               weight*elePassTrigger*elSF_LooseLLH)
              self.h_el_sl_trkd0sig.Fill(ele.trkd0sig,           weight*elePassTrigger*elSF_LooseLLH)
              self.h_el_sl_trkz0sintheta.Fill(ele.trkz0sintheta, weight*elePassTrigger*elSF_LooseLLH)
              self.h_el_sl_2D_pt_eta.Fill(ele.tlv.Pt()/GeV, abs(ele.eta), weight*elePassTrigger*elSF_LooseLLH)
              self.h_el_sl_2D_pt_Ceta.Fill(ele.tlv.Pt()/GeV, abs(ele.caloCluster_eta), weight*elePassTrigger*elSF_LooseLLH)


    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
    
    """ 
    #__________________________________________________________________________
    def get_obj_cutflow(self, obj_key, cut, list_weights=None, cut_prefix=""):
        for o in self.store[obj_key]:
          if hasattr(o,"cdict") and hasattr(o,"wdict"):
            obj_weight = 1.0
            if list_weights: 
              for w in list_weights:
                obj_weight *= o.GetWeight(w)
                if cut_prefix: 
                  if cut.startswith(cut_prefix): 
                    obj_passed = o.HasPassedCut(cut) and passed
            self.hists[self.region+"_"+obj_key].count_if(obj_passed, cut, obj_weight * weight)
    """

    #__________________________________________________________________________
    def reset_attributes(self,objects):
        for o in objects:
          o.ResetCuts()
          o.ResetWeights()
        return 

#------------------------------------------------------------------------------
class PlotAlgWJets(pyframe.algs.CutFlowAlg,CutAlg):
    """

    For making a set of standard plots after each cut in a cutflow.  PlotAlg
    inherets from CutAlg so all the functionality from CutAlg is available for
    applying selection. In addition you can apply weights at different points
    in the selection.

    The selection should be configured by specifying 'cut_flow' in the
    constructor as such:

    cut_flow = [
        ['Cut1', ['Weight1a','Weight1b'],
        ['Cut2', ['Weight2']],
        ['Cut3', None],
        ...
        ]

    The weights must be available in the store.

    'region' will set the name of the dir where the plots are saved

    Inhereting from CutFlowAlg provides the functionality to produce cutflow
    histograms that will be named 'cutflow_<region>' and 'cutflow_raw_<region>'

    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = 'PlotAlgWJets',
                 region   = '',
                 obj_keys = [], # make cutflow hist for just this objects
                 cut_flow = None,
                 plot_all = True,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region,obj_keys=obj_keys)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow = cut_flow
        self.region   = region
        self.plot_all = plot_all
        self.obj_keys = obj_keys
    
    #_________________________________________________________________________
    def initialize(self):
        pyframe.algs.CutFlowAlg.initialize(self)
        self.trigger_strings   = ["HLT_e26_lhvloose_nod0_L1EM20VH","HLT_e60_lhvloose_nod0","HLT_e120_lhloose_nod0","HLT_e140_lhloose_nod0"]
        self.trigger_bounds    = [65.                             ,125.                   ,145.                   ,99999999.]
        self.trigger_prescaled = [112.3913                        ,25.5606                ,6.69107                ,1.0      ]
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            # obj cutflow is computed at the end of the cutflow
            #if len(list_cuts)==len(self.cut_flow):
            if self.obj_keys:
             for k in self.obj_keys:
              for o in self.store[k]:
               if hasattr(o,"cdict") and hasattr(o,"wdict"):
                obj_passed = True
                obj_weight = 1.0
                if list_weights:
                 for w in list_weights:
                  if w.startswith("MuPairs"):
                   obj_weight *= o.GetWeight(w) 
                for c in list_cuts:
                 if c.startswith("MuPairs"):
                  obj_passed = o.HasPassedCut(c) and obj_passed
                self.hists[self.region+"_"+k].count_if(obj_passed and passed, c, obj_weight * weight)
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               #if passed:             
               self.plot(region, passed, list_cuts, cut, list_weights=list_weights, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):
        
        # should probably make this configurable
        ## get event candidate
        electrons  = self.store['electrons_loose_LooseLLH']
        met_trk    = self.store['met_trk']
        met_clus   = self.store['met_clus']
        
        EVT    = os.path.join(region, 'event')
        ELECTRONS = os.path.join(region, 'electrons')
        MET    = os.path.join(region, 'met')
        
        # -----------------
        # Create histograms
        # -----------------
        ## event plots
        self.h_averageIntPerXing = self.hist('h_averageIntPerXing', "ROOT.TH1F('$', ';averageInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_actualIntPerXing = self.hist('h_actualIntPerXing', "ROOT.TH1F('$', ';actualInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_NPV = self.hist('h_NPV', "ROOT.TH1F('$', ';NPV;Events', 35, 0., 35.0)", dir=EVT)
        self.h_nelectrons = self.hist('h_nelectrons', "ROOT.TH1F('$', ';N_{e};Events', 8, 0, 8)", dir=EVT)
        ## met plots
        self.h_met_clus_et = self.hist('h_met_clus_et', "ROOT.TH1F('$', ';E^{miss}_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_clus_phi = self.hist('h_met_clus_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(clus));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_trk_et = self.hist('h_met_trk_et', "ROOT.TH1F('$', ';E^{miss}_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_phi = self.hist('h_met_trk_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(trk));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_clus_sumet = self.hist('h_met_clus_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_sumet = self.hist('h_met_trk_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)

        self.h_met_trk_mt = self.hist('h_met_trk_mt', "ROOT.TH1F('$', ';m_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_clus_mt = self.hist('h_met_clus_mt', "ROOT.TH1F('$', ';m_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)

        ##Electron plots
        self.h_el_pt = self.hist('h_el_pt', "ROOT.TH1F('$', ';p_{T}(e) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_eta = self.hist('h_el_eta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_phi = self.hist('h_el_phi', "ROOT.TH1F('$', ';#phi(e);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_trkd0sig = self.hist('h_el_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_trkz0sintheta = self.hist('h_el_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)


        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          # trigger
          assert len(electrons)==1,"size of electrons should be exactly 1"
          ele = electrons[0]
          assert len(ele.isTrigMatchedToChain)==(len(self.chain.el_listTrigChains)/self.chain.nel),"size of isTrigMatchedToChain not the same as listTrigChains"
          elePassTrigger = 0
          for trig,bound,scale in zip(self.trigger_strings,self.trigger_bounds,self.trigger_prescaled):
            if ele.tlv.Pt()/GeV <= bound:
              for isMatched,triggerStr in zip(ele.isTrigMatchedToChain,self.chain.el_listTrigChains):
                if triggerStr==trig and isMatched==1:
                  for i in xrange(self.chain.passedTriggers.size()):
                    if self.chain.passedTriggers.at(i) == trig:
                      elePassTrigger = 1. if self.sampletype == "mc" else scale
                      break
                  break
              break
          ## event plots
          self.h_averageIntPerXing.Fill(self.chain.averageInteractionsPerCrossing, weight*elePassTrigger)
          self.h_actualIntPerXing.Fill(self.chain.actualInteractionsPerCrossing, weight*elePassTrigger)
          self.h_NPV.Fill(self.chain.NPV, weight*elePassTrigger)
          self.h_nelectrons.Fill(len(electrons), weight*elePassTrigger)
          ## met plots
          self.h_met_clus_et.Fill(met_clus.tlv.Pt()/GeV, weight*elePassTrigger)
          self.h_met_clus_phi.Fill(met_clus.tlv.Phi(), weight*elePassTrigger)
          self.h_met_trk_et.Fill(met_trk.tlv.Pt()/GeV, weight*elePassTrigger)
          self.h_met_trk_phi.Fill(met_trk.tlv.Phi(), weight*elePassTrigger)
          self.h_met_clus_sumet.Fill(met_clus.sumet/GeV, weight*elePassTrigger)
          self.h_met_trk_sumet.Fill(met_trk.sumet/GeV, weight*elePassTrigger)

          ele1T = ROOT.TLorentzVector()
          ele1T.SetPtEtaPhiM( electrons[0].tlv.Pt(), 0., electrons[0].tlv.Phi(), electrons[0].tlv.M() )

          self.h_met_trk_mt.Fill ( (ele1T+met_trk.tlv).M()/GeV , weight*elePassTrigger)
          self.h_met_clus_mt.Fill( (ele1T+met_clus.tlv).M()/GeV, weight*elePassTrigger)

          #electron
          self.h_el_pt.Fill(ele.tlv.Pt()/GeV, weight*elePassTrigger)
          self.h_el_eta.Fill(ele.eta, weight*elePassTrigger)
          self.h_el_phi.Fill(ele.tlv.Phi(), weight*elePassTrigger)
          self.h_el_trkd0sig.Fill(ele.trkd0sig, weight*elePassTrigger)
          self.h_el_trkz0sintheta.Fill(ele.trkz0sintheta, weight*elePassTrigger)


    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
    
    """ 
    #__________________________________________________________________________
    def get_obj_cutflow(self, obj_key, cut, list_weights=None, cut_prefix=""):
        for o in self.store[obj_key]:
          if hasattr(o,"cdict") and hasattr(o,"wdict"):
            obj_weight = 1.0
            if list_weights: 
              for w in list_weights:
                obj_weight *= o.GetWeight(w)
                if cut_prefix: 
                  if cut.startswith(cut_prefix): 
                    obj_passed = o.HasPassedCut(cut) and passed
            self.hists[self.region+"_"+obj_key].count_if(obj_passed, cut, obj_weight * weight)
    """

    #__________________________________________________________________________
    def reset_attributes(self,objects):
        for o in objects:
          o.ResetCuts()
          o.ResetWeights()
        return 

#------------------------------------------------------------------------------
class PlotAlgThreeLep(pyframe.algs.CutFlowAlg,CutAlg):
    """

    For making a set of standard plots after each cut in a cutflow.  PlotAlg
    inherets from CutAlg so all the functionality from CutAlg is available for
    applying selection. In addition you can apply weights at different points
    in the selection.

    The selection should be configured by specifying 'cut_flow' in the
    constructor as such:

    cut_flow = [
        ['Cut1', ['Weight1a','Weight1b'],
        ['Cut2', ['Weight2']],
        ['Cut3', None],
        ...
        ]

    The weights must be available in the store.

    'region' will set the name of the dir where the plots are saved

    Inhereting from CutFlowAlg provides the functionality to produce cutflow
    histograms that will be named 'cutflow_<region>' and 'cutflow_raw_<region>'

    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = 'PlotAlgThreeLep',
                 region   = '',
                 obj_keys = [], # make cutflow hist for just this objects
                 cut_flow = None,
                 plot_all = True,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region,obj_keys=obj_keys)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow = cut_flow
        self.region   = region
        self.plot_all = plot_all
        self.obj_keys = obj_keys
    
    #_________________________________________________________________________
    def initialize(self):
        pyframe.algs.CutFlowAlg.initialize(self)
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            # obj cutflow is computed at the end of the cutflow
            #if len(list_cuts)==len(self.cut_flow):
            if self.obj_keys:
             for k in self.obj_keys:
              for o in self.store[k]:
               if hasattr(o,"cdict") and hasattr(o,"wdict"):
                obj_passed = True
                obj_weight = 1.0
                if list_weights:
                 for w in list_weights:
                  if w.startswith("MuPairs"):
                   obj_weight *= o.GetWeight(w) 
                for c in list_cuts:
                 if c.startswith("MuPairs"):
                  obj_passed = o.HasPassedCut(c) and obj_passed
                self.hists[self.region+"_"+k].count_if(obj_passed and passed, c, obj_weight * weight)
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               #if passed:             
               self.plot(region, passed, list_cuts, cut, list_weights=list_weights, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):
        
        # should probably make this configurable
        ## get event candidate
        electrons  = self.store['electrons_loose_LooseLLH']
        muons = self.store['muons']

        leptons = electrons + muons

        met_trk    = self.store['met_trk']
        met_clus   = self.store['met_clus']
        jets       = self.store['jets']
        
        EVT    = os.path.join(region, 'event')
        LEPTONS = os.path.join(region, 'leptons')
        MET    = os.path.join(region, 'met')
        
        # -----------------
        # Create histograms
        # -----------------
        ## event plots
        self.h_averageIntPerXing = self.hist('h_averageIntPerXing', "ROOT.TH1F('$', ';averageInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_actualIntPerXing = self.hist('h_actualIntPerXing', "ROOT.TH1F('$', ';actualInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_NPV = self.hist('h_NPV', "ROOT.TH1F('$', ';NPV;Events', 35, 0., 35.0)", dir=EVT)
        self.h_nleptons = self.hist('h_nleptons', "ROOT.TH1F('$', ';N_{l};Events', 8, 0, 8)", dir=EVT)
        self.h_nsspairs = self.hist('h_nsspairs', "ROOT.TH1F('$', ';N_{e^{#pm}e^{#pm}};Events', 5, 0, 5)", dir=EVT)
        self.h_nbjets = self.hist('h_nbjets', "ROOT.TH1F('$', ';N_{b};Events', 20, 0, 20)", dir=EVT)
        self.h_njets = self.hist('h_njets', "ROOT.TH1F('$', ';N_{j};Events', 20, 0, 20)", dir=EVT)
        self.h_invMass = self.hist('h_invMass', "ROOT.TH1F('$', ';m(ll) [GeV];Events / (1 GeV)', 2000, 0, 2000)", dir=EVT)
        self.h_HT = self.hist('h_HT', "ROOT.TH1F('$', ';H_{T} [GeV];Events / (1 GeV)', 10000, 0, 10000)", dir=EVT)
        # self.h_HTmet = self.hist('h_HTmet', "ROOT.TH1F('$', ';H_{T} [GeV];Events / (1 GeV)', 10000, 0, 10000)", dir=EVT)
        self.h_invMassOS1 = self.hist('h_invMassOS1', "ROOT.TH1F('$', ';Leading OS m(ll) [GeV];Events / (1 GeV)', 2000, 0, 2000)", dir=EVT)
        self.h_invMassOS2 = self.hist('h_invMassOS2', "ROOT.TH1F('$', ';Subleading OS m(ll) [GeV];Events / (1 GeV)', 2000, 0, 2000)", dir=EVT)
        self.h_ZbosonPt = self.hist('h_ZbosonPt', "ROOT.TH1F('$', ';p_{T}(Z) [GeV];Events / (1 GeV)', 2000, 0, 2000)", dir=EVT)
        self.h_ZbosonEta = self.hist('h_ZbosonEta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 120, -6.0, 6.0)", dir=EVT)
        self.h_DR = self.hist('h_DR', "ROOT.TH1F('$', ';#DeltaR(ll);Events / (0.1)', 60, 0, 6.0)", dir=EVT)
        # self.h_mTtot = self.hist('h_mTtot', "ROOT.TH1F('$', ';m^{tot}_{T} [GeV];Events / (1 GeV)', 10000, 0.0, 10000.)", dir=EVT)
        ## met plots
        self.h_met_clus_et = self.hist('h_met_clus_et', "ROOT.TH1F('$', ';E^{miss}_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_clus_phi = self.hist('h_met_clus_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(clus));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_trk_et = self.hist('h_met_trk_et', "ROOT.TH1F('$', ';E^{miss}_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_phi = self.hist('h_met_trk_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(trk));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_clus_sumet = self.hist('h_met_clus_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_sumet = self.hist('h_met_trk_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(trk) [GeV];Events / (1 GeV)', 10000, 0.0, 10000.0)", dir=MET)


        ##Electron plots
        self.h_el_pt = self.hist('h_el_pt', "ROOT.TH1F('$', ';p_{T}(l) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=LEPTONS)
        self.h_el_eta = self.hist('h_el_eta', "ROOT.TH1F('$', ';#eta(l);Events / (0.1)', 50, -2.5, 2.5)", dir=LEPTONS)
        self.h_el_phi = self.hist('h_el_phi', "ROOT.TH1F('$', ';#phi(l);Events / (0.1)', 64, -3.2, 3.2)", dir=LEPTONS)
        self.h_el_trkd0sig = self.hist('h_el_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(l);Events / (0.1)', 100, 0., 10.)", dir=LEPTONS)
        self.h_el_trkz0sintheta = self.hist('h_el_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(l) [mm];Events / (0.01)', 200, -1, 1)", dir=LEPTONS)
        #leading
        self.h_el_lead_pt = self.hist('h_el_lead_pt', "ROOT.TH1F('$', ';p_{T}(l lead) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=LEPTONS)
        self.h_el_lead_eta = self.hist('h_el_lead_eta', "ROOT.TH1F('$', ';#eta(l lead);Events / (0.1)', 50, -2.5, 2.5)", dir=LEPTONS)
        self.h_el_lead_phi = self.hist('h_el_lead_phi', "ROOT.TH1F('$', ';#phi(l lead);Events / (0.1)', 64, -3.2, 3.2)", dir=LEPTONS)
        self.h_el_lead_trkd0sig = self.hist('h_el_lead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(l lead);Events / (0.1)', 100, 0., 10.)", dir=LEPTONS)
        self.h_el_lead_trkz0sintheta = self.hist('h_el_lead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(l lead) [mm];Events / (0.01)', 200, -1, 1)", dir=LEPTONS)
        #subleading
        self.h_el_sublead_pt = self.hist('h_el_sublead_pt', "ROOT.TH1F('$', ';p_{T}(l sublead) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=LEPTONS)
        self.h_el_sublead_eta = self.hist('h_el_sublead_eta', "ROOT.TH1F('$', ';#eta(l sublead);Events / (0.1)', 50, -2.5, 2.5)", dir=LEPTONS)
        self.h_el_sublead_phi = self.hist('h_el_sublead_phi', "ROOT.TH1F('$', ';#phi(l sublead);Events / (0.1)', 64, -3.2, 3.2)", dir=LEPTONS)
        self.h_el_sublead_trkd0sig = self.hist('h_el_sublead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(l sublead);Events / (0.1)', 100, 0., 10.)", dir=LEPTONS)
        self.h_el_sublead_trkz0sintheta = self.hist('h_el_sublead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(l sublead) [mm];Events / (0.01)', 200, -1, 1)", dir=LEPTONS)
        #third
        self.h_el_third_pt = self.hist('h_el_third_pt', "ROOT.TH1F('$', ';p_{T}(l third) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=LEPTONS)
        self.h_el_third_eta = self.hist('h_el_third_eta', "ROOT.TH1F('$', ';#eta(l third);Events / (0.1)', 50, -2.5, 2.5)", dir=LEPTONS)
        self.h_el_third_phi = self.hist('h_el_third_phi', "ROOT.TH1F('$', ';#phi(l third);Events / (0.1)', 64, -3.2, 3.2)", dir=LEPTONS)
        self.h_el_third_trkd0sig = self.hist('h_el_third_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(l third);Events / (0.1)', 100, 0., 10.)", dir=LEPTONS)
        self.h_el_third_trkz0sintheta = self.hist('h_el_third_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(l third) [mm];Events / (0.01)', 200, -1, 1)", dir=LEPTONS)

        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          assert len(leptons) in [2,3,4], "should have exactly 2/3/4 leptons at this point"
          NL = len(leptons)
          NSSPairs = 0
          NOSPairs = 0
          SSPairs = []
          OSPairs = []
          for pair in itertools.combinations(leptons,2):
            if (pair[0].trkcharge * pair[1].trkcharge) == 1 :
              # same-sign
              NSSPairs += 1
              SSPairs += [pair]
            else:
              NOSPairs += 1
              OSPairs += [pair]
          SSPairs.sort(key=lambda x: pair_mass(x), reverse=True )
          OSPairs.sort(key=lambda x: pair_mass(x), reverse=True )
          leptons.sort(key=lambda x: x.tlv.Pt(), reverse=True )

          assert len(SSPairs) < 3, "more than 2 SS pairs??"
          if len(SSPairs)==2:
            assert len(OSPairs)==4,"should be 4 OS with 2 SS"
            assert pair_mass(SSPairs[0]) >= pair_mass(SSPairs[1]), "SS pairs not sorted"
          assert leptons[0].tlv.Pt() >= leptons[1].tlv.Pt(), "leptons not sorted!"

          ## event plots 
          self.h_averageIntPerXing.Fill(self.chain.averageInteractionsPerCrossing, weight)
          self.h_actualIntPerXing.Fill(self.chain.actualInteractionsPerCrossing, weight)
          self.h_NPV.Fill(self.chain.NPV, weight)
          self.h_nleptons.Fill(len(leptons), weight)
          self.h_nsspairs.Fill( NSSPairs, weight)
          if NL > 2:
            assert len(OSPairs) in [2,4], "should be 2/4 OS pairs with >2 ele"
            self.h_invMassOS1.Fill( pair_mass(OSPairs[0])/GeV, weight)
            self.h_invMassOS2.Fill( pair_mass(OSPairs[1])/GeV, weight)
          self.h_invMass.Fill( average_mass(SSPairs)/GeV, weight)
          self.h_ZbosonPt.Fill( pair_pt(SSPairs[0])/GeV, weight)
          self.h_ZbosonEta.Fill( pair_eta(SSPairs[0]), weight)
          self.h_DR.Fill( pair_dr(SSPairs[0]), weight)
          self.h_HT.Fill( leptons_HT(leptons)/GeV, weight )

          nbjets = 0
          for jet in jets:
            if jet.isFix77:
              nbjets += 1
          self.h_njets.Fill(len(jets), weight)
          self.h_nbjets.Fill(nbjets, weight)

          ## met plots
          self.h_met_clus_et.Fill(met_clus.tlv.Pt()/GeV, weight)
          self.h_met_clus_phi.Fill(met_clus.tlv.Phi(), weight)
          self.h_met_trk_et.Fill(met_trk.tlv.Pt()/GeV, weight)
          self.h_met_trk_phi.Fill(met_trk.tlv.Phi(), weight)
          self.h_met_clus_sumet.Fill(met_clus.sumet/GeV, weight)
          self.h_met_trk_sumet.Fill(met_trk.sumet/GeV, weight)
          #electron
          for lep in leptons:
            self.h_el_pt.Fill(lep.tlv.Pt()/GeV, weight)
            self.h_el_eta.Fill(lep.eta, weight)
            self.h_el_phi.Fill(lep.tlv.Phi(), weight)
            self.h_el_trkd0sig.Fill(lep.trkd0sig, weight)
            self.h_el_trkz0sintheta.Fill(lep.trkz0sintheta, weight)
 
          self.h_el_lead_pt.Fill(leptons[0].tlv.Pt()/GeV, weight)
          self.h_el_lead_eta.Fill(leptons[0].eta, weight)
          self.h_el_lead_phi.Fill(leptons[0].tlv.Phi(), weight)
          self.h_el_lead_trkd0sig.Fill(leptons[0].trkd0sig, weight)
          self.h_el_lead_trkz0sintheta.Fill(leptons[0].trkz0sintheta, weight)

          self.h_el_sublead_pt.Fill(leptons[1].tlv.Pt()/GeV, weight)
          self.h_el_sublead_eta.Fill(leptons[1].eta, weight)
          self.h_el_sublead_phi.Fill(leptons[1].tlv.Phi(), weight)
          self.h_el_sublead_trkd0sig.Fill(leptons[1].trkd0sig, weight)
          self.h_el_sublead_trkz0sintheta.Fill(leptons[1].trkz0sintheta, weight)

          if NL == 3:
            self.h_el_third_pt.Fill(leptons[2].tlv.Pt()/GeV, weight)
            self.h_el_third_eta.Fill(leptons[2].eta, weight)
            self.h_el_third_phi.Fill(leptons[2].tlv.Phi(), weight)
            self.h_el_third_trkd0sig.Fill(leptons[2].trkd0sig, weight)
            self.h_el_third_trkz0sintheta.Fill(leptons[2].trkz0sintheta, weight)


    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
    
    """ 
    #__________________________________________________________________________
    def get_obj_cutflow(self, obj_key, cut, list_weights=None, cut_prefix=""):
        for o in self.store[obj_key]:
          if hasattr(o,"cdict") and hasattr(o,"wdict"):
            obj_weight = 1.0
            if list_weights: 
              for w in list_weights:
                obj_weight *= o.GetWeight(w)
                if cut_prefix: 
                  if cut.startswith(cut_prefix): 
                    obj_passed = o.HasPassedCut(cut) and passed
            self.hists[self.region+"_"+obj_key].count_if(obj_passed, cut, obj_weight * weight)
    """

    #__________________________________________________________________________
    def reset_attributes(self,objects):
        for o in objects:
          o.ResetCuts()
          o.ResetWeights()
        return

#------------------------------------------------------------------------------
class PlotAlgCRele(pyframe.algs.CutFlowAlg,CutAlg):
    """

    For making a set of standard plots after each cut in a cutflow.  PlotAlg
    inherets from CutAlg so all the functionality from CutAlg is available for
    applying selection. In addition you can apply weights at different points
    in the selection.

    The selection should be configured by specifying 'cut_flow' in the
    constructor as such:

    cut_flow = [
        ['Cut1', ['Weight1a','Weight1b'],
        ['Cut2', ['Weight2']],
        ['Cut3', None],
        ...
        ]

    The weights must be available in the store.

    'region' will set the name of the dir where the plots are saved

    Inhereting from CutFlowAlg provides the functionality to produce cutflow
    histograms that will be named 'cutflow_<region>' and 'cutflow_raw_<region>'

    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = 'PlotAlgCRele',
                 region   = '',
                 obj_keys = [],
                 cut_flow = None,
                 plot_all = True,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region,obj_keys=obj_keys)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow = cut_flow
        self.region   = region
        self.plot_all = plot_all
        self.obj_keys = obj_keys
    
    #_________________________________________________________________________
    def initialize(self):
        pyframe.algs.CutFlowAlg.initialize(self)
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            # obj cutflow is computed at the end of the cutflow
            #if len(list_cuts)==len(self.cut_flow):
            if self.obj_keys:
             for k in self.obj_keys:
              for o in self.store[k]:
               if hasattr(o,"cdict") and hasattr(o,"wdict"):
                obj_passed = True
                obj_weight = 1.0
                if list_weights:
                 for w in list_weights:
                  if w.startswith("MuPairs"):
                   obj_weight *= o.GetWeight(w) 
                for c in list_cuts:
                 if c.startswith("MuPairs"):
                  obj_passed = o.HasPassedCut(c) and obj_passed
                self.hists[self.region+"_"+k].count_if(obj_passed and passed, c, obj_weight * weight)
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               #if passed:             
               self.plot(region, passed, list_cuts, cut, list_weights=list_weights, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):
        
        # should probably make this configurable
        ## get event candidate
        electrons  = self.store['electrons_loose_LooseLLH']

        met_trk    = self.store['met_trk']
        met_clus   = self.store['met_clus']
        jets       = self.store['jets']
        
        EVT    = os.path.join(region, 'event')
        ELECTRONS = os.path.join(region, 'electrons')
        MET    = os.path.join(region, 'met')
        
        # -----------------
        # Create histograms
        # -----------------
        ## event plots
        self.h_averageIntPerXing = self.hist('h_averageIntPerXing', "ROOT.TH1F('$', ';averageInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_actualIntPerXing = self.hist('h_actualIntPerXing', "ROOT.TH1F('$', ';actualInteractionsPerCrossing;Events', 50, -0.5, 49.5)", dir=EVT)
        self.h_NPV = self.hist('h_NPV', "ROOT.TH1F('$', ';NPV;Events', 35, 0., 35.0)", dir=EVT)
        self.h_nelectrons = self.hist('h_nelectrons', "ROOT.TH1F('$', ';N_{e};Events', 8, 0, 8)", dir=EVT)
        self.h_nbjets = self.hist('h_nbjets', "ROOT.TH1F('$', ';N_{b};Events', 20, 0, 20)", dir=EVT)
        self.h_njets = self.hist('h_njets', "ROOT.TH1F('$', ';N_{j};Events', 20, 0, 20)", dir=EVT)
        self.h_invMass = self.hist('h_invMass', "ROOT.TH1F('$', ';m(ee) [GeV];Events / (1 GeV)', 2000, 0, 2000)", dir=EVT)
        self.h_ZbosonPt = self.hist('h_ZbosonPt', "ROOT.TH1F('$', ';p_{T}(Z) [GeV];Events / (1 GeV)', 2000, 0, 2000)", dir=EVT)
        self.h_ZbosonEta = self.hist('h_ZbosonEta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 120, -6.0, 6.0)", dir=EVT)
        self.h_DR = self.hist('h_DR', "ROOT.TH1F('$', ';#DeltaR(ee);Events / (0.1)', 60, 0, 6.0)", dir=EVT)
        self.h_mTtot = self.hist('h_mTtot', "ROOT.TH1F('$', ';m^{tot}_{T} [GeV];Events / (1 GeV)', 10000, 0.0, 10000.)", dir=EVT)
        self.h_HT = self.hist('h_HT', "ROOT.TH1F('$', ';H_{T} [GeV];Events / (1 GeV)', 10000, 0, 10000)", dir=EVT)
        self.h_HTmet = self.hist('h_HTmet', "ROOT.TH1F('$', ';H_{T} [GeV];Events / (1 GeV)', 10000, 0, 10000)", dir=EVT)
        ## met plots
        self.h_met_clus_et = self.hist('h_met_clus_et', "ROOT.TH1F('$', ';E^{miss}_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_clus_phi = self.hist('h_met_clus_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(clus));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_trk_et = self.hist('h_met_trk_et', "ROOT.TH1F('$', ';E^{miss}_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_phi = self.hist('h_met_trk_phi', "ROOT.TH1F('$', ';#phi(E^{miss}_{T}(trk));Events / (0.1)', 64, -3.2, 3.2)", dir=MET)
        self.h_met_clus_sumet = self.hist('h_met_clus_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(clus) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)
        self.h_met_trk_sumet = self.hist('h_met_trk_sumet', "ROOT.TH1F('$', ';#Sigma E_{T}(trk) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=MET)

        ##Electron plots
        self.h_el_pt = self.hist('h_el_pt', "ROOT.TH1F('$', ';p_{T}(e) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_eta = self.hist('h_el_eta', "ROOT.TH1F('$', ';#eta(e);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_phi = self.hist('h_el_phi', "ROOT.TH1F('$', ';#phi(e);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_trkd0sig = self.hist('h_el_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_trkz0sintheta = self.hist('h_el_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
        #leading
        self.h_el_lead_pt = self.hist('h_el_lead_pt', "ROOT.TH1F('$', ';p_{T}(e lead) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_lead_eta = self.hist('h_el_lead_eta', "ROOT.TH1F('$', ';#eta(e lead);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_lead_phi = self.hist('h_el_lead_phi', "ROOT.TH1F('$', ';#phi(e lead);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_lead_trkd0sig = self.hist('h_el_lead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e lead);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_lead_trkz0sintheta = self.hist('h_el_lead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e lead) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)
        #subleading
        self.h_el_sublead_pt = self.hist('h_el_sublead_pt', "ROOT.TH1F('$', ';p_{T}(e sublead) [GeV];Events / (1 GeV)', 2000, 0.0, 2000.0)", dir=ELECTRONS)
        self.h_el_sublead_eta = self.hist('h_el_sublead_eta', "ROOT.TH1F('$', ';#eta(e sublead);Events / (0.1)', 50, -2.5, 2.5)", dir=ELECTRONS)
        self.h_el_sublead_phi = self.hist('h_el_sublead_phi', "ROOT.TH1F('$', ';#phi(e sublead);Events / (0.1)', 64, -3.2, 3.2)", dir=ELECTRONS)
        self.h_el_sublead_trkd0sig = self.hist('h_el_sublead_trkd0sig', "ROOT.TH1F('$', ';d^{trk sig}_{0}(e sublead);Events / (0.1)', 100, 0., 10.)", dir=ELECTRONS)
        self.h_el_sublead_trkz0sintheta = self.hist('h_el_sublead_trkz0sintheta', "ROOT.TH1F('$', ';z^{trk}_{0}sin#theta(e sublead) [mm];Events / (0.01)', 200, -1, 1)", dir=ELECTRONS)

        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          assert len(electrons)==2, "should have exactly two tight electrons at this point"
          ele1T = ROOT.TLorentzVector()
          ele1T.SetPtEtaPhiM( electrons[0].tlv.Pt(), 0., electrons[0].tlv.Phi(), electrons[0].tlv.M() )
          ele2T = ROOT.TLorentzVector()
          ele2T.SetPtEtaPhiM( electrons[1].tlv.Pt(), 0., electrons[1].tlv.Phi(), electrons[1].tlv.M() )
          ## event plots 
          self.h_averageIntPerXing.Fill(self.chain.averageInteractionsPerCrossing, weight)
          self.h_actualIntPerXing.Fill(self.chain.actualInteractionsPerCrossing, weight)
          self.h_NPV.Fill(self.chain.NPV, weight)
          self.h_nelectrons.Fill(len(electrons), weight)
          self.h_invMass.Fill( (electrons[0].tlv+electrons[1].tlv).M()/GeV, weight)
          self.h_ZbosonPt.Fill( (electrons[0].tlv+electrons[1].tlv).Pt()/GeV, weight)
          self.h_ZbosonEta.Fill( (electrons[0].tlv+electrons[1].tlv).Eta(), weight)
          self.h_DR.Fill( electrons[0].tlv.DeltaR(electrons[1].tlv), weight)
          self.h_mTtot.Fill( (ele1T+ele2T+met_trk.tlv).M()/GeV, weight )
          self.h_HT.Fill( (electrons[0].tlv.Pt()+electrons[1].tlv.Pt())/GeV, weight )
          self.h_HTmet.Fill( (electrons[0].tlv.Pt()+electrons[1].tlv.Pt()+met_trk.tlv.Pt())/GeV, weight )

          nbjets = 0
          for jet in jets:
            if jet.isFix77:
              nbjets += 1
          self.h_njets.Fill(len(jets), weight)
          self.h_nbjets.Fill(nbjets, weight)

          ## met plots
          self.h_met_clus_et.Fill(met_clus.tlv.Pt()/GeV, weight)
          self.h_met_clus_phi.Fill(met_clus.tlv.Phi(), weight)
          self.h_met_trk_et.Fill(met_trk.tlv.Pt()/GeV, weight)
          self.h_met_trk_phi.Fill(met_trk.tlv.Phi(), weight)
          self.h_met_clus_sumet.Fill(met_clus.sumet/GeV, weight)
          self.h_met_trk_sumet.Fill(met_trk.sumet/GeV, weight)
          #electron
          for ele in electrons:
            self.h_el_pt.Fill(ele.tlv.Pt()/GeV, weight)
            self.h_el_eta.Fill(ele.eta, weight)
            self.h_el_phi.Fill(ele.tlv.Phi(), weight)
            self.h_el_trkd0sig.Fill(ele.trkd0sig, weight)
            self.h_el_trkz0sintheta.Fill(ele.trkz0sintheta, weight)

          ele1 = electrons[1]
          ele2 = electrons[0]
          if electrons[0].tlv.Pt() > electrons[1].tlv.Pt():
            ele1 = electrons[0]
            ele2 = electrons[1]
          assert ele1.tlv.Pt() >= ele2.tlv.Pt(), "leading electron has smaller pt than subleading"
 
          self.h_el_lead_pt.Fill(ele1.tlv.Pt()/GeV, weight)
          self.h_el_lead_eta.Fill(ele1.eta, weight)
          self.h_el_lead_phi.Fill(ele1.tlv.Phi(), weight)
          self.h_el_lead_trkd0sig.Fill(ele1.trkd0sig, weight)
          self.h_el_lead_trkz0sintheta.Fill(ele1.trkz0sintheta, weight)

          self.h_el_sublead_pt.Fill(ele2.tlv.Pt()/GeV, weight)
          self.h_el_sublead_eta.Fill(ele2.eta, weight)
          self.h_el_sublead_phi.Fill(ele2.tlv.Phi(), weight)
          self.h_el_sublead_trkd0sig.Fill(ele2.trkd0sig, weight)
          self.h_el_sublead_trkz0sintheta.Fill(ele2.trkz0sintheta, weight)


    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
    
    """ 
    #__________________________________________________________________________
    def get_obj_cutflow(self, obj_key, cut, list_weights=None, cut_prefix=""):
        for o in self.store[obj_key]:
          if hasattr(o,"cdict") and hasattr(o,"wdict"):
            obj_weight = 1.0
            if list_weights: 
              for w in list_weights:
                obj_weight *= o.GetWeight(w)
                if cut_prefix: 
                  if cut.startswith(cut_prefix): 
                    obj_passed = o.HasPassedCut(cut) and passed
            self.hists[self.region+"_"+obj_key].count_if(obj_passed, cut, obj_weight * weight)
    """

    #__________________________________________________________________________
    def reset_attributes(self,objects):
        for o in objects:
          o.ResetCuts()
          o.ResetWeights()
        return 

#------------------------------------------------------------------------------
class VarsAlg(pyframe.core.Algorithm):
    """
    
    calcualtes derived quantities, like masses, dphi etc...

    """
    #__________________________________________________________________________
    def __init__(self, 
                 name ='VarsAlg',
                 key_muons = 'muons',
                 key_jets = 'jets',
                 key_met = 'met_clus',
                 key_electrons = 'electrons',
                 require_prompt = False,
                 use_simple_truth = False,
                 remove_signal_muons = False,
                 remove_signal_electrons = False,
                 make_pure_emus = False,
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_jets = key_jets
        self.key_met = key_met
        self.key_electrons = key_electrons
        self.require_prompt = require_prompt
        self.use_simple_truth = use_simple_truth
        self.remove_signal_muons = remove_signal_muons
        self.remove_signal_electrons = remove_signal_electrons
        self.make_pure_emus = make_pure_emus

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]
        jets = self.store[self.key_jets]
        met = self.store[self.key_met]
        electrons = self.store[self.key_electrons]

        ## remove muons not T or L
        ## --------------------------------------------------
        for muon in self.store[self.key_muons][:]:
          if muon.tlv.Pt() < 30*GeV or muon.trkd0sig > 10.0 or (muon.trkd0sig > 3.0 and muon.isIsolated_FixedCutTightTrackOnly):
            self.store[self.key_muons].remove(muon)

        if ("mc" in self.sampletype) and self.remove_signal_muons and self.chain.mcChannelNumber in range(306538,306560):
          for muon in self.store[self.key_muons][:]:
            if muon.truthOrigin == 0:
              self.store[self.key_muons].remove(muon)

        if ("mc" in self.sampletype) and self.remove_signal_electrons and self.chain.mcChannelNumber in range(306538,306560):
          for ele in self.store[self.key_electrons][:]:
            if ele.truthOrigin == 0:
              self.store[self.key_electrons].remove(ele)

        if ("mc" in self.sampletype) and self.make_pure_emus and self.chain.mcChannelNumber in range(306538,306560):
          for ele in self.store[self.key_electrons][:]:
            if ele.truthOrigin != 0:
              self.store[self.key_electrons].remove(ele)
          for muon in self.store[self.key_muons][:]:
            if muon.truthOrigin != 0:
              self.store[self.key_muons].remove(muon)
          if [l for l in self.chain.HLpp_Daughters] == [-13,-13]:
            for muon in self.store[self.key_muons][:]:
              if muon.truthOrigin == 0 and muon.trkcharge == 1:
                self.store[self.key_muons].remove(muon)           
          if [l for l in self.chain.HLmm_Daughters] == [13,13]:
            for muon in self.store[self.key_muons][:]:
              if muon.truthOrigin == 0 and muon.trkcharge == -1:
                self.store[self.key_muons].remove(muon)   
          if [l for l in self.chain.HRpp_Daughters] == [-13,-13]:
            for muon in self.store[self.key_muons][:]:
              if muon.truthOrigin == 0 and muon.trkcharge == 1:
                self.store[self.key_muons].remove(muon)   
          if [l for l in self.chain.HRmm_Daughters] == [13,13]:
            for muon in self.store[self.key_muons][:]:
              if muon.truthOrigin == 0 and muon.trkcharge == -1:
                self.store[self.key_muons].remove(muon)   



        #assert len(muons)>=2, "less than 2 muons in event!"
        
        #assert self.store.has_key(self.key_met), "met key: %s not found in store!" % (self.key_met)
        #met = self.store[self.key_met]

        ## evaluate vars
        ## --------------------------------------------------           
        # if bool(len(electrons)==2):
        #   ele1 = electrons[0]
        #   ele1T = ROOT.TLorentzVector()
        #   ele1T.SetPtEtaPhiM( ele1.tlv.Pt(), 0., ele1.tlv.Phi(), ele1.tlv.M() )
        #   ele2 = electrons[1]
        #   ele2T = ROOT.TLorentzVector()
        #   ele2T.SetPtEtaPhiM( ele2.tlv.Pt(), 0., ele2.tlv.Phi(), ele2.tlv.M() )
        
        #   self.store['charge_product'] = ele2.trkcharge*ele1.trkcharge
        #   self.store['mVis']           = (ele2.tlv+ele1.tlv).M()
        #   self.store['mTtot']          = (ele1T + ele2T + met.tlv).M()  
        #   self.store['eles_dphi']     = ele2.tlv.DeltaPhi(ele1.tlv)
        #   self.store['eles_deta']     = ele2.tlv.Eta()-ele1.tlv.Eta()
        #   self.store['ee_invM']      = (ele1T + ele2T).M()



        # if bool(len(muons)==2):
        #   muon1 = muons[0]
        #   muon1T = ROOT.TLorentzVector()
        #   muon1T.SetPtEtaPhiM( muon1.tlv.Pt(), 0., muon1.tlv.Phi(), muon1.tlv.M() )
        #   muon2 = muons[1]
        #   muon2T = ROOT.TLorentzVector()
        #   muon2T.SetPtEtaPhiM( muon2.tlv.Pt(), 0., muon2.tlv.Phi(), muon2.tlv.M() )
        
        #   self.store['charge_product'] = muon2.trkcharge*muon1.trkcharge
        #   self.store['mVis']           = (muon2.tlv+muon1.tlv).M()
        #   self.store['mTtot']          = (muon1T + muon2T + met.tlv).M()  
        #   self.store['muons_dphi']     = muon2.tlv.DeltaPhi(muon1.tlv)
        #   self.store['muons_deta']     = muon2.tlv.Eta()-muon1.tlv.Eta()
        #   self.store['mumu_invM']      = (muon1T + muon2T).M()

          # definition of tag and probe 
          """
          lead_mu_is_tight = bool(muon1.isIsolated_FixedCutTightTrackOnly and muon1.trkd0sig<3.)
          lead_mu_is_loose = bool(not muon1.isIsolated_FixedCutTightTrackOnly and muon1.trkd0sig<10.)

          sublead_mu_is_tight = bool(muon2.isIsolated_FixedCutTightTrackOnly and muon2.trkd0sig<3.)
          sublead_mu_is_loose = bool(not muon2.isIsolated_FixedCutTightTrackOnly and muon2.trkd0sig<10.)
          
          if lead_mu_is_tight and sublead_mu_is_tight:
            if muon1.trkcharge > 0.0:
              self.store['tag'] = copy(muon1)
              self.store['probe'] = copy(muon2) 
            else:
              self.store['tag'] = copy(muon2)
              self.store['probe'] = copy(muon1) 
          elif lead_mu_is_loose or sublead_mu_is_tight:
            self.store['tag'] = copy(muon2)
            self.store['probe'] = copy(muon1) 
          elif sublead_mu_is_loose or lead_mu_is_tight:
            self.store['tag'] = copy(muon1)
            self.store['probe'] = copy(muon2) 
          """ 

        # tight muons
        muons_tight = []
        for mu in muons:
          if mu.isIsolated_FixedCutTightTrackOnly and mu.trkd0sig<=3.:
            muons_tight += [mu]
        self.store['muons_tight'] = muons_tight

        # # loose muons
        # muons_loose = []
        # for mu in muons:
        #   if mu.trkd0sig<10. and not mu.isIsolated_FixedCutTightTrackOnly:
        #     muons_loose += [mu]
        # self.store['muons_loose'] = muons_loose


        # loose electrons (no iso // LooseLLH)
        electrons_loose_LooseLLH = []
        for ele in electrons:
          if ("mc" in self.sampletype) and self.chain.mcChannelNumber in range(306538,306560):
            pass #do not truth match the electron
          elif self.require_prompt and ("mc" in self.sampletype) and ((not self.use_simple_truth and ele.electronType() not in [1,2,3]) or (self.use_simple_truth and ele.electronTypeSimple() not in [1])):
            continue
          if ( ele.pt>30*GeV and ele.LHLoose and ele.trkd0sig<5.0 and abs(ele.trkz0sintheta)<0.5 ) :
            electrons_loose_LooseLLH += [ele]
        self.store['electrons_loose_LooseLLH'] = electrons_loose_LooseLLH

        # tight electrons (isoLoose // MediumLLH)
        electrons_tight_MediumLLH_isolLoose = []
        for ele in electrons:
          if ("mc" in self.sampletype) and self.chain.mcChannelNumber in range(306538,306560):
            pass #do not truth match the electron
          elif self.require_prompt and ("mc" in self.sampletype) and ((not self.use_simple_truth and ele.electronType() not in [1,2,3]) or (self.use_simple_truth and ele.electronTypeSimple() not in [1])):
            continue
          if ( ele.pt>30*GeV and ele.isIsolated_Loose and ele.LHMedium and ele.trkd0sig<5.0 and abs(ele.trkz0sintheta)<0.5 ) :
            electrons_tight_MediumLLH_isolLoose += [ele]
        self.store['electrons_tight_MediumLLH_isolLoose'] = electrons_tight_MediumLLH_isolLoose

        # if (len(self.store["muons"]) + len(self.store['electrons_loose_LooseLLH']))==4:
        #   leptons = self.store["muons"] + self.store['electrons_loose_LooseLLH']
        #   totalCharge = 0
        #   for l in leptons:
        #     totalCharge += l.trkcharge
        #   if totalCharge == 0:
        #     mVis1 = 0
        #     mVis2 = 0
        #     posFlavor = ""
        #     negFlavor = ""
        #     for pair in itertools.combinations(leptons,2):
        #       if pair[0].trkcharge + pair[1].trkcharge == 2:
        #         mVis1 = (pair[0].tlv + pair[1].tlv).M()
        #         for lep in pair:
        #           if lep.m > 100:
        #             posFlavor += "m"
        #           else:
        #             posFlavor += "e"
        #       elif pair[0].trkcharge + pair[1].trkcharge == -2:
        #         mVis2 = (pair[0].tlv + pair[1].tlv).M()
        #         for lep in pair:
        #           if lep.m > 100:
        #             negFlavor += "m"
        #           else:
        #             negFlavor += "e"
        #     assert mVis1!=0 and mVis2!=0," not two same-sign lepton pairs !"
        #     if posFlavor == "me":
        #       posFlavor = "em"
        #     if negFlavor == "me":
        #       negFlavor = "em"
        #     self.store["mVis1"] = mVis1
        #     self.store["mVis2"] = mVis2
        #     self.store["fourLepFlavor"] = posFlavor+negFlavor


        # if bool(len(jets)) and bool(len(muons)):
        #   self.store['mujet_dphi'] = muons[0].tlv.DeltaPhi(jets[0].tlv)
        #   scdphi = 0.0
        #   scdphi += ROOT.TMath.Cos(met.tlv.Phi() - muons[0].tlv.Phi())
        #   scdphi += ROOT.TMath.Cos(met.tlv.Phi() - jets[0].tlv.Phi())
        #   self.store['scdphi'] = scdphi

        return True

#------------------------------------------------------------------------------
class PlotAlgFourLep(pyframe.algs.CutFlowAlg,CutAlg):
    """

    For making a set of standard plots after each cut in a cutflow.  PlotAlg
    inherets from CutAlg so all the functionality from CutAlg is available for
    applying selection. In addition you can apply weights at different points
    in the selection.

    The selection should be configured by specifying 'cut_flow' in the
    constructor as such:

    cut_flow = [
        ['Cut1', ['Weight1a','Weight1b'],
        ['Cut2', ['Weight2']],
        ['Cut3', None],
        ...
        ]

    The weights must be available in the store.

    'region' will set the name of the dir where the plots are saved

    Inhereting from CutFlowAlg provides the functionality to produce cutflow
    histograms that will be named 'cutflow_<region>' and 'cutflow_raw_<region>'

    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = 'PlotAlgFourLep',
                 region   = '',
                 obj_keys = [], # make cutflow hist for just this objects
                 cut_flow = None,
                 plot_all = True,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region,obj_keys=obj_keys)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow = cut_flow
        self.region   = region
        self.plot_all = plot_all
        self.obj_keys = obj_keys
    
    #_________________________________________________________________________
    def initialize(self):
        pyframe.algs.CutFlowAlg.initialize(self)
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            # obj cutflow is computed at the end of the cutflow
            #if len(list_cuts)==len(self.cut_flow):
            if self.obj_keys:
             for k in self.obj_keys:
              for o in self.store[k]:
               if hasattr(o,"cdict") and hasattr(o,"wdict"):
                obj_passed = True
                obj_weight = 1.0
                if list_weights:
                 for w in list_weights:
                  if w.startswith("MuPairs"):
                   obj_weight *= o.GetWeight(w) 
                for c in list_cuts:
                 if c.startswith("MuPairs"):
                  obj_passed = o.HasPassedCut(c) and obj_passed
                self.hists[self.region+"_"+k].count_if(obj_passed and passed, c, obj_weight * weight)
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               #if passed:             
               self.plot(region, passed, list_cuts, cut, list_weights=list_weights, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):
        
        EVT    = os.path.join(region, 'event')
        # -----------------
        # Create histograms
        # -----------------
        ## event plots
        self.h_mVis1 = self.hist('h_mVis1', "ROOT.TH1F('$', ';h_mVis1;Events', 10000, 0, 10000)", dir=EVT)
        self.h_mVis2 = self.hist('h_mVis2', "ROOT.TH1F('$', ';h_mVis2;Events', 10000, 0, 10000)", dir=EVT)

        if passed:
          mVis1  = self.store['mVis1']
          mVis2  = self.store['mVis2']


    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            ## could use this to fail when cuts not available
            #if not cuts.has_key(cn): return False
    
            ## pass if None
            if cn == 'ALL': continue
            #if cn.startswith("MuPairs"): continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
            #if not cut_passed:
            #    return False
        return cut_passed
    
    
    """ 
    #__________________________________________________________________________
    def get_obj_cutflow(self, obj_key, cut, list_weights=None, cut_prefix=""):
        for o in self.store[obj_key]:
          if hasattr(o,"cdict") and hasattr(o,"wdict"):
            obj_weight = 1.0
            if list_weights: 
              for w in list_weights:
                obj_weight *= o.GetWeight(w)
                if cut_prefix: 
                  if cut.startswith(cut_prefix): 
                    obj_passed = o.HasPassedCut(cut) and passed
            self.hists[self.region+"_"+obj_key].count_if(obj_passed, cut, obj_weight * weight)
    """

    #__________________________________________________________________________
    def reset_attributes(self,objects):
        for o in objects:
          o.ResetCuts()
          o.ResetWeights()
        return


#__________________________________________________________________________
def log_bins(nbins,xmin,xmax):
    xmin_log = math.log(xmin)
    xmax_log = math.log(xmax)
    log_bins = [ float(i)/float(nbins)*(xmax_log-xmin_log) + xmin_log for i in xrange(nbins+1)]
    bins = [ math.exp(x) for x in log_bins ]
    return bins

#__________________________________________________________________________
def log_bins_str(nbins,xmin,xmax):
    bins = log_bins(nbins,xmin,xmax)
    bins_str = "%d, array.array('f',%s)" % (len(bins)-1, str(bins))
    return bins_str 

#____________________________________________________________
def digitize(value, binEdges):
  assert isinstance(binEdges,list), "binEdges must be an array of bin edges"
  if value < binEdges[0]: return 0
  elif value >= binEdges[-1]: return len(binEdges)
  for i in range(len(binEdges)):
    edlow = binEdges[i]
    edhigh = binEdges[i+1]
    if value >= edlow and value < edhigh:
      return i+1

#__________________________________________________________________________
def pair_mass(pair):
  return (pair[0].tlv+pair[1].tlv).M()

#__________________________________________________________________________
def average_mass(pairs):
  npairs = 0
  mass = 0
  for pair in pairs:
    mass += (pair[0].tlv+pair[1].tlv).M()
    npairs += 1
  return mass/npairs


#__________________________________________________________________________
def pair_pt(pair):
  return (pair[0].tlv+pair[1].tlv).Pt()

#__________________________________________________________________________
def pair_eta(pair):
  return (pair[0].tlv+pair[1].tlv).Eta()

#__________________________________________________________________________
def pair_dr(pair):
  return pair[0].tlv.DeltaR(pair[1].tlv)

#__________________________________________________________________________
def leptons_HT(leptons):
  HT = 0
  for lep in leptons:
    HT += lep.tlv.Pt()
  return HT
